from .base import BaseKey
from .hash import HashKey
from .json import JsonKey
from .list import ListKey
from .set import SetKey
from .sorted_set import SortedSetKey
from .stream import StreamKey
from .string import StringKey


type_widgets = {
    "ReJSON-RL": JsonKey,
    "hash": HashKey,
    "string": StringKey,
    "list": ListKey,
    "set": SetKey,
    "zset": SortedSetKey,
    "stream": StreamKey,
}

KEY_VALUE_ID = "key-value"


def render_key(key_type: str, key_name: str) -> BaseKey:
    return type_widgets.get(key_type, BaseKey)(key=key_name, id=KEY_VALUE_ID)
