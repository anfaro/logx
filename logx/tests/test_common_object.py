from logx.common.common_object import CustomDate, Record, Multiple

def test_custom_date():
    a = CustomDate("11 02")
    b = CustomDate("5 6")
    c = CustomDate("4 3 2007")

    d = CustomDate("15 Agu")
    e = CustomDate("14 Mei 2005")
    f = CustomDate("18 jan 2004")

    g = CustomDate("17-12")
    h = CustomDate("8-jun")
    i = CustomDate("9-Jul-2026")

    assert a.result == {'data': ['11', 'Feb', str(CustomDate().today_year)], 'display': f'11 Februari {str(CustomDate().today_year)}'}
    assert b.result == {'data': ['5', 'Jun', str(CustomDate().today_year)], 'display': f'5 Juni {str(CustomDate().today_year)}'}
    assert c.result == {'data': ['4', 'Mar', '2007'], 'display': '4 Maret 2007'}
    assert d.result == {'data': ['15', 'Agu', str(CustomDate().today_year)], 'display': f'15 Agustus {str(CustomDate().today_year)}'}
    assert e.result == {'data': ['14', 'Mei', '2005'], 'display': '14 Mei 2005'}
    assert f.result == {'data': ['18', 'Jan', '2004'], 'display': '18 Januari 2004'}
    assert g.result == {'data': ['17', 'Des', str(CustomDate().today_year)], 'display': f'17 Desember {str(CustomDate().today_year)}'}
    assert h.result == {'data': ['8', 'Jun', str(CustomDate().today_year)], 'display': f'8 Juni {str(CustomDate().today_year)}'}
    assert i.result == {'data': ['9', 'Jul', '2026'], 'display': '9 Juli 2026'}


def test_record():
    a = Record("Test 1", 500, 500, "This is a Test")
    b = Record("Test 2", 1080, 1100, "Test diff")

    assert a.trx == 500
    assert a.trf == 500
    assert a.diff == 0

    assert b.trx == 1080
    assert b.trf == 1100
    assert b.diff == 20


def test_multiple():
    a_r = Record("Test 1", 500, 500, "Test dummy 1")
    b_r = Record("Test 2", 700, 700, "Test dummy 2")
    c_r = Record("Test 3", 350, 400, "Test dummy 3")
    d_r = Record("Test 4", 600, 600, "Test dummy 4")
    e_r = Record("Test 5", 1050, 1200, "Test dummy 5")

    m = Multiple("11 agu 2020", "Test multiple dummy")
    m.add(a_r)
    m.add(b_r)
    m.add(c_r)
    m.add(d_r)
    m.add(e_r)

    m_2 = Multiple()
    d = CustomDate()

    assert m._date.result == {'data': ['11', 'Agu', '2020'], 'display': '11 Agustus 2020'} #type: ignore
    assert m.total == 3200

    assert m.delete(4) == True
    assert m.total == 2150

    assert m.delete(5) == False

    assert m_2._date.result == d.result #type: ignore

    assert m.unpack() == {
        'day'   : '11',
        'month' : 'Agu',
        'year'  : '2020',
        'data'  : [
            ["Test 1", 500, 500, 0, "Test dummy 1"],
            ["Test 2", 700, 700, 0, "Test dummy 2"],
            ["Test 3", 350, 400, 50, "Test dummy 3"],
            ["Test 4", 600, 600, 0, "Test dummy 4"],
        ],
        'total' : 2150,
        'note'  : "Test multiple dummy"
    }

    assert m_2.unpack() == {}

    dummy = {
        '_id'   : "A_ID",
        'day'   : "14",
        'month' : "des",
        'year'  : "2021",
        'data'  : [["Test1", 650, 650, 0], ["Test2", 350, 400, 50, "Test repack"]],
        'total' : 1000
    }

    m_3 = Multiple()
    m_3.repack(dummy)

    assert m_3.total == 1000
    assert m_3._date.result == {'data': ['14', 'Des', '2021'], 'display': '14 Desember 2021'} #type: ignore
