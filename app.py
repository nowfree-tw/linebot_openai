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
import requests
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
Azureurl = os.getenv("Azureurl")
Azuresubscription_key = os.getenv("Azuresubscription_key")


def askotherquestion(question):
    
    headers = {
        "Ocp-Apim-Subscription-Key": Azuresubscription_key,
        "Content-Type": "application/json"
    }
    
    data = {
        "top": 3,
        "question": question,
        "includeUnstructuredSources": True
    }
    
    response = requests.post(Azureurl, headers=headers, json=data)
    
    if response.status_code == 200:
 #       print("請求成功！")
 #       print(response.json())  # 印出回應的內容
        return response.json()["answers"]
    else:
  #      print("請求失敗...")
#        print(response.text)  # 印出錯誤訊息
        return False



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
        elif item[0]=="url" and item[1].startswith("http"):
            messages.append(TextSendMessage(text="請參考下列網址: "+'{}'.format(item[1])))  # 如果是字符串，打包为文字消息
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
          },
          {
            "type": "button",
            "action": {
              "type": "postback",
              "label": "我有需要",
              "data": "postback1.1"
            },
            "style": "primary"
          }
        ],
        "spacing": "sm",
        "paddingAll": "13px",
        "action": {
          "type": "postback",
          "data": "postback1.1"
        }
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
            "text": "如何取得死亡證明書",
            "weight": "bold",
            "size": "xl",
            "wrap": true,
            "align": "center",
            "position": "relative",
            "action": {
              "type": "postback",
              "label": "action",
              "data": "postback1.2"
            }
          },
          {
            "type": "filler"
          },
          {
            "type": "button",
            "action": {
              "type": "postback",
              "label": "取得管道",
              "data": "postback1.2"
            },
            "style": "primary"
          }
        ],
        "spacing": "sm",
        "paddingAll": "13px",
        "action": {
          "type": "postback",
          "label": "取得管道",
          "data": "postback1.2"
        }
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
          },
          {
            "type": "button",
            "action": {
              "type": "postback",
              "label": "取得資訊",
              "data": "postback1.3"
            },
            "style": "primary"
          }
        ],
        "spacing": "sm",
        "paddingAll": "13px",
        "action": {
          "type": "postback",
          "label": "action",
          "data": "postback1.3"
        }
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
            "align": "center",
            "action": {
              "type": "postback",
              "label": "取得資訊",
              "data": "postback1.4"
            }
          },
          {
            "type": "button",
            "action": {
              "type": "postback",
              "label": "取得資訊",
              "data": "postback1.4"
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
          },
          {
            "type": "button",
            "action": {
              "type": "postback",
              "label": "我有需要",
              "data": "postback1.5"
            },
            "style": "primary"
          }
        ],
        "spacing": "sm",
        "paddingAll": "13px",
        "action": {
          "type": "postback",
          "label": "action",
          "data": "postback1.5"
        }
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
#    os.system('cls')
    print("I am here 0")
    '''
    print("Handle: reply_token: " + event.reply_token + ", message: " + event.message.text)
    content = "{},{},{}".format(event.message.text,event.message.text,event.message.text)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=content))
    '''
    msg = event.message.text.lower()  # 将输入文本转换为小写，以便不区分大小写处理
    print ("@@,Message:",msg)
    try:
        if msg == "病重即將去世，希望能離院回家度過最後時光":
            premsg="病危是個傷心的時刻，想完成回家的願望，可能遇到下列的問題："
            sendFlex1(event,premsg)
        elif msg == "到了生命末期，想在家安詳度過生命的最後階段":
            premsg="疾病與老化已無關勝敗，想在家安詳度過生命的最後階段，你可能需要下列資源："
            sendFlex3(event,premsg)
        elif msg == "家人死亡後，悲傷情緒難以平復":
            premsg="復原是條漫長的路..."
            sendFlex4(event,premsg)            
        elif msg == "感到日漸衰老，想開始安排安寧的晚年":
            premsg="生死是人生需要面對的最後一關，預作準備才能從容面對。你可能需要先思考下列問題："
            sendFlex2(event,premsg)  # 注意这里改为正确的函数名称，并传入 event

            pass
        else:
            print("I am here")
            GPT_answer = askotherquestion(msg)[0]  # 假设这里是处理其他消息的默认回应,只取第一個問題。
            print("Confidence:",GPT_answer["confidenceScore"])
#            source=GPT_answer["source"]

            try:
                source=GPT_answer["source"]
            except:
                pass
#            print (source)
            if GPT_answer["confidenceScore"] >= 0.3 and "dialog" in GPT_answer.keys():
                print ("prompts:",len(GPT_answer["dialog"]["prompts"]),"answers:",len(GPT_answer["answer"]))
                if len(GPT_answer["dialog"]["prompts"]) >0 and len(GPT_answer["answer"]) >0:
                    print("checkpoint 1")
                    promptlist = list()
                    for i in GPT_answer["dialog"]["prompts"]:
                        # 將 ["displayText"] 修改為 i["displayText"]
                        promptlist.append(i["displayText"])
                    print ("length:@@",len(promptlist))
                    if len(promptlist) >= 3:
                        promptlist=promptlist[0:3]
                    try:
                        msg1 = TextSendMessage(text=GPT_answer["answer"]+"\n資料來源：\n"+source)
                    except:
                        msg1 = TextSendMessage(text=GPT_answer["answer"])
                        
                    msg2 = ButtonMsg(promptlist) 
                    line_bot_api.reply_message(event.reply_token, [msg1,msg2])

                elif len(GPT_answer["dialog"]["prompts"]) ==0 and len(GPT_answer["answer"]) >0:
                    print("checkpoint 2")
                    try:
                        msg1 = TextSendMessage(text=GPT_answer["answer"]+"\n資料來源：\n"+source)
                    except:
                        msg1 = TextSendMessage(text=GPT_answer["answer"])
                    line_bot_api.reply_message(event.reply_token, msg1)
                elif len(GPT_answer["dialog"]["prompts"]) > 0 and len(GPT_answer["answer"]) ==0: 
                    print("checkpoint 3")
                    promptlist = list()
                    for i in GPT_answer["dialog"]["prompts"]:
                        # 將 ["displayText"] 修改為 i["displayText"]
                        promptlist.append(i["displayText"])
                    print ("length:@@",len(promptlist))
                    if len(promptlist) >= 3:
                        promptlist=promptlist[0:3]
                    print ("length:@@@",len(promptlist))
 
                    msg2 = ButtonMsg(promptlist)
                    line_bot_api.reply_message(event.reply_token, msg2)                    
                else:
                    print("checkpoint 3")

                    print("I am here ###", "nothing")

                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text="無內容"))
            else:
                    print("checkpoint 3")

                    print("I am here ###", "nothing")

                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text="請參考主選單內容"))

    except Exception as e:
        print("error:", e)  # 输出错误堆栈
        #error_message = '不好意思，有點小錯誤。'#######################################
        #line_bot_api.reply_message(event.reply_token, TextSendMessage(text=error_message))######################################

from linebot.models import (
    ButtonsTemplate, MessageAction, TemplateSendMessage
)

def ButtonMsg(promptlist):
    actions = [MessageAction(label=prompt[0:10], text=prompt) for prompt in promptlist]    
    buttons_template = ButtonsTemplate(
        title='你可能還想進一步了解：',
#        thumbnail_image_url='https://storage.googleapis.com/你的圖片連結.png',
        text='可選擇以下操作',
        actions=actions
    )
    return TemplateSendMessage(alt_text='進一步資訊', template=buttons_template)






#Flex Message Area

def sendFlex1(event,*args):  #彈性配置
    try:
        trycontent=Flex1Message
        flex_message = FlexSendMessage(alt_text="臨終回家", contents=trycontent)
        messages = list()    # 將 args 轉換成列表  #修改處
        for i in args:
            messages.append(TextSendMessage(text=i))
        messages.append(flex_message)  # 將 Flex Message 添加到列表中  #修改處
        line_bot_api.reply_message(event.reply_token,messages)

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
        msg1=["text","要讓病人順利運送到自宅房間，需考慮病人身體情況決定交通運輸工具：\n若病人能完成基本移動或使用輪椅，可考慮使用私人車輛，計程車，或復康巴士。"]
        msg2=["text","對行動不便或臥床病人，返家需以民間救護車運送。\n收費依照民間救護車標準計算：\n市區範圍一趟費用約 1500-2000元(包括車輛費用，技術員費用及衛材費用)，有需要亦可安排專業護理師跟車(600元/時)。\n詳細費用可連絡國泰醫院特約紅俥救護車公司估算。\n紅俥救護車公司電話號碼： (03)596-6666"]
        msg3=["text","你的問題回答如上。如果你還有其他問題，可以在下面的圖卡選擇情況或從主選單內挑選其它情境，以獲得需要的資訊。"]
        msg5=["flex","返家運送",Flex1Message]
        pack=[msg1,msg2,msg3,msg5]      
        message=MessagesPacker(pack)
        line_bot_api.reply_message(event.reply_token, message)

    elif event.postback.data=="postback1.2":
        msg1=["text","須備妥亡者身分證、家屬身分證及印章辦理。\n若在醫院過世：由醫院醫師開立死亡證明。 \n在家亡故：通知衛生所醫師開立死亡證明。\n東區衛生所：\n03-5236158\n北區衛生所：\n03-5353969\n香山區衛生所：\n03-5388109\n意外死亡：至派出所報案請檢察官開相驗證明。\n若已有合作禮儀公司，可詢問是否有醫師協助開立。"]
        #msg2=["text","你可以決定：\n當你處於疾病末期或昏迷等嚴重狀況時，是否接受維持生命的治療。\n及是否要接受人工管灌餵食。"]
        msg3=["text","你的問題回答如上。如果你還有其他問題，可以在下面的圖卡選擇情況或從主選單內挑選其它情境，以獲得需要的資訊。"]
        msg4=["text","所需死診份數依情況而定，通常一份為10張，需使用死亡證明書情況 ：\n1.終止存款戶頭。\n.2終止保險及申請保險給付。\n3.申請除戶戶籍謄本。\n4.地政事務所辦理不動產產權變更。\n5.申請殯儀館。\n6.國稅局理遺產變更。\n7.申請火（埋）葬許可。\n8.申請納骨塔（公墓）。\n9.另需準備多份訃聞及死亡證明書，供家屬向工作單位請假用。\n\nhttps://dep-n-health.hccg.gov.tw/ch/home.jsp?id=10041&parentpath=0,20&mcustomize=multimessages_view.jsp&toolsflag=Y&dataserno=201606060006&t=SalesPhoto&mserno=201606040001"]
        msg2=["text","除了取得死診之外，臨終前的準備事項:\n\n佛教\n準備唸佛機，耳聞佛音，親友來時，可引導在旁，協助唸佛。先給予短暫開示，語句盡量簡短切要（包括肯定他的一生、承諾家屬會過得很好、提醒他往光明的前方走），之後陪同病人持續唸佛號。（阿彌陀佛）\n更衣：可於臨終前換好衣服，或往生後助念 8 小時之後，再更衣。\n\n一般民間信仰\n「有穿什麼得什麼」之說，所以衣服在往生前先穿好。把口袋縫起來（可留給子孫更多）。\n手尾錢：放在病人手中或口袋中放錢（裝紅包袋中），送冰櫃前記得拿起來，日後分給孫子。\n\n基督教、天主教\n臨終彌留時，除親人隨伺在旁，可邀請教會牧師或神父、修女來（親友可代替）給予禱告、安慰、唱詩歌，在病人耳邊語，請他放心。祈求主保佑到最後一刻，牽他的手，抱他走天路。\n\n\n臨終後的注意事項\n\n佛教\n深信往生後8小時，神識尚未離開肉體，這時碰觸或哭泣，會加深不捨或痛苦，家人陪同念佛號。蓋上往生被。一般在病房可將遺體送到安息室助念，由家屬陪伴助念 8 小時。\n\n基督教及天主教\n宣布過世的時間後，牧師再次帶領家屬做慰禱。家屬與護理人員一起用溫水擦澡，穿上乾淨衣物。\n\n\n喪葬事宜越早準備愈好，可以比較多家葬儀社。葬儀社可以提供家屬了解遺體處理流程。"]
        msg5=["flex","死亡證明",Flex1Message]
        pack=[msg1,msg4,msg2,msg3,msg5]      
        message=MessagesPacker(pack)
        line_bot_api.reply_message(event.reply_token, message)
    elif event.postback.data=="postback1.3":
        msg1=["text","移除管路時機:\n\n在瀕死階段就可準備。瀕死症狀辨認如下:\n\n瀕死症狀:脈搏若有若無、目視前方、有聽覺但是不一定會回應。\n有拒食現象，大部分人意識清楚但閉眼休息或睡覺，部分呈譫妄。\n尿少而色深、一天一次或兩天一次、大多數病人會知道自己死亡將近。\n\n瀕死處理:\n\n維持一般身體清潔，尤其泌尿器官、皮膚縐褶處及傷口，空氣有異味時可使用檀香、除臭劑等。口腔要清潔、保持溼潤。不要強迫進食。親友來探視時可以觸摸、報告姓名及口頭的關心即可，但勿拉扯病人或要病人回答。請在房間外抒發情緒，勿在病人旁哭泣，影響其情緒。可以放病人喜愛輕柔音樂或宗教音樂、佛號等。\n死亡之後就可移除管路，方法如下所示。"]
        #msg2=["text","你可以決定：\n當你處於疾病末期或昏迷等嚴重狀況時，是否接受維持生命的治療。\n及是否要接受人工管灌餵食。"]
        msg3=["text","你的問題回答如上。如果你還有其他問題，可以在下面的圖卡選擇情況或從主選單內挑選其它情境，以獲得需要的資訊。"]
        msg4=["image","https://imgur.com/xsNh2T4.png"]
        msg2=["image","https://imgur.com/ogDjZ7Q.png"]
        msg5=["flex","管路移除",Flex1Message]
        pack=[msg1,msg2,msg4,msg3,msg5]      
        message=MessagesPacker(pack)
        line_bot_api.reply_message(event.reply_token, message)
    elif event.postback.data=="postback1.4":
        #msg1=["text","接受或拒絕維持生命治療：\n你可以決定：\n當你處於疾病末期或昏迷等嚴重狀況時，是否接受維持生命的治療。\n及是否要接受人工管灌餵食。"]
        #msg2=["text","你可以決定：\n當你處於疾病末期或昏迷等嚴重狀況時，是否接受維持生命的治療。\n及是否要接受人工管灌餵食。"]
        msg3=["text","參考以下清潔大體衛教影片：\n https://youtu.be/6mMTbiG_2KE?si=PW2kRKLOJnh_gkLH&t=2320"]
        msg1=["text","1.清潔：\n(1)使用溫熱毛巾擦拭身體。因為聽覺是最後消失的，所以我們可以一邊擦拭一邊告訴他正在做什麼，或可向其述說『沒有病痛了，安心離去吧！』，猶如往生者在世一般。\n(2)清潔後為預防大小便失禁而污染遺體，故需穿上尿布。如果患者生前即排斥使用，我們可以換個方式告訴他現在為他穿上褲子，並於入殮時可將尿布移除。\n(3)為避免因擦拭遺體時的翻動，造成胃內穢物流出，於清潔時可以在頭、肩膀下墊一塊大毛巾以利擦拭及避免穢物弄髒衣物。\n\n2.更衣：因人體死亡後肌肉會鬆弛造成大小便的滲出或胃內穢物流出，死亡6-8小時後遺體會開始漸漸僵硬，應盡快更衣。"]
        msg2=["text","3.闔眼：\n若病人此時眼睛未全閉時，可於耳旁訴說一些讓其安心的話，並用指尖在眼皮上向下輕壓一下，即可使雙眼自然閉合，或使用紙膠帶將眼皮稍微往下黏貼，6-8小時後再移除。\n\n4.闔嘴：\n(1)如往生者有使用假牙，可將其置回口中，以求相貌完整。\n(2)如有張口情形可於頭下置一枕頭，然後將毛巾捲成軸狀，放於下巴處，並將下巴往上推使嘴巴合攏，也可使用毛巾和布條托住下巴。以上兩種方法均須於6-8小時後移除毛巾或布條。\n\n5.其他：\n(1)若有水腫破皮現象，應使用尿布墊或毛巾，將水腫部位包起來，預防滲出液體。\n(2)必要時可著上淡妝，使其相貌看起來較柔順，就如同其在世一般。"]
        msg4=["text","你的問題回答如上。如果你還有其他問題，可以在下面的圖卡選擇情況或從主選單內挑選其它情境，以獲得需要的資訊。"]
        msg5=["flex","大體清潔",Flex1Message]
        pack=[msg1,msg2,msg3,msg4,msg5]      
        message=MessagesPacker(pack)
        line_bot_api.reply_message(event.reply_token, message)
    elif event.postback.data=="postback1.5":
        msg1=["text","若已有安寧居家團隊收案，可先聯絡安寧團隊協助。\n若無安寧居家團隊收案，可聯絡廠商。\nA.店名：長騰醫療儀器行\n 聯絡電話：035332888\n地址：新竹市東區經國路一段452之10號\n B.店名：康諾健康生活館\n 聯絡電話：035358250\n地址：300新竹市東區鐵道路二段5號\n"]
        #msg2=["text","你可以決定：\n當你處於疾病末期或昏迷等嚴重狀況時，是否接受維持生命的治療。\n及是否要接受人工管灌餵食。"]
        msg4=["text","你的問題回答如上。如果你還有其他問題，可以在下面的圖卡選擇情況或從主選單內挑選其它情境，以獲得需要的資訊。"]
        msg2=["text","新竹市輔具及居家無障礙環境改善服務特約廠商名單，請連結以下網址，下載附件：\nhttps://www.hcchb.gov.tw/service_a.php?service_id=6"]
        msg3=["text","常見器材使用之教學影片:\n\n抽痰機使用可參考連結\nhttps://youtu.be/RJM6EbJQTvg\n\n氧氣製造機使用可參考連結\nhttps://youtu.be/aFX4ud6awJk\n\n氧氣鼻導管使用可參考連結\nhttps://youtu.be/cIdqmXN3EI0"]
        msg5=["flex","氧氣租借",Flex1Message]
        pack=[msg1,msg2,msg3,msg4,msg5]      
        message=MessagesPacker(pack)
        line_bot_api.reply_message(event.reply_token, message)
                

    elif event.postback.data=="postback2.1":
        msg1=["text","當病人處於疾病末期、永久昏迷等五項「特定臨床條件」時機下，有權拒絕「維持生命治療」、「人工營養及流體餵養」 。\n\n病人須具備以下條件 :\n1.  法律上的完全行為能力人。\n2.  有健保卡（外籍人士有健保卡者亦可）。\n3.  精神狀況正常，能夠清楚、自主地表達意思。\n\n「預立醫療決定」是病人本人經「預立醫療照護諮商」後，已經清楚瞭解 「病人自主權利法」裡面規定，經由簽署書面文件，由兩位見證人見證或公證，經醫療機構核章，註記在健保卡上生效。\n\n\n預立醫療照護諮商，如下圖："]
        #msg2=["text","你可以決定：\n當你處於疾病末期或昏迷等嚴重狀況時，是否接受維持生命的治療。\n及是否要接受人工管灌餵食。"]
        msg3=["text","有些特約診所也提供到宅預立醫療照護諮商 ，可諮詢你的長照個管師。\n\n更多關於預立醫療照護諮商訊息，請參考\nhttps://www.hospice.org.tw/care/law\n\n如果你還有其他問題，可以從下方的圖卡選擇或從主選單內挑選其它情境，以獲得需要的資訊。"]
        msg2=["image","https://i.imgur.com/GK1Rj8R.png"]
        msg4=["image","https://i.imgur.com/aq3Y7xJ.jpeg"]
#        msg4=["text","你的問題回答如上。如果你還有其他問題，可以在下面的圖卡選擇情況或從主選單內挑選其它情境，以獲得需要的資訊。"]
        msg5=["flex","預立醫囑",Flex2Message]
        pack=[msg1,msg4,msg3,msg2,msg5]      
        message=MessagesPacker(pack)
        line_bot_api.reply_message(event.reply_token, message)
    
    elif event.postback.data=="postback2.2":
        msg1=["text","除癌症、漸凍人等末期病人外，可列入安寧療護服務對象的條件，包括：\n\n●老年期及初老期器質性精神病態\n●大腦變質\n●心臟衰竭\n●慢性氣道阻塞\n●肺部疾病\n●慢性肝病及肝硬化\n●急性腎衰竭\n●慢性腎衰竭\n●末期衰弱老人\n●末期骨髓增生不良症候群"]
        #msg2=["text","你可以決定：\n當你處於疾病末期或昏迷等嚴重狀況時，是否接受維持生命的治療。\n及是否要接受人工管灌餵食。"]
        msg2=["text","末期判定申請:\n\n●須向主治醫師表達申請意願。由二位醫師診斷為末期病人，醫師應具有相關專科醫師資格。\n●應有病人簽署之意願書。但未成年人簽署意願書時，應得其法定代理人之同意。"]
        msg3=["text","現行健保安寧療護醫療服務範圍包括醫院、居家及照護機構，由醫療團隊依末期病人需求，提供自入院、出院至居家相互扣連的整合性照護。\n\n此外，健保安寧居家療護之服務提供場域為老人安養、養護機構或身心障礙福利機構、護理之家，使末期病人能在長照機構接受安寧療護，減少末期病人及家屬往返醫院就醫之勞頓奔波，落實在地安老、提升生命末期之照護品質。"]
#        msg5=["flex","末期判定",Flex2Message]
        msg4=["text","如果你還有其他問題，可以從下方的圖卡選擇或從主選單內挑選其它情境，以獲得需要的資訊。"]
        msg5=["flex","末期判定",Flex2Message]
        pack=[msg1,msg2,msg3,msg4,msg5]
        message=MessagesPacker(pack)
        line_bot_api.reply_message(event.reply_token, message)            
    elif event.postback.data=="postback2.3":
        msg1=["text","申請資格：\n\n1.65 歲以上獨居老人、衰弱老人、失能老人。\n2.55 歲以上失能原住民。\n3.50 歲以上失智者。\n4.不分年齡的身心障礙者（領有身心障礙證明或手冊）。\n5.家庭照顧者、有外籍看護工家庭（喘息服務／短期照顧服務）。"]
        msg2=["text","可以透過以下方式來申請長照服務:\n\n1.直接撥打長照專線1966。\n2.聯絡新竹市長期照顧管理中心（035-355-191)。\n3.住院期間聯絡醫院內的“出院準備銜接長照服務小組“\n4.線上申請：\nhttps://www.hcchb.gov.tw/service_form.php"]
        msg3=["text","長照服務內容 (四包錢)：\n\n1.照顧服務主要為透過居家服務、日間照顧中心、家庭托顧等服務，提供身體與日常照顧服務；專業服務則是由專業醫事及社工人員如物理治療師、職能治療師、語言治療師、護理師、營養師、心理師等，針對自我功能提升、飲食、護理、困擾行為等提供個案及照顧者專業指導。\n2.提供就醫及復健交通接送服務。\n3.如果有輔具或是居家環境需要裝設扶手、移除門檻等改善工程，都可以申請。\n4.家中主要照顧者若需要休息，可以申請喘息服務，讓長輩到日間照顧中心、巷弄長照站、住宿式機構，或是請照顧服務員到府協助照顧。"]
        msg4=["text","如果你還有其他問題，可以從下方的圖卡選擇或從主選單內挑選其它情境，以獲得需要的資訊。"]
        msg5=["flex","長照資格",Flex2Message]
        pack=[msg1,msg2,msg3,msg4,msg5]      
        message=MessagesPacker(pack)
        line_bot_api.reply_message(event.reply_token, message)    
    elif event.postback.data=="postback2.4":
        msg1=["text","目前新竹市居家安寧服務由以下醫療機構附設之居家護理所所提供。\n末期病人若想要申請居家安寧服務 ，可以經由醫護人員轉介安寧居家護理師，或聯繫24小時居家安寧諮詢電話專線申請:"]
        msg2=["text","1.國立臺灣大學醫學院附設醫院新竹臺大分院\n電話: 0972-654296。\n2.財團法人馬偕紀念醫院新竹分院\n電話: 03-6118865(上班日)\n0975837365(非上班日)\n3.新竹國泰醫療財團法人 電話: 03-5278999#7777"]
        msg3=["text","當病況緊急變化時，如果上述居家安寧單位的24小時諮詢電話，無法提供足夠之及時協助，可以打電話至「新竹國泰醫院急診室」:\n03-5278999分機1190或7119"]
        msg4=["text","如果你還有其他問題，可以從下方的圖卡選擇或從主選單內挑選其它情境，以獲得需要的資訊。"]
        msg5=["flex","居家安寧機構",Flex2Message]
        pack=[msg1,msg2,msg3,msg4,msg5]      
        message=MessagesPacker(pack)
        line_bot_api.reply_message(event.reply_token, message)       
    elif event.postback.data=="postback2.5":
      msg1=["text","居家照顧服務除了可向政府申請公費補助之外，坊間也有自費的“短期看護“，“陪伴照護“或“家事服務“等選擇。"]
      msg2=["text","自費的居家照顧可以透過仲介、網路平台來尋找看護。相較長照2.0，自費的居服流程較為簡單，只需向服務單位提出，需求派案，談妥價格、服務項目、服務時間等條件後，再由照服員到府服務。"]
#      msg3=["text",""]
      msg3=["text","服務單位:\n清安照顧服務勞動合作社\n0979513281\n王專員\n(8:00AM~10:00PM)"]
      msg4=["text","如果你還有其他問題，可以從下方的圖卡選擇或從主選單內挑選其它情境，以獲得需要的資訊。"]
      msg5=["flex","自費服務",Flex2Message]
      pack=[msg1,msg2,msg3,msg4,msg5]      
      message=MessagesPacker(pack)
      line_bot_api.reply_message(event.reply_token, message)   

    elif event.postback.data=="postback3.1":
      #3-1 安寧長照有何不同
      msg1=["text","不同安寧服務名詞定義：\n\n安寧照顧：面對疾病威脅的病人及家屬，藉由安寧照護處置減少痛苦和不舒適，增進生活品質，為善終做準備，形式有“社區安寧“及“居家安寧“。\n\n社區安寧：結合住家附近的醫院、診所醫師、居家護理人員、或社工提供跨單位之照護，讓末期病人有尊嚴的善終。\n\n居家安寧：只由原治療醫院之安寧團隊人員，依病人需求提供居家訪視，減緩不適正確及提供家屬照護技巧指導。"]
      msg2=["text","居家安寧和長期照護皆是照顧病人生理及心理的需求，治療場所皆位於家中。\n\n長照服務：不是為善終準備，而是依其病人或其照顧者需要所提供的生活支持、協助、社會參與、照顧及相關醫護服務。\n\n依個案需求，社區居家安寧與長照服務兩者均可同時申請。"]
      msg3=["text","可為末期病人提供服務之新竹長照單位:\n\n清安居家長照機構(居家照顧)\n03-5165990\n子馨居家長照機構(居家照顧、專業復能)\n03-5730603\n順順居家護理所(專業復能)\n03-5724588"]    
#      msg3=["text","居家安寧和長期照護皆是照顧病人生理及心理的需求，治療場所皆位於家中依個案需求，社區居家安寧與長照服務兩者均可申請。若需其它資訊，請點選下列選單。"]
      #msg4=["text","服務單位:清安照顧服務勞動合作社 0979513281 (8am~10PM可接電話 王專員)"]
      msg4=["text","如果你還有其他問題，可以從下方的圖卡選擇或從主選單內挑選其它情境，以獲得需要的資訊。"]
      msg5=["flex","安寧與長照",Flex3Message]
      pack=[msg1,msg2,msg3,msg4,msg5]      
      message=MessagesPacker(pack)
      line_bot_api.reply_message(event.reply_token, message)   

    elif event.postback.data=="postback3.2":
        #3-2 哪些單位可以提通社區居家安寧服務
        msg1=["image","https://imgur.com/NFBluD2.png"]
        msg2=["text","下列單位可提供社區居家安寧服務：\n\n新竹市:\n北區：\n新竹台大附設居護所\n東區：\n南門醫院、新竹馬偕居家護理所、南門綜合醫院附設居護所、啟恩小兒科診所、國泰新竹居家護理所\n竹北市：\n東元醫院、美安居家護理所\n湖口鄉：\n新竹仁慈居家護理所\n五峰鄉：\n新竹縣五峰鄉居家護理所\n竹東鎮：\n北榮新竹分院、台大竹東分院附設居護所"]
        msg3=["text","其他社區安寧居家服務單位，可在此下載：\nhttps://www.hospice.org.tw/sites/default/files/attfiles/%E5%85%A8%E5%9C%8B%E5%AE%89%E5%AF%A7%E8%B3%87%E6%BA%90%28%E6%9C%80%E6%96%B0%E8%B3%87%E6%96%992023.09%29.pdf"]
        msg4=["text","如果你還有其他問題，可以從下方的圖卡選擇或從主選單內挑選其它情境，以獲得需要的資訊。"]
        msg5=["flex","安寧與長照服務單位",Flex3Message]
        pack=[msg1,msg2,msg3,msg4,msg5]
        message=MessagesPacker(pack)
        line_bot_api.reply_message(event.reply_token, message)   
  
    elif event.postback.data=="postback3.3":
        #3-3 社區居家安寧服務APPLY
        msg1=["text","●社區居家安寧申請資格為經醫師判定符合之病患，包含：\n  1. 癌症末期病患及對治癒性治療效果不佳者。\n  2. 末期運動神經元病患。\n  3.符合病人自主權利法所列的臨床條件者。\n  4. 已進入末期狀態，生命期餘約六個月。且主要診斷為：失智症末期、心臟衰竭、肺部其他疾病、慢性肝病和肝硬化、急性腎衰竭、末期骨髓增生不良症候群、末期衰弱老人、罕見疾病或預估生命受限。"]
        msg2=["text","●如果符合資格，可以打電話給社區居家安寧服務單位說明需求，他們會進行專業評估。"]
        msg4=["text","如果你還有其他問題，可以從下方的圖卡選擇或從主選單內挑選其它情境，以獲得需要的資訊。"]
        msg5=["flex","申請社區居家安寧服務",Flex3Message]
        pack=[msg1,msg2,msg4,msg5]      
        message=MessagesPacker(pack)
        line_bot_api.reply_message(event.reply_token, message)   
        
    elif event.postback.data=="postback3.4":
        #哪些狀況可以在家住院，並獲得必需的醫療服務
        msg1=["text","●在宅住院由專業醫師、護理人員、藥師、其他專業人員到宅訪視。\n\n提供的服務包含：在家抽血檢驗、點滴注射、抗生素藥物治療、傷口照護、X光檢查與指導和臨終照護。\n\n在宅住院是為發生急性病況變化的病人規劃，如發燒，泌尿道感染等。\n\n而在宅醫療是為穩定的病人而設計，如每月定期拿止痛藥物、三高藥物等。\n\n兩者共同點是:病人不用至醫院，由醫療團隊到家診療。末期病人都可申請。"]
        msg2=["text","在宅住院能提升病人及家屬的治療品質和生活品質，留在自己熟悉的家中或住宿型機構內。治療簡單的疾病如:\n輕微肺炎、泌尿道感染、蜂窩性組織炎。\n\n但需注意太複雜的疾病不能在宅住院。"]
        msg3=["text","欲申請在宅住院，請與居家醫療照護團隊進行聯絡。\n新竹國泰電話:\n03-5962998轉分機300\n或 0983702698\n\n由機構進行評估後，進行居家照護服務。"]
        msg4=["text","當病人選擇「在宅住院」時，照顧者自己可能需要學習一些照顧技巧，以補照顧專業團隊之服務缺口。馬偕安寧病房提供有益的教學影片:\n\n翻身擺位\nhttps://youtu.be/9fQOaYMNe88?si=W9ALd4TbXMEY8KJv\n\n鼻胃管餵食\nhttps://youtu.be/gkcF6rSW2Qs?si=yEYN7f8T-uH1HYLl\n\n口腔清潔\nhttps://youtu.be/ImpWCo3_H3U?si=kbqbMLOLear0Ahgw\n\n皮下針藥注射給藥方式之影片:\n\n末期病人會因病程進展導致有疼痛、喘等症狀不適，但病人無法吞嚥且無灌食管路，需改以施行皮下針藥注射給藥方式。\n在此狀況下照顧者須了解如何準備藥物注射細節如:皮下注射用物準備、打開藥瓶、抽取藥物、藥品及空針處理等。\n詳細步驟與常見問題可參考彰基安寧緩和科之衛教連結\n\nhttps://dpt.cch.org.tw/layout/layout_1/knowledge_detail.aspx?ID=3050&cID=476&Key=225\n\n\n如果你還有其他問題，可以從下方的圖卡選擇或從主選單內挑選其它情境，以獲得需要的資訊。"]
        msg5=["flex","在宅醫療",Flex3Message]
        pack=[msg1,msg2,msg3,msg4,msg5]      
        message=MessagesPacker(pack)
        line_bot_api.reply_message(event.reply_token, message)
    elif event.postback.data=="postback3.5":
        msg1=["text","末期病人靈性層面的問題是很複雜的，病人可能對生命的意義、生病所帶來的各種痛苦、死後生命的去向產生質疑。此刻病人特別需要周圍親人的關愛，以及提供靈性層面的關懷。\n\n有鑑於此，安寧照顧團隊中可設專屬的牧靈人員，靈性照顧是需要安排的，是需要儀典的，也需要專業知識的加入。牧靈人員為末期病人及家屬提供靈性服務。"]
        msg2=["text","靈性服務內容:\n\n1.提供病人在人生意義、愛與歸屬上尋得滿足。\n2.病患因痛苦所產生的各種人生疑惑、宗教信仰的困惑，提供宗教性的解答，並協助病患瞭解今生、來世之後之路，坦然無懼的面對死亡。\n3.協助病患解除不安、怨恨、罪惡等感覺，能夠寬恕別人與蒙獲寬恕，尋求釋放與獲得心靈的平安。\n4.執行宗教性懺悔或彌留時刻之祝福等儀式。儀典有心靈沉澱的作用，不只是對病人，對親人情緒的穩定也有幫助。\n5.協助喪葬禮儀，並提供完整的助喪服務。\n\n病患逝世後定時之追思、哀悼禮儀的執行與安排。令人感動的聚會是一種生命的體驗，許多人會因此而省思自己的人生目標與生命方向。"]
        msg4=["text","如果你還有其他問題，可以從下方的圖卡選擇或從主選單內挑選其它情境，以獲得需要的資訊。"]
        msg5=["flex","靈性需求",Flex3Message]
        pack=[msg1,msg2,msg4,msg5]      
        message=MessagesPacker(pack)
        line_bot_api.reply_message(event.reply_token, message)
        
    elif event.postback.data=="postback3.6":
        msg1=["text","面對善終，正向的態度與情緒是必要的，以下陳列能幫助病人和家屬從容面對死亡的方法。\n\n1.談論：勿隱瞞病情，談論有關疾病之事。\n2.接受：接受死亡也是生命的一部份，平靜地將每一天都過得更有意義。\n3.感念：感念每一天都是最好的安排，為日子中微不足道的行為給予感謝之意。\n4.認知：認知到生命並非完美，世事並非盡如人意。\n5.祈禱：祈禱禮佛，將不足展現於神的面前。\n6.學習：學習生命的不完美，與死亡共存。\n7.關係：將身邊的親朋好友置於舒服的關係，讓自己的心情落於平靜穩定，接受事實。\n8.安排：為將來做適合的安排，並與家人共同達成協議。\n9.設定：設定新目標，發現生活的意義。\n10.討論：與家人共同討論、抒發情緒。\n"]
        msg2=["text","面對死亡前可以與病人討論的內容\n\n相片：\n平時生活照多收集，生活上點滴，收集相冊作為日後紀念。\n半身正面彩色照（放大12 吋）以備葬禮懸掛。\n\n生平記錄:\n出生年月日，出生地，兄弟子女情形、就學經過、就業經過、成長、專長等。\n\n遺囑：（在能說話時先交代）\n留給家人的座右銘、教導期望等。可以錄音、錄影、寫信等方法保留。\n財產分配或債務等之處理交代。\n\n衣服準備：（臨終時穿著）\n整潔的內外衣褲各一套（依病人的喜好準備），及紙尿褲（避免弄髒衣服），以備臨終時換上，如要冰入冰櫃，可多準備一套，以備入殮時更換。（可先和葬儀社討論）\n高齡者可準備壽衣。（傳統習俗）"]
        msg4=["text","如果你還有其他問題，可以從下方的圖卡選擇或從主選單內挑選其它情境，以獲得需要的資訊。"]
        msg5=["flex","面對死亡",Flex3Message]
        pack=[msg1,msg2,msg4,msg5]      
        message=MessagesPacker(pack)
        line_bot_api.reply_message(event.reply_token, message)
    elif event.postback.data=="postback4.1":
        msg1=["text","哀傷期會出現否認（不相信事實）、生氣（責怪別人或自己）或強烈的沮喪。\n哀傷期如果延宕過久，就有可能出現一些病態性反應，如：憂鬱症、創傷後壓力症候群或急性精神病反應。\n萬一發現自己，陷入情緒低潮而無法自拔，或有任何不能理解的狀態時，可尋求專業人員協談。\n\n「悲傷輔導」是藉由支持團體、醫院社工、靈性團體、心理師，來幫助家屬平順地度過悲傷期，面對生命重拾自己。"]
        msg4=["text","如果你還有其他問題，可以從下方的圖卡選擇或從主選單內挑選其它情境，以獲得需要的資訊。"]
        msg5=["flex","悲傷輔導",Flex4Message]
        pack=[msg1,msg4,msg5]      
        message=MessagesPacker(pack)
        line_bot_api.reply_message(event.reply_token, message)

    elif event.postback.data=="postback4.2":
        msg1=["image","https://i.imgur.com/c6XQ5v2.png"]
        msg2=["image","https://i.imgur.com/d4mdFvy.png"]
        msg4=["text","如果你還有其他問題，可以從下方的圖卡選擇或從主選單內挑選其它情境，以獲得需要的資訊。"]
        msg5=["flex","悲傷輔導路徑",Flex4Message]
        pack=[msg1,msg2,msg4,msg5]      
        message=MessagesPacker(pack)
        line_bot_api.reply_message(event.reply_token, message)
    elif event.postback.data=="postback4.3":
        msg1=["text","藝術治療是一種結合創造性藝術表達和心理治療的助人專業。藝術治療提供一種非語言的溝通方式、安全不具威脅性的表達空間，以協助個案自我表現、自我溝通和自 我成長的機會。\n\n藝術治療師及當事人藉由作品看故事、說故事，可以 有效降低當事人在面對失落悲傷的防衛心理，或是不知從何談起的困境。由藝術創作所建立之安全信任的過渡空間，讓當事人在其中藉由媒材表達出內在隱而未顯的失落、悲傷。\n\n藝術治療範例可點選此連結:\nhttps://youtu.be/MtLp6RIxXSw"]
        msg2=["text","音樂治療是個專業的醫療相關職業，其中音樂被使用於治療關係中，以解決個案的生理、情緒、認知及社交需求。在評估每位個案後，合格的音樂治療師會提供需要的治療，包含創作、歌唱、律動及聆聽音樂。透過治療情境中的音樂互動，個案的能力被強化及轉移至生活中的其他面向。此外，音樂治療可以幫助不便運用口語表達的人，來有效的表達自己。許多科學研究亦證實音樂治療的療效，例如：音樂治療可以促進肢體運用達到全身性的復健、提高人們參與治療的動力、支持個案及其家人的情緒、及提供情緒表達的途徑。\n\n音樂治療範例可參考此連結:\nhttps://www.youtube.com/watch?v=k7SSGbhZlyA"]
        msg4=["text","如果你還有其他問題，可以從下方的圖卡選擇或從主選單內挑選其它情境，以獲得需要的資訊。"]
        msg5=["flex","藝術與音樂治療",Flex4Message]
        pack=[msg1,msg2,msg4,msg5]      
        message=MessagesPacker(pack)
        line_bot_api.reply_message(event.reply_token, message)


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
    
    
    

