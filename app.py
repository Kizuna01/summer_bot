from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage,LocationSendMessage
)
from bs4 import BeautifulSoup
app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('aqDysIcAyl6ZATAJ5kTL1wYcdqdx6Y1aduR8uZpUKc2ICO4tvmSFf7kEDK5ZAhYUCIuaobBgvphm3WMdYJcQy20RiKDpAsjPhzYAxIGKoDkYU8cQI6/xgwVDfbFzWvoYuDNoK7Yg7UKq5II9nyaLowdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('50c17d880561468ada3926c6d1134e44')

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'
def getKey(txt):
    dicts={'閉嘴':'你才閉嘴','噹噹噹':'only you能伴我取西經'}
    return dicts.get(txt,'我天生神力')
def getbike():
    url="https://data.ntpc.gov.tw/api/datasets/71CD1490-A2DF-4198-BEF1-318479775E8A/json?page=0&size=100"
    data=requests.get(url).text
    bike= json.loads(data)
    content=""
    count=0
    for row in bike:
        content +=row['sna']+'-'+row['sbi']+'-'+row['bemp']+'\n'
        count+=1
        if count==15 :
            break
    return content
def news():
    url='https://ctee.com.tw/livenews/aj'
    content=requests.get(url)
    content.encoding='UTF-8'
    content=content.text
    data=BeautifulSoup(content,'html.parser')
    count=0
    item=data.find_all('div',class_='item-content')
    t=[]
    for i in item:
        title=i.find_all('a')[1]
        url=title.get('href')
        title=title.text.strip()
        t.append(title+'\n'+url+'\n')
        count+=1
        if count==5:
            break
    return t
        
status=0

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg=event.message.text
    
    global status
    
    if '指令' == msg:
        message = TextSendMessage(text="/選擇 A B C \n 抽 \n 你家爆炸 \n 大樂透")
   
    #elif '冰' in msg:
    #    message=LocationSendMessage(title='冰',address='台中市火車站前',latitude=24.1379641,longitude=120.6834481)
    elif '/選擇' in msg:
        choice=msg.split(' ')
        x=random.randint(1,len(choice))
        msg='就決定是{}'.format (choice[x])
        message = TextSendMessage(text=msg)
    elif '抽' == msg:
            pretty=['https://ms0728707.000webhostapp.com/summer_img/emaster.jpg',
                    'https://ms0728707.000webhostapp.com/summer_img/one.jpg',
                    'https://ms0728707.000webhostapp.com/summer_img/dead01.jpg',
                    ]
            x=random.randint(0,2)
            imgurl=pretty[x]
            message = ImageSendMessage(original_content_url=imgurl,preview_image_url=imgurl)
  
    elif '你家爆炸' == msg:
        imgurl='https://ms0728707.000webhostapp.com/summer_img/bomb.jpg'#你家爆炸
        message = ImageSendMessage(original_content_url=imgurl,preview_image_url=imgurl)
  
    elif '大樂透' == msg:
        x=random.sample(range(1,49),6)
        y=[]
        for i in x:
             y.append(str(i))
        msg=','.join(y)
        message = TextSendMessage(text=msg)


  #  else:
  #      if status == 2:
  #          msg = queryAir(msg)
  #          status = 0 
  #          message = TextSendMessage(text=msg)


        
           
        

    #else:
     #   message = TextSendMessage(text=msg)
    line_bot_api.reply_message(
            event.reply_token,
            message)

import os
import requests
import json
from air import queryAir,getWeather
import random
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
