from __future__ import annotations
import os
import logging
from dataclasses import dataclass, field
from typing import List
from pylib_0xe.file.file import File

LOGGER = logging.getLogger(__name__)


@dataclass
class BaseReader:
    filename: str
    extension: str
    folders: List[str] = field(default_factory=lambda: ["configs"])
    home_path: List[str] = field(
        default_factory=lambda: [os.path.normpath(os.path.abspath(os.sep))]
    )
    base_path: str = field(default_factory=os.getcwd)
    file: str = field(default="")

    def recurse(self) -> BaseReader:
        found = False
        path = self.base_path

        def __build_path():
            if self.extension:
                return [path, *self.folders, f"{self.filename}.{self.extension}"]
            return [path, *self.folders, self.filename]

        try:
            while not found:
                if path in self.home_path:
                    raise Exception
                found = True
                try:
                    path_array = list(
                        filter(
                            lambda t: isinstance(t, str) and t,
                            __build_path(),
                        )
                    )
                    cur_path = os.path.join(*path_array)
                    if not os.path.isfile(cur_path):
                        raise Exception("not a valid file")
                    self.file = File.read_file(cur_path)
                except Exception:
                    path = os.path.abspath(os.path.normpath(os.path.join(path, "..")))
                    found = False
        except Exception:
            LOGGER.error(
                f"""Please provide a local \
                {self.base_path}/{self.filename}.{self.extension} file"""
            )
            exit(0)
        return self
