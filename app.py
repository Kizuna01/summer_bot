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
line_bot_api = LineBotApi('c6B7ydATJ4VZoSSIGeMXqEo5/xjnN7c7X0daq6dKx1kk9cRs/76N7ERytVkFoxiG3iwnbmYTG8+lnIGTD/f3AJGl5A0m64o/V4mfY2Pm2ASvHdCBDAvEW22aey5yh7zA7b76CD2l6w6MIaHePqqrhAdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('05cdeab692a18663ecfcf7834f124d15')

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
    
    if '自行車' in msg:
        msg=getbike()
        message = TextSendMessage(text=msg)
    elif '空氣' in msg:
        status=2
        msg = '請輸入地區'
        message = TextSendMessage(text=msg)
    elif '便當' in msg :
        foodout=[]
        food=['https://dogbaby2266.com/wp-content/uploads/2021/08/Miss-Energy-%E8%83%BD%E9%87%8F%E5%B0%8F%E5%A7%90-%E7%9B%B4%E7%87%9F%E8%8F%9C%E5%96%AE-min.jpg',#能量小姐
             'https://cdn.ftvnews.com.tw/summernotefiles/News/fd7369ff-a327-4405-8f73-1b27587453e4.jpg']#池上木盒
        for i in food:
            foodout.append(ImageSendMessage(original_content_url=i,preview_image_url=i))
        line_bot_api.reply_message(event.reply_token,foodout)
    elif '冰' in msg:
        message=LocationSendMessage(title='冰',address='台中市火車站前',latitude=24.1379641,longitude=120.6834481)
    elif '選擇' in msg:
        choice=msg.split(' ')
        x=random.randint(1,len(choice))
        msg='就決定是{}'.format (choice[x])
        message = TextSendMessage(text=msg)
    elif '熱量小幫手' in msg:
        msg='火鍋 早餐 便當 水果 \n subway 壽司 夜市 中式'
        message = TextSendMessage(text=msg)
    elif '抽' in msg:
            pretty=['https://cdn2.ettoday.net/images/2284/d2284228.jpg','https://img.news.ebc.net.tw/EbcNews/news/2019/11/20/1574269536_70403.jpg',
                    'https://farm8.staticflickr.com/7628/26916596801_f5a173caf0_c.jpg','https://img.ltn.com.tw/Upload/ent/page/800/2019/05/04/phpoAVxhH.jpg',
                    'https://img.mm52.com/r/rei_mizuna/rei_mizuna.jpg','https://pic.pimg.tw/a9431084/1390968127-3923862254_m.jpg',
                    'https://i.imgur.com/bs32YyV.jpg','https://assets.juksy.com/files/articles/100198/800x_100_w-5eabfd75aa28c.jpg',
                    'https://jdailyhk.com/wp-content/uploads/2017/01/I%E7%B4%9A-%E5%A4%A9%E6%9C%A8%E7%B4%949.jpg','https://i.ytimg.com/vi/SGwpQisyuug/hqdefault.jpg',
                    'https://images.chinatimes.com/newsphoto/2019-11-08/656/20191108001309.jpg','https://www.mirrormedia.com.tw/assets/images/20190409181552-a894917e1274b52732dc47323463a404-tablet.jpg',
                    'https://pic.pimg.tw/valiant/1555082154-3773155441_n.jpg','https://cdn2.ettoday.net/images/2284/d2284231.jpg',
                    'https://www.popo8.com/host/data/202102/16/9/p1613491138_27600.jpg_b.jpg','https://pbs.twimg.com/media/EhF-Pu1UwAEN-T2.jpg',
                    'https://i.imgur.com/9KKBNbN.jpg','https://assets.juksy.com/files/articles/80262/800x_100_w-5b446006baaca.jpg',
                    'https://i.pinimg.com/1200x/cd/08/2d/cd082d126d0f8824511105fab7bf4e95.jpg','https://www.mymypic.net/data/attachment/forum/202004/17/004947y2kdd88hyaea81s8.jpg',
                    'https://farm8.staticflickr.com/7524/26916597141_99ebaf0f2d.jpg','https://i.pinimg.com/originals/7f/0b/a7/7f0ba7e6d95075d33dcd7db320c971dc.jpg',
                    'https://pbs.twimg.com/media/EWIy7B2UcAADFAG.jpg','https://upload.cc/i1/2020/08/13/KfBQRY.jpg']
            x=random.randint(0,24)
            imgurl=pretty[x]
            message = ImageSendMessage(original_content_url=imgurl,preview_image_url=imgurl)
    elif '復仇者' in msg:
            avengers=['https://assets.juksy.com/files/articles/48057/800x_100_w-567a8ea3be9d0.jpg','https://img.ltn.com.tw/Upload/ent/page/800/2017/07/11/phpBls3Lw.jpg',
                    'https://images.chinatimes.com/newsphoto/2020-05-22/656/20200522001767.jpg','https://img.ltn.com.tw/Upload/ent/page/800/2017/07/31/phpaOdu0d.png',
                    'https://static.ettoday.net/images/3500/d3500323.jpg','https://assets.juksy.com/files/articles/89548/800x_100_w-5cb3ead749441.jpg',
                    'https://img.cinemablend.com/quill/0/0/5/e/4/1/005e41d016dfd922285dbd3bec4937aa416949ba.jpg','https://www.teepr.com/wp-content/uploads/2020/07/20190526132405_85.jpg',
                    'https://images.chinatimes.com/newsphoto/2020-07-15/656/20200715004880.jpg','https://img.ttshow.tw/images/media/frontcover/2020/08/20/004_hxtbiob.jpg',
                    'https://attach.setn.com/newsimages/2021/03/27/3085088-PH.jpg','https://news.agentm.tw/wp-content/uploads/black-widow-movie_1515653087555-768x480-1.jpg',
                    'https://inmywordz.com/wp-content/uploads/20180504163013_39.jpg','https://hk.ulifestyle.com.hk/cms/images/topic/1024x576/201907/20190731145218_0_maxresdefault.jpg',
                    'https://media.gq.com.tw/photos/604733815c98c68ff6ed0acc/master/pass/scarlet-witch-wandavision.png','https://www.teepr.com/wp-content/uploads/2019/12/https___hk.hypebeast.com_files_2018_05_elizabeth-olsen-want-avengers-costume-cover-cleavage-00-1.jpg',
                    'https://news.agentm.tw/wp-content/uploads/thanos-snap-on-earth.jpg','https://i.beauty321.com/816x/https://il.beauty321.com/gallery/albums_photo/10963-201905101552462906.jpg',
                    'https://www.teepr.com/wp-content/uploads/2019/05/%E7%BE%8E%E9%9A%8A%E7%9B%BE%E7%89%8CA.jpg','https://news.agentm.tw/wp-content/uploads/Thanos-hot-toy-cover.png',
                    'https://cdn2.ettoday.net/images/4043/d4043686.jpg','https://news.agentm.tw/wp-content/uploads/000-7.png',
                    'https://media.altpress.com/uploads/2020/09/Captain-America-Avengers-Endgame-min.jpg','https://cdn2.ettoday.net/images/3342/d3342642.jpg',
                    'https://news.agentm.tw/wp-content/uploads/4711921-untitled-1.jpg','https://news.agentm.tw/wp-content/uploads/67584235_2277918025597263_91842927822635008_n-%E6%8B%B7%E8%B2%9D-750x422.jpg',
                    'https://news.agentm.tw/wp-content/uploads/2017/10/Valkyrie-Ragnarok-Thor-1-1024x576.png','http://i1.hdslb.com/bfs/archive/e27158543580bc761b949cc25dd7df8937420ea5.jpg',
                    ]
            y=random.randint(0,29)
            imgurl=avengers[y]
            message = ImageSendMessage(original_content_url=imgurl,preview_image_url=imgurl)
    elif '水果' in msg:
        imgurl='https://www.healingdaily.com.tw/media/images/2020/11/124820476_3673846755999006_3499646163171754703_o_1605157386.jpg'#水果
        message = ImageSendMessage(original_content_url=imgurl,preview_image_url=imgurl)
    elif '夜市' in msg:
        imgurl='https://www.healingdaily.com.tw/media/images/2020/11/125507161_3685291601521188_119112334151225852_o_0_1606183965.jpg'#夜市
        message = ImageSendMessage(original_content_url=imgurl,preview_image_url=imgurl)
    elif '壽司' in msg:
        foodout=[]
        food=['https://img.ltn.com.tw/Upload/health/page/800/2021/08/24/phpH4bbQ1.jpg',#建議
            'https://img.nutruelifegood.com/2021/03/1615964325-303941d08cfb8e7d20fd4b9f3c9159f8.jpg',#爭鮮
             'https://pic.pimg.tw/drremin/1622165317-1690185448-g_l.jpg',#壽司郎
             ]
        for i in food:
            foodout.append(ImageSendMessage(original_content_url=i,preview_image_url=i))
        line_bot_api.reply_message(event.reply_token,foodout)
    elif '火鍋' in msg:
        foodout=[]
        food=['https://images.chinatimes.com/newsphoto/2021-02-21/656/20210221003719.jpg',#全圖
            'https://www.healingdaily.com.tw/media/images/2020/11/116935185_3393507374032947_1204503926942113906_o_1604920981.jpg',#湯底
             'https://www.healingdaily.com.tw/media/images/2020/11/117367709_3393507187366299_7475865154440236430_o_1604920963.jpg',#火鍋料
             'https://pic.pimg.tw/drremin/1624584009-808633920-g_l.png',#肉
             'https://www.healingdaily.com.tw/media/images/2020/11/117326914_3393507254032959_4393351299018645612_o_1605001202.jpg',#醬料
             ]
        for i in food:
            foodout.append(ImageSendMessage(original_content_url=i,preview_image_url=i))
        line_bot_api.reply_message(event.reply_token,foodout)
        
    elif '早餐' in msg:
        foodout=[]
        food=['https://cdn2.ettoday.net/images/5133/5133040.jpg',#早餐吐司
             'https://news.cts.com.tw/photo/cts/202011/202011262021924_l.jpg',#果醬吐司
             'https://tw.maminews.com/img/articles/2020/10/500x320_1602125897ae.jpg',#早餐漢堡
             'https://www.kingnet.com.tw/uploadFile/202101/1611740293-1317296updateNew1.jpeg',#早餐蛋餅
             'https://www.kingnet.com.tw/uploadFile/202101/1611740642-1307644updateNew2.jpeg',#早餐點心
             ]
             #'https://img.ltn.com.tw/Upload/health/page/800/2021/03/29/phpcVDoDl.jpg'#中式早餐
             
        for i in food:
            foodout.append(ImageSendMessage(original_content_url=i,preview_image_url=i))
        line_bot_api.reply_message(event.reply_token,foodout)
        #line_bot_api.reply_message(event.reply_token,[ImageSendMessage(original_content_url='https://cdn2.ettoday.net/images/5133/5133040.jpg',preview_image_url='https://cdn2.ettoday.net/images/5133/5133040.jpg'),
        #                                              ImageSendMessage(original_content_url='https://news.cts.com.tw/photo/cts/202011/202011262021924_l.jpg',preview_image_url='https://news.cts.com.tw/photo/cts/202011/202011262021924_l.jpg')])
        
    elif '中式' in msg:
        foodout=[]
        food=['https://img.ltn.com.tw/Upload/health/page/800/2021/03/29/phpcVDoDl.jpg',#中式早餐
             'https://cdn2.ettoday.net/images/5797/5797653.jpg',#麵食
             'https://cdn2.ettoday.net/images/5567/5567264.jpg',#國民美食
             'https://attach.setn.com/newsimages/2021/10/19/3368620-PH.jpg',#麵
             ]

             
        for i in food:
            foodout.append(ImageSendMessage(original_content_url=i,preview_image_url=i))
        line_bot_api.reply_message(event.reply_token,foodout)
    
    elif 'subway' in msg:
        foodout=[]
        food=['https://resource01-proxy.ulifestyle.com.hk/res/v3/image/content/2575000/2578744/bbbb_600.png',
             'https://i.pinimg.com/736x/24/1e/62/241e625de39b2d471f3cd6e8faf7892d.jpg']#醬
        for i in food:
            foodout.append(ImageSendMessage(original_content_url=i,preview_image_url=i))
        line_bot_api.reply_message(event.reply_token,foodout)
    
    elif '吃什麼' in msg:
         food=['https://cc.tvbs.com.tw/img/program/upload/2020/09/09/20200909204016-7fb822c3.jpg',
                   'https://storage.googleapis.com/www-cw-com-tw/article/202101/article-5ff76e12dff12.jpg',
                   'https://tw.savorjapan.com/gg/content_image/t0268_001.jpg',
                   'https://www.citylink.tw/songshan/wp-content/uploads/M720.jpg',
                   'https://foodtracer.taipei.gov.tw/Backend/upload//company/23309178/05da95d3-8373-4e74-b0c0-546977044f87.jpg',
                   'https://findlife.com.tw/menu/blog/wp-content/uploads/2020/06/4.jpg',
                   'https://snoopyblog.com/wp-content/uploads/2017/10/1509377834-3c81354d34ea77879a0733f3dfd63481.jpg']
         x=random.randint(0,6)
         imgurl=food[x]
         message = ImageSendMessage(original_content_url=imgurl,preview_image_url=imgurl)
    elif '常威' in msg :
        msg='我天生神力'
        message = TextSendMessage(text=msg)
    elif '大樂透' in msg:
        x=random.sample(range(1,49),6)
        y=[]
        for i in x:
             y.append(str(i))
        msg=','.join(y)
        message = TextSendMessage(text=msg)
    elif '新聞' in msg:
        new=[]
        for i in news():
            new.append(TextSendMessage(text=i))
        line_bot_api.reply_message(event.reply_token,new)

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