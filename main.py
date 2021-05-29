# Todd McCullough 2021

from datetime import date, datetime, timedelta
from flask import Flask
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for, send_file

from werkzeug.security import check_password_hash, generate_password_hash

import db
import functools
import numpy as np
import os
import pandas as pd

today = date.today().strftime('%Y-%m-%d')
year = today[:4]


app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
        SECRET_KEY='dev', # change to a random value later when deploying
        DATABASE=os.path.join(app.instance_path, 'main.sqlite'),
    )

def send_email():
    try:
        client = request.form['email']
        message = request.form['message']
        if client:
            send.send_email(client,message)
    except:
        pass

@app.context_processor
def inject_user():
    send_email()

    try:
        session['theme'] = request.form['theme']
    except:
        try:
            session['theme'] = session.get('theme')
        except:
            session['theme'] = 'dk'

    return dict(
    company = 'wip', ext = '.svg', folder = 'icons-iso',
    theme_mode = session['theme'],theme = 'clean',year = year,
    )

@app.route('/', methods=['GET','POST'])
def index():
    print( url_for(request.endpoint),' SESSION',session,'\n')

    # load the site csv send_file
    # this allows editing posts from another file and saves formatting in the html
    siteinfo = pd.read_csv('datasets/site/siteinfo.csv')

    df1 = siteinfo[siteinfo['section'] == 'land']
    df2 = siteinfo[siteinfo['section'] == 'one'].copy()
    df2 = df2.reset_index()
    df3 = siteinfo[siteinfo['section'] == 'two'].copy()
    df3 = df3.reset_index()
    df4 = siteinfo[siteinfo['section'] == 'three'].copy()
    df4 = df4.reset_index()
    df5 = siteinfo[siteinfo['section'] == 'four'].copy()
    df5 = df5.reset_index()
    print(df1)
    return render_template('index.html',

    landlst = df1, weblst = df2, dashlst = df3, datalst = df4, mllst = df5)

@app.route('/link', methods=['GET','POST'])
def link():
    return render_template('link.html')

@app.route('/about', methods=['GET','POST'])
def about():
    return render_template('about.html')


db.init_app(app)

if __name__ == "__main__":
    app.run()
