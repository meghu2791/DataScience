import requests
from requests.exceptions import MissingSchema
from bs4 import BeautifulSoup as soup
import re
import sys
import time


agent = requests.utils.default_headers()
agent.update({
    "User-Agent":'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
})

#agent = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}
#agent = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0'}
mainPage = requests.get('https://www.amazon.com/s/ref=sr_pg_1?fst=p90x%3A1&rh=i%3Aaps%2Ck%3Aaward+winners&keywords=award+winners&ie=UTF8&qid=1521496123', headers=agent)

csv = open("E:/CS 839/Project Stage 2/Table1_2_2.csv", "w", encoding='utf=8')
f = open("E:/CS 839/Project Stage 2/mainPage_2.txt", "w", encoding='utf=8')
f1 = open("E:/CS 839/Project Stage 2/bookPage_2.txt", "w", encoding='utf=8')
csv.write("title, author, rating, format, price, year\n")

f.write(str(mainPage.content))

count = 0
while mainPage.status_code == 200:
    parsed = soup(mainPage.content, 'html.parser')
    mainPage.close()
    books = parsed.findAll("div", {"class":"a-fixed-left-grid-col a-col-right"})
    print(len(books))
    #f1.write(str(books[0]))
    for i in range(len(books)):
        title = books[i].find("h2", {"class":"s-access-title"})['data-attribute']
        title = re.sub('[,]' , '', title)
        #print("Title: " + title)
        year = books[i].find("span", {"class":"a-size-small a-color-secondary"})
        if year == None:
            year = ''
        else:
            year = year.text.split(' ')
            if (len(year) == 3):
                year = year[2]
            else:
                year = ''
        #print("Year: " + year)
        authorName = books[i].findAll("span", {"class":"a-size-small a-color-secondary"})
        if (len(authorName) > 2):
            authorName = authorName[2].text
            authorName = re.sub('[,]', '', authorName)
        else:
            authorName = ''
        #print("Author Name: " + authorName)
        bookFormat = books[i].find("h3")
        if bookFormat == None:
            bookFormat = ''
        else:
            bookFormat = bookFormat.text
        #print("format: " + bookFormat)

        rating = books[i].findAll("span", {"class":"a-icon-alt"})
        #print(rating)
        if len(rating) == 2:
            rating = rating[1].text.split(' ')[0]
        else:
            rating = ''
        #print("Rating: " + rating)
        price = books[i].find("span", {"class":"a-size-base a-color-base"})
        if price == None:
            price = ''
        else:
            price = price.text
            price = re.sub('[,]', '', price)
        #print("Price: " + price)


        csv.write(title + ',' + authorName + ',' + rating + ',' + bookFormat + ',' + price + ',' + year +'\n')
        count = count + 1
        print("Book " + repr(count))


    if (count == 3050):
        break
    p = parsed.find("a", {"class":"pagnNext"})['href']
    nextLink = "https://www.amazon.com" + p
    #print(nextLink)
    if ((count % 50) == 0):
        time.sleep(4)
    mainPage = requests.get(nextLink, headers=agent)

csv.close()
