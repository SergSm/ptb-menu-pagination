# python telegram bot menu pagination
![Actions Status](https://github.com/SergSm/ptb-menu-pagination/workflows/ci/badge.svg)
[![Maintainability](https://api.codeclimate.com/v1/badges/9eade003d09d837c852e/maintainability)](https://codeclimate.com/github/SergSm/ptb-menu-pagination/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/9eade003d09d837c852e/test_coverage)](https://codeclimate.com/github/SergSm/ptb-menu-pagination/test_coverage)

# Description

Makes a google style pagination line for a list of items.

![](https://github.com/SergSm/ptb-menu-pagination/blob/main/example/media/example.png) ![](https://github.com/SergSm/ptb-menu-pagination/raw/main/example/media/example.png)

In other words it builds a menu for navigation if you have 
a lot of search results or whatever list of anything 

![](https://github.com/SergSm/ptb-menu-pagination/blob/main/example/media/example2.png) ![](https://github.com/SergSm/ptb-menu-pagination/raw/main/example/media/example2.png)


### Installation

```
pip install ptb-menu-navigation
```


or if you are working with source code and use Poetry tool:

```
make install
```

### Usage
```python
from paginator import get_menu
```


Use ```get_menu``` function to create a line of pages

#### Example:
```python
from paginator import get_menu 
from dataclasses import dataclass

# Define initial menu settings in the dataclass.
@dataclass
class Menu:
    items_per_page: int = 10
    pages_per_line: int = 3
    navigation_signature: str = '±'
    page_label: str = ' p. '

# Add the initial call of get_menu
def handling_input(update, context):
    # ...
    # On first invocation
    navigation = get_menu(total_items=len(search_results),
                          current_page=1,
                          menu_settings=Menu)
    # ...

# Add a callback to handle a page switching  
def navigate(update, context):
    # ...
    navigation = get_menu(total_items=len(search_results),
                          current_page=int(current_page),
                          menu_settings=Menu)     
    # ...            
```
where ```search_results``` is a list of strings and ```current_page```
is a number extracted from a ```callback_data```.

See ```examples/search_bot.py```

### Demo bot launch
Create a ```.env``` file with a ```TOKEN``` variable
inside of an ```/examples``` for launching 
the
[demo](https://github.com/SergSm/menu_pagination/blob/main/example/search_bot.py) bot.\
eg:\
```TOKEN=<YOUR_TELEGRAM_BOT_TOKEN_FROM_BOT_FATHER>```

You may also provide some additional menu values in the same ```.env``` file:
```
ITEMS_PER_PAGE=1
PAGES_PER_LINE=1
NAVIGATION_SIGNATURE="±"
PAGE_LABEL=" p. "
```
