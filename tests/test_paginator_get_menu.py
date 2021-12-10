from dataclasses import dataclass

import pytest

from paginator import get_menu

from .fixtures.fixtures import cases


params = 'items_per_page,' \
         'pages_per_line,' \
         'navigation_signature,' \
         'page_label,' \
         'total_items,' \
         'current_page,' \
         'expected'


@pytest.mark.parametrize(params, cases)
def test_get_menu(items_per_page: int,
                  pages_per_line: int,
                  navigation_signature: str,
                  page_label: str,
                  total_items: int,
                  current_page: int,
                  expected):

    # Defining input parameters
    #################################################
    @dataclass
    class Menu:
        items_per_page: int
        pages_per_line: int
        navigation_signature: str
        page_label: str

    menu = Menu(
        items_per_page=items_per_page,
        pages_per_line=pages_per_line,
        navigation_signature=navigation_signature,
        page_label=page_label)
    #################################################

    result = get_menu(total_items=int(total_items),
                      current_page=int(current_page),
                      menu_settings=menu)

    len_result = sum([len(listElem) for listElem in result])
    len_expected = sum([len(listElem) for listElem in expected])

    assert len_result == len_expected
    assert result == expected
    assert to_string(result) == to_string(expected)


def to_string(menu):
    menu_str = ""
    for x in menu:
        for y in x:
            menu_str += str(y)
    return menu_str
