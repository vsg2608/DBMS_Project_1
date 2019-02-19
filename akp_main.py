import psycopg2 as pg
from flask import Flask, render_template, redirect
import os
import sys

dbname = "project"
password = "3010"
conn = pg.connect(database = dbname, user = "postgres", password = password, host = "localhost", port = "5432")
cur = conn.cursor()

