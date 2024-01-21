import sys
import pymysql



# database connection setup

# add login credentials
user = "your_username"
password = "your_password"

sql_conn = pymysql.connect(
    user = user,
    password = password,
    port = 3306,
    cursorclass = pymysql.cursors.DictCursor,
    autocommit = True
)
cur = sql_conn.cursor()

def execute_query(str):
    res = cur.execute(str)
    return cur.fetchall()

execute_query("use math_contests;")


# add to list later
valid_contests = ["AMC_8"]
res = execute_query("select * from category;")
valid_categories = [row['category'] for row in res]


'''
Given list of tuples of year, number, marked up problem content, write html file
'''
def write_html(filename, problems):
    f = open(filename,'w')

    f.write("<!DOCTYPE html> \n")
    f.write("<html lang='en'> \n")
    f.write("<head>\n"
        + "\t<link rel='stylesheet' href='style.css'>\n"
        + "\t<meta name='viewport' content='width=device-width, initial-scale=1.0'>\n"
        + "\t</head>\n")
    f.write("<body>\n")

    f.write(f"\t<div class='problems'>\n")
    for (year, number, content) in problems:
        f.write("<div class='problem'>\n")
        f.write(f"<h3>Year {year}, problem {number}</h3>\n")
        f.write(content)
        f.write("\n</div>\n")

    f.write('\t</div>\n')

    f.write("</body>\n" + "</html>")
    f.close()


'''
Given a contest and problem category:
retrieves corresponding problems from math_contests databases

Example: main("AMC_8", "arithmetic")
'''
def main(contest, category):
    # ensure contest and category are valid
    if contest not in valid_contests:
        sys.exit("contest is invalid")
    if category not in valid_categories:
        sys.exit("category is invalid")

    filename = contest + "_" + category + ".html"

    res = execute_query(f"select year, number, content from {contest} where tags like '%{category}%';")
    problems = [(r['year'], r['number'], r['content']) for r in res]
    
    write_html(filename, problems)


