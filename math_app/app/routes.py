from app import app, db
from app.models import Category, Amc8
from flask import render_template
import sqlalchemy as sa

@app.route('/index')
@app.route('/home')
@app.route('/')
def index():
    return render_template('index.html', title='Home')


@app.route('/categories')
def categories():
    cats = db.session.scalars(sa.select(Category))

    return render_template('categories.html', categories=cats)


@app.route('/categories/<category>')
def problems(category):
    if (category == 'all'):
        problems = db.session.scalars(sa.select(Amc8))
    else:
        query = sa.select(Amc8).where(Amc8.tags.like('%{cat}%'.format(cat=category)))
        problems = db.session.scalars(query)

    return render_template('problems.html', contest="AMC8", category=category, problems=problems)