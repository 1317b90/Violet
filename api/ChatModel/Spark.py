import _thread as thread
import base64
import datetime
import hashlib
import hmac
import json
from urllib.parse import urlparse
import ssl
from datetime import datetime
from time import mktime
from urllib.parse import urlencode
from wsgiref.handlers import format_date_time
import websocket  # ！实际是websocket_client库
import time
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
import random

# token-----------------------------------------------------------------------------------------------------------------------------------------------------------

appid = "b9980596"
api_secret = "M2VkNDAyYmUzYzMyODM5OTg4YjJmMmQw"
api_key = "608d8eb3b7c38a3385a46899016205dc"

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------

# 记录模型回答
answer = ""

def create_url(Spark_url):
    # 解析Spark_url
    host = urlparse(Spark_url).netloc
    path = urlparse(Spark_url).path

    # 生成RFC1123格式的时间戳
    now = datetime.now()
    date = format_date_time(mktime(now.timetuple()))

    # 拼接字符串
    signature_origin = "host: " + host + "\n" + "date: " + date + "\n"+"GET " + path + " HTTP/1.1"

    # 进行hmac-sha256进行加密
    signature_sha = hmac.new(api_secret.encode('utf-8'), signature_origin.encode('utf-8'), digestmod=hashlib.sha256).digest()
    signature_sha_base64 = base64.b64encode(signature_sha).decode(encoding='utf-8')

    authorization_origin = f'api_key="{api_key}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature_sha_base64}"'
    authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')

    # 将请求的鉴权参数组合为字典
    v = {
        "authorization": authorization,
        "date": date,
        "host": host
    }

    # 拼接鉴权参数，生成url
    url = Spark_url + '?' + urlencode(v)
    return url

# 获取签名：用于文档对话与上传
def get_signature(timeStamp):
    m2 = hashlib.md5()
    data = bytes(appid + timeStamp, encoding="utf-8")
    m2.update(data)
    signature_origin = m2.hexdigest()
    signature = hmac.new(api_secret.encode('utf-8'), signature_origin.encode('utf-8'),
                         digestmod=hashlib.sha1).digest()
    signature = base64.b64encode(signature).decode(encoding='utf-8')
    return signature

# 获取header：用于文档上传
def get_header():
    timeStamp = str(int(time.time()))
    signature = get_signature(timeStamp)
    header = {
        "appId": appid,
        "timestamp": timeStamp,
        "signature": signature,
    }
    return header

# 创建文档问答的url
def create_doc_url():
    timeStamp = str(int(time.time()))
    originUrl = "wss://chatdoc.xfyun.cn/openapi/chat"
    signature = get_signature(timeStamp)
    url = originUrl + "?" + f'appId={appid}&timestamp={timeStamp}&signature={signature}'
    return url
    # 使用urlencode会导致签名乱码
    # return self.originUrl + "?" + urlencode(header)

# 收到websocket错误的处理
def on_error(ws, error):
    global answer
    answer = f'请求错误: {error}'

# 收到websocket关闭的处理
def on_close(ws, close_status_code, close_msg):
    pass
    # print("### closed ###")
    # print("关闭代码：", close_status_code)
    # print("关闭原因：", close_msg)

# 收到websocket连接建立的处理
def on_open(ws):
    thread.start_new_thread(run, (ws,))

def run(ws, *args):
    data = json.dumps(ws.question)
    ws.send(data)

# 收到websocket消息的处理(doc)
def on_message_doc(ws, message):
    global answer

    data = json.loads(message)
    code = data['code']
    if code != 0:
        answer = f'请求错误: {code}, {data}'
        ws.close()
    else:
        # 在data有content的情况下：
        if data.get("content"):
            content = data["content"]
            status = data["status"]

            answer += content
            if status == 2:
                ws.close()

# 收到websocket消息的处理

def on_message(ws, message):
    global answer

    data = json.loads(message)
    code = data['header']['code']

    if code != 0:
        answer = f'请求错误: {code}, {data}'
        ws.close()
    else:
        choices = data["payload"]["choices"]
        status = choices["status"]
        content = choices["text"][0]["content"]

        # 这里相当于逐步接收AI的消息，然后拼接
        answer += content
        if status == 2:
            ws.close()

# 当输入内容过长，则进行修剪
def checklen(question):
    def getlength(question):
        length = 0
        for content in question:
            temp = content["content"]
            leng = len(temp)
            length += leng
        return length

    while (getlength(question) > 8000):
        del question[0]
    return question

# ---------- 主要功能 ---------- 主要功能---------- 主要功能---------- 主要功能---------- 主要功能---------- 主要功能---------- 主要功能---------- 主要功能

# 单轮对话
def chat(domain, question,temperature,top_k,max_tokens):
    Spark_url = "wss://spark-api.xf-yun.com/v3.5/chat"  # 默认使用Max版本

    if domain == "general": # Lite
        Spark_url = "wss://spark-api.xf-yun.com/v1.1/chat"
    elif domain == "generalv3": # Pro
        Spark_url = "wss://spark-api.xf-yun.com/v3.1/chat"
    elif domain=="generalv3.5":
        pass
    else:
        return "模型版本有误！"

    checklen(question)
    wsUrl = create_url(Spark_url)
    websocket.enableTrace(False)
    ws = websocket.WebSocketApp(wsUrl, on_message=on_message, on_error=on_error, on_close=on_close, on_open=on_open)

    body = {
        "header": {
            "app_id": appid,
            "uid": "1234"
        },
        "parameter": {
            "chat": {
                "domain": domain,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "top_k": top_k,

                "auditing": "default"
            }
        },
        "payload": {
            "message": {
                "text": question
            }
        }
    }
    ws.question = body
    # 初始化
    global answer
    answer = ""
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
    return answer

# 文档对话
def doc_chat(wikiPromptTpl,fileIds,question,wikiFilterScore,temperature,sparkWhenWithoutEmbedding):
    '''
    参数解释：
        - wikiPromptTpl: wiki 大模型问答模板，在某些场景服务默认的 prompt 回答效果不好时，业务可以考虑通过自定义 prompt 来改善。<wikiquestion>替换的问题标识，<wikicontent>替换的文本内容标识
        - wikiFilterScore: wiki 结果分数阈值，低于这个阈值的结果丢弃。取值范围为(0,1] 参考值为：0.80非常宽松 0.82宽松 0.83标准0.84严格 0.86非常严格。
        - temperature: 大模型问答时的温度，取值 0-1，temperature 越大，大模型回答随机度越高
        - sparkWhenWithoutEmbedding: 用户问题未匹配到文档内容时，是否使用大模型兜底回答问题
    '''

    wsUrl=create_doc_url()
    body = {
        "header": {
            "app_id": appid,
            "uid": "1234"
        },
        "chatExtends": {
            "wikiPromptTpl": wikiPromptTpl,
            "wikiFilterScore": wikiFilterScore,
            "temperature": temperature,
            "sparkWhenWithoutEmbedding":sparkWhenWithoutEmbedding
        },
        "fileIds": [
            fileIds
        ],
        "messages": [
            {
                "role": "user",
                "content": question
            }
        ]
    }
    # 禁用WebSocket库的跟踪功能，使其不再输出详细的调试信息。
    websocket.enableTrace(False)
    ws = websocket.WebSocketApp(wsUrl, on_message=on_message_doc, on_error=on_error, on_close=on_close, on_open=on_open)
    ws.appid = appid
    ws.question = body

    # 初始化
    global answer
    answer = ""

    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
    return answer

# 上传文档
def upfile(fileName,files):
    request_url = "https://chatdoc.xfyun.cn/openapi/v1/file/upload"
    headers = get_header()
    body = {
        "url": "",
        "fileName": 'asdasd',
        "fileType": "wiki",
        "needSummary": False,
        "stepByStep": False,
        "callbackUrl": "your_callbackUrl",
    }
    return requests.post(request_url, files=files, data=body, headers=headers)