from bs4 import BeautifulSoup as bs
from urllib.parse import urlparse
from selenium import webdriver
import requests
import re


class WebAppCrowler:
    def __init__(self, root):
        if re.search(r'/$', root) is None:
            self.root = root + '/'
        else:
            self.root = root
        self.allow_domain = urlparse(root).netloc
        self.lst_dic_url = []
        self.write_json = "{\"list_url\":["
        self.driver = webdriver.Chrome()
        self.lst_dist = []
    
    def rules(self, href):
        if href not in self.lst_dist:
            if href is not None:
                if re.search(r'^#', href) is None:
                    if re.search(r'javascript:void\(0\)', href) is None:
                        self.lst_dist.append(href)
                        return True
        return False
        
    
    def crowl(self):
        def find_href(target, parent):
            self.lst_dic_url.append({'url': target, 'parent': parent})
            print('target : ' + target + ' parent : ' + str(parent))
            self.driver.get(target)
            current_domain = urlparse(self.driver.current_url).netloc
            if current_domain == self.allow_domain:
                html = self.driver.page_source
                soup = bs(html, 'lxml')
                for a in soup.find_all('a'):
                    href = a.get('href')
                    if self.rules(href):
                        if re.search('^https?://', href) is None:
                            if re.search('^/', href) is None:
                                t_url = self.root + href
                                find_href(t_url, target)
                            else:
                                t_url = self.root + re.sub(r'^/','',href)
                                find_href(t_url, target)
                        else:
                            if urlparse(href).netloc == self.allow_domain:
                                find_href(href, target)
                            else:
                                pass
                    else:
                        pass
        
        
        find_href(self.root, "None")
        self.driver.close()
        print(len(self.lst_dic_url))

        l = len(self.lst_dic_url)
        i = 0
        for dic in self.lst_dic_url:
            self.write_json += str(dic)
            i += 1
            if i < l:
                self.write_json += ","

        self.write_json += "]}"
        self.write_json = re.sub(r"'", '"', self.write_json)
        f = open('crowl_result.json', 'w')
        f.write(self.write_json)
        f.close()