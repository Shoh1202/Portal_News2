from django import template
from django.core.checks import register

register = template.Library()

@register.filter
def censor(text):
    if not text:
        return text

    bad_words = ["дурак", "плохой", "идиот"]

    words = text.split()
    result = []

    for word in words:
        clean_word = word.strip(".,!?;:")
        lower_word = clean_word.lower()

        if lower_word in bad_words:
            censored = "*" * len(clean_word)

            word = word.replace(clean_word, censored)

        result.append(word)

    return " ".join(result)

