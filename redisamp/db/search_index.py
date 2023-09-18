from dataclasses import dataclass
from typing import Literal

from .util import array_response_to_dict

@dataclass
class SearchAttribute:
    id: str
    name: str
    type: str
    type_options: list[str]

class SearchIndex:
    name: str = ""
    key_type: Literal["HASH", "JSON"]
    prefixes: list[str] = []
    attributes: list[SearchAttribute] = []
    num_docs: int = 0
    is_indexing: bool = False
    indexing_progress: float = 0.0

    _raw: dict

    def _parse_index_def(self, index_def: dict):
        index = array_response_to_dict(index_def)

        self.name = index["index_name"]
        self.key_type = index["index_definition"]["key_type"]
        self.prefixes = index["index_definition"]["prefixes"]
        self.num_docs = index["num_docs"]
        self.is_indexing = bool(int(index["indexing"]))
        self.indexing_progress = index["percent_indexed"]

        return index

    def __init__(self, index_def: dict):
        self._raw = self._parse_index_def(index_def)


    @property
    def size_mb(self) -> float:
        size_fields = (
            "inverted_sz_mb", 
            "vector_index_sz_mb", 
            "offset_vectors_sz_mb", 
            "doc_table_size_mb", 
            "sortable_values_size_mb",
            "key_table_size_mb",
        )
        return sum([self._raw[field] for field in size_fields])