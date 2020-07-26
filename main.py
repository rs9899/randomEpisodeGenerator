### Imports
import requests
from bs4 import BeautifulSoup
import re
import random

class Episode:
  def __init__(self , seasonNum , episodeNum, Name, Description):
    self.seasonNum  = 	seasonNum  
    self.episodeNum = 	episodeNum 
    self.Name  		  = 	Name 
    self.Description = 	Description

  def print(self):
    print("A random Episode for you")
    print("------------------")
    print("Season : " + str(self.seasonNum) + "  ,  Episode :  " + str(self.episodeNum))
    print("Title: " + self.Name )
    print("Description: ")
    print(self.Description)

  def printShort(self):
    print("Season : " + str(self.seasonNum) + "  ,  Episode :  " + str(self.episodeNum))
    

### Read the input 
nameOfShow = input("Enter the name of show you are planning to watch:\n")
imdbBase = "https://www.imdb.com/"
imdbUrl = "https://www.imdb.com/find?q=" + nameOfShow.replace(" ","+")

### Search imdb for the show
page = requests.get(imdbUrl)
soup = BeautifulSoup(page.text, 'html.parser')
soup.find('table', class_='findList').select('tr')[0].select('a')[0]['href']
imdbShow = imdbBase + soup.find('table', class_='findList').select('tr')[0].select('a')[0]['href']

page2 = requests.get(imdbShow)
soup = BeautifulSoup(page2.text, 'html.parser')
title_text = soup.find('div' , class_ = 'title_wrapper').select('h1')[0].text
summary_text = soup.find('div' , class_ = 'summary_text').text

print("This is the show we found from IMDb")
print("-----------------------------------")
print("Title: " + title_text.strip() )
print("Description: ")
print(summary_text.strip())
### For future, maybe wait for the user to correctly verify the show

## Season numbers
seasonList = [anc['href'][anc['href'].find('season') + 7 :]  for anc in soup.find('div' , class_ = 'seasons-and-year-nav').select('a') if 'season' in anc['href']]
seasonNum = []
for s in seasonList:
  Z = re.findall(r'\d+', s)
  for i in Z:
    seasonNum.append(int(i))

maxSeason = max(seasonNum)


### List pf episodes
epList = [] 
for sesn in range(maxSeason):
  p = requests.get(imdbShow + 'episodes?season='+str(sesn+1))
  s =  BeautifulSoup(p.text, 'html.parser')
  Titl = [elem.select('a')[0]['title'].strip() for elem in s.find('div' , class_ = 'eplist').select('strong') ]
  desc = [elem.text.strip() for elem in  s.find('div' , class_ = 'eplist').findAll('div' , class_ = 'item_description')]
  for i in range(len(Titl)):
    epList.append(Episode(sesn+1, i+1 , Titl[i] , desc[i] ))



### Random picker
TotalChoice = len(epList)
randEpisode = random.randint(1,TotalChoice)


### Output
epList[randEpisode-1].print()


time.sleep(60) # Sleep for 60 seconds 