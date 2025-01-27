from __future__ import annotations
from dataclasses import dataclass
from src.orchestrators.readers.base_reader import BaseReader


@dataclass
class TemplateReader(BaseReader):

    @staticmethod
    def read(selector: str, extension: str = "") -> str:
        idx = -1
        try:
            idx = selector.index(".")
        except ValueError:
            pass
        folders = ["configs"]
        if idx >= 0:
            field = selector[:idx]
            filename = selector[idx + 1 :]
            folders.append(field)
        else:
            filename = selector
        return TemplateReader(filename, extension, folders=folders).recurse().file
