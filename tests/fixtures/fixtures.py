from telegram import InlineKeyboardButton


cases = [
    # region case 1
    (3,  # items_per_page
     3,  # pages_per_line
     '±',  # navigation_signature
     str(' p. '),  # page_label
     9,  # total_items
     1,  # current_page

     # expected:
     [
         [
             InlineKeyboardButton(
                 text='✅1  p. ',
                 callback_data=f'{str(1)}'
                               f'±',
             ),
             InlineKeyboardButton(
                 text='2  p. ',
                 callback_data=f'{str(2)}'
                               f'±',
             ),
             InlineKeyboardButton(
                 text='3  p. ',
                 callback_data=f'{str(3)}'
                               f'±',
             ),
         ]
     ]
     ),
    # endregion

    # region case 2
    (1,  # items_per_page
     1,  # pages_per_line
     '±',  # navigation_signature
     str(' p. '),  # page_label
     1,  # total_items
     1,  # current_page

     # expected:
     [
         [
             InlineKeyboardButton(
                 text='✅1  p. ',
                 callback_data=f'{str(1)}'
                               f'±',
             )
         ]
     ]
     )
    # endregion
]
