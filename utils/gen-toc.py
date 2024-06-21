from enum import Enum
from pathlib import Path
import sys

headers = {1: 0, 2: 0, 3: 0, "appendix": 1}


class HeaderKind(Enum):
    CHAPTER = "CHAPTER"
    APPENDIX = "APPENDIX"


# def num_to_roman(x: int):
#     return {1: "I", 2: "II", 3: "III", 4: "IV", 5: "V"}[x]


def parse_header(line: str):
    h, title = line.split(maxsplit=1)
    xs = title.split("{")
    title = xs[0].strip()

    def to_kind(value: str):
        if "chapter" in value:
            return HeaderKind.CHAPTER
        elif "appendix" in value:
            return HeaderKind.APPENDIX
        else:
            return None

    return len(h), title, (to_kind(xs[1]) if len(xs) == 2 else None)


def level_to_section(level: int, kind: HeaderKind | None):
    if not kind:
        return ""

    result = ""
    headers[level] += 1

    match level:
        case 1:
            if kind == HeaderKind.CHAPTER:
                result = "Глава " + str(headers[1]) + ":"
            elif kind == HeaderKind.APPENDIX:
                result = "Приложение " + chr(64 + headers["appendix"]) + ":"
        case 2:
            result = f"{headers[1]}.{headers[2]}"
        case 3:
            result = f"{headers[1]}.{headers[2]}.{headers[3]}"

    return result


def title_to_id(title: str):
    return title.lower().replace(" ", "-")


if __name__ == "__main__" and len(sys.argv) == 2:
    last_kind = None


    with open(Path(sys.argv[1]).resolve(), "r", encoding="utf-8") as file, open("toc.md", "w", encoding="utf-8") as toc_file:
        print("# Оглавление", file=toc_file)

        for line in file.readlines():
            if line.startswith("#"):
                level, title, kind = parse_header(line)
                last_kind = kind or last_kind

                spaces = "  " * level
                section = level_to_section(level, last_kind)

                id = title_to_id(title)
                title = f"{section} {title}"
                title = f"**{title.strip()}**" if kind or level == 1 else title

                print(f"{spaces}- [{title}](#{id})", file=toc_file)
