from datetime import datetime

from logx.common.common_object import (
        CustomDate, Multiple, DatabaseResult, Result, Customer
)
from .settings_handler import DatabaseSettings
from logx.common.algo import update_process

from pymongo import MongoClient
from rich.table import Table
from rich.console import Console
from rich.text import Text
from rich import box

import dns


# Current DNS fix
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']


class Database:

    def __init__(self) -> None:
        self.settings = DatabaseSettings()

        if not self.settings.srv:
            client = MongoClient(
                host        = self.settings.host,
                port        = self.settings.port,
                username    = self.settings.user,
                password    = self.settings.passw,
                authSource  = self.settings.database
            )
        else:
            client = MongoClient(self.settings.host)

        self.db = client[self.settings.database]
        self.main = self.settings.record_collection_name
        self.test = self.settings.dev_collection_name
        self.history = self.settings.history_collection_name
        self.history_test = "modified_test"

    def get(self, date: str | CustomDate | list[str], test: bool = False, **kwargs) -> DatabaseResult | bool:
        """
        Optional:
        c: Collection Names
        show_table: bool (Default to False) Display result as a table
        """

        show_table = kwargs.get("show_table", False)

        def internal_func(date: str | CustomDate) -> Multiple | dict[None, None]:
            if type(date) == str:
                date = CustomDate(date)

            collection = self.db[kwargs.get("c", self.main)] if not test else self.db[self.test]
            result = collection.find_one(
                {
                    'day'   : date.result['data'][0],
                    'month' : date.result['data'][1],
                    'year'  : date.result['data'][2]
                }
            )

            if result:
                m = Multiple()
                m.repack(result)

                return m
            else:
                return {}

        def display(m: Multiple) -> None:
            table = Table(show_footer=True, box=box.SIMPLE_HEAD)
            console = Console()

            table.add_column("No")
            table.add_column("Name", overflow="crop")
            table.add_column("Transaction", footer=Text(m.total_idr, justify="center"))
            table.add_column("Transfer")
            table.add_column("Diff")
            table.add_column("Note")

            for num, items in enumerate(m.records):
                table.add_row(str(num + 1), items.cname, items.trx_idr, items.trf_idr, items.diff_idr, items.note)

            console.print(table, justify="center")

        a_result = []
        if type(date) == list:
            for i in date:
                res = internal_func(i) if internal_func(i) else {}

                if show_table and res:
                    display(res)
                elif not res:
                    a_result.append(f"{CustomDate(i).result['display']} not found!")
                else:
                    a_result.append(res)
        else:
            res = internal_func(date) if internal_func(date) else {}

            if show_table and res:
                display(res)
            elif not res:
                return DatabaseResult(Result.S_NFOUND, {})
            else:
                return DatabaseResult(Result.S_SUCCESS, res)

        if not show_table:
            return DatabaseResult(Result.S_SUCCESS, a_result)

    def get_all(self, test: bool = False) -> DatabaseResult:
        collection = self.db[self.main] if not test else self.db[self.test]
        holder = []

        result = collection.find()
        for i in result:
            res = Multiple()
            res.repack(i)

            if res.records:
                holder.append(res)

        return DatabaseResult(Result.S_SUCCESS, holder)

    def save(self, data: Multiple, test: bool = False) -> DatabaseResult:
        if not data:
            return DatabaseResult(Result.E_VAR, False)

        if self.get(data._date, test).C_RESULT == Result.S_SUCCESS:
            return DatabaseResult(Result.S_EXISTS, False)

        collection = self.db[self.main] if not test else self.db[self.test]
        result = collection.insert_one(data.unpack())

        return DatabaseResult(Result.S_SUCCESS, result.acknowledged)

    def update(self, data: Multiple, test: bool = False) -> DatabaseResult:

        r = self.get(data._date, test)
        if r.C_RESULT == Result.S_SUCCESS:
            history = self.db[self.history] if not test else self.db[self.history_test]
            collection = self.db[self.main] if not test else self.db[self.test]

            old_data = r.VALUE.unpack()
            unpacked_data = data.unpack()

            old_data['modified_at'] = datetime.today()
            changed = update_process(r.VALUE, data)

            old_data['data'] = changed['data']
            old_data['update_mode'] = changed['operation']
            del old_data['total']

            print(old_data)

            history.insert_one(old_data)
            result = collection.update_one({
                'day':      unpacked_data['day'],
                'month':    unpacked_data['month'],
                'year':     unpacked_data['year']
            }, { '$set': {
                'data':     unpacked_data['data'],
                'total':    unpacked_data['total'],
                'note':     unpacked_data['note'],
                'modified_date': datetime.today()
            }})

            return DatabaseResult(Result.S_SUCCESS, result.acknowledged)
        else:
            return DatabaseResult(Result.S_NFOUND, False)

    def delete(self, date: str | CustomDate, test: bool = False) -> DatabaseResult:

        r = self.get(date, test)
        if r.C_RESULT == Result.S_SUCCESS:
            collection = self.db[self.main] if not test else self.db[self.test]
            unpacked_data = r.VALUE.unpack()

            result = collection.delete_one({
                'day': unpacked_data['day'],
                'month': unpacked_data['month'],
                'year': unpacked_data['year']
            })

            if result.acknowledged:
                rs = self.get(date, c="history")
                if rs.C_RESULT == Result.S_SUCCESS:
                    c_rs = self.db["history"]
                    c_rs.delete_many({
                        'day': unpacked_data['day'],
                        'month': unpacked_data['month'],
                        'year': unpacked_data['year']
                    })

            return DatabaseResult(Result.S_SUCCESS, result.acknowledged)
        else:
            return DatabaseResult(Result.S_NFOUND, False)


    def get_customers_list(self) -> None:
        # Get all customer name and save to new collection

        data = self.get_all()
        c_name = {}

        for items in data.VALUE:
            for c_list in items.records:
                if c_list.cname not in list(c_name.keys()):
                    print(f"Appending {c_list.cname}")
                    c_name[c_list.cname] = Customer(c_list.cname, c_list.trx)
                else:
                    print(f"Increasing {c_list.cname}")
                    #c_res = c_name[c_list.cname]
                    #c_res.increase(c_list.trx)
                    #c_name[c_list.cname] = c_res
                    c_name[c_list.cname].increase(c_list.trx)

        return c_name
