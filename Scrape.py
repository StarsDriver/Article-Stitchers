
import requests
from lxml import etree
import re
from header import headers
import random


# 爬取单个百度文库文章
class ScrapeCertainPassage:

    def __init__(self, url, header=headers):

        self.url = url
        self.header = header

    def scrape(self):

        res = requests.get(self.url, headers=self.header)
        res = etree.HTML(res.text)
        doc_reqs = res.xpath('//body/script/text()')  # 获取所有script节点文本，返回列表，藏有文章数据源的在其中一个最长的字符串里
        doc_reqs = max(doc_reqs,key = len)  #找到最长字符串
        pattern = re.compile('pageIndex.*?pageLoadUrl":"(.*?)"}', re.S)  # 修饰符要加再compile里
        doc_reqs = re.findall(pattern, doc_reqs)

        all_passage = ''
        all_sentences = []
        for doc_req in doc_reqs:
            doc = requests.get(doc_req)
            doc.encoding = "unicode_escape"
            pattern = re.compile('"c":"(.*?)"."p"', re.S)
            docs = re.findall(pattern, doc.text)# 得到该页文章各句子组成的列表
            while ' ' in docs:
                docs.remove(' ') #删除所有空格
            if doc_req == doc_reqs[0]:      #得到标题
                title = docs[0]
            page_passage = ''
            for doc in docs:  # 组装为改页文章
                page_passage += doc
            all_passage += page_passage     #加入文章整体

        with open(f"./Passages/{title}{str(int(random.random()*100)/100)}.txt", "w",encoding='utf-8') as f:    #将文章写入
            f.write(all_passage)

        docs = re.split(r'[。！？]',all_passage)   #用句号感叹号问号分割字符串
        all_sentences.extend(docs)  #加入

        return all_sentences


if __name__ == "__main__":
    passage_scrape = ScrapeCertainPassage('https://wenku.baidu.com/view/117919ed31d4b14e852458fb770bf78a64293a60.html?fr=income3-doc-search')
    passage = passage_scrape.scrape()
    print(passage)

"""
#搜索关键词爬取百度文库
class ScrapKeyWord:

    def __init__(self,keyword = '自信',header = headers):#可传入某个表达网站的参数？

        self.keyword = keyword
        self.header = header
        self.cookies = header['Cookie']


    def get_passage_url(self):      #搜索关键词

        cookie_list = []
        for cookie in self.cookies.split('; '): #构造cookie字典
            cookie_dic = {}
            name = cookie.split('=')[0]
            value = cookie.split('=')[1]
            cookie_dic['name'] = name
            cookie_dic['value'] = value
            cookie_list.append(cookie_dic)
        
        browser = webdriver.Edge()
        browser.get('https://wenku.baidu.com/')
        
        for cookie in cookie_list:
            browser.add_cookie(cookie)
        
        browser.get('https://wenku.baidu.com/')
        time.sleep(5)
        browser.find_element(By.CLASS_NAME,"search-input").send_keys(self.keyword)      #搜索关键词
        browser.find_element(By.CLASS_NAME,"search-btn").click()
        time.sleep(5)
       # with open('meta.txt','w',encoding='utf-8')as f:
      #      f.write(browser.page_source)
        search_res = browser.find_elements(By.XPATH,'//a')
        
        res = requests.get('https://wenku.baidu.com/search?word=%E5%8B%87%E6%95%A2&lm=0&od=0&fr=top_home&ie=utf-8&searchType=0&pn=2',headers = self.header)
        with open('meta2.txt','w',encoding = 'utf-8')as f:
            f.write(res.text)
        passage_url = []    
        for res in search_res:
            passage_url.append(res.get_attribute("href"))
        
        print(passage_url)
        time.sleep(1000)
"""
