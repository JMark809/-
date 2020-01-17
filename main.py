import requests
import parsel
import os
def get_chapters(url):
    response = requests.get(url)
    #自动解决编码问题 .encoding 从http header 中猜测响应内容编码方式  .apprent_encoding 从内容中分析响应内容编码方式
    response.encoding = response.apparent_encoding
    return response.text
    #乱码问题 改编码（utf-8）

#得到网页解析并保存
def save_chapter(html):
    #定义选择器 （方便）不定义可直接parsel.Selector.css()
    sel = parsel.Selector(html)
    title_li = sel.xpath('//div[@class="p"]/a[last()]/text()').extract()
    title = "".join(title_li)
    name_li = sel.css('.content h1::text').extract()
    name = "".join(name_li).strip("正文 ")
    content = sel.xpath('//*[@id="content"]/text()').extract()
    # os.mkdir(r'D:/书趣阁下载/'+title+'/')
    with open('D:/书趣阁下载/'+title+'/'+name+'.txt',mode="w",encoding="utf-8") as f:
        for i in content:
            f.write(i+"\n")
    print(name)

if __name__ == "__main__":
    # 整合网站地址
    print("输入书籍主页面地址")
    index = input().replace('index.html ', '')
    index_html = get_chapters(index)
    index_sel = parsel.Selector(index_html)
    #css选择器（可改）
    links = index_sel.xpath('//div[@class="listmain"]//dt[last()]/following-sibling::dd//@href').extract()
    for link in links:
        dl = get_chapters(index+link)
        save_chapter(dl)
    print("爬取完成！")
