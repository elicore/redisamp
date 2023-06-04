TYPE_NAMES = {
    "ReJSON-RL": "JSON",
    "hash": "Hash",
    "string": "String",
    "list": "List",
    "set": "Set",
    "zset": "Sorted Set",
    "stream": "Stream",
    "graphdata": "Graph",
    "TSDB-TYPE": "TS",
    "MBbloom--": "Bloom",
}


class RedisKey:
    def __init__(self, name: str, type: str):
        self.name = name
        self.type = type

    def __str__(self) -> str:
        return self.name
