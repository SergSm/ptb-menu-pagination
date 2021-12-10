from math import ceil
from dataclasses import dataclass

from telegram import InlineKeyboardButton

from paginator.composers.map import build
from paginator.composers.menu import compose_tg_menu


# Navigation
@dataclass
class Menu:
    items_per_page: int
    pages_per_line: int
    navigation_signature: str
    page_label: str


def get_menu(total_items: int,
             current_page: int,
             menu_settings) -> list[list[InlineKeyboardButton]]:

    total_pages = ceil(total_items / menu_settings.items_per_page)
    total_lines = ceil(total_pages / menu_settings.pages_per_line)

    # eg:  ['<<2', '4', '5V', '6', '7>>']
    navigation_mockup = build(
        total_pages=total_pages,
        total_lines=total_lines,
        current_page=current_page,
        pages_per_line=menu_settings.pages_per_line
    )

    navigation_menu = compose_tg_menu(
        navigation_mockup,
        menu_settings.navigation_signature,
        menu_settings.page_label
    )

    return navigation_menu
