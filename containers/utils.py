symbols = (
    "абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ",
    "abvgdeejzijklmnoprstufhzcss_y_euaABVGDEEJZIJKLMNOPRSTUFHZCSS_Y_EUA",
)
tr = {ord(a): ord(b) for a, b in zip(*symbols)}


def normalize_group_name(name: str) -> str:
    name = "".join(map(lambda s: s.translate(tr), name))
    splitted = name.split("-")
    splitted = list(map(str.lower, splitted))
    splitted[-2] = splitted[-2][1:]

    return "-".join(splitted[-3:])
