{
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/abdullahnizami77/inshorts-scraping/blob/main/inshorts_scrapping.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "#Modular un-updated code"
      ],
      "metadata": {
        "id": "7u_YqPAwrce8"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "import urllib.request\n",
        "import urllib\n",
        "import urllib.parse\n",
        "from bs4 import BeautifulSoup\n",
        "from urllib.parse import quote\n",
        "import os\n",
        "import time\n",
        "import sys\n",
        "import random\n",
        "import string\n",
        "import re\n",
        "\n",
        "def myquote(quote_page):\n",
        "    url = urllib.parse.urlsplit(quote_page)\n",
        "    url = list(url)\n",
        "    url[2] = urllib.parse.quote(url[2])\n",
        "    url = urllib.parse.urlunsplit(url)\n",
        "    return url\n",
        "\n",
        "try:\n",
        "    if \"hindi\" in str(sys.argv[1]).lower():\n",
        "        file_name = \"/content/links.txt\"\n",
        "        destination_path = \"/content/dataset/hindi/\"\n",
        "        full_ds_path = \"/content/inshorts-dataset-hi/\"\n",
        "    else:\n",
        "        file_name = \"/content/links.txt\"\n",
        "        destination_path = \"/content/dataset/english/\"\n",
        "        full_ds_path = \"/content/inshorts-dataset-en/\"\n",
        "\n",
        "except:\n",
        "    print(\"\\tPlease provide 'Hindi' or 'English' after the command. Exit and run again.\")\n",
        "    input()\n",
        "    exit()\n",
        "\n",
        "os.makedirs(destination_path, exist_ok=True)\n",
        "os.makedirs(full_ds_path, exist_ok=True)\n",
        "\n",
        "linkfile = open(file_name, \"r\")\n",
        "links = linkfile.readlines()\n",
        "\n",
        "i = 0\n",
        "user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'\n",
        "headers = {'User-Agent': user_agent}\n",
        "k = 1\n",
        "\n",
        "display_top_n = 5\n",
        "\n",
        "for link_number, quote_page in enumerate(links, start=1):\n",
        "    quote_page = quote_page.strip()\n",
        "\n",
        "    if quote_page.count('http') > 1:\n",
        "        continue\n",
        "\n",
        "    print(f\"Processing link {link_number}/{len(links)}: {quote_page}\")\n",
        "\n",
        "    try:\n",
        "        page = urllib.request.urlopen(myquote(quote_page))\n",
        "    except Exception as e:\n",
        "        print(e)\n",
        "        input('wait1')\n",
        "        continue\n",
        "\n",
        "    if \"FILE_TERMINATES_HERE\" in quote_page:\n",
        "        break\n",
        "\n",
        "    rstring = ''.join(random.choices(string.ascii_uppercase, k=4))\n",
        "    dtstring = os.path.join(destination_path, re.search(r'\\d+$', quote_page)[0] + rstring + \".txt\")\n",
        "    dtstring2 = os.path.join(full_ds_path, re.search(r'\\d+$', quote_page)[0] + rstring + \".txt\")\n",
        "\n",
        "    file = open(dtstring, 'w')\n",
        "    article_len = 0\n",
        "\n",
        "    try:\n",
        "        soup = BeautifulSoup(page, 'html.parser')\n",
        "        selected_div = None\n",
        "        for div in soup.findAll('div'):\n",
        "            if div.text and 'read more at' in div.find(text=True):\n",
        "                selected_div = div\n",
        "                break\n",
        "        urlink = selected_div.find(\"a\", target=\"_blank\")['href']\n",
        "        request = urllib.request.Request(urlink, None, headers)\n",
        "        response = urllib.request.urlopen(request)\n",
        "        soup2 = BeautifulSoup(response, 'html.parser')\n",
        "        file.write(\"#originalArticleHeadline\" + \"\\n\")\n",
        "\n",
        "        if \"hindustantimes.com\" in urlink:\n",
        "            hlist = soup2.find('h1')\n",
        "            hlist2 = soup2.find('h2')\n",
        "            file.write(hlist.text + \"\\n\")\n",
        "            file.write(hlist2.text + \"\\n\")\n",
        "\n",
        "            file.write(\"#originalArticleBody\" + \"\\n\")\n",
        "            table = soup2.findAll('div', attrs={\"class\": \"story-content\"})\n",
        "            for x in table:\n",
        "                for p in x.findAll('p'):\n",
        "                    file.write(p.text + \"\\n\")\n",
        "\n",
        "        elif \"inextlive.com\" in urlink:\n",
        "          hlist = soup2.find('h1')\n",
        "          file.write(\"#originalArticleHeadline\" + \"\\n\")\n",
        "          file.write(hlist.text + \"\\n\")\n",
        "          file.write(\"#originalArticleBody\" + \"\\n\")\n",
        "          article = soup2.findAll('p')\n",
        "          for a in article:\n",
        "            if \"Copyright © 2023. All Rights Reserved\" not in a.text:\n",
        "              file.write(a.text + \"\\n\")\n",
        "\n",
        "\n",
        "        elif \"amarujala.com\" in urlink:\n",
        "            hlist = soup2.find('h1')\n",
        "            #hlist2 = soup2.find('h2')\n",
        "            file.write(hlist.text + \"\\n\")\n",
        "            #file.write(hlist2.text + \"\\n\")\n",
        "\n",
        "            file.write(\"#originalArticleBody\" + \"\\n\")\n",
        "            table = soup2.findAll('div', attrs={\"class\": \"article-desc ul_styling\"})\n",
        "            for x in table:\n",
        "                for p in x.findAll('p'):\n",
        "                    file.write(p.text + \"\\n\")\n",
        "\n",
        "        # I Will Add more website-specific parsing logic here as needed\n",
        "\n",
        "        else:\n",
        "            hlist = soup2.find('h1')\n",
        "            file.write(hlist.text + \"\\n\")\n",
        "            file.write(\"#originalArticleBody\" + \"\\n\")\n",
        "            article = soup2.findAll('p')\n",
        "            for a in article:\n",
        "                file.write(a.text + \"\\n\")\n",
        "    except Exception as e:\n",
        "        print('Abdullah Error', e)\n",
        "        #input('wait')\n",
        "        file.close()\n",
        "        os.remove(dtstring)\n",
        "        print('  --> Waiting of 1 sec. Press Ctrl+C to exit', dtstring, ' ' * 90, end='\\r')\n",
        "        time.sleep(1)\n",
        "        continue\n",
        "\n",
        "    file.write(\"\\n\")\n",
        "    file.write(\"-\" * 100 + \"\\n\")\n",
        "    file.write(\"#summaryHeadline\\n\" + soup.find(\"span\", itemprop=\"headline\").text.strip() + \"\\n\")\n",
        "    file.write(\"#summaryBody\\n\" + soup.find(\"div\", itemprop=\"articleBody\").text.strip() + \"\\n\")\n",
        "    file.write(\"#datePublished \" + soup.find(\"span\", itemprop=\"datePublished\").text.strip() + \" \")\n",
        "    file.write(soup.find(\"span\", clas=\"date\").text.strip() + \"\\n\")\n",
        "    #file.write(soup.find(\"span\", attrs={'class': 'short'}).text.strip() + \" by \" + soup.find(\"span\", attrs={\n",
        "        #'class': 'author'}).text.strip() + \" from News inShorts\\n\")\n",
        "    file.write(\"#reference_link: \" + quote_page + \"\\n\")\n",
        "    file.write(\"#original_link: \" + urlink)\n",
        "    file.close()\n",
        "\n",
        "    print('dtstring', dtstring)\n",
        "    #input('wait')\n",
        "\n",
        "    print(str(link_number) + \" \" + quote_page[29:-14] + \"\\n    Article and Summary pulled!\" + \" \" + datetime.datetime.now().strftime(\n",
        "        \"%H:%M:%S\") + ' ' * 100 + '\\n    file ' + dtstring2 + ' ' + \" \" * 100 + '\\n' + '-' * 50 + ' ' * 100)\n",
        "    if (k % display_top_n == 0):\n",
        "        print(\"\\033[A\" * (display_top_n * 4), end='')\n",
        "\n",
        "    k += 1\n",
        "\n",
        "print(\"\\n\" * 7 + str(k - 1) + \" Articles and their summaries pulled!\")\n"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "JTQQTrU94LPe",
        "outputId": "843fcbe6-34a4-44f3-b1f2-39e1f4e8c122"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Processing link 1/20: https://inshorts.com/hi/news/डेरा-सच्चा-सौदा-प्रमुख-गुरमीत-राम-रहीम-सिंह-अनुयायी-की-हत्या-के-लिए-दोषी-करार-1633677650409\n"
          ]
        },
        {
          "output_type": "stream",
          "name": "stderr",
          "text": [
            "<ipython-input-4-e28e4098310b>:77: DeprecationWarning: The 'text' argument to find()-type methods is deprecated. Use 'string' instead.\n",
            "  if div.text and 'read more at' in div.find(text=True):\n"
          ]
        },
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "dtstring /content/dataset/english/1633677650409KHMW.txt\n",
            "1 डेरा-सच्चा-सौदा-प्रमुख-गुरमीत-राम-रहीम-सिंह-अनुयायी-की-हत्या-के-लिए-दोषी-करार\n",
            "    Article and Summary pulled! 19:07:58                                                                                                    \n",
            "    file /content/inshorts-dataset-en/1633677650409KHMW.txt                                                                                                     \n",
            "--------------------------------------------------                                                                                                    \n",
            "Processing link 2/20: https://inshorts.com/hi/news/सहारनपुर-में-बसपा-के-फज़लुर्रहमान-सबसे-आगे-मसूद-को-भी-मिल-चुके-सवा-लाख-वोट-1558601614502\n",
            "dtstring /content/dataset/english/1558601614502PRSH.txt\n",
            "2 सहारनपुर-में-बसपा-के-फज़लुर्रहमान-सबसे-आगे-मसूद-को-भी-मिल-चुके-सवा-लाख-वोट\n",
            "    Article and Summary pulled! 19:07:59                                                                                                    \n",
            "    file /content/inshorts-dataset-en/1558601614502PRSH.txt                                                                                                     \n",
            "--------------------------------------------------                                                                                                    \n",
            "Processing link 3/20: https://inshorts.com/hi/news/गुरुग्राम-में-फ्लैट-के-नाम-पर-दिल्ली-के-व्यापारी-से-₹9125-की-ठगी-1556099842849\n",
            "dtstring /content/dataset/english/1556099842849LWXV.txt\n",
            "3 गुरुग्राम-में-फ्लैट-के-नाम-पर-दिल्ली-के-व्यापारी-से-₹9125-की-ठगी\n",
            "    Article and Summary pulled! 19:08:00                                                                                                    \n",
            "    file /content/inshorts-dataset-en/1556099842849LWXV.txt                                                                                                     \n",
            "--------------------------------------------------                                                                                                    \n",
            "Processing link 4/20: https://inshorts.com/hi/news/अपने-आत्मीय-मित्र-को-याद-कर-रहा-हूं-पासवान-की-बरसी-पर-उनके-परिवार-को-संदेश-में-पीएम-1631439024472\n",
            "dtstring /content/dataset/english/1631439024472JEPI.txt\n",
            "4 अपने-आत्मीय-मित्र-को-याद-कर-रहा-हूं-पासवान-की-बरसी-पर-उनके-परिवार-को-संदेश-में-पीएम\n",
            "    Article and Summary pulled! 19:08:01                                                                                                    \n",
            "    file /content/inshorts-dataset-en/1631439024472JEPI.txt                                                                                                     \n",
            "--------------------------------------------------                                                                                                    \n",
            "Processing link 5/20: https://inshorts.com/hi/news/मुज़फ्फरनगर-में-प्रेम-प्रसंग-के-चलते-हमलावरों-ने-की-युवक-की-गोली-मारकर-हत्या-1559907245740\n",
            "dtstring /content/dataset/english/1559907245740ZAUP.txt\n",
            "5 मुज़फ्फरनगर-में-प्रेम-प्रसंग-के-चलते-हमलावरों-ने-की-युवक-की-गोली-मारकर-हत्या\n",
            "    Article and Summary pulled! 19:08:02                                                                                                    \n",
            "    file /content/inshorts-dataset-en/1559907245740ZAUP.txt                                                                                                     \n",
            "--------------------------------------------------                                                                                                    \n",
            "\u001b[A\u001b[A\u001b[A\u001b[A\u001b[A\u001b[A\u001b[A\u001b[A\u001b[A\u001b[A\u001b[A\u001b[A\u001b[A\u001b[A\u001b[A\u001b[A\u001b[A\u001b[A\u001b[A\u001b[AProcessing link 6/20: https://inshorts.com/hi/news/मेरठ-में-लूट-का-विरोध-करने-पर-बदमाशों-ने-महिला-को-मारी-गोली-1556088289163\n",
            "dtstring /content/dataset/english/1556088289163XRGL.txt\n",
            "6 मेरठ-में-लूट-का-विरोध-करने-पर-बदमाशों-ने-महिला-को-मारी-गोली\n",
            "    Article and Summary pulled! 19:08:03                                                                                                    \n",
            "    file /content/inshorts-dataset-en/1556088289163XRGL.txt                                                                                                     \n",
            "--------------------------------------------------                                                                                                    \n",
            "Processing link 7/20: https://inshorts.com/hi/news/औरतों-का-मस्जिद-में-तरावीह-की-नमाज़-पढ़ना-गलत-सहारनपुर-उलेमा-1558429942308\n",
            "dtstring /content/dataset/english/1558429942308HATK.txt\n",
            "7 औरतों-का-मस्जिद-में-तरावीह-की-नमाज़-पढ़ना-गलत-सहारनपुर-उलेमा\n",
            "    Article and Summary pulled! 19:08:04                                                                                                    \n",
            "    file /content/inshorts-dataset-en/1558429942308HATK.txt                                                                                                     \n",
            "--------------------------------------------------                                                                                                    \n",
            "Processing link 8/20: https://inshorts.com/hi/news/मिडडे-मील-के-लिए-छत्तीसगढ़-में-8-किमी-पैदल-चलकर-राशन-लाते-दिखे-शिक्षक-1635151023140\n",
            "dtstring /content/dataset/english/1635151023140QLNR.txt\n",
            "8 मिडडे-मील-के-लिए-छत्तीसगढ़-में-8-किमी-पैदल-चलकर-राशन-लाते-दिखे-शिक्षक\n",
            "    Article and Summary pulled! 19:08:06                                                                                                    \n",
            "    file /content/inshorts-dataset-en/1635151023140QLNR.txt                                                                                                     \n",
            "--------------------------------------------------                                                                                                    \n",
            "Processing link 9/20: https://inshorts.com/hi/news/मुज़फ्फरनगर-में-180-स्टूडेंट्स-को-मिले-समान-अंक-बड़े-पैमाने-पर-नकल-की-आशंका-1556938453209\n",
            "dtstring /content/dataset/english/1556938453209HYWG.txt\n",
            "9 मुज़फ्फरनगर-में-180-स्टूडेंट्स-को-मिले-समान-अंक-बड़े-पैमाने-पर-नकल-की-आशंका\n",
            "    Article and Summary pulled! 19:08:07                                                                                                    \n",
            "    file /content/inshorts-dataset-en/1556938453209HYWG.txt                                                                                                     \n",
            "--------------------------------------------------                                                                                                    \n",
            "Processing link 10/20: https://inshorts.com/hi/news/मेरठ-में-ईंट-भट्ठों-पर-छापा-बिना-मानक-मिले-4-भट्ठों-पर-कार्रवाई-1556087609648\n",
            "dtstring /content/dataset/english/1556087609648HMXA.txt\n",
            "10 मेरठ-में-ईंट-भट्ठों-पर-छापा-बिना-मानक-मिले-4-भट्ठों-पर-कार्रवाई\n",
            "    Article and Summary pulled! 19:08:08                                                                                                    \n",
            "    file /content/inshorts-dataset-en/1556087609648HMXA.txt                                                                                                     \n",
            "--------------------------------------------------                                                                                                    \n",
            "\u001b[A\u001b[A\u001b[A\u001b[A\u001b[A\u001b[A\u001b[A\u001b[A\u001b[A\u001b[A\u001b[A\u001b[A\u001b[A\u001b[A\u001b[A\u001b[A\u001b[A\u001b[A\u001b[A\u001b[AProcessing link 11/20: https://inshorts.com/hi/news/टी20-विश्व-कप-में-भारतपाक-मैच-नहीं-होना-चाहिए-क्योंकि-सीमा-पर-स्थिति-आदर्श-नहीं-है-गिरिराज-1634553946252\n",
            "dtstring /content/dataset/english/1634553946252ACHL.txt\n",
            "11 टी20-विश्व-कप-में-भारतपाक-मैच-नहीं-होना-चाहिए-क्योंकि-सीमा-पर-स्थिति-आदर्श-नहीं-है-गिरिराज\n",
            "    Article and Summary pulled! 19:08:09                                                                                                    \n",
            "    file /content/inshorts-dataset-en/1634553946252ACHL.txt                                                                                                     \n",
            "--------------------------------------------------                                                                                                    \n",
            "Processing link 12/20: https://inshorts.com/hi/news/मेरठ-में-एक-स्कूल-पर-छात्रों-को-सिख-व-ईसाई-बता-छात्रवृत्ति-लेने-का-आरोप-1558266900235\n",
            "dtstring /content/dataset/english/1558266900235NOQL.txt\n",
            "12 मेरठ-में-एक-स्कूल-पर-छात्रों-को-सिख-व-ईसाई-बता-छात्रवृत्ति-लेने-का-आरोप\n",
            "    Article and Summary pulled! 19:08:10                                                                                                    \n",
            "    file /content/inshorts-dataset-en/1558266900235NOQL.txt                                                                                                     \n",
            "--------------------------------------------------                                                                                                    \n",
            "Processing link 13/20: https://inshorts.com/hi/news/दुख-की-घड़ी-में-अपने-भाइयोंबहनों-का-साथ-देने-लखीमपुर-जा-रहा-हूं-पंजाब-के-सीएम-1633334213049\n",
            "dtstring /content/dataset/english/1633334213049KEFB.txt\n",
            "13 दुख-की-घड़ी-में-अपने-भाइयोंबहनों-का-साथ-देने-लखीमपुर-जा-रहा-हूं-पंजाब-के-सीएम\n",
            "    Article and Summary pulled! 19:08:12                                                                                                    \n",
            "    file /content/inshorts-dataset-en/1633334213049KEFB.txt                                                                                                     \n",
            "--------------------------------------------------                                                                                                    \n",
            "Processing link 14/20: https://inshorts.com/hi/news/मेरठ-में-स्कूल-के-विद्युतीकरण-के-लिए-मिले-₹21000-नहीं-हुई-बिजली-व्यवस्था-1556097920472\n",
            "dtstring /content/dataset/english/1556097920472OHTT.txt\n",
            "14 मेरठ-में-स्कूल-के-विद्युतीकरण-के-लिए-मिले-₹21000-नहीं-हुई-बिजली-व्यवस्था\n",
            "    Article and Summary pulled! 19:08:13                                                                                                    \n",
            "    file /content/inshorts-dataset-en/1556097920472OHTT.txt                                                                                                     \n",
            "--------------------------------------------------                                                                                                    \n",
            "Processing link 15/20: https://inshorts.com/hi/news/मुज़फ्फरनगर-में-गंगनहर-में-गिरने-से-जेनरेटर-ऑपरेटर-की-मौत-1557544620618\n",
            "dtstring /content/dataset/english/1557544620618RRII.txt\n",
            "15 मुज़फ्फरनगर-में-गंगनहर-में-गिरने-से-जेनरेटर-ऑपरेटर-की-मौत\n",
            "    Article and Summary pulled! 19:08:14                                                                                                    \n",
            "    file /content/inshorts-dataset-en/1557544620618RRII.txt                                                                                                     \n",
            "--------------------------------------------------                                                                                                    \n",
            "\u001b[A\u001b[A\u001b[A\u001b[A\u001b[A\u001b[A\u001b[A\u001b[A\u001b[A\u001b[A\u001b[A\u001b[A\u001b[A\u001b[A\u001b[A\u001b[A\u001b[A\u001b[A\u001b[A\u001b[AProcessing link 16/20: https://inshorts.com/hi/news/मुज़फ्फरनगर-में-तमंचे-के-बल-पर-बुज़ुर्ग-दंपति-से-नकदी-समेत-ज़ेवरात-की-लूट-1559617206347\n",
            "dtstring /content/dataset/english/1559617206347TENZ.txt\n",
            "16 मुज़फ्फरनगर-में-तमंचे-के-बल-पर-बुज़ुर्ग-दंपति-से-नकदी-समेत-ज़ेवरात-की-लूट\n",
            "    Article and Summary pulled! 19:08:15                                                                                                    \n",
            "    file /content/inshorts-dataset-en/1559617206347TENZ.txt                                                                                                     \n",
            "--------------------------------------------------                                                                                                    \n",
            "Processing link 17/20: https://inshorts.com/hi/news/फिर-से-दरें-बढ़ने-पर-नए-उच्चतम-स्तर-पर-पहुंचे-पेट्रोलडीज़ल-के-दाम-1634192750683\n",
            "dtstring /content/dataset/english/1634192750683HVTP.txt\n",
            "17 फिर-से-दरें-बढ़ने-पर-नए-उच्चतम-स्तर-पर-पहुंचे-पेट्रोलडीज़ल-के-दाम\n",
            "    Article and Summary pulled! 19:08:16                                                                                                    \n",
            "    file /content/inshorts-dataset-en/1634192750683HVTP.txt                                                                                                     \n",
            "--------------------------------------------------                                                                                                    \n",
            "Processing link 18/20: https://inshorts.com/hi/news/लखनऊ-में-सांडों-का-आतंक-जारी-एक-सप्ताह-में-2-की-गई-जान-1556722800993\n",
            "dtstring /content/dataset/english/1556722800993BLXR.txt\n",
            "18 लखनऊ-में-सांडों-का-आतंक-जारी-एक-सप्ताह-में-2-की-गई-जान\n",
            "    Article and Summary pulled! 19:08:17                                                                                                    \n",
            "    file /content/inshorts-dataset-en/1556722800993BLXR.txt                                                                                                     \n",
            "--------------------------------------------------                                                                                                    \n",
            "Processing link 19/20: https://inshorts.com/hi/news/मेरठ-के-जानीखुर्द-में-कार-में-मिला-2-युवकों-का-शव-मचा-हड़कंप-1557466721935\n",
            "dtstring /content/dataset/english/1557466721935USOP.txt\n",
            "19 मेरठ-के-जानीखुर्द-में-कार-में-मिला-2-युवकों-का-शव-मचा-हड़कंप\n",
            "    Article and Summary pulled! 19:08:18                                                                                                    \n",
            "    file /content/inshorts-dataset-en/1557466721935USOP.txt                                                                                                     \n",
            "--------------------------------------------------                                                                                                    \n",
            "Processing link 20/20: https://inshorts.com/hi/news/पाकिस्तान-की-जीत-पर-भारत-में-पटाखे-फोड़ने-वालों-का-डीएनए-भारतीय-नहीं-अनिल-विज-1635238671592\n",
            "dtstring /content/dataset/english/1635238671592MSUB.txt\n",
            "20 पाकिस्तान-की-जीत-पर-भारत-में-पटाखे-फोड़ने-वालों-का-डीएनए-भारतीय-नहीं-अनिल-विज\n",
            "    Article and Summary pulled! 19:08:19                                                                                                    \n",
            "    file /content/inshorts-dataset-en/1635238671592MSUB.txt                                                                                                     \n",
            "--------------------------------------------------                                                                                                    \n",
            "\u001b[A\u001b[A\u001b[A\u001b[A\u001b[A\u001b[A\u001b[A\u001b[A\u001b[A\u001b[A\u001b[A\u001b[A\u001b[A\u001b[A\u001b[A\u001b[A\u001b[A\u001b[A\u001b[A\u001b[A\n",
            "\n",
            "\n",
            "\n",
            "\n",
            "\n",
            "\n",
            "20 Articles and their summaries pulled!\n"
          ]
        }
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "2p-Gge3N1__z"
      },
      "source": [
        "# Exploratory Code"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 2,
      "metadata": {
        "id": "frC0_OIs2Ei_"
      },
      "outputs": [],
      "source": [
        "import urllib.request\n",
        "import urllib\n",
        "import urllib.parse\n",
        "from bs4 import BeautifulSoup\n",
        "from urllib.parse import quote\n",
        "import datetime\n",
        "import os\n",
        "import time\n",
        "import sys\n",
        "import random, string, re"
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "def encode_hindi_url(quote_page):\n",
        "    url = urllib.parse.urlsplit(quote_page)\n",
        "    url = list(url)\n",
        "    url[2] = urllib.parse.quote(url[2])\n",
        "    url = urllib.parse.urlunsplit(url)\n",
        "    return url\n",
        "\n",
        "input_file = \"links.txt\"\n",
        "\n",
        "try:\n",
        "    file = open(input_file, \"r\", encoding=\"utf-8\")\n",
        "    links = file.readlines()\n",
        "    file.close()\n",
        "except FileNotFoundError:\n",
        "    print(f\"File '{input_file}' not found.\")\n",
        "    exit()\n",
        "\n",
        "\n",
        "output_directory = \"scraped_headings/\"\n",
        "\n",
        "\n",
        "if not os.path.exists(output_directory):\n",
        "    os.makedirs(output_directory)\n",
        "\n",
        "\n",
        "for i, link in enumerate(links[:5]):  # Only top 5 links\n",
        "    link = link.strip()\n",
        "    print(f\"Scraping link {i + 1}: {link}\")\n",
        "\n",
        "\n",
        "    encoded_link = encode_hindi_url(link)\n",
        "\n",
        "    try:\n",
        "        page = urllib.request.urlopen(encoded_link)\n",
        "    except Exception as e:\n",
        "        print(f\"Error fetching {encoded_link}: {e}\")\n",
        "        continue\n",
        "\n",
        "    soup = BeautifulSoup(page, 'html.parser')\n",
        "\n",
        "\n",
        "    heading = soup.find(\"span\", itemprop=\"headline\")\n",
        "\n",
        "    if heading:\n",
        "        heading_text = heading.text.strip()\n",
        "\n",
        "        filename = os.path.join(output_directory, f\"heading_{i + 1}.txt\")\n",
        "\n",
        "        with open(filename, \"w\", encoding=\"utf-8\") as file:\n",
        "            file.write(heading_text)\n",
        "\n",
        "        print(f\"Heading {i + 1} saved.\")\n",
        "\n",
        "    time.sleep(random.uniform(1, 3))\n",
        "\n",
        "print(f\"Scraping complete for the top 5 links. Headings saved in '{output_directory}'\")"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "n2k7MWNPrQeA",
        "outputId": "65b277f7-3b0a-4631-e5e3-373abe59113c"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Scraping link 1: https://inshorts.com/hi/news/डेरा-सच्चा-सौदा-प्रमुख-गुरमीत-राम-रहीम-सिंह-अनुयायी-की-हत्या-के-लिए-दोषी-करार-1633677650409\n",
            "Heading 1 saved.\n",
            "Scraping link 2: https://inshorts.com/hi/news/सहारनपुर-में-बसपा-के-फज़लुर्रहमान-सबसे-आगे-मसूद-को-भी-मिल-चुके-सवा-लाख-वोट-1558601614502\n",
            "Heading 2 saved.\n",
            "Scraping link 3: https://inshorts.com/hi/news/गुरुग्राम-में-फ्लैट-के-नाम-पर-दिल्ली-के-व्यापारी-से-₹9125-की-ठगी-1556099842849\n",
            "Heading 3 saved.\n",
            "Scraping link 4: https://inshorts.com/hi/news/अपने-आत्मीय-मित्र-को-याद-कर-रहा-हूं-पासवान-की-बरसी-पर-उनके-परिवार-को-संदेश-में-पीएम-1631439024472\n",
            "Heading 4 saved.\n",
            "Scraping link 5: https://inshorts.com/hi/news/मुज़फ्फरनगर-में-प्रेम-प्रसंग-के-चलते-हमलावरों-ने-की-युवक-की-गोली-मारकर-हत्या-1559907245740\n",
            "Heading 5 saved.\n",
            "Scraping complete for the top 5 links. Headings saved in 'scraped_headings/'\n"
          ]
        }
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "# Amar Ujala (Working + Non Modular)"
      ],
      "metadata": {
        "id": "Imei6ixEu24v"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "from bs4 import BeautifulSoup\n",
        "import requests\n",
        "import re\n",
        "\n"
      ],
      "metadata": {
        "id": "8BLqwxEsMU6_"
      },
      "execution_count": 1,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "url = 'https://www.amarujala.com/delhi-ncr/gurgaon/21556042696-gurgaon-news?utm_campaign=fullarticle&utm_medium=referral&utm_source=inshorts'\n",
        "response = requests.get(url)\n",
        "\n",
        "if response.status_code != 200:\n",
        "    print(\"Failed to retrieve the webpage.\")\n",
        "    exit()\n",
        "\n",
        "soup = BeautifulSoup(response.content, 'html.parser')\n"
      ],
      "metadata": {
        "id": "d-Tt4stNMzFH"
      },
      "execution_count": 2,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "headlines = soup.find_all('h1')\n",
        "\n",
        "for headline in headlines:\n",
        "    print(\"Headline:\", headline.text.strip())"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "CxcwJUQen_d7",
        "outputId": "1fea4044-44ca-4744-a486-8990346d690d"
      },
      "execution_count": 3,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Headline: फलैट के नाम पर जाली कागजात बनाकर व्यापारी से 91.25 की धोखाधड़ी\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "article_div = soup.find('div', class_='article-desc tested')\n",
        "if article_div is None:\n",
        "    article_div= soup.find('div', class_='article-desc ul_styling')\n",
        "\n",
        "if article_div:\n",
        "    article_text = article_div.get_text(separator=\"\\n\")\n",
        "    print(article_text)\n",
        "\n",
        "else:\n",
        "    print(\"Article content not found on the page.\")"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "BF0LTcYFt2IH",
        "outputId": "630f86c2-abe2-4c63-de92-60f7a41172ce"
      },
      "execution_count": 4,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "\n",
            "\n",
            "\n",
            "\n",
            "\n",
            "                                                                                 \n",
            "                जाली कागजात बनाकर व्यापारी से 91.25 लाख की धोखाधड़ी \n",
            "                \n",
            "                \n",
            "                 \n",
            "                    \n",
            "\n",
            "\n",
            "\n",
            "\n",
            "\n",
            "\n",
            " \n",
            "यह वीडियो/विज्ञापन हटाएं\n",
            "\n",
            "\n",
            "\n",
            "                \n",
            "                \n",
            "                \n",
            "\n",
            "                                                \n",
            "                \n",
            "                                                                                                \n",
            "                                 \n",
            "                क्रॉसर...\n",
            "                \n",
            "                \n",
            "                \n",
            "\n",
            "                                                \n",
            "                \n",
            "                                                                                                \n",
            "                                 \n",
            "                \n",
            "\n",
            "                \n",
            "                \n",
            "                \n",
            "\n",
            "                                                \n",
            "                \n",
            "                                                                                                \n",
            "                                 \n",
            "                - निर्माणाधीन को-ऑपरेटिव हाउसिंग सोसाइटी में फ्लैट दिलाने के नाम पर की ठगी\n",
            "                \n",
            "                \n",
            "                \n",
            "\n",
            "                                                \n",
            "                \n",
            "                                                                                                \n",
            "                                 \n",
            "                \n",
            "\n",
            "                \n",
            "                \n",
            "                \n",
            "\n",
            "                                                \n",
            "                \n",
            "                                                                                                \n",
            "                                 \n",
            "                अमर उजाला ब्यूरो\n",
            "                \n",
            "                \n",
            "                \n",
            "\n",
            "                                                \n",
            "                \n",
            "                                                                                                \n",
            "                                 \n",
            "                \n",
            "\n",
            "                \n",
            "                \n",
            "                \n",
            "\n",
            "                                                \n",
            "                \n",
            "                                                                                                \n",
            "                                 \n",
            "                गुरुग्राम। सेक्टर-43 स्थित निर्माणाधीन को-ऑपरेटिव हाउसिंग सोसाइटी के नाम पर जाली कागजात बनाकर दिल्ली के व्यापारी से 91.25 लाख की धोखाधड़ी करने का मामला सामने आया है। पीड़ित व्यापारी से आरोपी ने दो माह के भीतर बैंक और नकदी के माध्यम से रुपये लिए। इसी बीच सोसाइटी के शेयर सर्टिफिकेट नंबर-8 की जांच कराने पर फर्जीवाड़े का खुलासा हुआ। पीड़ित ने सुशांतलोक थाना पुलिस में प्रवीण कुमार के खिलाफ धोखाधड़ी का मामला दर्ज कराया है। दिल्ली सराय रोहिल्ला स्थित विवेकानंद पुरी निवासी रणबीर सिंह ने पुलिस को दी शिकायत में बताया कि उन्होंने गुरुग्राम में फ्लैट खरीदने के लिए अपने साढू जयपाल सिंह के माध्यम से गुरुग्राम सेक्टर-43 रैनबो अपार्टमेंट फ्लैट नबंर-1202 निवासी प्रवीण गुप्ता से मुलाकात की। प्रवीण  ने उनको बताया कि सेक्टर-43 स्थित निर्माणाधीन द बजरंग को-ऑपरेटिव ग्रुप हाउसिंग सोसाइटी लिमिटेड में उसके और उसकी बुआ पवित्रा के नाम से दो फ्लैट बुक हैं। दोनों फ्लैट के लिए 1.42 करोड़ में सौदा तय हो गया। इसके बाद प्रवीण कुमार ने जाली शेयर सर्टिफिकेट नंबर-8 तैयार कर पीड़ित को दिखाया। इसके बाद पीड़ित रणबीर सिंह ने फरवरी और मार्च में 91.25 लाख का भुगतान कर दिया, जिसमें 63.05 लाख बैंक और 28.20 लाख का नकद भुगतान किया। पुलिस के मुताबिक सोसाइटी का ड्रॉ निकलने की तारीख टलने के बाद उन्होंने सोसायटी प्रबंधन से जांच पड़ताल की तो सामने आया कि प्रवीण गुप्ता और उनकी बुआ समेत अन्य के नाम से ऐसा कोई फ्लैट ही बुक नहीं है। प्रबंधन की ओर से शेयर सर्टिफिकेट नंबर-8 को भी फर्जी करार दिया गया। इसके बाद उन्होंने शिकायत दी। \n",
            "                \n",
            "                \n",
            "                \n",
            "\n",
            "                                                \n",
            "                \n",
            "                                                                                                                                \n",
            "                                 \n",
            "                \n",
            "\n",
            "                \n",
            "                \n",
            "                \n",
            "\n",
            "                                                \n",
            "                \n",
            "                                                                                                \n",
            "                                 \n",
            "                -----------\n",
            "                \n",
            "                \n",
            "                \n",
            "\n",
            "                                                \n",
            "                \n",
            "                                                                                                \n",
            "                                                \n",
            "\n",
            "\n",
            "\n",
            "\n",
            "\n",
            "\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "cleaned_article = ' '.join(article_text.split())\n",
        "cleaned_article = '\\n'.join(line.strip() for line in cleaned_article.splitlines() if line.strip())\n",
        "cleaned_article = re.sub(r'\\s+([.,;!?])', r'\\1', cleaned_article)\n",
        "print(cleaned_article)\n",
        "\n",
        "\n",
        "\n",
        "\n",
        "\n"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "ZjFAr2pruZTP",
        "outputId": "75e29973-480a-44e3-eb63-5cec692c51a8"
      },
      "execution_count": 36,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "जाली कागजात बनाकर व्यापारी से 91.25 लाख की धोखाधड़ी यह वीडियो/विज्ञापन हटाएं क्रॉसर... - निर्माणाधीन को-ऑपरेटिव हाउसिंग सोसाइटी में फ्लैट दिलाने के नाम पर की ठगी अमर उजाला ब्यूरो गुरुग्राम। सेक्टर-43 स्थित निर्माणाधीन को-ऑपरेटिव हाउसिंग सोसाइटी के नाम पर जाली कागजात बनाकर दिल्ली के व्यापारी से 91.25 लाख की धोखाधड़ी करने का मामला सामने आया है। पीड़ित व्यापारी से आरोपी ने दो माह के भीतर बैंक और नकदी के माध्यम से रुपये लिए। इसी बीच सोसाइटी के शेयर सर्टिफिकेट नंबर-8 की जांच कराने पर फर्जीवाड़े का खुलासा हुआ। पीड़ित ने सुशांतलोक थाना पुलिस में प्रवीण कुमार के खिलाफ धोखाधड़ी का मामला दर्ज कराया है। दिल्ली सराय रोहिल्ला स्थित विवेकानंद पुरी निवासी रणबीर सिंह ने पुलिस को दी शिकायत में बताया कि उन्होंने गुरुग्राम में फ्लैट खरीदने के लिए अपने साढू जयपाल सिंह के माध्यम से गुरुग्राम सेक्टर-43 रैनबो अपार्टमेंट फ्लैट नबंर-1202 निवासी प्रवीण गुप्ता से मुलाकात की। प्रवीण ने उनको बताया कि सेक्टर-43 स्थित निर्माणाधीन द बजरंग को-ऑपरेटिव ग्रुप हाउसिंग सोसाइटी लिमिटेड में उसके और उसकी बुआ पवित्रा के नाम से दो फ्लैट बुक हैं। दोनों फ्लैट के लिए 1.42 करोड़ में सौदा तय हो गया। इसके बाद प्रवीण कुमार ने जाली शेयर सर्टिफिकेट नंबर-8 तैयार कर पीड़ित को दिखाया। इसके बाद पीड़ित रणबीर सिंह ने फरवरी और मार्च में 91.25 लाख का भुगतान कर दिया, जिसमें 63.05 लाख बैंक और 28.20 लाख का नकद भुगतान किया। पुलिस के मुताबिक सोसाइटी का ड्रॉ निकलने की तारीख टलने के बाद उन्होंने सोसायटी प्रबंधन से जांच पड़ताल की तो सामने आया कि प्रवीण गुप्ता और उनकी बुआ समेत अन्य के नाम से ऐसा कोई फ्लैट ही बुक नहीं है। प्रबंधन की ओर से शेयर सर्टिफिकेट नंबर-8 को भी फर्जी करार दिया गया। इसके बाद उन्होंने शिकायत दी। -----------\n"
          ]
        }
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "# Cricket Tracker (Working + Non Modular)"
      ],
      "metadata": {
        "id": "cFfk8oFRwpX-"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "url = 'https://hindi.crictracker.com/fans-trolled-riyan-parag-on-social-media-for-a-catch/?fbclid=IwAR0YCLRo3_jNv-2rVr0vMZD2Q7iR8qVoZDJ6cgbr4m4D0YydqxN9tKtUGH0&amp=&utm_campaign=fullarticle&utm_medium=referral&utm_source=inshorts'\n",
        "response = requests.get(url)\n",
        "\n",
        "if response.status_code != 200:\n",
        "    print(\"Failed to retrieve the webpage.\")\n",
        "    exit()\n",
        "\n",
        "soup = BeautifulSoup(response.content, 'html.parser')"
      ],
      "metadata": {
        "id": "wPxTOALy1gbJ"
      },
      "execution_count": 48,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "headlines = soup.find_all('h1')\n",
        "\n",
        "for headline in headlines:\n",
        "    print(\"Headline:\", headline.text.strip())"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "outputId": "eba96efe-41bd-40fb-ecf9-fa134b5c4ae9",
        "id": "xR0AvKw62ajf"
      },
      "execution_count": 49,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Headline: कैच पकड़ने के बाद रियान पराग की घटिया हरकत देख भड़के फैन्स\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "paragraphs = soup.find_all('p')\n",
        "\n",
        "\n",
        "hindi_text = \"\"\n",
        "for p in paragraphs:\n",
        "    if any('\\u0900' <= c <= '\\u097F' for c in p.get_text()):\n",
        "        hindi_text += p.get_text() + \"\\n\"\n",
        "\n",
        "print(hindi_text)"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "hHFmKnQz4W80",
        "outputId": "305733ea-d043-4b3c-8136-111df40ac1d7"
      },
      "execution_count": 50,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Prashantउप-संपादक\n",
            "अद्यतन - मई 16, 2022 12:01 अपराह्न\n",
            "राजस्थान टीम के युवा खिलाड़ी रियान पराग हमेशा खबरों में रहते हैं, राजस्थान के मैच में इनका प्रदर्शन अच्छा हो या नहीं ये सुर्खियां बटोर ही लेते हैं। रियान पराग पर राजस्थान टीम काफी भरोसा करती है, इसलिए सालों से रियान इस टीम के साथ जुड़े हुए हैं। लेकिन कल रात LSG के खिलाफ हुए मैच के दौरान कुछ ऐसा हो गया, जिसे देख क्रिकेट फैन्स काफी गुस्सा हो गए और रियान पराग को सोशल मीडिया पर काफी बुरी तरह से ट्रोल कर दिया।\n",
            "रियान पराग गेंद और बल्ले दोनों से कमाल करना जानते हैं, लेकिन वो लगातार शानदार प्रदर्शन करने में फेल हो जाते हैं। वहीं दूसरी ओर फील्डिंग में इस युवा खिलाड़ी का कोई जवाब नहीं है, कल रात लखनऊ सुपर जायंट्स के खिलाफ हुए मैच में भी पराग ने इस क्षेत्र में अपना दम दिखाया। जहां उन्होंने बोल्ट के साथ मिलकर एक शानदार कैच पकड़ा, वहीं जब उन्होंने एक और कैच पकड़ा तो उन्होंने कुछ ऐसा कर दिया जो फैन्स को पसंद नहीं आया।\n",
            "*रियान पराग ने पकड़ा था मार्कस स्टोइनिस का एक कैच।\n",
            "*लेकिन गेंद रियान के हाथ में आने से पहले जमीन पर लग गई थी।\n",
            "*तीसरे अंपायर ने फिर दे दिया था मार्कस को नॉट आउट।\n",
            "*लेकिन बाद पराग ने फिर पकड़ा कैच, अंपायर की तरफ करने लगे इशारा।\n",
            "— अरविन्द राजपुरोहित (@avrajpurohit100) May 16, 2022\n",
            "वहीं LSG के खिलाफ राजस्थान ने पहले बल्लेबाजी करते हुए 178 रन बनाए थे, जहां टीम की तरफ जायसवाल, संजू और देवदत्त का बल्ला बोला था। दूसरी ओर LSG की टीम 154 रन ही बनाई और राजस्थान ने इस मैच को 24 रनों से जीत लिया, इस जीत के साथ राजस्थान टीम अंक तालिका पर दूसरे नंबर पर आ गई है और प्लेऑफ के टीम करीब भी आ चुकी है। लेकिन अब राहुल की टीम के लिए टेंशन काफी ज्यादा ही बढ़ गई है।\n",
            "\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "hindi_pattern = re.compile(r'[\\u0900-\\u097F]+')\n",
        "hindi_text_matches = hindi_pattern.findall(hindi_text)\n",
        "hindi_text = ' '.join(hindi_text_matches)\n",
        "print(hindi_text)"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "eQp3mJ8o46jM",
        "outputId": "de194b0b-a931-42a6-e942-fd77815e46a8"
      },
      "execution_count": 51,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "उप संपादक अद्यतन मई अपराह्न राजस्थान टीम के युवा खिलाड़ी रियान पराग हमेशा खबरों में रहते हैं राजस्थान के मैच में इनका प्रदर्शन अच्छा हो या नहीं ये सुर्खियां बटोर ही लेते हैं। रियान पराग पर राजस्थान टीम काफी भरोसा करती है इसलिए सालों से रियान इस टीम के साथ जुड़े हुए हैं। लेकिन कल रात के खिलाफ हुए मैच के दौरान कुछ ऐसा हो गया जिसे देख क्रिकेट फैन्स काफी गुस्सा हो गए और रियान पराग को सोशल मीडिया पर काफी बुरी तरह से ट्रोल कर दिया। रियान पराग गेंद और बल्ले दोनों से कमाल करना जानते हैं लेकिन वो लगातार शानदार प्रदर्शन करने में फेल हो जाते हैं। वहीं दूसरी ओर फील्डिंग में इस युवा खिलाड़ी का कोई जवाब नहीं है कल रात लखनऊ सुपर जायंट्स के खिलाफ हुए मैच में भी पराग ने इस क्षेत्र में अपना दम दिखाया। जहां उन्होंने बोल्ट के साथ मिलकर एक शानदार कैच पकड़ा वहीं जब उन्होंने एक और कैच पकड़ा तो उन्होंने कुछ ऐसा कर दिया जो फैन्स को पसंद नहीं आया। रियान पराग ने पकड़ा था मार्कस स्टोइनिस का एक कैच। लेकिन गेंद रियान के हाथ में आने से पहले जमीन पर लग गई थी। तीसरे अंपायर ने फिर दे दिया था मार्कस को नॉट आउट। लेकिन बाद पराग ने फिर पकड़ा कैच अंपायर की तरफ करने लगे इशारा। अरविन्द राजपुरोहित वहीं के खिलाफ राजस्थान ने पहले बल्लेबाजी करते हुए रन बनाए थे जहां टीम की तरफ जायसवाल संजू और देवदत्त का बल्ला बोला था। दूसरी ओर की टीम रन ही बनाई और राजस्थान ने इस मैच को रनों से जीत लिया इस जीत के साथ राजस्थान टीम अंक तालिका पर दूसरे नंबर पर आ गई है और प्लेऑफ के टीम करीब भी आ चुकी है। लेकिन अब राहुल की टीम के लिए टेंशन काफी ज्यादा ही बढ़ गई है।\n"
          ]
        }
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "# Timesnowhindi (working + Non Modular)"
      ],
      "metadata": {
        "id": "D6P9JKyiXMSZ"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "url = 'https://www.timesnowhindi.com/amp/india/article/rahul-gandhi-appeals-to-party-leaders-and-workers-not-to-celebrate-his-birthday/416284?utm_campaign=fullarticle&utm_medium=referral&utm_source=inshorts'\n",
        "response = requests.get(url)\n",
        "\n",
        "if response.status_code != 200:\n",
        "    print(\"Failed to retrieve the webpage.\")\n",
        "    exit()\n",
        "\n",
        "soup = BeautifulSoup(response.content, 'html.parser')\n",
        "\n",
        "headlines = soup.find_all('h1')\n",
        "\n",
        "for headline in headlines:\n",
        "    print(\"Headline:\", headline.text.strip())\n",
        "\n",
        "article_text = \"\"\n",
        "paragraphs = soup.find_all(\"p\")\n",
        "for paragraph in paragraphs:\n",
        "  article_text += paragraph.get_text() + \"\\n\"\n",
        "print(article_text)\n"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "Q2n9Sy9wcUQH",
        "outputId": "0233b2f2-cadc-4fef-b9b1-7429f52e1f81"
      },
      "execution_count": 6,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Headline: Rahul Gandhi Birthday:52 के हुए राहुल गांधी, बर्थडे पर की अपील-'युवा परेशान हैं, मेरे जन्मदिन पर जश्न न मनाएं'\n",
            "नयी दिल्ली: कांग्रेस नेता राहुल गांधी (Rahul Gandhi) ने पार्टी नेताओं और कार्यकर्ताओं से संडे को उनका जन्मदिन नहीं मनाने की अपील की है।राहुल ने पार्टी नेताओं और कार्यकर्ताओं से एक संदेश में कहा कि देश के युवा परेशान हैं और सड़कों पर विरोध कर रहे हैं, कांग्रेस कार्यकर्ताओं को उनके साथ खड़ा होना चाहिए, कांग्रेस के पूर्व अध्यक्ष राहुल गांधी रविवार को 52 साल (Rahul Gandhi turned 52) के हो गए हैं।\n",
            "अखिल भारतीय कांग्रेस कमेटी (AICC) के महासचिव (संचार) जयराम रमेश द्वारा ट्विटर पर पोस्ट किए गए एक संदेश में राहुल गांधी ने कहा कि देश में माहौल इस समय बेहद चिंताजनक है।\n",
            "राहुल ने सशस्त्र सेनाओं में भर्ती के लिए 'अग्निपथ' योजना के खिलाफ देश के कई हिस्सों में हो रहे विरोध प्रदर्शनों की ओर इशारा करते हुए कहा, 'देश के युवा परेशान हैं। हमें इस समय उनके और उनके परिवारों के साथ खड़ा होना चाहिए।'\n",
            "उन्होंने कहा, 'मैं देश भर के सभी कांग्रेस कार्यकर्ताओं और अपने शुभचिंतकों से अपील करता हूं कि मेरे जन्मदिन के मौके पर किसी भी तरह का जश्न न मनाएं।'\n",
            "केंद्र सरकार की अग्निपथ भर्ती योजना का विरोध कर रहे युवाओं के समर्थन में कांग्रेस पार्टी आज जंतर मंतर पर सत्याग्रह करेगी। सभी कांग्रेस सांसद, सीडब्ल्यूसी सदस्य और एआईसीसी पदाधिकारी इस सत्याग्रह में भाग लेंगे। सशस्त्र बलों में नई भर्ती योजना के खिलाफ देश के अलग-अलग हिस्सों में विरोध प्रदर्शन शुरू हो गए हैं। कुछ जगहों पर विरोध प्रदर्शन हिंसक भी हुए हैं।\n",
            "जंतर मंतर पर सत्याग्रह सुबह 10 बजे से शुरू होगा। कांग्रेस पार्टी के एक नेता ने कहा कि ये फैसला इसलिए लिया गया, क्योंकि 'अग्निपथ' योजना ने हमारे देश के युवाओं को आक्रोशित कर दिया है और वे सड़कों पर उतरकर विरोध प्रकट कर रहे हैं। हमारी जिम्मेदारी है कि हम उनके साथ खड़े रहें।\n",
            "कांग्रेस की अंतरिम अध्यक्ष सोनिया गांधी ने देश के युवाओं के नाम संदेश में कहा, 'आप भारतीय सेना में भर्ती होकर देश सेवा का महत्वपूर्ण कार्य करने की अभिलाषा रखते हैं। सेना में लाखों खाली पद होने के बावजूद पिछले तीन साल से भर्ती न होने का दर्द मैं समझ सकती हूं। एयरफोर्स में भर्ती की परीक्षा देकर रिजल्ट और नियुक्ति का इंतजार कर रहे युवाओं के साथ भी मेरी पूरी सहानुभूति है।'उन्होंने कहा, 'मुझे दुख है कि सरकार ने आपकी आवाज को दरकिनार करते हुए नई सेना भर्ती योजना की घोषणा की है, जो कि पूरी तरह से दिशाहीन है। आपके साथ-साथ कई पूर्व सैनिक और रक्षा विशेषज्ञों ने भी इस योजना पर सवालिया निशान उठाए हैं।' कांग्रेस अध्यक्ष ने कहा, 'मैं आपसे भी अनुरोध करती हूं कि अपनी जायज मांगों के लिए शांतिपूर्ण और अहिंसक ढंग से आंदोलन करें। कांग्रेस आपके साथ है।' \t\n",
            "Times Now Navbharat पर पढ़ें India News in Hindi, साथ ही ब्रेकिंग न्यूज और लाइव न्यूज अपडेट के लिए हमें गूगल न्यूज़ पर फॉलो करें ।\n",
            "\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [],
      "metadata": {
        "id": "VpaeVmEDp1Sq"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "source": [
        "#livehindustan (Not working)"
      ],
      "metadata": {
        "id": "gO7fsLO-6ADC"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "url = 'https://www.livehindustan.com/cricket/story-ipl-2021-david-warner-posts-selfie-from-stands-in-dubai-watches-video-srh-vs-kkr-match-4730766.amp.html?utm_campaign=fullarticle&utm_medium=referral&utm_source=inshorts'\n",
        "response = requests.get(url)\n",
        "\n",
        "if response.status_code != 200:\n",
        "    print(\"Failed to retrieve the webpage.\")\n",
        "    exit()\n",
        "\n",
        "soup = BeautifulSoup(response.content, 'html.parser')"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "8Ic6pqfZ8tyz",
        "outputId": "e50f086d-d9c6-480a-9dd0-ad58dbb3838c"
      },
      "execution_count": 2,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Failed to retrieve the webpage.\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "headlines = soup.find_all('h1')\n",
        "\n",
        "for headline in headlines:\n",
        "    print(\"Headline:\", headline.text.strip())"
      ],
      "metadata": {
        "id": "HSJQOeo48wSp"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "source": [
        "# Jagran (Working + Non Modular)"
      ],
      "metadata": {
        "id": "erot_EdcsVGB"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "url = 'https://www.jagran.com/bihar/katihar-inveastigation-19191026.html?utm_campaign=fullarticle&utm_medium=referral&utm_source=inshorts'\n",
        "response = requests.get(url)\n",
        "\n",
        "if response.status_code != 200:\n",
        "    print(\"Failed to retrieve the webpage.\")\n",
        "    exit()\n",
        "\n",
        "soup = BeautifulSoup(response.content, 'html.parser')\n",
        "\n",
        "headlines = soup.find_all('h1')\n",
        "\n",
        "for headline in headlines:\n",
        "    print(\"Headline:\", headline.text.strip())\n",
        "\n",
        "article_div = soup.find('div', class_='articlecontent')\n",
        "\n",
        "if article_div:\n",
        "    article_text = article_div.get_text(separator=\"\\n\")\n",
        "    #print(article_text)\n",
        "\n",
        "else:\n",
        "    print(\"Article content not found on the page.\")\n",
        "\n",
        "cleaned_article = ' '.join(article_text.split())\n",
        "\n",
        "cleaned_article = '\\n'.join(line.strip() for line in cleaned_article.splitlines() if line.strip())\n",
        "\n",
        "cleaned_article = re.sub(r'\\s+([.,;!?])', r'\\1', cleaned_article)\n",
        "\n",
        "print(cleaned_article)\n"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "outputId": "a85d4c40-8921-4200-a88c-e646c12f01f1",
        "id": "g4UViHOys2AV"
      },
      "execution_count": 12,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Headline: सूर्यास्त बाद स्टीमर परिचालन की सूचना पर औचक निरीक्षण\n",
            "कटिहार। मनिहारी व साहेबगंज के बीच गंगा में सूर्यास्त के बाद स्टीमर परिचालन की सूचना पर गुरुवार की देर शाम अनुमंडल पदाधिकारी संदीप कुमार, भुमि सुधार उपसमाहर्ता रविकांत सिन्हा व सीओ संजीव कुमार ने मनिहारी लंच घाट पहुंच औचक निरीक्षण किया। कुछ देर बाद मनिहारी थाना के अनि रूपेश रंजन व अनि नवनीत कुमार भी पहुंचे। एसडीओ ने लंच घाट पर कई बातों की जानकारी भी ली। एसडीओ संदीप कुमार ने कहा कि गंगा नदी मार्ग में मनिहारी क्षेत्र में अवैध जहाजों के परिचालन पर सख्त कार्रवाई की जाएगी। किसी कीमत पर इसे बर्दाश्त नहीं किया जाएगा। उन्होंने कहा कि सूर्यास्त के बाद जहाजों व नावों का परिचालन हर हाल में वर्जित है। इसके उल्लघंन करने पर सख्त कार्रवाई की जाएगी। उन्होंने सरकार के तय निर्देश व बिहार बंगाल फेरी एक्ट का हर हाल में पालन करने का निर्देश बंदोबस्तधारी को दिया। एसडीओ ने सीओ के प्रति नाराजगी भी जताई और उन्हें आवश्यक दिशा- निर्देश भी दिया। यद्यपि ंऔचक निरीक्षण के क्रम में लंच घाट मनिहारी पर एक भी जहाज नहीं था। बताया गया कि जहाज साहिबगंज समदा घाट में लगी हुई है।\n"
          ]
        }
      ]
    }
  ],
  "metadata": {
    "colab": {
      "provenance": [],
      "collapsed_sections": [
        "7u_YqPAwrce8",
        "2p-Gge3N1__z",
        "Imei6ixEu24v",
        "cFfk8oFRwpX-",
        "D6P9JKyiXMSZ",
        "gO7fsLO-6ADC",
        "erot_EdcsVGB"
      ],
      "authorship_tag": "ABX9TyPr5d4pkV4dIMnnxShBcruw",
      "include_colab_link": true
    },
    "kernelspec": {
      "display_name": "Python 3",
      "name": "python3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "nbformat": 4,
  "nbformat_minor": 0
}