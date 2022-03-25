from rich.table import Table
from rich.console import Console

from textual.app import App
from textual.widgets import Placeholder, Header, ScrollView

from logx.data.database_handler import Database

class ConsoleGui(App):

    async def on_mount(self) -> None:

        body = ScrollView(auto_width=True)

        await self.view.dock(Header(tall=False, clock=False), edge="top")
        await self.view.dock(body, edge="top")

        d = Database()
        c = Console()
        result = d.get("24", show_table=True)

        await body.update(c.print(result, justify="center"))
