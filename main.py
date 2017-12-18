import sys
sys.path.append("./check_xss/")
sys.path.append("./crawler/")
from urllib import parse as urlparse
from selenium import webdriver
from selenium.webdriver.common.alert import Alert
from webappcrowler import WebAppCrowler
from CheckXSS import check_xss
import requests
import json
import re

#Usage
args = sys.argv
argc = len(args)
if argc < 2:
    print("Usage :# python main.py [URL]")
    quit()

#runch browser
driver = webdriver.Firefox()
URL = args[1]

#crowling
crowler = WebAppCrowler(URL)
crowler.crowl()
f = open('crowl_result.json', 'r')
jsonf = json.load(f)
lst_url_dic = jsonf['list_url']

#check
for dic in lst_url_dic:
    print()
    print("----- check : " + dic['url'])
    if re.search(r'[^#]+?\?[^#]+?=', dic['url']):
        try:
            check_xss(dic['url'],driver)
        except:
            import traceback
            traceback.print_exc()
    else:
        print('not exists query parameter.')

driver.quit()
driver.close()
