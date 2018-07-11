#!/usr/bin/env python3
"""This script crawls eco99fm, parses the URLs and yields an m3u list"""

from basicstruct import BasicStruct
import click
from fake_useragent import UserAgent
import multiprocessing
from typing import Dict, List, Tuple, Optional, Any
import re
import requests
from selenium import webdriver

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# For a single playlist url (http://eco99fm.maariv.co.il/music_channel/1.aspx)
M3U_RE = re.compile(
    '<input type="hidden" id="FileUrl" name="FileUrl" value="(?P<m3u>.+?)"/>'
)
IMAGE_URL_RE = re.compile(
    '<meta property="og:image" content="(?P<image_url>.+?)" />'
)
PLAYLIST_TITLE_RE = re.compile(
    '<meta property="og:title" content="(?P<title>.+?)">'
)

# For multiple playlist page (See MUSIC_CHANNELS_URL)
FULL_SINGLE_PAGE_HREF_RE = re.compile(
    "http://eco99fm.maariv.co.il/music_channel/(?P<page>\d+).aspx\?"
    "t=(?P<sub_cat>\d+)"
)

PLAYLIST_URL_TEMPLATE = "http://eco99fm.maariv.co.il/music_channel/{}.aspx"
BASE_URL = "http://eco99fm.maariv.co.il/"
MUSIC_CHANNELS_URL = BASE_URL + "music_channels/"


class MainCategory(BasicStruct):
    __slots__ = ("name", "id", "sub_categories")

    def __init__(self, name: str, id: int) -> None:
        self.name = name
        self.id = id
        self.sub_categories = {}  # type: Dict[int, SubCategory]


class SubCategory(BasicStruct):
    __slots__ = ("name", "id", "playlist_urls")

    def __init__(self, name: str, _id: int) -> None:
        self.name = name
        self.id = _id
        self.playlist_urls = []  # type: List[str]


class Playlist(BasicStruct):
    __slots__ = ("name", "url", "m3u_url", "image_url")

    def __init__(self, name: str, url: str, m3u_url: str,
                 image_url: str) -> None:
        self.name = name
        self.url = url
        self.m3u_url = m3u_url
        self.image_url = image_url


class SeleniumCrawler:

    MAIN_CATEGORIES = range(1, 9)

    def __init__(self):
        # Using Chrome because that's what I usually use the UI for, and
        # because it was easy to install
        self.driver = webdriver.Chrome()  # type: WebDriver
        self.categories = {}  # type: Dict[int, MainCategory]

    def handle_page(self):
        self.driver.get(MUSIC_CHANNELS_URL)
        for main_cat in self.MAIN_CATEGORIES:
            elem = self.driver.find_element_by_id(
                "MainTag_{}".format(main_cat)
            )
            self._handle_main_category(main_cat, elem)

    def _handle_main_category(
        self,
        main_cat_id: int,
        main_cat_elem: WebElement
    ):
        text_elem = main_cat_elem.find_element_by_class_name("MainTag_Name")
        main_cat = MainCategory(text_elem.text, main_cat_id)
        self.categories[main_cat_id] = main_cat

        main_cat_elem.click()  # Open sub categories
        inner_tags_elem = self.driver.find_element_by_id("InnerTags")
        inner_main_elem = inner_tags_elem.find_element_by_id(
            "innerMainTag_{}".format(main_cat_id)
        )
        a_elems = inner_main_elem.find_elements_by_tag_name("a")
        for a_elem in a_elems:
            sub_cat_id = int(a_elem.get_attribute("data-option-value"))
            text_elem = a_elem.find_element_by_class_name("MainTag_Name")
            sub_cat = SubCategory(text_elem.text, sub_cat_id)
            main_cat.sub_categories[sub_cat_id] = sub_cat
            img_elem = a_elem.find_element_by_tag_name("img")
            img_elem.click()
            self._handle_sub_category(sub_cat)

    def _handle_sub_category(self, sub_cat: SubCategory):

        WebDriverWait(self.driver, 1).until(
            EC.frame_to_be_available_and_switch_to_it("sliderFrame"))

        slide_container = WebDriverWait(self.driver, 1).until(
            EC.presence_of_element_located((By.CLASS_NAME,
                                            'ms-slide-container')))

        slides = slide_container.find_elements_by_class_name(
            "playSlider"
        )

        for slide in slides:
            a_elem = slide.find_element_by_tag_name("a")
            href = a_elem.get_attribute("href")
            match = FULL_SINGLE_PAGE_HREF_RE.match(href)
            page_id = int(match.group("page"))
            url = PLAYLIST_URL_TEMPLATE.format(page_id)

            sub_cat.playlist_urls.append(url)

        # Switch back to defult context
        self.driver.switch_to.default_content()


def _get_url(url: str) -> requests.Response:
    req = requests.get(url, headers={'User-Agent': UserAgent().chrome})
    if req.status_code != requests.status_codes.codes.ok:
        raise RuntimeError("Coudln't crawl {}".format(url))

    return req


def handle_url(url: str, main_cat: MainCategory,
               sub_cat: SubCategory) -> Playlist:
    req = _get_url(url)

    # URL
    m3u_match = M3U_RE.search(req.text)
    if m3u_match is None:
        raise RuntimeError("Coudln't find m3u link for {}".format(url))

    image_match = IMAGE_URL_RE.search(req.text)
    if image_match is None:
        raise RuntimeError("Coudln't find image link for {}".format(url))

    title_match = PLAYLIST_TITLE_RE.search(req.text)
    if title_match is None:
        raise RuntimeError("Coudln't find title link for {}".format(url))

    name = ' - '.join([
        main_cat.name,
        sub_cat.name,
        title_match.group("title"),
    ])

    return Playlist(name, url, m3u_match.group("m3u"),
                    BASE_URL + image_match.group("image_url"))


def handle_url_wrapper(
        to_process: Tuple[str, MainCategory, SubCategory]) -> Playlist:
    url, main_cat, sub_cat = to_process
    return handle_url(url, main_cat, sub_cat)


def multi_process_urls(to_process: List[Tuple[str, MainCategory, SubCategory]]
                       ) -> List[Playlist]:
    pool = multiprocessing.Pool(10)
    return pool.map(handle_url_wrapper, to_process)


def dummy_test_single_url():
    main_cat = MainCategory("main cat", 0)
    sub_cat = SubCategory("sub cat", 1)
    url = "http://eco99fm.maariv.co.il/music_channel/478.aspx"
    res = multi_process_urls([(url, main_cat, sub_cat)])
    print(res)


def write_m3u_file(out_m3u: Any, playlists: List[Playlist]) -> None:
    out_m3u.write("#EXTM3U\n")
    out_m3u.write("##\n")
    out_m3u.write("\n")

    for idx, playlist in enumerate(sorted(playlists)):
        out_m3u.write('#EXTINF:{}, tvg-logo="{}", {}\n'.format(
            idx, playlist.image_url, playlist.name
        ))
        out_m3u.write("{}\n".format(playlist.m3u_url))
        out_m3u.write("\n")


@click.command()
@click.argument('out_m3u', type=click.File("wt"))
def main(out_m3u: click.utils.LazyFile):
    """Crawls the eco99fm site writing an m3u playlist to the given M3U_FILE"""
    crawler = SeleniumCrawler()
    crawler.handle_page()
    to_process = []
    for main_cat in crawler.categories.values():
        for sub_cat in main_cat.sub_categories.values():
            for url in sub_cat.playlist_urls:
                to_process.append((url, main_cat, sub_cat))

    playlists = multi_process_urls(to_process)
    write_m3u_file(out_m3u, playlists)


if __name__ == "__main__":
    main()
