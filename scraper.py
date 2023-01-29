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

# Create lists to store the scraped information
dates = []
titles = []
urls = []

# Make a GET request to the webpage
for i in range(0, 44):
    url = f'https://www.24chasa.bg/search?q=%D1%83%D0%BA%D1%80%D0%B0%D0%B8%D0%BD%D1%81%D0%BA%D0%B8%20%D0%B1%D0%B5%D0%B6%D0%B0%D0%BD%D1%86%D0%B8&page={i}'
    response = requests.get(url)
    html = response.text

    # Use BeautifulSoup to parse the HTML
    soup = BeautifulSoup(html, 'html.parser')

    # Find the elements containing the article information
    articles = soup.find_all('article', class_='grid-layout-item')


    # Use a loop to extract the information from each article

    for article in articles:
        date = article.find('time')['datetime']
        date = date.split()
        date.pop(1)
        date_list = date[0].split('-')
        date_list.pop(3)
        my_order = [1, 2, 0]
        date_list = [date_list[i] for i in my_order]
        date_list[2] = '22'
        date_final = f'{date_list[0]}/{date_list[1]}/{date_list[2]}'

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
