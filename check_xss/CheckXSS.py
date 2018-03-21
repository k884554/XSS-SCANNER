from urllib import parse
import sys
sys.path.append("./check_xss/generate_param/")
from GenParam import gen_param
from selenium.webdriver.common.alert import Alert
import re

def check_xss(url, driver):
    def check(url, driver, double_encoding=False, response_splitting=False):
        obj_url = parse.urlparse(url)
        dic_qs = parse.parse_qs(obj_url.query)

        for _, key in enumerate(dic_qs.keys()):
            if _ == 0:
                p = "\?"+key+"="+dic_qs[key][0]
                rp = "?"+key+"=ANTI_XSS"+str(_)
                print(re.sub(p, rp, url))
                G = gen_param(re.sub(p, rp, url))
                param = G.generate()
                if double_encoding == True:
                    param = parse.quote(parse.quote(param))
                if response_splitting == True:
                    param = "%0d%0a%0d%0a" + parse.quote(param)
                print("----- PARAM   : " + param)
                req_url = re.sub("ANTI_XSS"+str(_), param, re.sub(p, rp, url))
            else:
                p = "\&"+key+"="+dic_qs[key][0]
                rp = "&"+key+"=ANTI_XSS"+str(_)
                req_urls.append(re.sub(p, rp, url))
                param = G.generate()
                print("----- PARAM   : " + param)
                req_url = re.sub("ANTI_XSS"+str(_), param, re.sub(p, rp, url))
            print("----- REQ_URL : " + req_url)
            driver.get(req_url)
            Alert(driver).accept()

    try:
        print('======== CHECKING STANDARD XSS ========')
        check(url, driver)
        print("EXISTS!")
    except Exception as e:
        # print('=== エラー内容 ===')
        # print('type:' + str(type(e)))
        # print('args:' + str(e.args))
        # print('message:' + e.message)
        # print('e自身:' + str(e))
        try:
            print('==== CHECKING DOUBLE-ENCODING XSS ====')
            check(url, driver, double_encoding=True)
            print("EXISTS!")
        except Exception as e:
            # print('=== エラー内容 ===')
            # print('type:' + str(type(e)))
            # print('args:' + str(e.args))
            # print('message:' + e.message)
            # print('e自身:' + str(e))
            try:
                print('==== CHECKING RESPONSE-SPLITTING XSS ====')
                check(url, driver, response_splitting=True)
                print("EXISTS!")
            except:
                print("NOT EXIST.")
