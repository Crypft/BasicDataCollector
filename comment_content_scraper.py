import requests
from bs4 import BeautifulSoup
import pandas as pd

# read in the list of links from an Excel file
links = pd.read_excel('comment_links_fakti.xlsx', header=None, names=['Links'])

# create an empty list to store the comments
comments_list = []
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}

# iterate over the links and scrape the comments
for link in links['Links']:
    res = requests.get(link, headers=headers)
    soup = BeautifulSoup(res.content, 'html.parser')

    comments = soup.find_all('li', class_='discussion-comment')

    for comment in comments:
        if comment.find('div', id="m_fakti_in_comments"):
            continue
        text = comment.find('div', class_='discussion-comment-text')
        if text:
            text = text.get_text(strip=True)
            likes = comment.find('a', class_='voteplus VotePlus').get_text(strip=True)
            dislikes = comment.find('a', class_='votemin VoteMinus').get_text(strip=True)
        else:
            text = 'Removed by moderator'
            likes = 0
            dislikes = 0

        comments_list.append({
            'Link': link,
            'Comment': text,
            'Likes': likes,
            'Dislikes': dislikes
        })

df = pd.DataFrame(comments_list)
df.to_excel('comments.xlsx', index=False)





