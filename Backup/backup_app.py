from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import re
import os
import configparser
from groq import Groq
from dotenv import load_dotenv

app = Flask(__name__)

config = configparser.ConfigParser()
config.read('config.ini')
load_dotenv()

line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None))
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET', None))

line_bot_api.push_message(os.getenv('DEV_UID', None), TextSendMessage(text='You can start !'))

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

Lmodel = os.getenv('MMODEL', None)

@handler.add(MessageEvent)
def handle_message(event):
    message = event.message.text
    
    if re.match("提示",message):
        remessage = "預設使用繁體中文回答\n太久未啟動需先喚醒。\n輸入'模型'可以更換模型\n\n如果我開始瘋狂說英文\n請對我說'Speak Chinese'\n\nThank you  :)"
        line_bot_api.reply_message(event.reply_token,TextSendMessage(remessage))        
    
    elif re.match("模型",message):
        buttons_template_message = TemplateSendMessage(
        alt_text = "模型",
        template=CarouselTemplate( 
            columns=[ 
                CarouselColumn( 
                    thumbnail_image_url ="https://raw.githubusercontent.com/Jung217/groq_line_bot/main/pic/_5523b2f6-6e5c-4535-a110-5dc2f6a173eb.jpg",
                    title = "更換模型", 
                    text ="請選擇一種 Model", 
                    actions =[
                        MessageAction( 
                            label="Gemma 7b",
                            text="gemma-7b-it"),
                        MessageAction( 
                            label="LLaMA3 70b",
                            text="llama3-70b-8192"),
                        MessageAction( 
                            label="Mixtral 8x7b",
                            text="mixtral-8x7b-32768")
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template_message)

    elif re.match("gemma-7b-it",message) or re.match("llama3-8b-8192",message) or re.match("llama3-70b-8192",message) or re.match("mixtral-8x7b-32768",message):
        line_bot_api.reply_message(event.reply_token, TextSendMessage("Model changed."))
    else:
        client = Groq(
            api_key="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",
        )

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": message + "，用繁體中文回答",
                }
            ],
            model=Lmodel,
        )  
        line_bot_api.reply_message(event.reply_token,TextSendMessage(chat_completion.choices[0].message.content))

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)