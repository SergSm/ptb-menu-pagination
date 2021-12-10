from math import ceil

from paginator.consts import (
    BACKWARD_LABEL,
    CURRENT_LABEL,
    FORWARD_LABEL
)


def mark_if_current_page(current_page: int,
                         page_number: int) -> str:
    """Adds label to the left of a page number"""
    return str(CURRENT_LABEL) + str(page_number) \
        if page_number == current_page else \
        str(page_number)


def compose_first_line(current_page: int,
                       pages_per_line: int,
                       total_pages: int) -> list[str]:
    start = []
    middle = [
        mark_if_current_page(current_page, page)
        for page in range(1, min(pages_per_line, total_pages) + 1)
    ]
    end = [] if total_pages <= pages_per_line \
        else str(pages_per_line + 1) + str(FORWARD_LABEL)

    return start, middle, end


def compose_last_line(current_line: int,
                      total_pages: int,
                      current_page: int,
                      pages_per_line: int) -> list[str]:

    start = str(BACKWARD_LABEL) + \
            str(current_line * pages_per_line - pages_per_line)
    middle = [
        mark_if_current_page(current_page, page)
        for page in range(
            current_line * pages_per_line - pages_per_line + 1,
            total_pages + 1
        )
    ]

    end = []

    return start, middle, end


def compose_middle_line(current_line: int,
                        current_page: int,
                        pages_per_line: int) -> list[str]:

    start = str(BACKWARD_LABEL) + \
            str(current_line * pages_per_line - pages_per_line)
    middle = [
        mark_if_current_page(current_page, page)
        for page in range(
            current_line * pages_per_line - pages_per_line + 1,
            current_line * pages_per_line + 1
        )
    ]
    end = str(pages_per_line * current_line + 1) + str(FORWARD_LABEL)

    return start, middle, end


def build(total_pages: int,
          total_lines: int,
          current_page: int,
          pages_per_line: int) -> list[str]:
    """
    Builds a markup map as a list of str

    Example of a returned li    st:
    [1] is a page
    [1] [2] [3] - is a line
    [<<4] and [7>>] - are decoration pages

          [V1] [2] [3] [4>>]      - first line example
    [<<4] [5V] [6] [7]            - last line example
    [<<3] [4V] [5] [6]   [7>>]    -  middle line example
    The current page marked as V and may be any page from a current
    line with the exception of decoration pages ([<<4] and [7>>])
    """

    result = []

    current_line = ceil(current_page / pages_per_line)

    if current_line == 1:

        start, middle, end = compose_first_line(
            current_page=current_page,
            pages_per_line=pages_per_line,
            total_pages=total_pages
        )

    elif current_line == total_lines:

        start, middle, end = compose_last_line(
            current_line=current_line,
            total_pages=total_pages,
            current_page=current_page,
            pages_per_line=pages_per_line
        )
    else:  # middle line

        start, middle, end = compose_middle_line(
            current_line=current_line,
            current_page=current_page,
            pages_per_line=min(pages_per_line, total_pages)
        )

    result.append(start) if start else result
    result.extend(middle)
    result.append(end) if end else result

    return result
