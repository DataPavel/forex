from flask import Flask, render_template, flash, jsonify, request, redirect, url_for, Response
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, SelectField, SelectMultipleField, IntegerField, DecimalField

import os
from datetime import datetime

from wtforms.validators import InputRequired, DataRequired
from babel.numbers import format_decimal

import jinja2

import plotly
import json

import pandas as pd
import numpy as np

import utils
import plots



pd.options.mode.chained_assignment = None

# Decimal format for Jinja2
def FormatDecimal(value):
    return format_decimal(float(value), format='#,##0')
def FormatScore(value):
    return format_decimal(float(value), format='#,##0.##')

jinja2.filters.FILTERS['FormatDecimal'] = FormatDecimal
jinja2.filters.FILTERS['FormatScore'] = FormatScore





app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'


class FilterForm(FlaskForm):

    start_date = DateField('Start Date', validators=[InputRequired()])
    end_date = DateField('End Date', validators=[InputRequired()])
    base = SelectField('Base', choices=['USD', 'EUR'],
        validate_choice=True, validators=[InputRequired()])
    currency = StringField('Currency', validators=[InputRequired()])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET',"POST"])
def index():
    form = FilterForm()
    if form.validate_on_submit():
        start_date = form.start_date.data
        end_date = form.end_date.data
        base = form.base.data
        currency = form.currency.data.upper()

        df = utils.create_query_visual(start_date="'"+str(start_date)+"'",
            end_date="'"+str(end_date)+"'", currency="'"+str(currency)+"'")
        fx = utils.create_fx_table(df, base)
        fig = plots.rates_area(fx, currency, base)
        graph=json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        num = len(list(fx.columns))

        return render_template('main.html', form=form, 
            graph=graph, fx=fx, currency=currency, num=num)
    return render_template('index.html', form=form)

@app.route('/download/')
def download():
    df = utils.create_query_download()
    return Response(
       df.to_csv(index=False),
       mimetype="text/csv",
       headers={"Content-disposition":
       "attachment; filename=rates.csv"})

@app.route('/update/')
def update():
    utils.import_to_db()
    flash('Exchange rates are up to date')
    return redirect(url_for('index'))
