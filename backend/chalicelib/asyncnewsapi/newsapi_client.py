import aiohttp

from newsapi import const
from newsapi.newsapi_exception import NewsAPIException
from newsapi.utils import is_valid_string, stringify_date_param

# Partial Fork of the NewsApiClient, replacing requests with aiohttp


class AsyncNewsApiClient(object):
    """The core client object used to fetch data from News API endpoints.

    :param api_key: Your API key, a length-32 UUID string provided for your News API account.
        You must `register <https://newsapi.org/register>`_ for a News API key.
    :type api_key: str
    """

    def __init__(self, api_key):
        self.api_key = api_key

    async def get_everything(  # noqa: C901
        self,
        q=None,
        qintitle=None,
        sources=None,
        domains=None,
        exclude_domains=None,
        from_param=None,
        to=None,
        language=None,
        sort_by=None,
        page=None,
        page_size=None,
    ):
        """Call the `/everything` endpoint.

        Search through millions of articles from over 30,000 large and small news sources and blogs.

        :param q: Keywords or a phrase to search for in the article title and body.  See the official News API
            `documentation <https://newsapi.org/docs/endpoints/everything>`_ for search syntax and examples.
        :type q: str or None

        :param qintitle: Keywords or a phrase to search for in the article title and body.  See the official News API
            `documentation <https://newsapi.org/docs/endpoints/everything>`_ for search syntax and examples.
        :type q: str or None

        :param sources: A comma-seperated string of identifiers for the news sources or blogs you want headlines from.
            Use :meth:`NewsApiClient.get_sources` to locate these programmatically, or look at the
            `sources index <https://newsapi.org/sources>`_.
        :type sources: str or None

        :param domains:  A comma-seperated string of domains (eg bbc.co.uk, techcrunch.com, engadget.com)
            to restrict the search to.
        :type domains: str or None

        :param exclude_domains:  A comma-seperated string of domains (eg bbc.co.uk, techcrunch.com, engadget.com)
            to remove from the results.
        :type exclude_domains: str or None

        :param from_param: A date and optional time for the oldest article allowed.
            If a str, the format must conform to ISO-8601 specifically as one of either
            ``%Y-%m-%d`` (e.g. *2019-09-07*) or ``%Y-%m-%dT%H:%M:%S`` (e.g. *2019-09-07T13:04:15*).
            An int or float is assumed to represent a Unix timestamp.  All datetime inputs are assumed to be UTC.
        :type from_param: str or datetime.datetime or datetime.date or int or float or None

        :param to: A date and optional time for the newest article allowed.
            If a str, the format must conform to ISO-8601 specifically as one of either
            ``%Y-%m-%d`` (e.g. *2019-09-07*) or ``%Y-%m-%dT%H:%M:%S`` (e.g. *2019-09-07T13:04:15*).
            An int or float is assumed to represent a Unix timestamp.  All datetime inputs are assumed to be UTC.
        :type to: str or datetime.datetime or datetime.date or int or float or None

        :param language: The 2-letter ISO-639-1 code of the language you want to get headlines for.
            See :data:`newsapi.const.languages` for the set of allowed values.
        :type language: str or None

        :param sort_by: The order to sort articles in.
            See :data:`newsapi.const.sort_method` for the set of allowed values.
        :type sort_by: str or None

        :param page: The number of results to return per page (request).
            20 is the default, 100 is the maximum.
        :type page: int or None

        :param page_size: Use this to page through the results if the total results found is
            greater than the page size.
        :type page_size: int or None

        :return: JSON response as nested Python dictionary.
        :rtype: dict
        :raises NewsAPIException: If the ``"status"`` value of the response is ``"error"`` rather than ``"ok"``.
        """

        payload = {}

        # Keyword/Phrase
        if q is not None:
            if is_valid_string(q):
                payload["q"] = q
            else:
                raise TypeError("keyword/phrase q param should be of type str")

        # Keyword/Phrase in Title
        if qintitle is not None:
            if is_valid_string(qintitle):
                payload["qintitle"] = qintitle
            else:
                raise TypeError("keyword/phrase qintitle param should be of type str")

        # Sources
        if sources is not None:
            if is_valid_string(sources):
                payload["sources"] = sources
            else:
                raise TypeError("sources param should be of type str")

        # Domains To Search
        if domains is not None:
            if is_valid_string(domains):
                payload["domains"] = domains
            else:
                raise TypeError("domains param should be of type str")

        if exclude_domains is not None:
            if isinstance(exclude_domains, str):
                payload["excludeDomains"] = exclude_domains
            else:
                raise TypeError("exclude_domains param should be of type str")

        # Search From This Date ...
        if from_param is not None:
            payload["from"] = stringify_date_param(from_param)

        # ... To This Date
        if to is not None:
            payload["to"] = stringify_date_param(to)

        # Language
        if language is not None:
            if is_valid_string(language):
                if language not in const.languages:
                    raise ValueError("invalid language")
                else:
                    payload["language"] = language
            else:
                raise TypeError("language param should be of type str")

        # Sort Method
        if sort_by is not None:
            if is_valid_string(sort_by):
                if sort_by in const.sort_method:
                    payload["sortBy"] = sort_by
                else:
                    raise ValueError("invalid sort")
            else:
                raise TypeError("sort_by param should be of type str")

        # Page Size
        if page_size is not None:
            if type(page_size) == int:
                if 0 <= page_size <= 100:
                    payload["pageSize"] = page_size
                else:
                    raise ValueError(
                        "page_size param should be an int between 1 and 100"
                    )
            else:
                raise TypeError("page_size param should be an int")

        # Page
        if page is not None:
            if type(page) == int:
                if page > 0:
                    payload["page"] = page
                else:
                    raise ValueError("page param should be an int greater than 0")
            else:
                raise TypeError("page param should be an int")

        print(payload)

        # Send Request
        async with aiohttp.ClientSession("https://newsapi.org") as session:
            async with session.get(
                "/v2/everything",
                headers={
                    "Content-Type": "Application/JSON",
                    "Authorization": self.api_key,
                },
                timeout=30,
                params=payload,
            ) as r:
                # Check Status of Request
                if r.status != 200:
                    raise NewsAPIException(await r.json())
                return await r.json()
