from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

#======python的函數庫==========
import tempfile, os
import datetime
import openai
import time
import traceback
#======python的函數庫==========

app = Flask(__name__)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
# Channel Access Token
line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))
# Channel Secret
handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))
# OPENAI API Key初始化設定
openai.api_key = os.getenv('OPENAI_API_KEY')


def GPT_response(text):
    # 接收回應
    response = openai.Completion.create(model="gpt-3.5-turbo-instruct", prompt=text, temperature=0.5, max_tokens=500)
    print(response)
    # 重組回應
    answer = response['choices'][0]['text'].replace('。','')
    return answer


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
    msg = event.message.text.lower()  # 将输入文本转换为小写，以便不区分大小写处理
    try:
        if msg == "flex":
            sendFlex(event)  # 注意这里改为正确的函数名称，并传入 event
        else:
            GPT_answer = "OKOK"  # 假设这里是处理其他消息的默认回应
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=GPT_answer))
    except Exception as e:
        print(traceback.format_exc())  # 输出错误堆栈
        error_message = '你所使用的OPENAI API key額度可能已經超過，請於後台Log內確認錯誤訊息'
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=error_message))

def sendFlex(event):  # 彈性配置
    try:
        bubble = BubbleContainer(
            type="carousel",
            contents=[
                {
                    "type": "bubble",
                    "size": "micro",
                    "hero": {
                        "type": "image",
                        "url": "https://scdn.line-apps.com/n/channel_devcenter/img/flexsnapshot/clip/clip10.jpg",
                        "size": "full",
                        "aspectMode": "cover",
                        "aspectRatio": "320:213"
                    },
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {"type": "text", "text": "Brown Cafe", "weight": "bold", "size": "sm", "wrap": true},
                            {
                                "type": "box",
                                "layout": "baseline",
                                "contents": [
                                    {"type": "icon", "size": "xs", "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"},
                                    {"type": "text", "text": "4.0", "size": "xs", "color": "#8c8c8c", "margin": "md", "flex": 0}
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {"type": "text", "text": "東京旅行", "wrap": true, "color": "#8c8c8c", "size": "xs", "flex": 5}
                                ]
                            }
                        ],
                        "spacing": "sm",
                        "paddingAll": "13px"
                    }
                }
                # 添加其他 bubbles
            ]
        )
        message = FlexSendMessage(alt_text="彈性配置範例", contents=bubble)
        line_bot_api.reply_message(event.reply_token, message)
    except Exception as e:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f'發生錯誤！{str(e)}'))

@handler.add(PostbackEvent)
def handle_message(event):
    print(event.postback.data)


@handler.add(MemberJoinedEvent)
def welcome(event):
    uid = event.joined.members[0].user_id
    gid = event.source.group_id
    profile = line_bot_api.get_group_member_profile(gid, uid)
    name = profile.display_name
    message = TextSendMessage(text=f'{name}歡迎加入')
    line_bot_api.reply_message(event.reply_token, message)
        
        
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
