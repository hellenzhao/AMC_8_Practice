'''
Code to scrape a given math contest given corresponding links
'''


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_all_elements_located as presence, all_of
import time
import csv


# setup
options = Options()
options.add_argument('--headless')


'''
Preprocesses the list of tag lists by turning each list into a comma separated string
'''
def preprocess_tags(tags):
    tags = [(','.join(tag)).lower() for tag in tags]
    return tags


'''
Given url of community discussion post, retrieves the tags of the problem
'''
def tags_of_one_problem(url):
    driver = webdriver.Chrome(options)
    wait = WebDriverWait(driver, 10)
    driver.get(url)
    wait.until(presence((By.ID, "cmty-topic-view-right")))

    # cmty-topic-view-left also has mini post previews with tags
    post = driver.find_element(By.ID, "cmty-topic-view-right")
    # the edit button also has cmty-item-tag, so ignore that
    tags = post.find_element(By.CLASS_NAME, "cmty-itembox").find_elements(By.TAG_NAME, "a")
    
    return [tag.text for tag in tags]


'''
Given url of one year's contest, the contest name (ex: "AMC_8" or "AJHSME"), and year:
scrapes every problem, its tags, and its answer
'''
def problems_of_one_year(url, contest, year):
    answer_url = f"https://artofproblemsolving.com/wiki/index.php/{year}_{contest}_Answer_Key"

    driver = webdriver.Chrome(options)
    wait = WebDriverWait(driver, 10)

    driver.get(url)
    wait.until(presence((By.CLASS_NAME, "cmty-view-post-item-text")))

    problems = driver.find_elements(By.CLASS_NAME, "cmty-view-post-item-text")
    problems = [p.get_attribute('innerHTML') for p in problems]

    topic_links = driver.find_elements(By.CLASS_NAME, "cmty-view-post-topic-link")
    tag_links = [link.find_element(By.TAG_NAME, "a").get_attribute('href') for link in topic_links]
    tags = [','.join(tags_of_one_problem(link)) for link in tag_links]

    driver.get(answer_url)
    wait.until(presence((By.CLASS_NAME, "mw-parser-output")))
    answers = driver.find_elements(By.TAG_NAME, "li")
    answers = [a.text for a in answers]
    
    return (problems, tags, answers)


###
### MAKE an A vs B version of this
###


'''
Scrolls down the page to load all elements

taken from:
https://stackoverflow.com/questions/20986631/how-can-i-scroll-a-web-page-using-selenium-webdriver-in-python/27760083#27760083
'''
def scroll(driver, pause=1):
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(pause)

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


'''
Given the url of the contest collection page, retrieves every link and year of contests
'''
def get_contests(url):
    driver = webdriver.Chrome(options)
    wait = WebDriverWait(driver, 10)
    driver.get(url)
    wait.until(presence((By.CLASS_NAME, "cmty-category-cell")))
    scroll(driver)

    contests = driver.find_elements(By.CLASS_NAME, "cmty-cat-cell-top-legit")
    contest_links = [contest.find_element(By.CLASS_NAME, "cmty-full-cell-link").get_attribute('href') for contest in contests]
    years = [contest.get_attribute('title')[6:] for contest in contests]

    return (contest_links, years)


'''
Given url of contest collection page and contest name:
retrieve all problems and write to csv file
'''
def get_all_problems(url, contest_name):
    (contest_links, years) = get_contests(url)

    file_name = f"./Scraped_{contest_name}.csv"

    with open(file_name, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow(["year", "number", "content", "answer", "tags"])

        for i, year in enumerate(years):
            if (contest_name == "AMC_8" and int(year) <= 1998):
                (problems, tags, answers) = problems_of_one_year(contest_links[i], "AJHSME", year)
            else:
                (problems, tags, answers) = problems_of_one_year(contest_links[i], contest_name, year)

            for number in range(1, 26):
                writer.writerow([int(year), number, problems[number-1].replace("\n", " "), answers[number-1], tags[number-1] ])

            

'''
Smaller version of above method for testing purposes
'''
def get_all_problems_testing(url, contest_name, limit=1):
    (contest_links, years) = get_contests(url)

    file_name = f"./Scraped_{contest_name}_test.csv"

    with open(file_name, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')

        writer.writerow(["year", "number", "content", "answer", "tags"])

        for i, year in enumerate(years):
            if (i > limit):
                break
            (problems, tags, answers) = problems_of_one_year(contest_links[i], contest_name, year)

            for number in range(1, 26):
                writer.writerow([int(year), number, problems[number-1].replace("\n", " "), answers[number-1], tags[number-1] ])
