"""
This file contains all system object
Created by Anang Faturrohman <anang42429@gmail.com>
"""

from __future__ import annotations 
from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Iterable, Any


# Utility Functions
def idr_currency(source: int) -> str:
    """
    Convert a number to IDR Currency
    """

    if source == 0:
        return ""

    currency = "Rp. "

    # Adding 3 zeros
    source = str(source)
    source = source.split('.') if '.' in source else source
    if type(source) == list:
        if len(source[1]) == 1:
            source[1] = source[1] + '00'
        elif len(source[1]) == 2:
            source[1] = source[1] + '0'
        else:
            source[1] = source[1] + '000'

        source = ''.join(source)

    else:
        source = source + '000'


    # Adding thousand separator
    source = format(int(source), ',d').replace(',', '.')

    source = currency + source
    return source

# Class Object

class CustomDate:
    """
    Opt: Optional
    Template ( [Day] [Opt-Month] [Opt-Year] )

    Possible Input Format (str):
    1. 11-jan-2021
    2. 11 jan 2021
    3. 11-01-2021
    4. 11-1-2021
    """

    __month_name = {
        1: ["Januari", "Jan"],
        2: ["Februari", "Feb"],
        3: ["Maret", "Mar"],
        4: ["April", "Apr"],
        5: ["Mei", "Mei"],
        6: ["Juni", "Jun"],
        7: ["Juli", "Jul"],
        8: ["Agustus", "Agu"],
        9: ["September", "Sep"],
        10: ["Oktober", "Okt"],
        11: ["November", "Nov"],
        12: ["Desember", "Des"]
    }

    today_day   = datetime.today().day
    today_month = datetime.today().month
    today_year  = datetime.today().year

    result = {}

    def __init__(self, date: str = "NOINPUT") -> None:
        if date != "NOINPUT":
            self.date = date
        else:
            self.date = ""

        self.get_result()
        self.system_date_format()

    def __handle_month_name(self, date: str) -> int:
        month_values = list(self.__month_name.values())
        index = 0

        for i, val in enumerate(month_values):
            if date.capitalize() in val:
                index = i
                break

        return list(self.__month_name.keys())[index]

    def __repr__(self) -> str:
        return self.result['display']

    def __eq__(self, o: CustomDate) -> bool:
        return self.system_date == o.system_date

    def __gt__(self, o: CustomDate) -> bool:
        return self.system_date > o.system_date

    def __lt__(self, o: CustomDate) -> bool:
        return self.system_date < o.system_date

    def get_result(self) -> None:
        date_splitted = self.date.split("-") if "-" in self.date else self.date.split(" ")

        match (len(date_splitted), bool(self.date)):
            case (1, False):
                self.result = {
                    'data': [str(self.today_day), self.__month_name[self.today_month][1], str(self.today_year)],
                    'display': f"{self.today_day} {self.__month_name[self.today_month][0]} {self.today_year}"
                }
            case (1, True):
                self.result = {
                    'data': [date_splitted[0], self.__month_name[self.today_month][1], str(self.today_year)],
                    'display': f"{date_splitted[0]} {self.__month_name[self.today_month][0]} {self.today_year}"
                }
            case (2, True):
                try:
                    int(date_splitted[1])
                    date_splitted[1] = int(date_splitted[1].lstrip("0")) if "0" in date_splitted[1] else int(date_splitted[1]) #type: ignore
                except ValueError:
                    date_splitted[1] = self.__handle_month_name(date_splitted[1]) #type: ignore

                self.result = {
                    'data': [date_splitted[0], self.__month_name[date_splitted[1]][1], str(self.today_year)],
                    'display': f"{date_splitted[0]} {self.__month_name[date_splitted[1]][0]} {self.today_year}"
                }
            case (3, True):
                try:
                    int(date_splitted[1])
                    date_splitted[1] = int(date_splitted[1].lstrip("0")) if "0" in date_splitted[1] else int(date_splitted[1]) #type: ignore
                except ValueError:
                    date_splitted[1] = self.__handle_month_name(date_splitted[1]) #type: ignore

                self.result = {
                    'data': [date_splitted[0], self.__month_name[date_splitted[1]][1], date_splitted[2]], #type: ignore
                    'display': f"{date_splitted[0]} {self.__month_name[date_splitted[1]][0]} {date_splitted[2]}" #type: ignore
                }
            case _:
                print("ERROR! Too many input")
                return

    def system_date_format(self) -> None:
        month = {
            "Jan": "Jan",
            "Feb": "Feb",
            "Mar": "Mar",
            "Apr": "Apr",
            "Mei": "May",
            "Jun": "Jun",
            "Jul": "Jul",
            "Agu": "Aug",
            "Sep": "Sep",
            "Okt": "Oct",
            "Nov": "Nov",
            "Des": "Dec"
        }

        custom = self.result['data'].copy()
        custom[1] = month[custom[1]]
        self.system_date = datetime.strptime(' '.join(custom), "%d %b %Y")
        

@dataclass
class Record:

    """
    Record (DataClass)

    Input:
    - Customer Name (Required)          (cname)
    - Total Transaction (Required)      (trx)
    - Total Paid By Transfer (Required) (trf)
    - Difference (Auto Generated)       (diff)
    - Note (Optional)                   (note)
    """

    cname   : str
    trx     : int
    trf     : int
    diff    : int = field(init=False)
    note    : str = ""

    trx_idr : str = field(init=False)
    trf_idr : str = field(init=False)
    diff_idr: str = field(init=False)

    def __post_init__(self) -> None:
        self.diff = self.trf - self.trx

        self.trx_idr = idr_currency(self.trx)
        self.trf_idr = idr_currency(self.trf)
        self.diff_idr= idr_currency(self.diff)

    def unpack(self) -> List[str, int]:
        return [self.cname, self.trx, self.trf, self.diff, self.note]

@dataclass
class Customer:
    id : int = field(init=False)
    name : str
    total: int
    total_idr: str = field(init=False, default='')

    def __post_init__(self) -> None:
        self.total_idr = idr_currency(self.total)

    def increase(self, t_value: int) -> None:
        self.total = self.total + t_value
        self.total_idr = idr_currency(self.total)

    def unpack(self) -> dict[str, Any]:
        return {
            '_id': self.id,
            'name':self.name,
            'total':self.total
        }

    def repack(self, data: dict[str, Any]) -> None:
        self.id = str(data['_id'])
        self.name = data['name']
        self.total = data['total']
        self.total_idr = idr_currency(data['total'])

    def __repr__(self) -> str:
        return self.name

@dataclass
class Multiple:

    """
    Multiple (DataClass)
        A collections of multiple records (class Record)

    Input:
    - Id (Auto Generated)                                   (_id)
    - Date (Required)                                       (_date)
    - Note (Optional)                                       (note)
    - Records (Multiple Record - Variable - Auto Generated) (records)
    - Total (Auto Generated)                                (total)
    """

    _id     : str = field(init=False, default='')
    _date   : str | CustomDate = ""
    note    : str = ""
    records : List[Record] = field(init=False, default_factory=list)
    total   : int = field(init=False, default=0)

    total_idr: str = field(init=False)

    def __post_init__(self) -> None:
        self._date = CustomDate(self._date) #type: ignore

    def __len__(self) -> int:
        return len(self.records)

    def __iter__(self) -> Iterable:
        return iter(self.records)

    def add(self, record: Record):
        self.total += record.trx
        self.total_idr = idr_currency(self.total)
        self.records.append(record)

    def delete(self, index: int) -> bool:
        try:
            self.total -= self.records[index].trx
            del self.records[index]

            return True

        except IndexError:
            return False

    def unpack(self) -> dict[str, str | int | List[Any]]:
        if len(self.records) == 0:
            return {}

        modified = []
        for i in self.records:
            modified.append(i.unpack())

        return {
            'day'   : self._date.result['data'][0], #type: ignore
            'month' : self._date.result['data'][1], #type: ignore
            'year'  : self._date.result['data'][2], #type: ignore
            'data'  : modified,
            'total' : self.total,
            'total_idr': self.total_idr,
            'note'  : self.note
        }

    def repack(self, data: dict) -> None:
        if not data:
            return

        self._id = str(data['_id'])
        self._date = CustomDate(f"{data['day']} {data['month']} {data['year']}")
        self.note = data.get('description', "")
        
        for i in data['data']:
            note = i[4] if len(i) == 5 else ""
            t = Record(i[0], i[1], i[2], note)
            self.add(t)


@dataclass
class Result:
    """
    Result Code
    S_SUCCESS   :   A Successfull operation
    S_EXISTS    :   A Successfull operation result document already exists (Database)
    S_NFOUND    :   A Successfull operation yield no document result
    E_CONN      :   Failed to connect to a database
    E_VAR       :   Assigned variable is empty
    """

    S_SUCCESS   = [0, "Operation Successfully executed!"]
    S_EXISTS    = [1, "Document already exists!"]
    S_NFOUND    = [2, "No document found!"]
    E_CONN      = [3, "Failed to connect to database!"]
    E_VAR       = [4, "Empty data!"]


@dataclass
class DatabaseResult:

    """
    A database operation result
    
    C_RESULT    :   Code Result (class Result)
    MESSAGE     :   A result description
    VALUE       :   Operation value
    """

    C_RESULT    : Result
    MESSAGE     : str = field(init=False, default='')
    VALUE       : Any

    def __post_init__(self):
        self.MESSAGE = self.C_RESULT[1]
