from flask import Flask, render_template
from logx.data.database_handler import Database
from logx.common.common_object import idr_currency

app = Flask(__name__)

@app.route('/')
def welcome():
    d = Database()
    v = d.get('20').VALUE

    modified = []
    for items in v.records:
        d1 = dict(
            name=items.cname,
            trx=items.trx_idr,
            trf=items.trf_idr,
            diff=items.diff_idr,
            note=items.note
        )
        modified.append(d1)

    return render_template('welcome.html', m=modified)



app.run(debug=True)
