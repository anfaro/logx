from logx.common.algo import Node, BinarySearch, update_process
from logx.common.common_object import CustomDate, Multiple, Record
from logx.data.database_handler import Database

def test_add():

    m1 = Multiple("12 mar 2021")
    m2 = Multiple("17 feb 2021")
    m3 = Multiple("14 des 2000")
    m4 = Multiple("20 jan 2021")
    m5 = Multiple("3 okt 2020")
    m6 = Multiple("20 jan 2021") # For test duplicate

    n1 = Node()
    b1 = BinarySearch()
    b1.add(n1, m1)
    b1.add(n1, m2)
    b1.add(n1, m3)
    b1.add(n1, m4)
    b1.add(n1, m5)
    b1.add(n1, m6)

    b1.traverse(n1)
    print(b1.traverse_result)

    result = b1.find(n1, "20 jan 2021")

    not_found = b1.find(n1, "21 okt 2020")
    assert not_found == {}

def test_sort_db():
    db = Database()
    a_node = Node()
    bns = BinarySearch()

    db_result = db.get_all()

    print("Before Traverse")
    for i in db_result.VALUE:
        bns.add(a_node, i)
        print(i._date)

    print("\nAfter Traverse")
    bns.traverse(a_node)
    for i in bns.traverse_result:
        print(i._date)

def test_update_process():
    a = Multiple()
    b = Multiple()

    c = Multiple()
    d = Multiple()

    a.add(Record("Test", 560, 560))
    a.add(Record("Test2", 100, 100))
    a.add(Record("Test3", 1000, 1000))
    b.add(Record("Test", 560, 560))
    b.add(Record("Test2", 100, 100))
    b.add(Record("Test3", 1000, 1000))
    b.add(Record("Test4", 750, 800))

    assert update_process(a, b) == {'operation': "Added", 'data': [Record("Test4", 750, 800).unpack()]}

    c.add(Record("Test", 800, 800))
    c.add(Record("Test2", 900, 900))
    c.add(Record("Test3", 750, 800))
    d.add(Record("Test", 800, 800))
    d.add(Record("Test3", 750, 800))

    assert update_process(c, d) == {'operation': "Remove", 'data': [Record("Test2", 900, 900).unpack()]}
