from bs4 import BeautifulSoup
from loguru import logger

from llm_engineering.domain.documents import ArticleDocument

from .base import BaseCrawler


class MediumCrawler(BaseCrawler):
    model = ArticleDocument

    def set_extra_driver_options(self, options) -> None:
        options.add_argument(r"--profile-driectory=Profile 2")

    def extract(self, link: str, **kwargs) -> None:
        old_model = self.model.find(link=link)
        if old_model is not None:
            logger.info(f"Article already exists in the db : {link}")
            return
        logger.info(f"Starting to scap article: {link}")

        self.driver.get(link)
        self.scroll_page()

        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        title = soup.find_all("h1", class_="pw-post-title")
        subtitle = soup.find_all("h2", class_="pw-subtitle-paragraph")

        data = {
            "Title": title[0].string if title else None,
            "Subtitle": subtitle[0].string if subtitle else None,
            "Content": soup.get_text(),
        }
        self.driver.close()

        user = kwargs["user"]
        instance = self.model(
            content=data, link=link, platform="medium", author_id=user.id, author_full_name=user.full_name
        )
        instance.save()

        logger.info(f"Successufully scraped and saved medium article: {link}")
