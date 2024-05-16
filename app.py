from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import re
import os
import configparser

app = Flask(__name__)

config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi('8mHVNSHnlj3xx9180Kt+XKh6oVyljAhhV/qOrXL2XXorpdwIO5eard7Jfkvd2wR8P+cEQdUJQ3sEcI0clytSMsoaMH7fQZt4zjHoOUMdJXx9A9fsVr25H6gESwSPYJ3kOe3BF4+4qNnQzZXMVr5tbgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('fe4ffd95d0f99b968144e632168904cc')

line_bot_api.push_message('U9331f84776672cb357b3b8b9f89ebeaf', TextSendMessage(text='You can start !'))

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
 
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
 
    return 'OK'

@handler.add(MessageEvent)
def handle_message(event):
    message = event.message.text
    sendString = ""

    if re.match("提示",message):
        remessage = "觸發驚喜的密語:\n\n恭喜\n今天我生日\n金門大學在哪\n\n試著輸入看看吧!"
        line_bot_api.reply_message(event.reply_token,TextSendMessage(remessage))        

    elif re.match("運勢",message):
        buttons_template_message = TemplateSendMessage(
        alt_text = "運勢",
        template=CarouselTemplate( 
            columns=[ 
                CarouselColumn( 
                    thumbnail_image_url ="https://mednote.files.wordpress.com/2019/10/img_1689.jpg",
                    title = "讓貓貓企鵝小助手\n為你測試運氣吧!", 
                    text ="請選擇一種方法測", 
                    actions =[
                        MessageAction( 
                            label="擲筊",
                            text="擲筊"),
                        MessageAction( 
                            label="抽籤",
                            text="抽籤"),
                        MessageAction( 
                            label="星座",
                            text="星座運勢")
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template_message)

    elif re.match("更多功能",message):
        image_message = ImageSendMessage(
            original_content_url='https://raw.githubusercontent.com/Jung217/Penguin-cat-assistant/main/pic/tired.jpg',
            preview_image_url='https://raw.githubusercontent.com/Jung217/Penguin-cat-assistant/main/pic/tired.jpg'
        )
        line_bot_api.reply_message(event.reply_token, image_message)

    else:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(message))

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)