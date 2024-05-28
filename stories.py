from GoogleNews import GoogleNews
from newsapi import NewsApiClient

googlenews = GoogleNews(lang="en", region="GB", start="04/01/2020", encode="utf-8")

api = NewsApiClient(api_key="d3f8935cccc84a7a8e7e30c14d47c673")


def getGoogleNewsStories(searchTerm):
    googlenews.clear()
    googlenews.get_news(searchTerm)
    return googlenews.results()


def getNewsApiStories(searchTerm):
    return api.get_everything(q=searchTerm)["articles"]


def getStories(placename, topic):
    searchTerm = f"{placename} {topic}"
    return getGoogleNewsStories(searchTerm)  # getNewsApiStories(searchTerm)
