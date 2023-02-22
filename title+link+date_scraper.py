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
comments = []
views = []

# Make a GET request to the webpage
for i in range(0, 51):
    url = f'https://fakti.bg/search?q=%D1%83%D0%BA%D1%80%D0%B0%D0%B8%D0%BD%D1%81%D0%BA%D0%B8+%D0%B1%D0%B5%D0%B6%D0%B0%D0%BD%D1%86%D0%B8&sort=date&c=0&fromdate=01.02.2022&todate=31.12.2022&page={i}'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}
    response = requests.get(url, headers=headers)
    html = response.text

    # Use BeautifulSoup to parse the HTML
    soup = BeautifulSoup(html, 'html.parser')

    # Find the elements containing the article information
    section = soup.select_one('#main')
    articles = section.find_all('li')


    # Use a loop to extract the information from each article

    for article in articles:
        date = str(article.find('div', class_='ndt'))
        date_object = datetime.strptime(date[17:-6], '%d.%m.%Y')
        date_str = str(date_object.date())
        date_list = date_str.split('-')
        date_final = f'{date_list[1]}/{date_list[2]}/{date_list[0][2:]}'

        title = article.find('span', class_='post-title').text
        # title = title.replace('\n', '')
        # title = title.strip()

        link = article.find('a')['href']
        link_final = f'https://fakti.bg/{link}'

        view_count = str(article.find('div', class_='nv'))
        views_final = view_count[16:-6]
        views_final = views_final.replace(' ', '')

        comment_count = str(article.find('div', class_='nc'))
        comments_final = comment_count[16:-6]
        comments_final = comments_final.replace(' ', '')

        # Append the information to the appropriate list
        dates.append(date_final)
        titles.append(title)
        urls.append(link_final)
        views.append(views_final)
        comments.append(comments_final)

# Create a pandas dataframe with the scraped information
df = pd.DataFrame({'title': titles, 'url': urls, 'date': dates, 'views': views, 'comments': comments})

# Save the dataframe to a CSV file
df.to_excel('articles.xlsx', index=False)
