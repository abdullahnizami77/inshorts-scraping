# -*- coding: utf-8 -*-
"""inshorts-scrapping.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/11hXlkN6l5et6u4tp-68AwB7_hj2DVPIw

#Modular un-updated code
"""

import urllib.request
import urllib
import urllib.parse
from bs4 import BeautifulSoup
from urllib.parse import quote
import os
import time
import sys
import random
import string
import re

def myquote(quote_page):
    url = urllib.parse.urlsplit(quote_page)
    url = list(url)
    url[2] = urllib.parse.quote(url[2])
    url = urllib.parse.urlunsplit(url)
    return url

try:
    if "hindi" in str(sys.argv[1]).lower():
        file_name = "/content/links.txt"
        destination_path = "/content/dataset/hindi/"
        full_ds_path = "/content/inshorts-dataset-hi/"
    else:
        file_name = "/content/links.txt"
        destination_path = "/content/dataset/english/"
        full_ds_path = "/content/inshorts-dataset-en/"

except:
    print("\tPlease provide 'Hindi' or 'English' after the command. Exit and run again.")
    input()
    exit()

os.makedirs(destination_path, exist_ok=True)
os.makedirs(full_ds_path, exist_ok=True)

linkfile = open(file_name, "r")
links = linkfile.readlines()

i = 0
user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
headers = {'User-Agent': user_agent}
k = 1

display_top_n = 5

for link_number, quote_page in enumerate(links, start=1):
    quote_page = quote_page.strip()

    if quote_page.count('http') > 1:
        continue

    print(f"Processing link {link_number}/{len(links)}: {quote_page}")

    try:
        page = urllib.request.urlopen(myquote(quote_page))
    except Exception as e:
        print(e)
        input('wait1')
        continue

    if "FILE_TERMINATES_HERE" in quote_page:
        break

    rstring = ''.join(random.choices(string.ascii_uppercase, k=4))
    dtstring = os.path.join(destination_path, re.search(r'\d+$', quote_page)[0] + rstring + ".txt")
    dtstring2 = os.path.join(full_ds_path, re.search(r'\d+$', quote_page)[0] + rstring + ".txt")

    file = open(dtstring, 'w')
    article_len = 0

    try:
        soup = BeautifulSoup(page, 'html.parser')
        selected_div = None
        for div in soup.findAll('div'):
            if div.text and 'read more at' in div.find(text=True):
                selected_div = div
                break
        urlink = selected_div.find("a", target="_blank")['href']
        request = urllib.request.Request(urlink, None, headers)
        response = urllib.request.urlopen(request)
        soup2 = BeautifulSoup(response, 'html.parser')
        file.write("#originalArticleHeadline" + "\n")

        if "hindustantimes.com" in urlink:
            hlist = soup2.find('h1')
            hlist2 = soup2.find('h2')
            file.write(hlist.text + "\n")
            file.write(hlist2.text + "\n")

            file.write("#originalArticleBody" + "\n")
            table = soup2.findAll('div', attrs={"class": "story-content"})
            for x in table:
                for p in x.findAll('p'):
                    file.write(p.text + "\n")

        elif "inextlive.com" in urlink:
          hlist = soup2.find('h1')
          file.write("#originalArticleHeadline" + "\n")
          file.write(hlist.text + "\n")
          file.write("#originalArticleBody" + "\n")
          article = soup2.findAll('p')
          for a in article:
            if "Copyright © 2023. All Rights Reserved" not in a.text:
              file.write(a.text + "\n")


        elif "amarujala.com" in urlink:
            hlist = soup2.find('h1')
            #hlist2 = soup2.find('h2')
            file.write(hlist.text + "\n")
            #file.write(hlist2.text + "\n")

            file.write("#originalArticleBody" + "\n")
            table = soup2.findAll('div', attrs={"class": "article-desc ul_styling"})
            for x in table:
                for p in x.findAll('p'):
                    file.write(p.text + "\n")

        # I Will Add more website-specific parsing logic here as needed

        else:
            hlist = soup2.find('h1')
            file.write(hlist.text + "\n")
            file.write("#originalArticleBody" + "\n")
            article = soup2.findAll('p')
            for a in article:
                file.write(a.text + "\n")
    except Exception as e:
        print('Abdullah Error', e)
        #input('wait')
        file.close()
        os.remove(dtstring)
        print('  --> Waiting of 1 sec. Press Ctrl+C to exit', dtstring, ' ' * 90, end='\r')
        time.sleep(1)
        continue

    file.write("\n")
    file.write("-" * 100 + "\n")
    file.write("#summaryHeadline\n" + soup.find("span", itemprop="headline").text.strip() + "\n")
    file.write("#summaryBody\n" + soup.find("div", itemprop="articleBody").text.strip() + "\n")
    file.write("#datePublished " + soup.find("span", itemprop="datePublished").text.strip() + " ")
    file.write(soup.find("span", clas="date").text.strip() + "\n")
    #file.write(soup.find("span", attrs={'class': 'short'}).text.strip() + " by " + soup.find("span", attrs={
        #'class': 'author'}).text.strip() + " from News inShorts\n")
    file.write("#reference_link: " + quote_page + "\n")
    file.write("#original_link: " + urlink)
    file.close()

    print('dtstring', dtstring)
    #input('wait')

    print(str(link_number) + " " + quote_page[29:-14] + "\n    Article and Summary pulled!" + " " + datetime.datetime.now().strftime(
        "%H:%M:%S") + ' ' * 100 + '\n    file ' + dtstring2 + ' ' + " " * 100 + '\n' + '-' * 50 + ' ' * 100)
    if (k % display_top_n == 0):
        print("\033[A" * (display_top_n * 4), end='')

    k += 1

print("\n" * 7 + str(k - 1) + " Articles and their summaries pulled!")


"""# Amar Ujala (Working + Non Modular)"""

from bs4 import BeautifulSoup
import requests
import re

url = 'https://www.amarujala.com/delhi-ncr/gurgaon/21556042696-gurgaon-news?utm_campaign=fullarticle&utm_medium=referral&utm_source=inshorts'
response = requests.get(url)

if response.status_code != 200:
    print("Failed to retrieve the webpage.")
    exit()

soup = BeautifulSoup(response.content, 'html.parser')

headlines = soup.find_all('h1')

for headline in headlines:
    print("Headline:", headline.text.strip())

article_div = soup.find('div', class_='article-desc tested')
if article_div is None:
    article_div= soup.find('div', class_='article-desc ul_styling')

if article_div:
    article_text = article_div.get_text(separator="\n")
    print(article_text)

else:
    print("Article content not found on the page.")

cleaned_article = ' '.join(article_text.split())
cleaned_article = '\n'.join(line.strip() for line in cleaned_article.splitlines() if line.strip())
cleaned_article = re.sub(r'\s+([.,;!?])', r'\1', cleaned_article)
print(cleaned_article)

"""# Cricket Tracker (Working + Non Modular)"""

url = 'https://hindi.crictracker.com/fans-trolled-riyan-parag-on-social-media-for-a-catch/?fbclid=IwAR0YCLRo3_jNv-2rVr0vMZD2Q7iR8qVoZDJ6cgbr4m4D0YydqxN9tKtUGH0&amp=&utm_campaign=fullarticle&utm_medium=referral&utm_source=inshorts'
response = requests.get(url)

if response.status_code != 200:
    print("Failed to retrieve the webpage.")
    exit()

soup = BeautifulSoup(response.content, 'html.parser')

headlines = soup.find_all('h1')

for headline in headlines:
    print("Headline:", headline.text.strip())

paragraphs = soup.find_all('p')


hindi_text = ""
for p in paragraphs:
    if any('\u0900' <= c <= '\u097F' for c in p.get_text()):
        hindi_text += p.get_text() + "\n"

print(hindi_text)

hindi_pattern = re.compile(r'[\u0900-\u097F]+')
hindi_text_matches = hindi_pattern.findall(hindi_text)
hindi_text = ' '.join(hindi_text_matches)
print(hindi_text)

"""# Timesnowhindi (working + Non Modular)"""

url = 'https://www.timesnowhindi.com/amp/india/article/rahul-gandhi-appeals-to-party-leaders-and-workers-not-to-celebrate-his-birthday/416284?utm_campaign=fullarticle&utm_medium=referral&utm_source=inshorts'
response = requests.get(url)

if response.status_code != 200:
    print("Failed to retrieve the webpage.")
    exit()

soup = BeautifulSoup(response.content, 'html.parser')

headlines = soup.find_all('h1')

for headline in headlines:
    print("Headline:", headline.text.strip())

article_text = ""
paragraphs = soup.find_all("p")
for paragraph in paragraphs:
  article_text += paragraph.get_text() + "\n"
print(article_text)



"""#livehindustan (Not working)"""

url = 'https://www.livehindustan.com/cricket/story-ipl-2021-david-warner-posts-selfie-from-stands-in-dubai-watches-video-srh-vs-kkr-match-4730766.amp.html?utm_campaign=fullarticle&utm_medium=referral&utm_source=inshorts'
response = requests.get(url)

if response.status_code != 200:
    print("Failed to retrieve the webpage.")
    exit()

soup = BeautifulSoup(response.content, 'html.parser')

headlines = soup.find_all('h1')

for headline in headlines:
    print("Headline:", headline.text.strip())

"""# Jagran (Working + Non Modular)"""

url = 'https://www.jagran.com/bihar/katihar-inveastigation-19191026.html?utm_campaign=fullarticle&utm_medium=referral&utm_source=inshorts'
response = requests.get(url)

if response.status_code != 200:
    print("Failed to retrieve the webpage.")
    exit()

soup = BeautifulSoup(response.content, 'html.parser')

headlines = soup.find_all('h1')

for headline in headlines:
    print("Headline:", headline.text.strip())

article_div = soup.find('div', class_='articlecontent')

if article_div:
    article_text = article_div.get_text(separator="\n")
    #print(article_text)

else:
    print("Article content not found on the page.")

cleaned_article = ' '.join(article_text.split())

cleaned_article = '\n'.join(line.strip() for line in cleaned_article.splitlines() if line.strip())

cleaned_article = re.sub(r'\s+([.,;!?])', r'\1', cleaned_article)

print(cleaned_article)