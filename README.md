## Math_Practice

- A two part project that I coded to help my brother practice amc8 math problems!
- Part 1: math_scraping has code that web scrapes the amc8 problems, creates a database, and inserts those problems into the database
- Part 2: math_app is a simple web app that displays the problems in the database based on their category


## Built with

- Flask (https://flask.palletsprojects.com/en/3.0.x/)
- MySQL (https://www.mysql.com/)
- Python (https://www.python.org/)
- Html, Css, JavaScript


## Development

First git clone the repo to get a local copy of the code.
```
git clone https://github.com/hellenzhao/AMC_8_Practice.git
cd AMC_8_Practice
```

Install dependencies:
```
pip install selenium ipython-sql pymysql sqlalchemy pandas
```

Insert database login credentials:
* math_scraping: make_amc8_html.py, make_contests_db.ipynb
* math_app: config.py


Web scraping / database setup:
* Web scrape the amc8 problems by running get_amc8.py - this will take a while, and is optional since I've included Scraped_AMC_8.csv already
* Run make_contests_db.ipynb to create the database and insert the problems.


Now to run math_app, first install dependencies in a virtual environment (below commands work for Mac):
```
cd math_app
python3 -m venv venv
source venv/bin/activate
pip install flask python-dotenv flask-sqlalchemy pymysql
```

Start a local web server by running:
```
flask run
```

Open http://127.0.0.1:5000 to view in browser.
