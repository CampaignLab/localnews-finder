import aiohttp
import asyncio
from bs4 import BeautifulSoup

# Fork of the GoogleNews library, replacing requests with aiohttp


class GoogleNews:
    def __init__(self, lang: str = "en", region: str = "US"):
        self.lang = lang
        self.region = region
        self._text = ""
        self.date = ""
        self.desc = ""
        self.link = ""
        self.img = ""
        self.result = []
        self.total = []
        self.urls = []

    async def _get_news_page(
        self,
        search: str,
        when: str = None,
        from_: str = None,
        to_: str = None,
        page: int = 1,
    ):
        url = f"/search?q={search}&hl={self.lang}&gl={self.region}&ceid={self.region}%3A{self.lang}"
        if when is not None:
            url += f"&tbs=qdr:{when}"
        if from_ is not None and to_ is not None:
            url += f"&tbs=cdr:1,cd_min:{from_},cd_max:{to_}"

        async with aiohttp.ClientSession("https://news.google.com") as session:
            print(f"Searching {url}")
            async with session.get(url) as response:
                text = await response.text()
                print(text)
                return text

    async def search(
        self, key: str, when: str = None, from_: str = None, to_: str = None
    ):
        self._text = key
        self.total = []
        self.urls = []

        tasks = []
        for page in range(1, 2):  # Assuming you want the first 10 pages
            task = asyncio.ensure_future(
                self._fetch_and_parse(key, when, from_, to_, page)
            )
            tasks.append(task)

        responses = await asyncio.gather(*tasks)
        for result in responses:
            self.total.extend(result)

        return self.total

    async def _fetch_and_parse(
        self, key: str, when: str, from_: str, to_: str, page: int
    ):
        html = await self._get_news_page(key, when, from_, to_, page)
        return self._parse(html)

    def _parse(self, html: str):
        soup = BeautifulSoup(html, "html.parser")
        items = soup.find_all("div", attrs={"class": "dbsr"})
        results = []

        for item in items:
            title = item.find("div", attrs={"class": "JheGif nDgy9d"}).get_text()
            link = item.a["href"]
            media = item.find("div", attrs={"class": "XTjFC WF4CUc"}).get_text()
            date = item.find("span", attrs={"class": "WG9SHc"}).find("span").get_text()
            description = item.find("div", attrs={"class": "Y3v8qd"}).get_text()
            img = item.find("img")["src"] if item.find("img") else None

            results.append(
                {
                    "title": title,
                    "media": media,
                    "date": date,
                    "desc": description,
                    "link": link,
                    "img": img,
                }
            )

        return results

    async def get_news(
        self, key: str, when: str = None, from_: str = None, to_: str = None
    ):
        return await self.search(key, when, from_, to_)

    def clear(self):
        self.__texts = []
        self.__links = []
        self.__results = []
        self.__totalcount = 0


# Example usage
if __name__ == "__main__":
    google_news = GoogleNews(lang="en", region="GB")
    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(google_news.get_news("Python programming"))
    for result in results:
        print(result)
