# parse_object.pyにオブジェクト指向取り入れたらいらないかも
from app.parse_object import parse_kstyle, parse_kpopmonster


def soup_parser(site_name):
    parsers = {
        "kstyle": parse_kstyle,
        "kpopmonster": parse_kpopmonster
    }

    return parsers[site_name]
