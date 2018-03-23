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
mainPage = requests.get('https://www.goodreads.com/list/show/264.Books_That_Everyone_Should_Read_At_Least_Once?page=9', headers=agent)

csv = open("E:/CS 839/Project Stage 2/Table1_1_2.csv", "w", encoding='utf=8')
f = open("E:/CS 839/Project Stage 2/mainPage.txt", "w", encoding='utf=8')
f1 = open("E:/CS 839/Project Stage 2/bookPage.txt", "w", encoding='utf=8')
csv.write("title, author, rating, format, pages\n")

#f.write(str(mainPage.content))

#page = mainPage
count = 800
while mainPage.status_code == 200:
    parsed = soup(mainPage.content, 'html.parser')
    mainPage.close()
    books = parsed.findAll("a", {"class":"bookTitle", "itemprop":"url"})
    print(len(books))
    for i in range(len(books)):
        book_href = "https://www.goodreads.com" + books[i]['href']
        #print(book_href)
        if ((count % 100) == 0):
            time.sleep(3)
        bookPage = requests.get(book_href, headers=agent)
        if bookPage.status_code == 200:
            parsedBookPage = soup(bookPage.content, 'html.parser')
            bookPage.close()
            #f1.write(str(bookPage.content))
            title = books[i].span.text
            title = re.sub('[,]' , '', title)
            #print("Title: " + title)
            authorName = parsedBookPage.find("a", {"class":"authorName"}).span.text
            #print("Author Name: " + authorName)
            rating = parsedBookPage.find("span", {"class":"average"}).text
            #print("Rating: " + rating)
            bookFormat = parsedBookPage.find("span", {"itemprop":"bookFormat"})
            if bookFormat == None:
                bookFormat = ''
            else:
                bookFormat = bookFormat.text
            #print("format: " + bookFormat)
            pages = parsedBookPage.find("span", {"itemprop":"numberOfPages"})
            if pages == None:
                pages = ''
            else:
                pages = pages.text.split(' ')[0]

            #print("pages: " + pages)

            csv.write(title + ',' + authorName + ',' + rating + ',' + bookFormat + ',' + pages + '\n')
            count = count + 1
            print("Book " + repr(count))

    if (count == 3000):
        break
    p = parsed.find("div", {"class":"pagination"})
    p = p.find("a", {"class":"next_page"})['href']
    nextLink = "https://www.goodreads.com" + p
    mainPage = requests.get(nextLink, headers=agent)
    #print(nextLink)

csv.close()
