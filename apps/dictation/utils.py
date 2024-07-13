from typing import List, Any

ADVERBS = [
    "already",
    "also",
    "always",
    "bravely",
    "carefully",
    "cheerfully",
    "daily",
    "even",
    "ever",
    "finally",
    "here",
    "immediately",
    "just",
    "loudly",
    "never",
    "now",
    "occasionally",
    "often",
    "previously",
    "rarely",
    "recently",
    "seldom",
    "so",
    "sometimes",
    "still",
    "usually",
    "very",
]

PAST_PARTICIPLES = [
    "awoken",
    "been",
    "born(e)",
    "beaten",
    "become",
    "begun",
    "bent",
    "bet",
    "bound",
    "bitten",
    "bled",
    "blown",
    "broken",
    "bred",
    "brought",
    "broadcast",
    "built",
    "burnt",
    "burned",
    "burst",
    "bought",
    "caught",
    "chosen",
    "clung",
    "come",
    "cost",
    "crept",
    "cut",
    "dealt",
    "dug",
    "done",
    "drawn",
    "dreamt",
    "dreamed",
    "drunk",
    "driven",
    "eaten",
    "fallen",
    "fed",
    "felt",
    "fought",
    "found",
    "flown",
    "forbidden",
    "forgotten",
    "forgiven",
    "frozen",
    "got",
    "given",
    "gone",
    "ground",
    "grown",
    "hung",
    "had",
    "heard",
    "hidden",
    "hit",
    "held",
    "hurt",
    "kept",
    "knelt",
    "known",
    "laid",
    "led",
    "leant",
    "leaned",
    "learnt",
    "learned",
    "left",
    "lent",
    "lain",
    "lied",
    "lit",
    "lighted",
    "lost",
    "made",
    "meant",
    "met",
    "mown",
    "mowed",
    "overtaken",
    "paid",
    "put",
    "read",
    "ridden",
    "rung",
    "risen",
    "run",
    "sawn",
    "sawed",
    "said",
    "seen",
    "sold",
    "sent",
    "set",
    "sewn",
    "sewed",
    "shaken",
    "should",
    "shed",
    "shone",
    "shot",
    "shown",
    "shrunk",
    "shut",
    "sung",
    "sunk",
    "sat",
    "slept",
    "slid",
    "smelt",
    "sown",
    "sowed",
    "spoken",
    "spelt",
    "spelled",
    "spent",
    "spilt",
    "spilled",
    "spun",
    "spat",
    "spread",
    "stood",
    "stolen",
    "stuck",
    "stung",
    "stunk",
    "struck",
    "sworn",
    "swept",
    "swollen",
    "swelled",
    "swum",
    "swung",
    "taken",
    "taught",
    "torn",
    "told",
    "thought",
    "thrown",
    "understood",
    "woken",
    "worn",
    "wept",
    "would",
    "won",
    "wound",
    # exeptions:
    "better",
    "best",
]

IRREGULAR = ["bleed", "breed", "feed", "shed", "speed", "rather"]
ADVS_PRONS = ["he", "she", "it", "there", "here"]
PUNCTUATION = [",", ".", "?", ":", ";", "!", "-"]

REG_ADVERB = r"(?<=[I|he])\'d(?= already|also|always|bravely|carefully|cheerfully|daily|even|ever|finally|here|immediately|just|loudly|never|now|occasionally|often|previously|rarely|recently|seldom|so|sometimes|still|usually|very)"
REG_PAST_PARTICIPLE = r"awoken|been|borne|beaten|become|begun|bent|bet|bound|bitten|bled|blown|broken|bred|brought|broadcast|built|burnt|burned|burst|bought|caught|chosen|clung|come|cost|crept|cut|dealt|dug|done|drawn|dreamt|dreamed|drunk|driven|eaten|fallen|fed|felt|fought|found|flown|forbidden|forgotten|forgiven|frozen|got|given|gone|ground|grown|hung|had|heard|hidden|hit|held|hurt|kept|knelt|known|laid|led|leant|leaned|learnt|learned|left|lent|lain|lied|lit|lighted|lost|made|meant|met|mown|mowed|overtaken|paid|put|read|ridden|rung|risen|run|sawn|sawed|said|seen|sold|sent|set|sewn|sewed|shaken|should|shed|shone|shot|shown|shrunk|shut|sung|sunk|sat|slept|slid|smelt|sown|sowed|spoken|spelt|spelled|spent|spilt|spilled|spun|spat|spread|stood|stolen|stuck|stung|stunk|struck|sworn|swept|swollen|swelled|swum|swung|taken|taught|torn|told|thought|thrown|understood|woken|worn|wept|would|won|wound|better|best|"
REG_VERBE_ED = r"\b(\w+ed)\b"


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


# def require_product_name_fr_not_empty(data):
#     """Verify if product_name_fr is not empty."""
#     return True if data.get("product_name_fr") else False


# def require_product_image_url_not_empty(data):
#     """Verify if image is not empty."""
#     return True if data.get("image_url") else False


# def require_brands_not_empty(data):
#     """Verify if brands is not empty."""
#     return True if data.get("brands") else False


# def require_nutriscore_grade_not_empty(data):
#     """Verify if nutriscore_grade is not empty."""
#     return True if data.get("nutriscore_grade") else False


# def require_nutriments_not_empty(data):
#     """Verify if nutriments is not empty."""
#     return True if data.get("nutriments") else False


# def require_lang_equal_to_fr(data):
#     """Verify if lang is equal to fr."""
#     return True if data.get("lang") == "fr" else False


# def require_categories_lc_equal_to_fr(data):
#     """Verify if categories_lc is equal to fr."""
#     return True if data.get("categories_lc") == "fr" else False


# def require_categories_without_lot_of_dashes(data):
#     """Ignore categories with lot of tirets."""
#     item = re.search(r"(\w+\-){1,}", data.get("categories"))
#     return False if item else True


# def require_len_categories_greater_than_one(data):
#     """Verify if there is more than one category."""
#     return True if len(data.get("categories").split(",")) > 1 else False


# def require_valid_product_name(data):
#     """Verify if the product is different from 'Chargement…'."""
#     return True if data.get("product_name_fr") != "Chargement…" else False


# def create_text(self, yt_transcript) -> list:
#     reg = r"(\(.*\))|(\[.*\])"
#     texts = []
#     for line in yt_transcript:
#         line["text"] = re.sub(reg, "", line["text"])
#         texts += [
#             line["text"]
#             .replace("\ufeff", "")
#             .replace("\n", " ")
#             .replace("—", ", ")
#             .replace("\xa0", "")
#             .replace("\u2013", "-")
#             .replace("’", "'")
#             .replace("‘", "'")
#             .replace("“", '"')
#             .replace("”", '"')
#             .replace("…", "...")
#         ]
#         line["text"] = re.sub(r"\s{2,}", " ", line["text"])

#     cleaned_text = []
#     for line in texts:
#         cleaned_text += (
#             [line[:-1]] if line.endswith("\u2014") or line.endswith("-") else [line]
#         )

#     return cleaned_text


# def normalize_remove_cariage_return(data):
#     """Delete cariage return."""

#     if "\n" in data.get("text"):
#         return data.update(
#             product_name_fr=data.get("product_name_fr").replace("\n", " ")
#         )
#     return data


# def normalize_categories_without_suffix_and_bad_datas(data):
#     """Delete expr like -> en: and fr: with all that comes after."""
#     if data:
#         item = re.search(r"\,\s{0,}\w{2}:", data.get("categories"))
#         if item:
#             return data.update(categories=data.get("categories")[: item.start()])
#         return data


# def normalize_product_to_replace_slash_by_dash_in_name(data):
#     """Replace slash by dash in product_name_fr."""
#     if data:
#         if "/" in data.get("product_name_fr"):
#             return data.update(
#                 product_name_fr=data.get("product_name_fr").replace("/", "-")
#             )
#         return data


# class OffCleaner(Cleaner):
#     """State."""

#     validators = [
#         require_product_name_fr_not_empty,
#         require_product_image_url_not_empty,
#         require_brands_not_empty,
#         require_nutriscore_grade_not_empty,
#         require_nutriments_not_empty,
#         require_lang_equal_to_fr,
#         require_categories_lc_equal_to_fr,
#         require_categories_without_lot_of_dashes,
#         require_len_categories_greater_than_one,
#         require_valid_product_name,
#     ]

#     normalizers = [
#         normalize_product_without_cariage_return,
#         normalize_categories_without_suffix_and_bad_datas,
#         normalize_product_to_replace_slash_by_dash_in_name,
#     ]
