'''get daily news'''

'''Text with hyperlink won't be saved'''

import requests
from time import localtime, sleep
from lxml import etree


def get_time():
    date_ = f'{str(localtime().tm_year).zfill(4)}-{str(localtime().tm_mon).zfill(2)}-{str(localtime().tm_mday).zfill(2)}'
    return date_


# delete duplicated
def title_tidy(title_list):
    t_index = []
    for i in range(1, len(title_list)):
        if title_list[i] == title_list[i - 1]: t_index.append(i)
    t_index.reverse()
    for i in range(len(t_index)): title_list.pop(t_index[i])
    return title_list


# tidy text, seems a little bit redundant
def text_tidy(p_text):
    text_ = p_text.replace('’', "'")
    text_ = text_.replace(' \n\n', ' ')
    text_ = text_.replace('\n\n ', ' ')
    text_ = text_.replace('\n\n,', ' ,')
    text_ = text_.replace(',\n\n', ', ')
    text_ = text_.replace(';\n\n', '; ')
    text_ = text_.replace('\n\n;', ' ;')
    text_ = text_.replace(':\n\n', ': ')
    text_ = text_.replace('\n\n:', ' :')
    text_ = text_.replace('"\n\n', '" ')
    text_ = text_.replace('\n\n"', ' "')
    text_ = text_.replace("'\n\n", "' ")
    text_ = text_.replace("\n\n'", " '")
    return text_


def save(text, file_name, mode='w', encoding='utf-8'):
    with open(f'{file_name}.txt', mode, encoding=encoding) as f: f.write(text)


def nbc():
    url = 'https://www.nbcnews.com/'
    res = requests.get(url)
    html = etree.HTML(res.text)
    href = html.xpath('//h2/a/@href')
    href = title_tidy(href)
    quant = int(input(f'There are {len(href)} pieces detected. How many would you download:'))
    if quant > len(href) or quant < 1:
        print("Outnumber!")
        quit()
    count = 0
    save('', f'NBC_news_title_{get_time()}')
    save('', f'NBC_news_text_{get_time()}')
    for i in range(quant):
        url = href[i]
        sleep(0.1)  # delete to speed up
        res = requests.get(url)
        html = etree.HTML(res.text)
        title = html.xpath('//h1/text()')
        if len(title) == 0:
            print(f'Video or other news. Link: {url}')
            continue
        title = title[0]
        author = html.xpath('//span[@class="byline-name"]/a/text() | //span[@class="byline-name" and not(a)]/text()')
        author = ', '.join(author)
        text = html.xpath('//p[@class=""]/text()')
        text = '\n\n'.join(text)
        text = text_tidy(text)
        count += 1
        save(f'Title: {title}\nLink: {url}\n\n', f'NBC_news_title_{get_time()}', 'a')  # news title
        save(f'Title: {title}\n\nOrigin: {url}\n\nAuthor: {author}\n\n\n', f'NBC_news_text_{get_time()}', 'a')
        save(f'{text}' + '\n\n------------------------------\n\n', f'NBC_news_text_{get_time()}', 'a')
        print(f'Title: {title}. Link: {href[i]}.')
    print(f'Files saved with {count} articles available.')


def cnn():
    head = 'https://www.cnn.com'
    res = requests.get(head + '/')
    html = etree.HTML(res.text)
    href = html.xpath('//a[@data-link-type="article"]/@href')
    href = title_tidy(href)
    quant = int(input(f'{len(href)} data detected. How many would you like to download:'))
    if quant > len(href) or quant < 1:
        print("Outnumber!")
        quit()
    count = 0
    save('', f'CNN_news_title_{get_time()}')
    save('', f'CNN_news_text_{get_time()}')
    for i in range(quant):
        url = head + href[i]
        sleep(0.1)  # delete to speed up
        res = requests.get(url)
        html = etree.HTML(res.text)
        title = html.xpath('//h1[@data-editable="headlineText"]/text()')
        if len(title) == 0:
            print(f'Video or other news. Link: {url}')
            continue
        title = title[0].strip()
        author = html.xpath('//span[@class="byline__name"]/text()')
        author = ', '.join(author)
        text = html.xpath('//p[@class="paragraph inline-placeholder"]/text()')
        for k in range(len(text)): text[k].strip()
        text = ''.join(text)
        text = text_tidy(text)
        count += 1
        save(f'Title: {title}\nLink: {url}\n\n', f'CNN_news_title_{get_time()}', 'a')  # news title
        save(f'Title: {title}\n\nOrigin: {url}\n\nAuthor: {author}\n\n\n', f'CNN_news_text_{get_time()}', 'a')
        save(f'{text}' + '\n\n------------------------------\n\n', f'CNN_news_text_{get_time()}', 'a')
        print(f'Title: {title}. Link: {url}')
    print(f'Files saved with {count} articles available.')


def abc():
    head = 'https://abcnews.go.com/'
    res = requests.get(head)
    html = etree.HTML(res.text)
    href1 = html.xpath('//div[@class="HeadlinesTrio"]/a/@href')
    href2 = html.xpath('//div[@class="title card"]/a[@class="AnchorLink"]/@href | //div[@class="title"]/a[@class="AnchorLink"]/@href')
    href3 = html.xpath('//a[@target="_self"]/@href')
    href4 = html.xpath('//a[@class="AnchorLink VideoTile"]/@href')
    href = href1 + href2 + href3 + href4
    href = title_tidy(href)
    quant = int(input(f'{len(href)} data detected. How many would you like to download:'))
    if quant > len(href) or quant < 1:
        print("Outnumber!")
        quit()
    count = 0
    save('', f'ABC_news_title_{get_time()}')
    save('', f'ABC_news_text_{get_time()}')
    for i in range(quant):
        url = href[i]
        sleep(0.1)  # delete to speed up
        res = requests.get(url)
        html = etree.HTML(res.text)
        title = html.xpath('//div[@data-testid="prism-headline"]/h1/text()')
        if len(title) == 0:
            print(f'Video or other news. Link: {url}')
            continue
        title = title[0]
        author = html.xpath('//a[@data-testid="prism-linkbase"]/text()')
        author = ', '.join(author)
        text = html.xpath('//div[@data-testid="prism-article-body"]/p/text()')
        text = '\n\n'.join(text)
        text = text_tidy(text)
        count += 1
        save(f'Title: {title}\nLink: {url}\n\n', f'ABC_news_title_{get_time()}', 'a')  # news title
        save(f'Title: {title}\n\nOrigin: {url}\n\nAuthor: {author}\n\n\n', f'ABC_news_text_{get_time()}', 'a')
        save(f'{text}' + '\n\n------------------------------\n\n', f'ABC_news_text_{get_time()}', 'a')
        print(f'Title: {title}. Link: {url}')
    print(f'Files saved with {count} articles available.')


def fox():
    head = 'https://www.foxnews.com/'
    res = requests.get(head)
    html = etree.HTML(res.text)
    href = html.xpath('//h3[@class="title"]/a/@href')
    href = title_tidy(href)
    quant = int(input(f'{len(href)} data detected. How many would you like to download:'))
    if quant > len(href) or quant < 1:
        print("Outnumber!")
        quit()
    count = 0
    save('', f'FOX_news_title_{get_time()}')
    save('', f'FOX_news_text_{get_time()}')
    for i in range(quant):
        if href[i][0:4] != 'http': href[i] = 'https:' + href[i]
        url = href[i]
        sleep(0.1)  # delete to speed up
        res = requests.get(url)
        html = etree.HTML(res.text)
        title = html.xpath('//h1[@itemprop="headline"]/text()')
        if len(title) == 0:
            print(f'Video or other news. Link: {url}')
            continue
        title = title[0]
        author = html.xpath('//a[@rel="author"]/strong/text()')
        author = ', '.join(author)
        text = html.xpath('//div[@itemprop="articleBody"]/p/text()')
        text = '\n\n'.join(text)
        text = text_tidy(text)
        count += 1
        save(f'Title: {title}\nLink: {url}\n\n', f'FOX_news_title_{get_time()}', 'a')  # news title
        save(f'Title: {title}\n\nOrigin: {url}\n\nAuthor: {author}\n\n\n', f'FOX_news_text_{get_time()}', 'a')
        save(f'{text}' + '\n\n------------------------------\n\n', f'FOX_news_text_{get_time()}', 'a')
        print(f'Title: {title}. Link: {url}')
    print(f'Files saved with {count} articles available.')


def bbc():
    head = 'https://www.bbc.com'
    res = requests.get(head + '/')
    html = etree.HTML(res.text)
    href = html.xpath('//h2[@data-testid="card-headline"]/../../../../../@href | //h2[@data-testid="card-headline"]/../../../../@href')
    href = title_tidy(href)
    quant = int(input(f'{len(href)} data detected. How many would you like to download:'))
    if quant > len(href) or quant < 1:
        print("Outnumber!")
        quit()
    count = 0
    save('', f'BBC_news_title_{get_time()}')
    save('', f'BBC_news_text_{get_time()}')
    for i in range(quant):
        url = head + href[i]
        sleep(0.1)  # delete to speed up
        res = requests.get(url)
        html = etree.HTML(res.text)
        title = html.xpath('//section[@data-component="headline-block"]/h1/text()')
        if len(title) == 0:
            print(f'Video or other news. Link: {url}')
            continue
        title = title[0]
        author = html.xpath('//div[@data-testid="byline"]/div/span[@data-testid="byline-name"]/text()')
        author = ', '.join(author)
        text = html.xpath('//section[@data-component="text-block"]/p/b/text() | //section[@data-component="text-block"]/p/text()')
        text = '\n\n'.join(text)
        text = text_tidy(text)
        count += 1
        save(f'Title: {title}\nLink: {url}\n\n', f'BBC_news_title_{get_time()}', 'a')  # news title
        save(f'Title: {title}\n\nOrigin: {url}\n\nAuthor: {author}\n\n\n', f'BBC_news_text_{get_time()}', 'a')
        save(f'{text}' + '\n\n------------------------------\n\n', f'BBC_news_text_{get_time()}', 'a')
        print(f'Title: {title}. Link: {url}')
    print(f'Files saved with {count} articles available.')


if __name__ == '__main__':
    # Hello, World! :)
    news = input('Choose news site["nbc","cnn","abc","fox","bbc"]:').lower()
    if news == 'nbc': nbc()
    elif news == 'cnn': cnn()
    elif news == 'abc': abc()
    elif news == 'fox': fox()
    elif news == 'bbc': bbc()
    else:
        print('Oops! It seems a wrong input. Please retry...')
        sleep(2)