#FIXME: Use for checking dictionary of chars?
layout_ru_eng = {'ё': '`', 'Ё': '~', '"': '@', '№': '#', ';': '$', ',': '^', '?': '&', 'й': 'q',
                 'Й': 'Q',
                 'ц': 'w', 'Ц': 'W', 'У': 'E', 'у': 'e', 'К': 'R', 'к': 'r', 'Е': 'T', 'е': 't',
                 'Н': 'Y',
                 'н': 'y', 'Г': 'U', 'г': 'u', 'Ш': 'I', 'ш': 'i', 'Щ': 'O', 'щ': 'o', 'З': 'P',
                 'з': 'p',
                 'Х': '{', 'х': '', 'ъ': '}', 'Ъ': '}', 'Ф': 'A', 'ф': 'a',
                 'Ы': 'S',
                 'ы': 's', 'В': 'D', 'в': 'd', 'А': 'F', 'а': 'f', 'П': 'G', 'п': 'g', 'Р': 'H',
                 'р': 'h',
                 'О': 'J', 'о': 'j', 'Л': 'K', 'л': 'k', 'Д': 'L', 'д': 'l', 'Ж': ':', 'ж': ';',
                 'Э': '"',
                 'э': '\'', 'Я': 'Z', 'я': 'z', 'Ч': 'X', 'ч': 'x', 'С': 'C', 'с': 'c', 'М': 'V',
                 'м': 'v',
                 'И': 'B', 'и': 'b', 'Т': 'N', 'т': 'n', 'Ь': 'M', 'ь': 'm', 'Б': '<', 'б': ',',
                 'Ю': '>',
                 'ю': '.'}

layout_eng_ru = dict(zip(layout_ru_eng.values(), layout_ru_eng.keys()))


class LayoutSwapper:
    def __init__(self):
        pass
    def swap_engrus(self, word):
        res = ""
        for ch in word:
            res += layout_eng_ru.get(ch, ch)
        return res

