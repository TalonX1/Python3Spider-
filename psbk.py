import requests
from lxml import etree
import json
import pymongo


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome'
                  '/68.0.3440.106 Safari/537.36'
}
base_url = 'https://www.qiushibaike.com'



def detail_page(url):
    response = requests.get(url, headers=headers)
    html = etree.HTML(response.text)
    url_messages = html.xpath('//div[@id="content-left"]/div/a[1]/@href')
    print(url_messages)
    for url_message in url_messages:
        detail_url = base_url + url_message
        parse_page(detail_url)


def parse_page(url):
    html = etree.HTML(requests.get(url, headers=headers).text)
    time = ''.join(html.xpath('//div[@class="source"]/a[last()-1]/text()'))
    author = ''.join(html.xpath('//div[@class="author clearfix"]/a[2]/h2/text()'))
    text = ''.join(html.xpath('//div[@id="single-next-link"]/div/text()'))
    stats = ''.join(html.xpath('//span[@class="stats-vote"]/i/text()'))
    comments = ''.join(html.xpath('//span[@class="stats-comments"]/i/text()'))
    best_comment_author = ''.join(html.xpath('//div[@class="cmt-name"][1]/text()'))
    best_comment_content = ''.join(html.xpath('//div[@class="comments-table"][1]//div[@class="main-text"]/text()'))
    if author:
        author = author
    else:
        author = '匿名用户'
    messsage = [{
        '时间': time.replace('\n', ''),
        '作者': author,
        '内容': text.replace('\n', ''),
        '点赞': stats,
        '评论': comments,
        '神评论作者': best_comment_author.replace('\n', ''),
        '神评论内容': best_comment_content.replace('\n', '')

    }]

    print(messsage)
    save_text(messsage)
    save_to_mongo(messsage)


def save_text(message):
    with open('qsbk.txt', 'a', encoding='utf-8') as file:
        file.write(json.dumps(message, ensure_ascii=False) + '\n')


def save_to_mongo(messsage):
    client = pymongo.MongoClient(host='localhost', port=27017)
    db = client['糗事百科']
    collection = db['message']
    collection.insert(messsage)


def main():
    for page in range(1, 10):
        url = base_url + '/text/page/' + str(page)
        print(url)
        detail_page(url)


if __name__ == '__main__':
    main()














