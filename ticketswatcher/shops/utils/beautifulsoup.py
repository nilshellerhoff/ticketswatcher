import bs4
from typing import Union


def try_get_attribute(soup: bs4.BeautifulSoup | bs4.element.Tag, selector: str, attr: str = None) -> bs4.element.Tag | str | None :
    """try to get an attribute from soup

    Parameters:
        soup: soup to be used
        selector: css selector
        attr: attribute to be returned

    Returns:
        str: attribute value / None if not existant
    """

    element = soup.select_one(selector)

    if element is None:
        return None
    else:
        return element.get(attr)


def try_get_text(soup: bs4.BeautifulSoup | bs4.element.Tag, selector: str) -> str | None :
    """try to get the text of an element from soup

    Parameters:
        soup: soup to be used
        selector: css selector

    Returns:
        str: text value / None if not existant
    """

    element = soup.select_one(selector)

    if element is None:
        return None
    else:
        return element.text
