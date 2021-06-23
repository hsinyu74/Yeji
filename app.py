from flask import Flask, request, abort

from translate import Translator

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *


app = Flask(__name__)
#translator = Translator (from_lang='zh-Hant', to_lang='en')

lang='en'

# Channel Access Token
line_bot_api = LineBotApi('UixFncuOGHnCLGppaaAfAw+iyhCZsBAIu7FOAY2yMdsPTVQSK+kMrN7wNiBSZnIgKsgocsG6Z+ez4AlpIbxi/X1WdorF40OeB+zdkBf3RGzfSnJ+1qXb268NytL2J4yBV1h5IacPEm1rlpNESmFE5QdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('93ee5830c1026467b3a3a46f6f228118')

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

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global lang
    if event.message.text == "中翻英":
        msg = TextSendMessage(text = '語言設定為英文') 
        lang = 'en'
    elif event.message.text == "中翻日":
        msg =  TextSendMessage(text = '語言設定為日文')
        lang='ja'
    elif event.message.text == "圖片秀":
        msg =  image_carousel_message1() 
    else:
        translator = Translator (from_lang='zh-Hant', to_lang=lang)
        msg =  TextSendMessage(text = translator.translate(event.message.text))     
    line_bot_api.reply_message(event.reply_token, msg)


def image_carousel_message1():
    message = TemplateSendMessage(
        alt_text='圖片旋轉木馬',
        template=ImageCarouselTemplate(
            columns=[
                ImageCarouselColumn(
                    image_url="https://scontent.fkhh1-2.fna.fbcdn.net/v/t1.6435-9/c550.0.960.960a/s851x315/198788323_1863295620518459_5430969629091532543_n.jpg?_nc_cat=108&ccb=1-3&_nc_sid=da31f3&_nc_ohc=pYjvYmDNR5QAX-cyJ7j&_nc_ht=scontent.fkhh1-2.fna&tp=28&oh=1f0db722cdc2e5342296b56315658a79&oe=60D6B5C6",
                    action=URITemplateAction(
                        label="itzy-1",
                        uri="https://scontent.fkhh1-2.fna.fbcdn.net/v/t1.6435-9/c550.0.960.960a/s851x315/198788323_1863295620518459_5430969629091532543_n.jpg?_nc_cat=108&ccb=1-3&_nc_sid=da31f3&_nc_ohc=pYjvYmDNR5QAX-cyJ7j&_nc_ht=scontent.fkhh1-2.fna&tp=28&oh=1f0db722cdc2e5342296b56315658a79&oe=60D6B5C6"
                    )
                ),
                ImageCarouselColumn(
                    image_url="https://scontent.fkhh1-1.fna.fbcdn.net/v/t1.6435-9/c0.0.1080.1080a/s851x315/204849963_1863295607185127_1565262460705902606_n.jpg?_nc_cat=106&ccb=1-3&_nc_sid=da31f3&_nc_ohc=CYN4W4288n8AX9wE9xZ&tn=1-Z280gLE5GPBuxs&_nc_ht=scontent.fkhh1-1.fna&tp=28&oh=da5c033fba3c0402b1da2e4c5f927dff&oe=60D6DA4B",
                    action=URITemplateAction(
                        label="itzy-2",
                        uri="https://scontent.fkhh1-1.fna.fbcdn.net/v/t1.6435-9/c0.0.1080.1080a/s851x315/204849963_1863295607185127_1565262460705902606_n.jpg?_nc_cat=106&ccb=1-3&_nc_sid=da31f3&_nc_ohc=CYN4W4288n8AX9wE9xZ&tn=1-Z280gLE5GPBuxs&_nc_ht=scontent.fkhh1-1.fna&tp=28&oh=da5c033fba3c0402b1da2e4c5f927dff&oe=60D6DA4B"
                    )
                ),
                
                ImageCarouselColumn(
                    image_url="https://scontent.fkhh1-2.fna.fbcdn.net/v/t1.6435-9/c81.0.423.423a/s851x315/202576973_1863295573851797_1183309706691661445_n.jpg?_nc_cat=104&ccb=1-3&_nc_sid=da31f3&_nc_ohc=TX_8UKIYs9wAX_NUvsV&tn=1-Z280gLE5GPBuxs&_nc_ht=scontent.fkhh1-2.fna&tp=28&oh=509cac6b6830bf8cdf7c549bf9703e23&oe=60D85E45",
                    action=URITemplateAction(
                        label="itzy-3",
                        uri="https://scontent.fkhh1-2.fna.fbcdn.net/v/t1.6435-9/c81.0.423.423a/s851x315/202576973_1863295573851797_1183309706691661445_n.jpg?_nc_cat=104&ccb=1-3&_nc_sid=da31f3&_nc_ohc=TX_8UKIYs9wAX_NUvsV&tn=1-Z280gLE5GPBuxs&_nc_ht=scontent.fkhh1-2.fna&tp=28&oh=509cac6b6830bf8cdf7c549bf9703e23&oe=60D85E45"
                    )
                )
            ]
        )
    )
    return message

# requirements.txt 中要加入 translate , 也就是要 pip install traslate
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    