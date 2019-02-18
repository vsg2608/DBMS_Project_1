""" Demo Python Flask Application """

import os
import sys

import psycopg2 as pg

from flask import Flask, render_template, redirect

dbname = "project"
password = "3010"
conn = pg.connect(database = dbname, user = "postgres", password = password, host = "localhost", port = "5432")
cur = conn.cursor()

app = Flask(__name__)


@app.route("/")
def root():
    cur.execute(
        """
        SELECT * from rest limit 10;
    """)
    rows = cur.fetchall()
    print(rows)
    return render_template("base.html", rows=rows)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
