import requests
from bs4 import BeautifulSoup
import pprint #neat print

res = requests.get('https://news.ycombinator.com/news')
#res2 = requests.get('https://news.ycombinator.com/news?p=2')
soup = BeautifulSoup(res.text, 'html.parser')
#soup2 = BeautifulSoup(res2.text, 'html.parser')

links = soup.select('.titleline > a')
#>a is css, where selects all anchor from titleline
subtext = soup.select('.subtext')
#links2 = soup2.select('.titleline > a') 
#subtext2 = soup2.select('.subtext')

#mega_links = links + links2
#mega_subtext = subtext + subtext2

def sort_stories_by_votes(hnlist):
  return sorted(hnlist, key= lambda k:k['votes'], reverse=True)
#returing the votes by their hgighst
def create_custom_hn(links, subtext):
  hn = []
  for idx, item in enumerate(links):
    title = item.getText() 
    href = item.get('href', None) #link
    vote = subtext[idx].select('.score')
    if len(vote):#if valid ie len>0
      points = int(vote[0].getText().replace(' points', ''))#replace the empty value to a string wuth null value, so that no error is generated
      if points > 99:
        hn.append({'Title': title, 'Link': href, 'Votes': points}) # Modified column names
  return sort_stories_by_votes(hn)

# Create DataFrame
data = create_custom_hn(links, subtext)
df = pd.DataFrame(data)

# Save DataFrame to Excel
df.to_excel('hacker_news_data.xlsx', index=False)
