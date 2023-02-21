from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd

# set up the webdriver
s = Service("path/to/chromedriver")
options = Options()
options.headless = True
driver = webdriver.Chrome(service=s, options=options)

# read in the input file with links
df_links = pd.read_excel('comment_links_blitz.xlsx', header=None, names=['Links'])
links = df_links['Links'].tolist()

# initialize output list
output_data = []

# loop through the links and extract the comments
for link in links:
    driver.get(link)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    comments = soup.find_all('div', class_='comment-body')
    for comment in comments:
        comment_text = comment.find('p').get_text()
        likes = comment.find('i', class_='bx-like').find_next('span', class_='votes').get_text()
        dislikes = comment.find('i', class_='bx-dislike').find_next('span', class_='votes').get_text()
        output_data.append([link, comment_text, likes, dislikes])

# write the output to a new excel file
output_df = pd.DataFrame(output_data, columns=['Link', 'Comment', 'Likes', 'Dislikes'])
output_df.to_excel('output_file.xlsx', index=False)

# quit the webdriver
driver.quit()
