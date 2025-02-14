"""Extra filters."""

from django import template

register = template.Library()


@register.filter(name="starize")
def starize(level):
    """Return the star rating."""
    return "⭐" * int(level)


@register.filter(name="label_star")
def label_star(level):
    """Return the label of the star rating."""
    labels = {
        "1": "Very easy",
        "2": "Easy",
        "3": "Normal",
        "4": "Hard",
        "5": "Very hard",
    }
    return labels[level]


@register.filter(name="duration")
def get_duration(dictation):
    """Return the duration of the dictation in minutes."""
    a = dictation.timestamps["data"][0]
    b = dictation.timestamps["data"][-1]
    return round(b / 60 - a / 60)


@register.simple_tag(name="practice_status")
def practice_status(total_line, lines):
    """Return the percentage of completion of the dictation."""
    return (
        round((len(lines["data"]) / (total_line)) * 100)
        if len(lines["data"]) > 0
        else 0
    )


@register.filter(name="format_domain")
def format_domain(dns):
    """Format string to remove the 4 last chars and capitalize d and e."""
    return "".join(
        [letter.capitalize() if letter in ["d", "e"] else letter for letter in dns[:-4]]
    )
