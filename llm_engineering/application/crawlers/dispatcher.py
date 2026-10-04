import re
from urllib.parse import urlparse

from loguru import logger
from .base import BaseCrawler
from .custom_article import CustomArticleCrawler
from .medium import MediumCrawler
from .linkedin import LinkedInCrawler
from .github import GithubCrawler


class CrawlerDispatcher:
    def __init__(self) -> None:
        self.crawlers = {}

    @classmethod
    def build(cls) -> "CrawlerDispatcher":
        dispatcher = cls()

        return dispatcher

    def register_medium(self) -> "CrawlerDispatcher":
        self.register("https://medium.com", MediumCrawler)
        return self

    def register_linkedin(self) -> "CrawlerDispatcher":
        self.register("https://linkedin.com", LinkedInCrawler)
        return self

    def register_github(self) -> "CrawlerDispatcher":
        self.register("https://github.com", GithubCrawler)
        return self

    def register(self, domain: str, crawler: type[BaseCrawler]) -> None:
        parsed_domain = urlparse(domain)
        domain = parsed_domain.netloc

        self.crawlers[r"https://(www\.)?{}/*".format(re.escape(domain))] = crawler

    def get_crawler(self, url: str) -> BaseCrawler:
        for pattern, crawler in self._crawlers.items():
            if re.match(pattern, url):
                return crawler()
            else:
                logger.warning(f"No crawler found for {url}. Defaulting to CustomArticleCrawler.")
            return CustomArticleCrawler
