from typing import Tuple
from enum import IntEnum, Enum


class TupleEnum(Tuple, Enum):
    pass


class StrEnum(str, Enum):
    pass


class Color(TupleEnum):
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    DARK_GRAY = (110, 110, 110)


class Font(StrEnum):
    DEFAULT = ''


class TextScope(IntEnum):
    NONE = 0
    '''Placeholder, should be defined when implementing.'''
    SYS = 1
