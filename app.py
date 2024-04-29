# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 22:45:29 2024

@author: nowfr
"""

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
from linebot.models import TextSendMessage, FlexSendMessage, ImageSendMessage
import os

import warnings
from linebot import LineBotSdkDeprecatedIn30



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
true=True



def GPT_response(text):
    # 接收回應
    response = openai.Completion.create(model="gpt-3.5-turbo-instruct", prompt=text, temperature=0.5, max_tokens=500)
    print(response)
    # 重組回應
    answer = response['choices'][0]['text'].replace('。','')
    return answer


##訊息打包函數

def MessagesPacker(pack):
    messages = []  # 创建一个空列表
    for item in pack:
        if item[0]=="text":
            messages.append(TextSendMessage(text=item[1]))  # 如果是字符串，打包为文字消息
        elif item[0]=="flex":
            messages.append(FlexSendMessage(alt_text=item[1], contents=item[2]))  # 如果是字典，打包为 Flex Message
        elif item[0]=="image" and item[1].startswith("http"):
            messages.append(ImageSendMessage(original_content_url=item[1], preview_image_url=item[1]))  # 如果是以"http"开头的字符串，打包为图片消息
        else:
            raise ValueError("打包函數不包括此類型")  # 如果是其他类型，引发错误
    return messages  # 返回消息列表


##FlexMessageData
Flex1Message={ 
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
Flex2Message={
  "type": "carousel",
  "contents": [
    {
      "type": "bubble",
      "size": "giga",
      "hero": {
        "type": "image",
        "url": "https://i.imgur.com/Yyck3Vh.jpeg",
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
            "align": "center",
            "action": {
              "type": "postback",
              "label": "123",
              "data": "postback2.1"
            },
            "contents": []
          },
          {
            "type": "filler"
          },
          {
            "type": "button",
            "action": {
              "type": "postback",
              "label": "我想了解",
              "data": "postback2.1"
            },
            "style": "primary"
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
            "align": "center",
            "action": {
              "type": "postback",
              "label": "action",
              "data": "postback2.2"
            }
          },
          {
            "type": "button",
            "action": {
              "type": "postback",
              "label": "我想了解",
              "data": "postback2.2"
            },
            "style": "primary"
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
            "align": "center",
            "action": {
              "type": "postback",
              "label": "action",
              "data": "postback2.3"
            }
          },
          {
            "type": "button",
            "action": {
              "type": "postback",
              "label": "我想了解",
              "data": "postback2.3"
            },
            "style": "primary"
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
            "align": "center",
            "action": {
              "type": "postback",
              "label": "action",
              "data": "postback2.4"
            }
          },
          {
            "type": "filler"
          },
          {
            "type": "button",
            "action": {
              "type": "postback",
              "label": "我想了解",
              "data": "postback2.4"
            },
            "style": "primary"
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
            "align": "center",
            "action": {
              "type": "postback",
              "label": "action",
              "data": "postback2.5"
            }
          },
          {
            "type": "filler"
          },
          {
            "type": "button",
            "action": {
              "type": "postback",
              "label": "我想了解",
              "data": "postback2.5"
            },
            "style": "primary"
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
Flex3Message={
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
            "text": "安寧照護和\n長期照護有何不同?",
            "weight": "bold",
            "size": "xl",
            "wrap": true,
            "action": {
              "type": "postback",
              "label": "action",
              "data": "postback3.1"
            },
            "align": "center"
          },
          {
            "type": "button",
            "action": {
              "type": "postback",
              "label": "我想了解",
              "data": "postback3.1"
            },
            "style": "primary"
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
            "wrap": true,
            "action": {
              "type": "postback",
              "label": "action",
              "data": "postback3.2"
            }
          },
          {
            "type": "button",
            "action": {
              "type": "postback",
              "label": "我想了解",
              "data": "postback3.2"
            },
            "style": "primary"
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
            "wrap": true,
            "action": {
              "type": "postback",
              "label": "action",
              "data": "postback3.3"
            }
          },
          {
            "type": "filler"
          },
          {
            "type": "button",
            "action": {
              "type": "postback",
              "label": "我想了解",
              "data": "postback3.3"
            },
            "style": "primary"
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
            "wrap": true,
            "action": {
              "type": "postback",
              "label": "action",
              "data": "postback3.4"
            }
          },
          {
            "type": "button",
            "action": {
              "type": "postback",
              "label": "我想了解",
              "data": "postback3.4"
            },
            "style": "primary"
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
            "wrap": true,
            "action": {
              "type": "postback",
              "label": "action",
              "data": "postback3.5"
            },
            "contents": []
          },
          {
            "type": "filler"
          },
          {
            "type": "button",
            "action": {
              "type": "postback",
              "label": "我想知道…",
              "data": "postback3.5"
            },
            "style": "primary"
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
            "wrap": true,
            "action": {
              "type": "postback",
              "label": "action",
              "data": "postback3.6"
            }
          },
          {
            "type": "filler"
          },
          {
            "type": "button",
            "action": {
              "type": "postback",
              "label": "我想了解",
              "data": "postback3.6"
            },
            "style": "primary"
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
Flex4Message={
  "type": "carousel",
  "contents": [
    {
      "type": "bubble",
      "size": "giga",
      "hero": {
        "type": "image",
        "url": "https://i.imgur.com/lrX4o5f.jpeg",
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
            "text": "什麼是悲傷輔導?",
            "weight": "bold",
            "size": "xl",
            "wrap": true,
            "align": "center",
            "action": {
              "type": "postback",
              "label": "action",
              "data": "postback4.1"
            }
          },
          {
            "type": "filler"
          },
          {
            "type": "button",
            "action": {
              "type": "postback",
              "label": "我想了解",
              "data": "postback4.1"
            },
            "style": "primary"
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
            "text": "悲傷治療",
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
        "url": "https://i.imgur.com/HNHlvlw.jpeg"
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "如何尋找悲傷輔導?",
            "weight": "bold",
            "size": "xl",
            "wrap": true,
            "align": "center",
            "action": {
              "type": "postback",
              "label": "action",
              "data": "postback4.2"
            }
          },
          {
            "type": "filler"
          },
          {
            "type": "button",
            "action": {
              "type": "postback",
              "label": "我想了解",
              "data": "postback4.2"
            },
            "style": "primary"
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
            "text": "悲傷治療",
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
        "url": "https://i.imgur.com/JGeEnuZ.jpeg",
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
            "text": "藝術治療與音樂治療\n如何降低悲傷情緒?",
            "weight": "bold",
            "size": "xl",
            "wrap": true,
            "align": "center",
            "action": {
              "type": "postback",
              "label": "action",
              "data": "postback4.3"
            }
          },
          {
            "type": "button",
            "action": {
              "type": "postback",
              "label": "我想了解",
              "data": "postback4.3"
            },
            "style": "primary"
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
            "text": "悲傷治療",
            "align": "end"
          }
        ]
      }
    }
  ]
}


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
            premsg="復原是條漫長的路..."
            sendFlex4(event,premsg)
            
        elif msg == "感到日漸衰老，想開始安排安寧的晚年":
            premsg="生死是人生需要面對的最後一關，預作準備才能從容面對。你可能需要先思考下列問題。"
            sendFlex2(event,premsg)  # 注意这里改为正确的函数名称，并传入 event

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
        trycontent=Flex1Message
        message = FlexSendMessage(alt_text="臨終回家", contents=trycontent)
        line_bot_api.reply_message(event.reply_token,message)
    except Exception as e:
        print("error:",e)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤！'))

def sendFlex3(event,*args):  #彈性配置
    try:
        trycontent=Flex3Message
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
        trycontent=Flex2Message
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


def sendFlex4(event,*args):  #彈性配置
    try:
        trycontent=Flex4Message
        flex_message = FlexSendMessage(alt_text="悲傷治療", contents=trycontent)
        
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
def handle_postback_event(event):
    print (event.postback.data)
    if event.postback.data=="postback1.1":
        pass
        ##        pack=[]
##        msg1=["text","wahaha"]
##        msg2=["image","https://i.imgur.com/F3ftAED.jpg"]
##        msg3=["flex","預立醫囑",Flex1Message]
##        pack=[msg1,msg2,msg3]
##        message=MessagesPacker(pack)
##        line_bot_api.reply_message(event.reply_token, message)

    elif event.postback.data=="postback2.1":
        msg1=["text","接受或拒絕維持生命治療：\n你可以決定：\n當你處於疾病末期或昏迷等嚴重狀況時，是否接受維持生命的治療。\n及是否要接受人工管灌餵食。"]
        #msg2=["text","你可以決定：\n當你處於疾病末期或昏迷等嚴重狀況時，是否接受維持生命的治療。\n及是否要接受人工管灌餵食。"]
        msg3=["text","簽署需具備的條件：\n1.法律上的完全行為能力人，意思是成年人且沒有受限行為能力。\n2.必須擁有健保卡。如果你是外籍人士，並且擁有健保卡，也是符合條件的。\n3.精神狀況正常，能夠清楚、自主地表達自己的意思。\n預立醫療決定：\n這是一個文件，說明你在嚴重狀況下的醫療意願。\n要讓這個文件生效，你需要先和專業人員談過，然後由兩位見證人見證或公證，最後由醫療機構核章，並註記在健保卡上。\n\n有些特約診所也提供到宅預立醫療照護諮商服務"]
        msg4=["image","https://i.imgur.com/aq3Y7xJ.jpeg"]
        msg2=["image","https://i.imgur.com/GK1Rj8R.png"]
        msg5=["flex","預立醫囑",Flex2Message]
        pack=[msg1,msg3,msg4,msg2,msg5]      
        message=MessagesPacker(pack)
        line_bot_api.reply_message(event.reply_token, message)
    
    elif event.postback.data=="postback2.2":
        msg1=["text","除癌症、漸凍人等末期病人外，可列入安寧療護服務對象的條件，包括：\n老年期及初老期器質性精神病態\n大腦變質\n心臟衰竭\n慢性氣道阻塞\n肺部疾病\n慢性肝病及肝硬化\n急性腎衰竭\n慢性腎衰竭\n末期衰弱老人\n末期骨髓增生不良症候群"]
        #msg2=["text","你可以決定：\n當你處於疾病末期或昏迷等嚴重狀況時，是否接受維持生命的治療。\n及是否要接受人工管灌餵食。"]
        msg3=["text","申請:由二位醫師診斷為末期病人，醫師應具有相關專科醫師資格。\n應有意願人簽署之意願書。但未成年人簽署意願書時，應得其法定代理人之同意。"]
        msg5=["flex","末期判定",Flex2Message]
        pack=[msg1,msg3,msg5]      
        message=MessagesPacker(pack)
        line_bot_api.reply_message(event.reply_token, message)            
    elif event.postback.data=="postback2.3":
        msg1=["image","https://i.imgur.com/HpPAJAP.png"]
        #msg2=["text","你可以決定：\n當你處於疾病末期或昏迷等嚴重狀況時，是否接受維持生命的治療。\n及是否要接受人工管灌餵食。"]
        msg3=["image","https://i.imgur.com/zMsc0X4.png"]
        msg5=["flex","長照資格",Flex2Message]
        pack=[msg1,msg3,msg5]      
        message=MessagesPacker(pack)
        line_bot_api.reply_message(event.reply_token, message)    
    elif event.postback.data=="postback2.5":
          msg1=["text","居家照顧服務除了可向政府申請公費補助之外，還有坊間自費的短期看護、陪伴照護或家事服務等選擇。"]
          msg2=["text","自費的居家照顧可以透過仲介、網路平台來尋找看護。相較長照2.0，自費的居服流程較為簡單，只需向服務單位提出"]
          msg3=["text","需求派案，談妥價格、服務項目、服務時間等條件後，再由照服員到府服務。"]
          msg4=["text","服務單位:清安照顧服務勞動合作社 0979513281 (8am~10PM可接電話 王專員)"]
          msg5=["flex","自費服務",Flex2Message]
          pack=[msg1,msg2,msg3,msg4,msg5]      
          message=MessagesPacker(pack)
          line_bot_api.reply_message(event.reply_token, message)   

    elif event.postback.data=="postback2.4":
        msg1=["text","目前新竹市居家安寧服務由以下醫療機構附設之居家護理所所提供。\n可以經由醫護人員轉介安寧居家護理師，或聯繫24小時居家安寧諮詢電話專線申請:"]
        msg2=["text","1.國立臺灣大學醫學院附設醫院新竹臺大分院\n電話: 0972-654296"]
        msg3=["text","2.財團法人馬偕紀念醫院新竹分院\n電話: 03-6118865(上班日)\n0975837365(非上班日)"]
        msg4=["text","3.新竹國泰醫療財團法人 電話: 03-5278999#7777"]
        msg5=["flex","長照機構",Flex2Message]
        pack=[msg1,msg2,msg3,msg4,msg5]      
        message=MessagesPacker(pack)
        line_bot_api.reply_message(event.reply_token, message)   

    elif event.postback.data=="postback3.1":
        pass
    elif event.postback.data=="postback2.1":
        pass
    elif event.postback.data=="postback2.1":
        pass
    elif event.postback.data=="postback2.1":
        pass
    elif event.postback.data=="postback2.1":
        pass
    elif event.postback.data=="postback2.1":
        pass
    elif event.postback.data=="postback2.1":
        pass
    elif event.postback.data=="postback2.1":
        pass
    elif event.postback.data=="postback2.1":
        pass
    elif event.postback.data=="postback2.1":
        pass
    elif event.postback.data=="postback2.1":
        pass
    elif event.postback.data=="postback2.1":
        pass
    elif event.postback.data=="postback2.1":
        pass
    


@handler.add(MemberJoinedEvent)
def welcome(event):
    uid = event.joined.members[0].user_id
    gid = event.source.group_id1
    profile = line_bot_api.get_group_member_profile(gid, uid)
    name = profile.display_name
    message = TextSendMessage(text=f'{name}歡迎加入')
    line_bot_api.reply_message(event.reply_token, message)
        
        

if __name__ == "__main__":
    warnings.filterwarnings("ignore", category=LineBotSdkDeprecatedIn30)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    
    
    

