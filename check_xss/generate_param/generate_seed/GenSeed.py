from urllib import parse as urlparse
import re
import requests

class gen_seed:
    def __init__(self, str_url):
        self.str_url = str_url
    
    def generate(self):
        
        obj_url = urlparse.urlparse(self.str_url)
        dic_qs = urlparse.parse_qs(obj_url.query)
        
        req = requests.get(self.str_url)
        req_text = re.sub(r'\n', '',req.text)
        edi_text = ""

        for val in dic_qs.values():
            edi_text = re.sub(val[0] + '.*', '<', req_text)
            edi_text = re.sub(r'>.*?<','><',edi_text)
            edi_text = re.sub(r'\".+?\"','\"\"',edi_text)
            edi_text = re.sub(r'<!.*?>','',edi_text)
            edi_text = re.sub(r'.$','',edi_text)
            edi_text = edi_text.lower()

        def cls_tag_edit(edi_text):
            while True:
                try:
                    pos = re.search('</.+?>[^\n]',edi_text).end()

                    lst_text = []

                    for i, char in enumerate(edi_text):
                        if i == pos - 1:
                            lst_text.append("\n")
                            lst_text.append(edi_text[i])
                            i += 1
                        else:
                            lst_text.append(char)

                    edi_text = ""

                    for c in lst_text:
                        edi_text += c

                except:
                    edi_text = edi_text.lower().replace("\n", ",")
                    edi_text = re.sub(r'data-.+?=""', "", edi_text)
                    edi_text = re.sub(r'=', '=,', edi_text)
                    edi_text = re.sub(r'"', ',",', edi_text)
                    edi_text = re.sub(r'>(?!,)', ',>', edi_text)
                    edi_text = re.sub(r'><', ',>,<', edi_text)
                    edi_text = re.sub(r'/>', ',/>,', edi_text)
                    edi_text = re.sub(r',,+', ',', edi_text)
                    edi_text = re.sub(r'\s\s+', ' ', edi_text)
                    edi_text = re.sub(r'\s', ',', edi_text)
                    edi_text = re.sub(r',,+', ',', edi_text)
                    return edi_text

        edi_text = cls_tag_edit(edi_text)
        edi_text = re.sub(r',$','',edi_text)
        lst_chunk = edi_text.split(",")
        lst_pad = "<html,>,<head,>,<title,>,</title>,</head>,<body,>,<h1,id=,\",\",>,</h1>,<h2,>,</h2>,<h3,>,</h3>".split(",")
        seed = ""
        
        if len(lst_chunk) >= 20:
            for p in range(len(lst_chunk) - 20,len(lst_chunk), 1):
                seed += (lst_chunk[p])
                if p < len(lst_chunk) - 1:
                    seed += ","
        else:
            if "" not in lst_chunk:
                lst_chunk = lst_pad + lst_chunk
            else:
                lst_chunk = lst_pad
            for p in range(len(lst_chunk) - 20,len(lst_chunk), 1):
                seed += (lst_chunk[p])
                if p < len(lst_chunk) - 1:
                    seed += ","

#        seed = ""
#        for p in range(len(lst_chunk) - 20,len(lst_chunk), 1):
#            seed += (lst_chunk[p])
#            if p < len(lst_chunk) - 1:
#                seed += ","
        
        #seed = re.sub(r',$','',seed)
        return seed