# from bs4 import BeautifulSoup
# import requests
# import pandas as pd
#
# url = 'https://www.example.com/article'
# response = requests.get(url)
# html = response.text
#
# soup = BeautifulSoup(html, 'html.parser')
# comments = soup.find_all('div', {'class': 'comment-content'})
#
# comments_list = []
# for comment in comments:
#     comments_list.append(comment.text)
#
# df = pd.DataFrame(comments_list, columns=['comments'])
#
# df.to_csv('comments.csv', index=False)

from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import datetime
# Create lists to store the scraped information
dates = []
titles = []
urls = []

# Make a GET request to the webpage
for i in range(0, 22):
    url = f'https://blitz.bg/search?q=%D1%83%D0%BA%D1%80%D0%B0%D0%B8%D0%BD%D1%81%D0%BA%D0%B8%20%D0%B1%D0%B5%D0%B6%D0%B0%D0%BD%D1%86%D0%B8&page={i}'
    response = requests.get(url)
    html = response.text

    # Use BeautifulSoup to parse the HTML
    soup = BeautifulSoup(html, 'html.parser')

    # Find the elements containing the article information
    articles = soup.find_all('div', class_='single-tech-inner-news')


    # Use a loop to extract the information from each article

    for article in articles:
        date = article.find_all('span')
        date_dirty = str(date[1])
        date_object = datetime.strptime(date_dirty[6:16], '%d.%m.%Y')
        date_str = str(date_object.date())
        date_list = date_str.split('-')
        date_final = f'{date_list[1]}/{date_list[2]}/{date_list[0][2:]}'

        title = article.find('h3').text
        title = title.replace('\n', '')
        title = title.strip()

        link = article.find('a')['href']

        # Append the information to the appropriate list
        dates.append(date_final)
        titles.append(title)
        urls.append(link)

    # Create a pandas dataframe with the scraped information
    df = pd.DataFrame({'title': titles, 'url': urls, 'date': dates})

 # Save the dataframe to a CSV file
df.to_excel('articles.xlsx', index=False)
