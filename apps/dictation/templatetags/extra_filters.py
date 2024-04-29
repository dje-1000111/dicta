"""Extra filters."""

from django import template

register = template.Library()


@register.filter(name="starize")
def starize(level):
    return "⭐" * int(level)


@register.filter(name="label_star")
def label_star(level):
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
    a = dictation.timestamps["data"][0]
    b = dictation.timestamps["data"][-1]
    return round(b / 60 - a / 60)


@register.simple_tag(name="practice_status")
def practice_status(total_line, lines):
    return (
        round((len(lines["data"]) / (total_line)) * 100)
        if len(lines["data"]) > 0
        else 0
    )
