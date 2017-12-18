import sys
sys.path.append("/Users/NAGAO/antixss/prototype/predict/")
sys.path.append("/Users/NAGAO/antixss/prototype/generate_seed/")
from predict_without_space import predict_wos
from GenSeed import gen_seed

class gen_param:
    def __init__(self, str_url):
        self.rxss = "<script>alert(\"IDS\");</script>"
        self.str_url = str_url
    def generate(self):
        G = gen_seed(self.str_url)
        seed = G.generate()
        P = predict_wos(seed)
        pred = P.predict()
        
        print("----- URL     : " + self.str_url)
        print("----- SEED    : " + seed)
        print("----- PREDS   : " + pred)

        param = pred + self.rxss
        
        return param