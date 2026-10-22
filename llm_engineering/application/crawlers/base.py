import platform
import shutil
import sys
import time
from abc import ABC, abstractmethod
from tempfile import mkdtemp

import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from llm_engineering.domain.documents import NoSQLBaseDocument


class BaseCrawler(ABC):
    model: type[NoSQLBaseDocument]

    @abstractmethod
    def extract(self, link: str, **kwargs) -> None: ...


# Google ships no Chrome/chromedriver for Linux ARM and Selenium Manager doesn't support it,
# so there we use the distro's Chromium driver (apt: chromium-driver, snap: chromium.chromedriver).
IS_LINUX_ARM = sys.platform.startswith("linux") and platform.machine() in ("aarch64", "arm64")

if IS_LINUX_ARM:
    chromedriver_path = shutil.which("chromedriver") or shutil.which("chromium.chromedriver")
    if chromedriver_path is None:
        raise RuntimeError(
            "chromedriver not found on PATH. On Linux ARM install Chromium's driver: `sudo apt install chromium chromium-driver`."
        )
else:
    # check if the current version of chromedriver exists
    # and if it doesn't, downloads it automatically, then
    # adds to path
    chromedriver_autoinstaller.install()


class BaseSeleniumCrawler(BaseCrawler, ABC):
    def __init__(self, scroll_limit=5) -> None:
        options = webdriver.ChromeOptions()

        options.add_argument("--no-sandbox")
        options.add_argument("--headless=new")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--log-level=3")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-background-networking")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument(f"--user-data-dir={mkdtemp()}")
        options.add_argument(f"--data-path={mkdtemp()}")
        options.add_argument(f"--disk-cache-dir={mkdtemp()}")
        options.add_argument("--remote-debugging-port=9226")

        self.set_extra_driver_options(options)

        self.scroll_limit = scroll_limit
        service = Service(executable_path=chromedriver_path) if IS_LINUX_ARM else None
        self.driver = webdriver.Chrome(options=options, service=service)

    def set_extra_driver_options(self, options: Options) -> None:
        pass

    def login(self) -> None:
        pass

    def scroll_page(self) -> None:
        """scroll through the linkedin page based on the scroll limit."""
        current_scroll = 0
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height or (self.scroll_limit and current_scroll >= self.scroll_limit):
                break
            last_height = new_height
            current_scroll += 1
