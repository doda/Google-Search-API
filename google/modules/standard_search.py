from utils import _get_search_url, get_html
from bs4 import BeautifulSoup
import urlparse


class GoogleResult:

    """Represents a google search result."""

    def __init__(self):
        self.name  # The title of the link
        self.link  # The external link
        self.google_link  # The google link
        self.description  # The description of the link
        self.thumb  # Link to a thumbnail of the website (NOT implemented yet)
        self.cached  # Link to cached version of the page (NOT implemented yet)
        self.page  # Page this result was on (When searching more than one)
        self.index  # What index on this page it was on

    def __repr__(self):
        name = self._limit_str_size(self.name, 55)
        description = self._limit_str_size(self.description, 49)

        list_google = ["GoogleResult(",
                       "name={}".format(name), "\n", " " * 13,
                       "description={}".format(description)]

        return "".join(list_google)

    def _limit_str_size(self, str_element, size_limit):
        """Limit the characters of the string, adding .. at the end."""

        if not str_element:
            return None

        elif len(str_element) > size_limit:
            return str_element.decode("utf-8")[:size_limit] + ".."

        else:
            return str_element.decode("utf-8")


# PUBLIC
def search(query, pages=1):
    """Returns a list of GoogleResult.

    Args:
        query: String to search in google.
        pages: Number of pages where results must be taken.

    Returns:
        A GoogleResult object."""

    results = []
    for i in range(pages):
        url = _get_search_url(query, i)
        html = get_html(url)

        if html:
            soup = BeautifulSoup(html)
            lis = soup.findAll("li", attrs={"class": "g"})

            j = 0
            for li in lis:
                res = GoogleResult()
                res.page = i
                res.index = j

                res.name = _get_name(li)
                res.link = _get_link(li)
                res.google_link = _get_google_link(li)
                res.description = _get_description(li)
                res.thumb = _get_description()
                res.cached = _get_description()

                results.append(res)
                j += 1

    return results


# PRIVATE
def _get_name(li):
    """Return the name of a google search."""
    a = li.find("a")
    return a.text.strip()


def _get_link(li):
    """Return external link from a search."""

    a = li.find("a")
    link = a["href"]

    if link.startswith("/url?") or link.startswith("/search?"):
        return None

    else:
        return link


def _get_google_link(li):
    """Return google link from a search."""

    a = li.find("a")
    link = a["href"]

    if link.startswith("/url?") or link.startswith("/search?"):
        return urlparse.urljoin("http://www.google.com", link)

    else:
        return None


def _get_description(li):
    """Return the description of a google search.

    TODO: There are some text encoding problems to resovle."""

    sdiv = li.find("div", attrs={"class": "s"})
    if sdiv:
        stspan = sdiv.find("span", attrs={"class": "st"})

        return stspan.text.encode("utf-8").strip()

    else:
        return None


def _get_thumb():
    """Return the link to a thumbnail of the website."""
    pass


def _get_cached():
    """Return a link to the cached version of the page."""
    pass