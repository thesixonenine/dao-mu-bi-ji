import re
import time

import requests
from bs4 import BeautifulSoup

next_re = re.compile("（翻页提示.*）")
file_name_re = re.compile("\\d{2}")


def main():
    # 目录的网址
    # baseurl = "https://www.daomubiji.com/dao-mu-bi-ji-1"
    base_name = 'mi-hai-gui-chao'
    article_link = "https://www.daomubiji.com/" + base_name + "-01.html"
    sub_dir = '6-' + base_name
    while len(article_link) != 0 and article_link.startswith('https://www.daomubiji.com/' + base_name):
        head = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"}
        time.sleep(1)
        req = requests.get(url=article_link, headers=head)
        time.sleep(1)
        req.encoding = 'UTF-8'
        soup = BeautifulSoup(req.text, 'html.parser')
        content = soup.find('div', class_="content", attrs={"class": "content"})
        # print(content)
        title_split = content.find('h1', class_='article-title').text.split(' ')
        title = title_split[1] + ' ' + title_split[2]
        # print(title)
        article = content.find('article', class_="article-content").text
        article = next_re.sub('', article)
        article = article.replace('\n', '\n\n')
        # print(article)
        file_name = file_name_re.findall(article_link)[0]
        # file_name = str(int(file_name) + 75)
        with open(sub_dir + '/' + file_name + '.md', 'w', encoding='UTF-8', newline='\n') as f:
            f.write("# " + title + '\n')
            f.write(article)
        with open('SUMMARY.md', 'a', encoding='UTF-8', newline='\n') as f:
            f.write("  * [" + title + '](' + sub_dir + '/' + file_name + '.md)\n')
        article_link = content.find('a', attrs={"rel": "next"}).attrs['href']
        print(article_link)


if __name__ == "__main__":
    main()
