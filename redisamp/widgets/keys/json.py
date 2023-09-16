from redisamp.db import db
from redisamp.widgets.keys import BaseKey


from rich.text import Text
from textual.app import ComposeResult
from textual.binding import Binding, BindingType
from textual.widgets import Tree
from textual.widgets.tree import TreeNode


from typing import ClassVar


class JsonKey(BaseKey):
    tree: Tree = Tree("")

    BINDINGS: ClassVar[list[BindingType]] = [
        Binding("right", "expand_node", "Expand", show=False),
        Binding("left", "collapse_node", "Collapse", show=False),
    ]

    def action_expand_node(self) -> None:
        if selected := self.tree.cursor_node:
            if selected.allow_expand and not selected.is_expanded:
                selected.expand()

    def action_collapse_node(self) -> None:
        if selected := self.tree.cursor_node:
            if selected.allow_expand and selected.is_expanded:
                selected.collapse()

    def compose(self) -> ComposeResult:
        redis = db.sync
        json_obj = redis.json().get(self.key)

        self.tree = Tree("")
        self.tree_from_json(self.tree.root, json_obj)
        self.tree.root.expand()
        yield self.tree

    @classmethod
    def tree_from_json(cls, node: TreeNode, json_data: object) -> None:
        """Adds JSON data to a node.
        Args:
            node (TreeNode): A Tree node.
            json_data (object): An object decoded from JSON.
        """
        from rich.highlighter import ReprHighlighter

        highlighter = ReprHighlighter()

        def add_node(name: str, node: TreeNode, data: object) -> None:
            """Adds a node to the tree.
            Args:
                name (str): Name of the node.
                node (TreeNode): Parent node.
                data (object): Data associated with the node.
            """
            if isinstance(data, dict):
                label = Text.assemble(
                    Text.from_markup(f"[b]{name}[/b] : {{ "),
                    highlighter(repr(len(data))),
                    " }",
                )
                node.set_label(label)
                if len(data) > 0:
                    for key, value in data.items():
                        new_node = node.add("")
                        add_node(key, new_node, value)
                else:
                    node.allow_expand = False
            elif isinstance(data, list):
                label = Text.assemble(
                    Text.from_markup(f"[b]{name}[/b] : [ "),
                    highlighter(repr(len(data))),
                    " ]",
                )
                node.set_label(label)
                if len(data) > 0:
                    for index, value in enumerate(data):
                        new_node = node.add("")
                        add_node(f"[{index}]", new_node, value)
                else:
                    node.allow_expand = False
            else:
                node.allow_expand = False

                # figure out how to display the value according to its type
                # json values should be rendered rather than python ones
                if type(data) == bool:
                    if data:
                        rendered_data = Text.from_markup("[blue]true[/blue]")
                    else:
                        rendered_data = Text.from_markup("[red]false[/red]")
                elif data is None:
                    rendered_data = Text.from_markup("[purple]null[/purple]")
                else:
                    rendered_data = highlighter(repr(data))

                if name:
                    label = Text.assemble(
                        Text.from_markup(f"[b]{name}[/b] : "),
                        rendered_data
                    )
                else:
                    label = rendered_data
                node.set_label(label)

        add_node("$", node, json_data)