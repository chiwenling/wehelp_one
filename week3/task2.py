print("==task2==")
import urllib.request as req
import csv

def get_one_page(url):

    my_headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
              'cookie': 'over18=1;'}
    request = req.Request(url, headers=my_headers)
    with req.urlopen(request) as response:
        data = response.read().decode("utf-8")

    import bs4
    root = bs4.BeautifulSoup(data,"html.parser")

    #note:找標題
    titles = []
    title_word = root.find_all("div",class_="title")
    
    for title in title_word:
        if title.a is not None:
            titles.append(title.a.string)
        else: 
            titles.append(None)
            continue
    
    #note:找讚數噓數
    counts = root.find_all("div", class_="nrec")
    totals = []
    for count in counts:
        if count.span is None:
            totals.append(0)
        else:
            totals.append(count.span.string)

    #note:找文章連結，爬文章內的資訊
    page_data = []
    links = root.find_all("div", class_="title") 
    for i, link in enumerate(links):
        post_url = ""
        if link.a == None:
            continue
        else:
            post_url = "https://www.ptt.cc"+link.a["href"]    
            post = req.Request(post_url, headers=my_headers)
            with req.urlopen(post) as response:
                post.text = response.read().decode("utf-8")

            root2 = bs4.BeautifulSoup(post.text, "html.parser")

            rootPost = root2.find("div", id="main-content")
            article_info = rootPost.find_all("span", class_="article-meta-value")

            if len(article_info) != 0:  
                time = article_info[3].string  
            
            page_data.append([titles[i],totals[i],time])
    return page_data
           

#note:要換三頁
#note:要儲存成csv
data = []
data.extend(get_one_page("https://www.ptt.cc/bbs/Lottery/index.html"))
data.extend(get_one_page("https://www.ptt.cc/bbs/Lottery/index2080.html"))
data.extend(get_one_page("https://www.ptt.cc/bbs/Lottery/index2079.html"))

csv_file = "article.csv"
with open(csv_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(data)