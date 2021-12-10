from telegram import InlineKeyboardButton

from paginator.consts import (
    BACKWARD_LABEL, FORWARD_LABEL
)


def compose_tg_menu(navigation_mockup: list[str],
                    callback_signature_char: str,
                    page_label: str) -> list[list[InlineKeyboardButton]]:
    """
    Creates a list of a list of InlineKeyboardButton

    Args:
        navigation_mockup (list[str]): eg: ['<<2', '4', '5V', '6', '7>>']  # noqa
        callback_signature_char: str
        page_label: str
    """

    menu = []

    # Create a telegram inline buttons structure for a render
    for idx, button in enumerate(navigation_mockup):

        # Extract number
        page_number = int(''.join(filter(str.isdigit, button)))

        if button.find(BACKWARD_LABEL) != -1:  # [<<2]
            label = f'{BACKWARD_LABEL}'
        elif button.find(FORWARD_LABEL) != -1:  # [7>>]
            label = f'{FORWARD_LABEL}'
        else:  # [4]
            label = f'{button} {page_label}'

        menu.append(
            InlineKeyboardButton(
                text=label,
                callback_data=f'{str(page_number)}'
                              f'{str(callback_signature_char)}'
            )
        )

    return [menu]
