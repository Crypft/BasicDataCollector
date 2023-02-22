from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
import time

# set up the webdriver
s = Service("path/to/chromedriver")
options = Options()
options.headless = True
driver = webdriver.Chrome(service=s, options=options)

# read in the input file with links
links = pd.read_excel('comment_links_dnevnik.xlsx', header=None, names=['Links'])

# initialize output list
output_data = []

# loop through the links and extract the comments
for link in links['Links']:
    driver.get(link)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # scroll down to the bottom of the page repeatedly until all comments are loaded
    while True:
        last_height = driver.execute_script("return document.documentElement.scrollHeight")
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    comments = soup.find_all('div', class_='cr')
    for comment in comments:
        comment_text = ""
        if comment.find('div', class_='ci'):
            ci = comment.find('div', class_='ci')
            if ci.find('div', class_='p') and not ci.find('div', class_='c-reply'):
                comment_text = ci.find('div', class_='p').get_text(strip=True)
            else:
                comment_text = ci.get_text(strip=True)
        likes = 0
        if comment.find('a', class_='e-plus'):
            likes = int(comment.find('a', class_='e-plus').get_text(strip=True))
        dislikes = 0
        if comment.find('a', class_='e-minus'):
            dislikes = int(comment.find('a', class_='e-minus').get_text(strip=True))
        output_data.append([link, comment_text, likes, dislikes])

# write the output to a new excel file
output_df = pd.DataFrame(output_data, columns=['Link', 'Comment', 'Likes', 'Dislikes'])

# merge duplicate link cells
output_df['Link'] = output_df['Link'].fillna(method='ffill')

# remove duplicate rows
output_df.drop_duplicates(subset=['Link', 'Comment', 'Likes', 'Dislikes'], inplace=True)

# fill in empty link cells
output_df['Link'] = output_df['Link'].fillna('')

# write the output to a new Excel file
output_df.to_excel('output_file.xlsx', index=False)

# quit the webdriver
driver.quit()