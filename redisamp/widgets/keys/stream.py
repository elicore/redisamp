from redisamp.db import db
from redisamp.widgets.keys import BaseKey

from rich.text import Text
from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import DataTable, Label
from walrus import Stream


import datetime


class StreamKey(BaseKey):
    @staticmethod
    def message_id_to_str(message_id: str) -> str:
        ts, sequence = message_id.split("-")
        timestamp = (
            int(ts) / 1000
        )  # timestamp is in milliseconds, unix timestamp is in seconds
        ms = ts[-3:]  # milliseconds value
        date_time = datetime.datetime.fromtimestamp(int(timestamp))

        # convert timestamp to string in dd-mm-yyyy HH:MM:SS
        str_date_time = date_time.strftime(f"%d-%m-%Y %H:%M:%S.{ms}")

        return f"{str_date_time}-{sequence}"

    def compose(self) -> ComposeResult:
        redis = db.sync
        table = DataTable(fixed_columns=1)
        table.cursor_type = "row"
        stream = Stream(redis, self.key)

        field_names = set()

        # get the last 100 messages in the stream
        messages = stream.revrange(count=100)

        # gather the field names to build the data table
        [field_names.update(m[1].keys()) for m in messages]
        if field_names:
            table.add_columns("ID", *field_names)

            for message in messages:
                message_id_display = self.message_id_to_str(message[0])
                cells = [message_id_display] + [message[1][f]
                                                for f in field_names if f in message[1]]
                table.add_row(*cells, key=message[0])
            yield table
            # TODO remove, this is a workaround for a bug that causes this widget not to be rendered
            yield Label(" ")
        else:
            yield Container(
                Label(
                    Text.assemble("No Messages in ", (self.key, "bold underline"))
                ), 
                id="stream-no-messages"
                    )