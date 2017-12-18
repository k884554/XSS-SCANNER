# XSS-SCANNER
Webアプリケーションのクローリング結果をXSS脆弱性検証するツール。 <br>
機械学習(LSTM)を用いてパラメータの作成を行います。

# Requirement libraries
* requests
* beautifulsoup4
* selenium
* tensorflow
* keras
* numpy

# Operation check environment
* Python 3.6.2
* beautifulsoup4 4.6.0
* selenium 3.5.0
* tensorflow 1.3.0
* keras 2.0.8
* numpy 1.13.3

# Usage
```
# python main.py [ROOT-URL]
```

#### Examples
```
# python main.py http://127.0.0.1:8080/
Using TensorFlow backend.

----- check : http://127.0.0.1:8080/
not exists query parameter.

----- check : http://127.0.0.1:8080/xss/reflect/full1?in=change_me
======== CHECKING STANDARD XSS ========
http://127.0.0.1:8080/xss/reflect/full1?in=ANTI_XSS0
['>', '</h1>', '<h2', '>', '</h2>', '<h3', '>', '</h3>', '<html', '>', '<head', '>', '<title', '>', '</title>', '</head>', '<body', '>', '<br', '>']
></h1><h2></h2><h3></h3><html><head><title></title></head><body><br>"
----- URL     : http://127.0.0.1:8080/xss/reflect/full1?in=ANTI_XSS0
----- SEED    : >,</h1>,<h2,>,</h2>,<h3,>,</h3>,<html,>,<head,>,<title,>,</title>,</head>,<body,>,<br,>
----- PREDS   : lang=target="">
----- PARAM   : lang=target=""><script>alert("IDS");</script>
----- REQ_URL : http://127.0.0.1:8080/xss/reflect/full1?in=lang=target=""><script>alert("IDS");</script>
EXISTS!
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
```

## Author

[Kazushi Nagao](https://github.com/k884554)
