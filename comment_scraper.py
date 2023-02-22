# import requests
# from bs4 import BeautifulSoup
# import pandas as pd
#
# # Read input Excel file
# df = pd.read_excel('article_links.xlsx', header=None, names=['Link'])
#
# # Loop through links and extract comment numbers
# comment_counts = []
# for link in df['Link']:
#     response = requests.get(link)
#     if response.status_code == 200:
#         soup = BeautifulSoup(response.text, 'html.parser')
#         comment_count = soup.select_one('a.comments > span')
#         if comment_count:
#             comment_counts.append(int(comment_count.text.strip()))
#         else:
#             comment_counts.append(0)
#     else:
#         comment_counts.append(None)
#
# # Add comment numbers to DataFrame
# df['Comment Count'] = comment_counts
#
# # Write output to new Excel file
# df.to_excel('output_comment_counts.xlsx', index=False)
#

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

# Read input Excel file
df = pd.read_excel('article_links_blitz.xlsx', header=None, names=['Link'])

# Loop through links and extract comment numbers
comment_counts = []
for link in df['Link']:
    response = requests.get(link)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        comment_count = soup.select_one('span[itemprop="http://schema.org/interactionCount"] > a')
        if comment_count:
            comment_count_text = comment_count.text.strip()
            comment_count_num = re.findall(r'\d+', comment_count_text)
            if comment_count_num:
                comment_counts.append(int(comment_count_num[0]))
            else:
                comment_counts.append(0)
        else:
            comment_counts.append(0)
    else:
        comment_counts.append(None)

# Add comment numbers to DataFrame
df['Comment Count'] = comment_counts

# Write output to new Excel file
df.to_excel('output_comment_counts.xlsx', index=False)
