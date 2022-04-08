"""
Demo bot to show a search results handling.
Notion! use_context=True - is a must use when instantiating an Updater
"""

from math import ceil
from pathlib import Path
from dataclasses import dataclass
import logging
import os

from dotenv import load_dotenv

from telegram import (
    Update,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    InlineKeyboardMarkup
)

from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackContext,
    ConversationHandler,
    MessageHandler,
    Filters,
    CallbackQueryHandler,
)

from paginator import get_menu

load_dotenv('.env')

# region logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# endregion

# region settings

TOKEN = os.environ.get('TOKEN')


# Navigation
@dataclass
class Menu:
    items_per_page: int = int(os.getenv('ITEMS_PER_PAGE', 10))
    pages_per_line: int = int(os.getenv('PAGES_PER_LINE', 3))
    navigation_signature: str = os.getenv('NAVIGATION_SIGNATURE', '±')
    page_label: str = os.getenv('PAGE_LABEL', ' p. ')

# endregion

# region constants


bot_command_start = 'start'
bot_search_command = 'search'


# STATES
STATE_SEARCH = 'SEARCH'
STATE_INPUT = 'ENDSEARCH'
STATE_CHOSE = 'USRCHCIE'
STATE_FINISH = 'FNISHSRCH'


# Start text
start_text = 'Hello!\n' \
             'Type /{0} to enter ' \
             'a searching mode and then ' \
             'type what you want to find'.format(bot_search_command)

# Reply keyboard button search hint
navigation_hint = "Use arrows to navigate on the menu " \
                  "or make a choice"

# Reply keyboard button text for stopping a search
user_entered_finish = "🚫 end search"

# Key names for a user context
context_results = 'results'
context_current_page = 'current_page'
context_message_id = 'message_id'
context_menu_chat_id = 'menu_chat_id'
context_reply_message_id = 'reply_message_id'
context_menu_settings = 'menu_settings'

# endregion

# region bot commands handlers


def start(update: Update, context: CallbackContext):
    """Sends a greeting on a /start command
    and sets up a Reply to enter a search mode"""

    user = update.message.from_user
    logger.info("User %s started", user.first_name)

    reply_keyboard_buttons = [
        ['/' + bot_search_command],
    ]

    # send a first greeting message and
    # add a reply variant below an input field
    update.message.reply_text(
        text=start_text,
        reply_markup=ReplyKeyboardMarkup(reply_keyboard_buttons,
                                         resize_keyboard=True)
    )


def search(update: Update, context: CallbackContext) -> str:

    user = update.message.from_user
    logger.info("User %s initiated the search.", user.first_name)

    update.message.reply_text(
        text="⏳ Write a search query ",
        reply_markup=ReplyKeyboardRemove()  # removes '/search' from a previous step  # noqa
    )

    return f'{STATE_INPUT}'


def handling_input(update: Update, context: CallbackContext) -> str:
    """
    Send user 2 messages with
    ReplyKeyboardButtons and InlineKeyboardButtons(w/ navigation)
    containing search results to his text input
    """

    # region extract info from Update
    user = update.message.from_user
    logger.info("User %s has entered data to search", user.first_name)
    user_input = update.message.text  # Get last user text
    # endregion

    search_results = search_db(user_input)

    current_page = 1

    # region context filling
    # put the found data to a user session to access it later
    context.user_data[context_menu_settings] = Menu
    context.user_data[context_results] = search_results
    context.user_data[context_current_page] = current_page
    context.user_data[context_menu_chat_id] = update.message.chat_id
    # endregion

    page_results = search_results[0:Menu.items_per_page]

    total_lines = ceil(len(search_results) /
                       Menu.items_per_page)

    if total_lines:

        navigation = get_menu(total_items=len(search_results),
                              current_page=1,
                              menu_settings=Menu)

        # Send results to a user accompanied with a navigation
        update.message.reply_text(
            text='\n'.join(page_results),
            reply_markup=InlineKeyboardMarkup(navigation)
        )

    # We add a 1 to get the id of our menu message
    context.user_data[
        context_message_id] = update.message.message_id + 1

    # Create search buttons as a list of result w/ first finish button
    reply_buttons = [[x] for x in page_results]
    reply_buttons.insert(0, [user_entered_finish])

    # We send this message as a hack due to a Telegram inability
    # to provide both ReplyKeyboardMarkup
    # and InlineKeyboardMarkup in the same message
    update.message.reply_text(
        text=navigation_hint,
        reply_markup=ReplyKeyboardMarkup(reply_buttons)
    )

    # context reply text fill
    context.user_data[
        context_reply_message_id] = update.message.message_id + 2

    return STATE_FINISH \
        if user_input == user_entered_finish \
        else STATE_CHOSE


def chose(update: Update, context: CallbackContext):
    user = update.message.from_user
    logger.info("User %s has made a choice", user.first_name)

    # Get last user text
    user_input = update.message.text

    if user_input == user_entered_finish:
        # Remove reply keyboard
        update.message.reply_text(
            text="The search has been completed 🏁",
            reply_markup=ReplyKeyboardRemove()
        )

        # Removes inline keyboard
        context.bot.delete_message(
            chat_id=context.user_data[context_menu_chat_id],
            message_id=context.user_data[context_message_id]
        )

        logger.info("User %s has finished a search", user.first_name)

        return -1
    else:
        add_to_cart(user_input)
        return STATE_CHOSE


def navigate(update: Update, context: CallbackContext):
    """
    This function is being used every time a user switch pages
        It does 3 things:
            1) Rerenders navigation line of pages
            2) Updates text in a message with page results
            3) Updates reply buttons (by deleting a previous
             reply message and sending an another one)
    """

    callback_data = update.callback_query.data

    user = update.effective_user
    logger.info("User %s has navigated to %s", user.first_name,
                callback_data)

    if not isinstance(callback_data, str):
        raise ValueError(f'Callback data not a str. {__name__}')

    menu = context.user_data[context_menu_settings]
    current_page = callback_data.split(menu.navigation_signature)[0]

    message_id = context.user_data[context_message_id]
    chat_id = context.user_data[context_menu_chat_id]
    search_results = context.user_data[context_results]

    page_results = search_results[
                   menu.items_per_page * int(current_page)
                   - menu.items_per_page:
                   menu.items_per_page * int(current_page)
                   ]

    total_pages = ceil(len(search_results) /
                       menu.items_per_page)

    if total_pages:

        navigation = get_menu(
            total_items=len(search_results),
            current_page=int(current_page),
            menu_settings=menu
        )

        # Edit inline keyboard
        context.bot.edit_message_text(
            text='\n'.join(page_results),
            chat_id=chat_id,
            message_id=message_id,
            reply_markup=InlineKeyboardMarkup(navigation)
        )

        reply_buttons = [[x]for x in page_results]
        reply_buttons.insert(0, [user_entered_finish])

        context.bot.delete_message(chat_id=chat_id,
                                   message_id=context.user_data[
                                       context_reply_message_id])

        new_reply_message = context.bot.send_message(
            text=navigation_hint,
            chat_id=chat_id,
            reply_markup=ReplyKeyboardMarkup(reply_buttons)
        )

        context.user_data[
            context_reply_message_id] = new_reply_message.message_id


# endregion

# region database stub


def get_search_results(search_query: str) -> list:  # noqa
    """Example of getting data from a database"""
    working_dir = Path(__file__).resolve().parent
    fixture_dir = working_dir / 'fixtures'
    reference = 'data.txt'

    def get_file(path_to_file):
        with open(path_to_file) as f:
            content = f.read()
        return content

    data = get_file(fixture_dir / reference)
    results = data.split('\n')

    return [
        elem for elem
        in results
        if elem.upper().find(search_query.upper()) > -1
    ]

# endregion

# region business logic stub functions


def add_to_cart(*args, **kwargs):  # noqa
    """Stub for handling a user choice"""

    # do some stuff with an item received from a user choice
    # eg: "add to cart" if you building a shop

    logger.info("Added to a cart")


def search_db(query):
    """Stub for handling a search results for displaying to a user"""
    return get_search_results(search_query=query)


# endregion

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" \n caused error "%s"',
                   update,
                   context.error)


def main():
    """Runs the bot"""
    # Create the Updater and pass it your bot's token
    updater = Updater(
        TOKEN,
        use_context=True  # Must use
    )

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # /start command handler
    dispatcher.add_handler(CommandHandler(bot_command_start, start))

    # noinspection PyTypeChecker
    search_conversation_handler = ConversationHandler(
        entry_points=[CommandHandler(bot_search_command, search)],
        states={
            STATE_INPUT: [
                MessageHandler(Filters.text, handling_input),
            ],
            STATE_CHOSE: [
                MessageHandler(Filters.text, chose),
            ]
        },
        fallbacks=[
            CommandHandler(bot_search_command, search),
        ]
    )

    # user input handler
    dispatcher.add_handler(search_conversation_handler)

    # navigation handler
    dispatcher.add_handler(
        CallbackQueryHandler(navigate,
                             pattern='^[0-9]+'          # page number
                                     + str(Menu.navigation_signature))
    )

    dispatcher.add_error_handler(error)

    # start the bot in a polling mode
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives
    # SIGINT, SIGTERM or SIGABRT.
    # This should be used most of the time, since start_polling()
    # is non-blocking and will stop the bot gracefully
    updater.idle()


if __name__ == '__main__':
    main()
