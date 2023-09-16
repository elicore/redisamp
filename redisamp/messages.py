from textual.message import Message


class KeysFilterChanged(Message):
    def __init__(self, filter_expression: str = '*') -> None:
        self.filter_expression = filter_expression
        super().__init__()