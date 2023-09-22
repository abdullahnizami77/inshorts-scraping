import requests
from bs4 import BeautifulSoup
import urllib.parse
import time
import re

'''
there are two major functions in code, scrape_article function is refrence function for extracting refrence article link from inshorts website ,
process_url_and_write_to_file function is actual function for scrapping website
'''

def myquote(quote_page):
    url = urllib.parse.urlsplit(quote_page)
    url = list(url)
    url[2] = urllib.parse.quote(url[2])
    url = urllib.parse.urlunsplit(url)
    return url

def scrape_article(link):
    try:
        response = requests.get(link)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        selected_div = None
        for div in soup.findAll('div'):
            if div.text and 'read more at' in div.find(text=True):
                selected_div = div
                break
        
        reference_link = None
        if selected_div:
            reference_link = selected_div.find("a", target="_blank")['href']
            print("Reference article link:", reference_link)
        else:
            print("No reference article link found.")

        return reference_link

    except requests.exceptions.RequestException as e:
        print('Error:', e)

links = [
    "https://inshorts.com/hi/news/डेरा-सच्चा-सौदा-प्रमुख-गुरमीत-राम-रहीम-सिंह-अनुयायी-की-हत्या-के-लिए-दोषी-करार-1633677650409",
    "https://inshorts.com/hi/news/सहारनपुर-में-बसपा-के-फज़लुर्रहमान-सबसे-आगे-मसूद-को-भी-मिल-चुके-सवा-लाख-वोट-1558601614502",
    "https://inshorts.com/hi/news/गुरुग्राम-में-फ्लैट-के-नाम-पर-दिल्ली-के-व्यापारी-से-₹9125-की-ठगी-1556099842849",
    "https://inshorts.com/hi/news/अपने-आत्मीय-मित्र-को-याद-कर-रहा-हूं-पासवान-की-बरसी-पर-उनके-परिवार-को-संदेश-में-पीएम-1631439024472",
    "https://inshorts.com/hi/news/मुज़फ्फरनगर-में-प्रेम-प्रसंग-के-चलते-हमलावरों-ने-की-युवक-की-गोली-मारकर-हत्या-1559907245740",
    "https://inshorts.com/hi/news/मेरठ-में-लूट-का-विरोध-करने-पर-बदमाशों-ने-महिला-को-मारी-गोली-1556088289163",
    "https://inshorts.com/hi/news/औरतों-का-मस्जिद-में-तरावीह-की-नमाज़-पढ़ना-गलत-सहारनपुर-उलेमा-1558429942308",
    "https://inshorts.com/hi/news/मिडडे-मील-के-लिए-छत्तीसगढ़-में-8-किमी-पैदल-चलकर-राशन-लाते-दिखे-शिक्षक-1635151023140",
    "https://inshorts.com/hi/news/मुज़फ्फरनगर-में-180-स्टूडेंट्स-को-मिले-समान-अंक-बड़े-पैमाने-पर-नकल-की-आशंका-1556938453209",
    "https://inshorts.com/hi/news/मेरठ-में-ईंट-भट्ठों-पर-छापा-बिना-मानक-मिले-4-भट्ठों-पर-कार्रवाई-1556087609648",
    "https://inshorts.com/hi/news/टी20-विश्व-कप-में-भारतपाक-मैच-नहीं-होना-चाहिए-क्योंकि-सीमा-पर-स्थिति-आदर्श-नहीं-है-गिरिराज-1634553946252",
    "https://inshorts.com/hi/news/मेरठ-में-एक-स्कूल-पर-छात्रों-को-सिख-व-ईसाई-बता-छात्रवृत्ति-लेने-का-आरोप-1558266900235",
    "https://inshorts.com/hi/news/दुख-की-घड़ी-में-अपने-भाइयोंबहनों-का-साथ-देने-लखीमपुर-जा-रहा-हूं-पंजाब-के-सीएम-1633334213049",
    "https://inshorts.com/hi/news/मेरठ-में-स्कूल-के-विद्युतीकरण-के-लिए-मिले-₹21000-नहीं-हुई-बिजली-व्यवस्था-1556097920472",
    "https://inshorts.com/hi/news/मुज़फ्फरनगर-में-गंगनहर-में-गिरने-से-जेनरेटर-ऑपरेटर-की-मौत-1557544620618",
    "https://inshorts.com/hi/news/मुज़फ्फरनगर-में-तमंचे-के-बल-पर-बुज़ुर्ग-दंपति-से-नकदी-समेत-ज़ेवरात-की-लूट-1559617206347",
    "https://inshorts.com/hi/news/फिर-से-दरें-बढ़ने-पर-नए-उच्चतम-स्तर-पर-पहुंचे-पेट्रोलडीज़ल-के-दाम-1634192750683",
    "https://inshorts.com/hi/news/लखनऊ-में-सांडों-का-आतंक-जारी-एक-सप्ताह-में-2-की-गई-जान-1556722800993",
    "https://inshorts.com/hi/news/मेरठ-के-जानीखुर्द-में-कार-में-मिला-2-युवकों-का-शव-मचा-हड़कंप-1557466721935",
    "https://inshorts.com/hi/news/पाकिस्तान-की-जीत-पर-भारत-में-पटाखे-फोड़ने-वालों-का-डीएनए-भारतीय-नहीं-अनिल-विज-1635238671592"
]



reference_links = []

for link_number, link in enumerate(links, start=1):
    print(f"Processing link {link_number}/{len(links)}: {link}")
    reference_link = scrape_article(link)
    reference_links.append(reference_link)

print("Reference article links:")
for i, ref_link in enumerate(reference_links, start=1):
    print(f"{i}. {ref_link}")


# MAIN CODE HERE

def process_url_and_write_to_file(url):
    try:

        response = requests.get(url)
        response.raise_for_status()


        soup = BeautifulSoup(response.content, 'html.parser')

        timestamp = str(int(time.time()))
        filename = f"{timestamp}.txt"

        with open(filename, 'w', encoding='utf-8') as file:
            headlines = soup.find_all('h1')
            for headline in headlines:
                file.write("#originalArticleHeadline "+"\n" + headline.text.strip() + "\n")

            article_div = soup.find('div', class_='article-desc')
            if article_div is None:
                print('\nError for ' + url)
            if article_div:
                article_text = article_div.get_text(separator="\n")
            else:
                file.write("Article content not found on the page.\n")

            cleaned_article = ' '.join(article_text.split())
            cleaned_article = '\n'.join(line.strip() for line in cleaned_article.splitlines() if line.strip())
            cleaned_article = re.sub(r'\s+([.,;!?])', r'\1', cleaned_article)


            file.write("#originalArticleBody" + "\n" + cleaned_article)
            print("Processed:", url)

            date_time_div = soup.find('div', class_='auther-time')
            if date_time_div:
                date_time_text = date_time_div.get_text(separator="\n")
                date_time_lines = date_time_text.strip().split('\n')
                article_date = date_time_lines[-1].replace('Updated', '').strip()
                file.write("\n#article_date\n" + article_date + "\n")


                try:
                  author_name = date_time_div.find_all('span')[1].text.strip()
                  file.write("#articleAuthor\n" + author_name )
                except:
                  print(" No Author for" + url) 



    except requests.exceptions.RequestException as e:
        print('Error:', e)


for i, ref_link in enumerate(reference_links, start=1):
    print(f"Processing reference article link {i}/{len(reference_links)}: {ref_link}")
    process_url_and_write_to_file(ref_link)
    time.sleep(1)
