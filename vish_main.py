import psycopg2 as pg
from flask import Flask, render_template, redirect
import os
import sys

dbname = "project"
password = "Password@123"
conn = pg.connect(database = dbname, user = "postgres", password = password, host = "13.233.41.140", port = "5432")
cur = conn.cursor()

