import re
import time

import requests
from bs4 import BeautifulSoup

next_re = re.compile("（翻页提示.*）")


def main():
    # 目录的网址
    # baseurl = "https://www.daomubiji.com/dao-mu-bi-ji-1"
    article_link = "https://www.daomubiji.com/qi-xing-lu-wang-01.html"
    while len(article_link) != 0:
        head = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"}
        time.sleep(1)
        req = requests.get(url=article_link, headers=head)
        time.sleep(1)
        req.encoding = 'UTF-8'
        soup = BeautifulSoup(req.text, 'html.parser')
        content = soup.find('div', class_="content", attrs={"class": "content"})
        print(content)
        title_split = content.find('h1', class_='article-title').text.split(' ')
        title = title_split[1] + ' ' + title_split[2]
        print(title)
        article = content.find('article', class_="article-content").text
        article = next_re.sub('', article)
        article = article.replace('\n', '\n\n')
        print(article)
        article_link = content.find('a', attrs={"rel": "next"}).attrs['href']
        print(article_link)


if __name__ == "__main__":
    main()
