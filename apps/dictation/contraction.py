"""Contraction."""

from .utils import ADVERBS, PAST_PARTICIPLES, PUNCTUATION, IRREGULAR


def is_genitive(index, segment_list):
    """Check if is a genitive."""
    if segment_list[index][-1] in PUNCTUATION:
        sg = segment_list[:-1] + [segment_list[index][:-1]]
        return sg[index][-2:] == "'s"
    return segment_list[-2:] == "'s"


def is_past_perfect_with_adverb(index, segment_list):
    """Check if it's past perfect with adverb next."""
    return segment_list[index + 1] in ADVERBS


def past_perfect_with_adverb(index, segment_list):
    """Concatenate had to replace 'd."""
    segment_list[index] = segment_list[index].split("'")[0] + " had"
    return segment_list[index]


def is_past_perfect(index, segment_list):
    """Check if it's past perfect."""
    return (
        segment_list[index + 1] in PAST_PARTICIPLES and segment_list[index + 2] != "if"
    ) or (segment_list[index + 1][-2:] == "ed" and segment_list[index + 2] != "if")


def past_perfect(index, segment_list):
    """Concatenate had to replace 'd."""
    if is_punctuation_after_targeted_segment(index, segment_list):
        segment_list = segment_list[:-1]
    segment_list[index] = segment_list[index].split("'")[0] + " had"
    return segment_list[index]


def is_would(index, segment_list, irregular) -> bool:
    """Check if it's conditional and rather."""
    return (
        segment_list[index + 1] not in irregular
        and segment_list[index + 1][-2:] != "ed"
        or (segment_list[index + 1][-2:] != "ed" and segment_list[index + 2] == "if")
        or segment_list[index + 1] == "rather"
    )


def would(index, segment_list):
    """Concatenate would to replace 'd."""
    if is_punctuation_after_targeted_segment(index, segment_list):
        segment_list = segment_list[:-1]
    segment_list[index] = segment_list[index].split("'")[0] + " would"
    return segment_list[index]


def put_back_punctuation(index, segment_list):
    """Put the punctuation mark at the end."""
    return segment_list[index][-1] if segment_list[index][-1] in PUNCTUATION else None


def s_common_punctuation(index, segment_list):
    """Putback the punctuation removed before to the modified segment."""
    punctu = put_back_punctuation(index, segment_list)
    new_segment = segment_list[index].split("'")[0] + " is"
    segment_list[index] = f"{new_segment}{punctu}" if punctu else new_segment
    return segment_list[index]


def present_continuous(index, segment_list):
    """Concatenate is to 's in order to make present continuous tense."""
    punctu = put_back_punctuation(index, segment_list)
    new_segment = segment_list[index].split("'")[0] + " is"
    segment_list[index] = f"{new_segment}{punctu}" if punctu else new_segment
    return segment_list[index]


def present_perfect(index, segment_list):
    """Concatenate has."""
    punctu = put_back_punctuation(index, segment_list)
    new_segment = segment_list[index].split("'")[0] + " has"
    segment_list[index] = f"{new_segment}{punctu}" if punctu else new_segment
    return segment_list[index]


def is_present_continuous(index, segment_list) -> bool:
    """Check if it's present continuous.

    from all_s_cases (only)
    """
    return (
        segment_list[index + 1].endswith("ing")
        and segment_list[index + 2] not in ["is", "are"]
    ) or "".join(segment_list).endswith("ing.")


def is_punctuation_after_targeted_segment(index, segment_list) -> bool:
    """Check if there is some punctuation at the end of the targeted segment."""
    return segment_list[index][-1] in PUNCTUATION


def bypass_punctuation_after_targeted_segment(index, segment_list):
    """Putback punctuation."""
    punctu = put_back_punctuation(index, segment_list)
    segment_list[index] = segment_list[index].split("'")[0] + f" is{punctu}"
    return segment_list[index]


def is_let_before_s(index, segment_list) -> bool:
    """Check if it's let before 's."""
    return segment_list[index][:-2].lower() == "let"


def lets(index, segment_list):
    """Concatenate us after let."""
    segment_list[index] = segment_list[index].split("'")[0] + " us"
    return segment_list[index]


def is_to_be(index, segment_list) -> bool:
    """Check for is case."""
    return (
        segment_list[index][:-2].lower() in ["he", "she", "it", "there", "here"]
        and segment_list[index + 1] not in PAST_PARTICIPLES
        or segment_list[index + 1] in ["my", "his", "her", "what"]
    )


def to_be(index, segment_list):
    """Return is case."""
    punctu = put_back_punctuation(index, segment_list)
    new_segment = segment_list[index].split("'")[0] + " is"
    segment_list[index] = f"{new_segment}{punctu}" if punctu else new_segment
    return segment_list[index]


def is_present_perfect(index, segment_list):
    """Check if it's present perfect."""
    return (
        segment_list[index][:-2].lower() in ["he", "she", "it", "what"]
        or segment_list[index + 1] in PAST_PARTICIPLES
    )


def is_possess_duration_distance(index, segment_list) -> bool:
    """Check if it's genitif of possession or duration or distance."""
    return (
        segment_list[index + 1] not in PAST_PARTICIPLES
        and not segment_list[index + 1].endswith("ed")
        and not segment_list[index + 1].endswith("ing")
        and not segment_list[index].split("'")[0].lower() in ["that", "this"]
    )


def possess_duration_distance(index, segment_list):
    """Return genitif of possession or duration or distance."""
    punctu = put_back_punctuation(index, segment_list)
    segment_list[index] = (
        segment_list[index] + punctu if punctu else segment_list[index]
    )
    return segment_list[index]


def is_demonstrative_before(index, segment_list):
    """Check if."""
    return segment_list[index + 1].endswith("ed") or segment_list[index].split("'")[
        0
    ].lower() in ["that", "this"]


def demonstrative(index, segment_list):
    """Concatenate is."""
    segment_list[index] = segment_list[index].split("'")[0] + " is"
    return segment_list[index]


def general_is_case(index, segment_list):
    """Return general is case."""
    punctu = put_back_punctuation(index, segment_list)
    new_segment = f"{segment_list[index]}{punctu}"
    segment_list[index] = new_segment if punctu else segment_list[index]
    return segment_list[index]


def all_d_cases(index, segment_list, irregular):
    """Manage had and would."""
    if is_past_perfect(index, segment_list):
        past_perfect(index, segment_list)
    elif is_past_perfect_with_adverb(index, segment_list):
        past_perfect_with_adverb(index, segment_list)
    elif is_would(index, segment_list, irregular):
        would(index, segment_list)


def all_s_cases(index, segment_list):
    """Check all is case."""
    if is_genitive(index, segment_list):
        punctu = put_back_punctuation(index, segment_list)
        new_segment = segment_list[:-1] + [segment_list[index][:-1]]
        if punctu:
            segment_list = segment_list[:-1] + [segment_list[index][:-1] + punctu]
        else:
            segment_list = segment_list[:-1] + [segment_list[index][:-1]]
        segment_list = (
            segment_list[:-1] + [segment_list[index][:-1] + punctu]
            if punctu
            else new_segment
        )
    else:
        if is_present_continuous(index, segment_list):
            present_continuous(index, segment_list)
        elif is_punctuation_after_targeted_segment(index, segment_list):
            bypass_punctuation_after_targeted_segment(index, segment_list)
        elif is_let_before_s(index, segment_list):
            lets(index, segment_list)
        elif is_to_be(index, segment_list):
            to_be(index, segment_list)
        elif is_present_perfect(index, segment_list):
            present_perfect(index, segment_list)
        elif is_possess_duration_distance(index, segment_list):
            possess_duration_distance(index, segment_list)
        elif is_demonstrative_before(index, segment_list):
            demonstrative(index, segment_list)
        else:
            general_is_case(index, segment_list)


def all_negative_cases(index, segment_list):
    if is_wont_case(index, segment_list):
        negative_future(index, segment_list)
    if is_nt_case(index, segment_list):
        nt_case(index, segment_list)
    if is_can_case(index, segment_list):
        can_case(index, segment_list)


def nt_case(index, segment_list):
    """Concatenate not."""
    if index < len(segment_list) - 1 and segment_list[index + 1] in [
        "I",
        "you",
        "he",
        "she",
        "we",
        "they",
    ]:
        item = segment_list[index].split("'")[0]
        segment_list[index] = item[:-1] if item.lower() != "will" else item
        segment_list.insert(index + 2, "not")
    else:
        punctu = put_back_punctuation(index, segment_list)
        item = segment_list[index].split("'")[0]
        new_segment = f"{item[:-1]} not" if item.lower() != "will" else item
        segment_list[index] = f"{new_segment}{punctu}" if punctu else new_segment
        return segment_list[index]


def is_wont_case(index, segment_list):
    return segment_list[index].split("'")[0].lower() == "won"


def is_can_case(index, segment_list):
    return segment_list[index].split("'")[0].lower() == "can"


def is_nt_case(index, segment_list):
    return segment_list[index].split("'")[0].lower() not in ["won", "can"]


def future(index, segment_list):
    """Concatenate will."""
    punctu = put_back_punctuation(index, segment_list)
    new_segment = segment_list[index].split("'")[0] + " will"
    segment_list[index] = f"{new_segment}{punctu}" if punctu else new_segment
    return segment_list[index]


def negative_future(index, segment_list):
    punctu = put_back_punctuation(index, segment_list)
    new_segment = segment_list[index].split("'")[0] + "ill"
    segment_list[index] = f"{new_segment}{punctu}" if punctu else new_segment
    return segment_list[index]


def can_case(index, segment_list):
    punctu = put_back_punctuation(index, segment_list)
    new_segment = segment_list[index].split("'")[0] + "not"
    segment_list[index] = f"{new_segment}{punctu}" if punctu else new_segment
    return segment_list[index]


def are_case(index, segment_list):
    """Concatenate are."""
    punctu = put_back_punctuation(index, segment_list)
    new_segment = segment_list[index].split("'")[0] + " are"
    segment_list[index] = f"{new_segment}{punctu}" if punctu else new_segment
    return segment_list[index]


def have_case(index, segment_list):
    """Concatenate have."""
    segment_list[index] = segment_list[index].split("'")[0] + " have"
    return segment_list[index]


def am_case(index, segment_list):
    """Concatenate am."""
    segment_list[index] = segment_list[index].split("'")[0] + " am"
    return segment_list[index]


def lengthen_sentence(segment: str) -> str:
    """Return converted contraction."""
    segment_list = segment.split()
    for index, word in enumerate(segment_list):
        if "'d" in word:
            all_d_cases(index, segment_list, IRREGULAR)
        if "'s" in word:
            all_s_cases(index, segment_list)
        if "n't" in word:
            all_negative_cases(index, segment_list)
        if "'ll" in word:
            future(index, segment_list)
        if "'re" in word:
            are_case(index, segment_list)
        if "'ve" in word:
            have_case(index, segment_list)
        if "'m" in word:
            am_case(index, segment_list)
    return " ".join(segment_list)
