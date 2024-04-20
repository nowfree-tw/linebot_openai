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
    
    '''
    print("Handle: reply_token: " + event.reply_token + ", message: " + event.message.text)
    content = "{},{},{}".format(event.message.text,event.message.text,event.message.text)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=content))
    '''
    msg = event.message.text.lower()  # 将输入文本转换为小写，以便不区分大小写处理
    print (msg)
    try:
        if msg == "病重即將去世，希望能離院回家度過最後時光":
            sendFlex1(event)  # 注意这里改为正确的函数名称，并传入 event
        elif msg == "到了生命末期，想在家安祥度過生命的最後階段":
            sendFlex3(event)  # 注意这里改为正确的函数名称，并传入 event
        elif msg == "家人死亡後，悲傷情緒難以平復":
            #sendFlex4(event)  # 注意这里改为正确的函数名称，并传入 event
            pass
        elif msg == "感到日漸衰老，想開始安排安寧的晚年":
            premsg="生死是人生需要面對的最後一關，預作準備才能從容面對。你可能需要先思考下列問題。"
            sendFlex2(event,premsg)  # 注意这里改为正确的函数名称，并传入 event
#
#            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=premsg))
 #           sendFlex3(event)  # 注意这里改为正确的函数名称，并传入 event
            #sendFlex2(event)  # 注意这里改为正确的函数名称，并传入 event
            pass
        else:
            GPT_answer = "你提到了:"+msg  # 假设这里是处理其他消息的默认回应
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=GPT_answer))
    except Exception as e:
        print("error:",e)  # 输出错误堆栈
        error_message = '你所使用的OPENAI API key額度可能已經超過，請於後台Log內確認錯誤訊息'
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=error_message))


#Flex Message Area

def sendFlex1(event):  #彈性配置

    try:
        trycontent={
  "type": "carousel",
  "contents": [
    {
      "type": "bubble",
      "size": "giga",
      "hero": {
        "type": "image",
        "url": "https://i.imgur.com/VEdIQdA.jpeg",
        "size": "full",
        "aspectMode": "cover",
        "aspectRatio": "320:213"
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "克服家中環境的阻礙\n讓病人順利回到自宅房間",
            "weight": "bold",
            "size": "xl",
            "wrap": true,
            "align": "center"
          },
          {
            "type": "filler"
          }
        ],
        "spacing": "sm",
        "paddingAll": "13px"
      },
      "footer": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "臨終回家",
            "align": "end"
          }
        ]
      }
    },
    {
      "type": "bubble",
      "size": "giga",
      "hero": {
        "type": "image",
        "url": "https://i.imgur.com/4J5hfvg.jpeg",
        "size": "full",
        "aspectMode": "cover",
        "aspectRatio": "320:213"
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "\n如何取得死亡證明書",
            "weight": "bold",
            "size": "xl",
            "wrap": true,
            "align": "center"
          }
        ],
        "spacing": "sm",
        "paddingAll": "13px"
      },
      "footer": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "臨終回家",
            "align": "end"
          }
        ]
      }
    },
    {
      "type": "bubble",
      "size": "giga",
      "hero": {
        "type": "image",
        "url": "https://i.imgur.com/TSTRT8T.jpeg",
        "size": "full",
        "aspectMode": "cover",
        "aspectRatio": "320:213"
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "移除病患身上留存管路\n(點滴、鼻管、尿管)",
            "weight": "bold",
            "size": "xl",
            "wrap": true,
            "align": "center"
          }
        ],
        "spacing": "sm",
        "paddingAll": "13px"
      },
      "footer": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "臨終回家",
            "align": "end"
          }
        ]
      }
    },
    {
      "type": "bubble",
      "size": "giga",
      "hero": {
        "type": "image",
        "size": "full",
        "aspectMode": "cover",
        "aspectRatio": "320:213",
        "url": "https://i.imgur.com/QUMR9G4.jpeg"
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "死亡之後\n如何進行大體清潔",
            "weight": "bold",
            "size": "xl",
            "wrap": true,
            "align": "center"
          }
        ],
        "spacing": "sm",
        "paddingAll": "13px"
      },
      "footer": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "臨終回家",
            "align": "end"
          }
        ]
      }
    },
    {
      "type": "bubble",
      "size": "giga",
      "hero": {
        "type": "image",
        "url": "https://i.imgur.com/ekpuUiQ.jpeg",
        "size": "full",
        "aspectMode": "cover",
        "aspectRatio": "320:213"
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "在死亡之前\n哪裡可以短期租借氧氣機",
            "weight": "bold",
            "size": "xl",
            "wrap": true,
            "align": "center"
          }
        ],
        "spacing": "sm",
        "paddingAll": "13px"
      },
      "footer": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "臨終回家",
            "align": "end"
          }
        ]
      }
    }
  ]
}
        message = FlexSendMessage(alt_text="臨終回家", contents=trycontent)
        line_bot_api.reply_message(event.reply_token,message)
    except Exception as e:
        print("error:",e)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤！'))

def sendFlex3(event,*args):  #彈性配置
    try:
        trycontent={
  "type": "carousel",
  "contents": [
    {
      "type": "bubble",
      "size": "giga",
      "hero": {
        "type": "image",
        "url": "https://i.imgur.com/F3ftAED.jpg",
        "size": "full",
        "aspectMode": "cover",
        "aspectRatio": "320:213"
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "安寧照護和長期照護有何不同?",
            "weight": "bold",
            "size": "xl",
            "wrap": true
          },
          {
            "type": "filler"
          }
        ],
        "spacing": "sm",
        "paddingAll": "13px"
      },
      "footer": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "居家安寧",
            "align": "end"
          }
        ]
      }
    },
    {
      "type": "bubble",
      "size": "giga",
      "hero": {
        "type": "image",
        "url": "https://i.imgur.com/Iz0v6dJ.jpeg",
        "size": "full",
        "aspectMode": "cover",
        "aspectRatio": "320:213"
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "哪些單位可以提供社區居家安寧服務?",
            "weight": "bold",
            "size": "xl",
            "wrap": true
          }
        ],
        "spacing": "sm",
        "paddingAll": "13px"
      },
      "footer": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "居家安寧",
            "align": "end"
          }
        ]
      }
    },
    {
      "type": "bubble",
      "size": "giga",
      "hero": {
        "type": "image",
        "url": "https://i.imgur.com/1Yc3pHE.jpeg",
        "size": "full",
        "aspectMode": "cover",
        "aspectRatio": "320:213"
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "如何申請社區居家安寧服務?",
            "weight": "bold",
            "size": "xl",
            "wrap": true
          }
        ],
        "spacing": "sm",
        "paddingAll": "13px"
      },
      "footer": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "居家安寧",
            "align": "end"
          }
        ]
      }
    },
    {
      "type": "bubble",
      "size": "giga",
      "hero": {
        "type": "image",
        "size": "full",
        "aspectMode": "cover",
        "aspectRatio": "320:213",
        "url": "https://i.imgur.com/nfaFYD8.jpeg"
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "哪些狀況可以在家住院，並獲得必要之醫療照護",
            "weight": "bold",
            "size": "xl",
            "wrap": true
          }
        ],
        "spacing": "sm",
        "paddingAll": "13px"
      },
      "footer": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "居家安寧",
            "align": "end"
          }
        ]
      }
    },
    {
      "type": "bubble",
      "size": "giga",
      "hero": {
        "type": "image",
        "url": "https://i.imgur.com/SnaLNVU.jpegf7906f5a2",
        "size": "full",
        "aspectMode": "cover",
        "aspectRatio": "320:213"
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "什麼是靈性的需求?",
            "weight": "bold",
            "size": "xl",
            "wrap": true
          }
        ],
        "spacing": "sm",
        "paddingAll": "13px"
      },
      "footer": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "居家安寧",
            "align": "end"
          }
        ]
      }
    },
    {
      "type": "bubble",
      "size": "giga",
      "hero": {
        "type": "image",
        "size": "full",
        "aspectMode": "cover",
        "aspectRatio": "320:213",
        "url": "https://i.imgur.com/d6C5t7X.jpeg"
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "如何讓自己及家屬面對死亡?",
            "weight": "bold",
            "size": "xl",
            "wrap": true
          }
        ],
        "spacing": "sm",
        "paddingAll": "13px"
      },
      "footer": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "居家安寧",
            "align": "end"
          }
        ]
      }
    }
  ]
}
        flex_message = FlexSendMessage(alt_text="居家安寧", contents=trycontent)
        
        # 需要準備發送的消息列表
        messages = list()    # 將 args 轉換成列表  #修改處
        for i in args:
            messages.append(TextSendMessage(text=i))
        messages.append(flex_message)  # 將 Flex Message 添加到列表中  #修改處

        # 使用 reply_message 發送一個消息列表
        line_bot_api.reply_message(event.reply_token, messages)  #修改處

    except Exception as e:
        print("error:", e)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤！'))

def sendFlex2(event,*args):  #彈性配置
    try:
        trycontent={
  "type": "carousel",
  "contents": [
    {
      "type": "bubble",
      "size": "giga",
      "hero": {
        "type": "image",
        "url": "https://i.imgur.com/EqQFaC9.jpeg",
        "size": "full",
        "aspectMode": "cover",
        "aspectRatio": "320:213"
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "否決插管、壓胸、電擊\n如何辦理預立醫囑？",
            "weight": "bold",
            "size": "xl",
            "wrap": true,
            "align": "center"
          },
          {
            "type": "filler"
          }
        ],
        "spacing": "sm",
        "paddingAll": "13px"
      },
      "footer": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "晚年生命自主",
            "align": "end"
          }
        ]
      }
    },
    {
      "type": "bubble",
      "size": "giga",
      "hero": {
        "type": "image",
        "url": "https://i.imgur.com/EfFam6e.jpeg",
        "size": "full",
        "aspectMode": "cover",
        "aspectRatio": "320:213"
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "末期判定有什麼條件？\n如何申請？\n健保有何資源？",
            "weight": "bold",
            "size": "xl",
            "wrap": true,
            "align": "center"
          }
        ],
        "spacing": "sm",
        "paddingAll": "13px"
      },
      "footer": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "晚年生命自主",
            "align": "end"
          }
        ]
      }
    },
    {
      "type": "bubble",
      "size": "giga",
      "hero": {
        "type": "image",
        "url": "https://i.imgur.com/P9cWpFB.jpeg",
        "size": "full",
        "aspectMode": "cover",
        "aspectRatio": "320:213"
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "誰能符合長照資格?\n如何申請長照?\n有什麼長照資源？",
            "weight": "bold",
            "size": "xl",
            "wrap": true,
            "align": "center"
          }
        ],
        "spacing": "sm",
        "paddingAll": "13px"
      },
      "footer": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "晚年生命自主",
            "align": "end"
          }
        ]
      }
    },
    {
      "type": "bubble",
      "size": "giga",
      "hero": {
        "type": "image",
        "size": "full",
        "aspectMode": "cover",
        "aspectRatio": "320:213",
        "url": "https://i.imgur.com/mexcUcT.jpeg"
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "新竹市居家安寧服務單位?\n如何申請?",
            "weight": "bold",
            "size": "xl",
            "wrap": true,
            "align": "center"
          }
        ],
        "spacing": "sm",
        "paddingAll": "13px"
      },
      "footer": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "晚年生命自主",
            "align": "end"
          }
        ]
      }
    },
    {
      "type": "bubble",
      "size": "giga",
      "hero": {
        "type": "image",
        "url": "https://i.imgur.com/OMHbAmk.jpeg",
        "size": "full",
        "aspectMode": "cover",
        "aspectRatio": "320:213"
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "想自費提高晚年生活品質\n有哪些項目可以申請?",
            "weight": "bold",
            "size": "xl",
            "wrap": true,
            "align": "center"
          }
        ],
        "spacing": "sm",
        "paddingAll": "13px"
      },
      "footer": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "晚年生命自主",
            "align": "end"
          }
        ]
      }
    }
  ]
}
        flex_message = FlexSendMessage(alt_text="晚年生命自主", contents=trycontent)
        
        # 需要準備發送的消息列表
        messages = list()    # 將 args 轉換成列表  #修改處
        for i in args:
            messages.append(TextSendMessage(text=i))
        messages.append(flex_message)  # 將 Flex Message 添加到列表中  #修改處

        # 使用 reply_message 發送一個消息列表
        line_bot_api.reply_message(event.reply_token, messages)  #修改處

    except Exception as e:
        print("error:", e)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤！'))



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
