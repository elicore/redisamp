from dataclasses import dataclass

# Redis data types
@dataclass
class RedisType:
    type_id: str
    name: str
    bgcolor: str

REDIS_TYPES = {
    "ReJSON-RL":    RedisType("ReJSON-RL", "JSON", "#b8c5db"),
    "hash":         RedisType("hash", "Hash", "#cdddf8"),
    "string":       RedisType("string", "String", "#c7b0ea"),
    "list":         RedisType("list", "List", "#a5d4c3"),
    "set":          RedisType("set", "Set", "#d4baa7"),
    "zset":         RedisType("zset", "ZSet", "#d9a0c6"),
    "stream":       RedisType("stream", "Stream", "#c7cea8"),
    "graphdata":    RedisType("graphdata", "Graph", "#acccd7"),
    "TSDB-TYPE":    RedisType("TSDB-TYPE", "TS", "#c7c7c7"),
    "MBbloom--":    RedisType("MBbloom--", "Bloom", "#3f4b5f"),
}
