import re

from transliterate import translit

SURNAME_TRANSLIT = {
    "Kh": "H",
    "kh": "h",
}


def unify_fio(fio: str) -> str:
    for key, value in SURNAME_TRANSLIT.items():
        fio = fio.replace(key, value)

    translitted = translit(fio, "ru")
    with_spaces = re.sub(r"\s", " ", translitted)
    return with_spaces.replace("ё", "е").replace("Ё", "Е")
