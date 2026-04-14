import re
from typing import List, Any


class Cleaner:
    """Clean all data."""

    validators: List[Any] = []
    normalizers: List[Any] = []

    def is_valid(self, data):
        """Verify if the key has a value."""
        for validator in self.validators:
            if not validator(data):
                return False
        return True

    def normalize(self, data):
        """Normalize some entries."""
        for normalizer in self.normalizers:
            data = normalizer(data)
        return data

    def clean(self, collection):
        """Return a data list if is_valid is True."""
        return [self.normalize(data) for data in collection if self.is_valid(data)]


def remove_non_breaking_space(data):
    """Remove non-breaking Space."""

    if "&nbsp;" in data:
        data = data.replace("&nbsp;", "")
    return data


def replace_dash_with_comma(data):
    """Replace dash with comma."""

    if "—" in data:
        data = data.replace("—", ", ")
    return data


def replace_opening_single_quote_with_straight(data):
    """Replace opening single quote with straight quote."""

    if "’" in data:
        data = data.replace("’", "'")
    return data


def replace_closing_single_quote_with_straight(data):
    """Replace closing single quote with straight quote."""

    if "‘" in data:
        data = data.replace("‘", "'")
    return data


def replace_three_dots_with_dot_dot_dot(data):
    """Replace three dots with dot dot dot."""

    if "…" in data:
        data = data.replace("…", "...")
    return data


# def replace_opening_double_quote_with_straight(data):
def remove_opening_double_quote(data):
    """Replace opening double quote with straight quote."""

    if "“" in data:
        # data = data.replace("“", "'")
        data = data.replace("“", "")
    return data


# def replace_closing_double_quote_with_straight(data):
def remove_closing_double_quote(data):
    """Replace opening double quote with straight quote."""

    if "”" in data:
        # data = data.replace("”", "'")
        data = data.replace("”", "")
    return data


def replace_en_dash_char_with_dash(data):
    """Remove en dash char."""

    if "\u2013" in data:
        data = data.replace("\u2013", "-")
    return data


def remove_latin_non_breaking_space(data):
    """Remove latin non breaking space."""

    if "\xa0" in data:
        data = data.replace("\xa0", "")
    return data


def remove_byte_order_mark(data):
    """Remove BOM."""

    if "\ufeff" in data:
        data = data.replace("\ufeff", "")
    return data


def remove_square_brackets(data):
    """Remove square brackets."""
    return re.sub(r"\[.*\]", "", data)


def remove_dash_at_the_begining(data):
    return re.sub(r"^-\s", "", data)


class HandleCleaner(Cleaner):
    """Handle Cleaner."""

    normalizers = [
        remove_non_breaking_space,
        replace_dash_with_comma,
        replace_opening_single_quote_with_straight,
        replace_closing_single_quote_with_straight,
        # replace_opening_double_quote_with_straight,
        # replace_closing_double_quote_with_straight,
        remove_opening_double_quote,
        remove_closing_double_quote,
        replace_three_dots_with_dot_dot_dot,
        replace_en_dash_char_with_dash,
        remove_latin_non_breaking_space,
        remove_byte_order_mark,
        remove_dash_at_the_begining,
        remove_square_brackets,
    ]
