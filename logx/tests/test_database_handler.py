import random

from logx.data.database_handler import Database
from logx.common.common_object import *


def test_save():
    multiple_data = Multiple("12 nov 2021", "A Test")
    
    for i in range(10):
        trx_value = random.randint(100, 5500)
        tr = Record(
            f"Test {i}",
            trx_value,
            trx_value + random.randint(0, 100),
            f"Test added {i}"
        )

        multiple_data.add(tr)

    db = Database()
    assert db.save(multiple_data, test=True).C_RESULT == Result.S_SUCCESS

def test_exists():
    multiple_data = Multiple("12 nov 2021", "A Test")
    multiple_data.add(Record("Test 1", 450, 450, "Yes, this is a test"))

    db = Database()
    assert db.save(multiple_data, test=True).C_RESULT == Result.S_EXISTS

def test_get():
    db = Database()
    result = db.get("12 nov 2021", test=True)

    assert result.C_RESULT == Result.S_SUCCESS

def test_get_all():
    db = Database()
    result = db.get_all()

    assert bool(result) == True

def test_update():
    multiple_data = Multiple("12 nov 2021", "A Test")
    tr = Record("Test Update", 200, 200, "Testing an update")
    multiple_data.add(tr)

    db = Database()
    assert db.update(multiple_data, test=True).VALUE == True

def test_delete():
    db = Database()
    assert db.delete("12 nov 2021", test=True).VALUE == True
