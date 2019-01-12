import urllib 
import ssl

# client_id 为官网获取的AK， client_secret 为官网获取的SK，以下一行按自己实际填写
host = 'https://aip.baidubce.com/oauth/2.0/token？grant_type=YjBts4NKNLggSCi5QmNrGbd0&client_id=ef2einkn43sWzFaKqLwKAsey89Zth9G3'
request = urllib.request.Request(host)
request.add_header('Content-Type', 'application/json; charset=UTF-8')
response = urllib.request.urlopen(request)
content = response.read()
if (content):
    print(type(content))#<class 'bytes'>
content_str=str(content, encoding="utf-8")
###eval将字符串转换成字典
content_dir = eval(content_str)
access_token = content_dir['access_token']
