import os, random
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from linebot.exceptions import InvalidSignatureError

app = Flask(__name__)

line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))

TARGET_USER_ID = os.getenv('TARGET_USER_ID')

REPLIES_MENTION = [
    "是，行，必須的!",
    "是的長官",
    "是的元首(45°",
    "damn~",
    "當然",
    "ok",
    "好啊",
    "喔好吧",
    "行",
    "行",
    "行。"
]

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers.get('X-Line-Signature','')
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message
    text = msg.text or ""

    mention = getattr(msg, 'mention', None)
    if mention and hasattr(mention, 'mentionees'):
        for m in mention.mentionees:
            if m.user_id == TARGET_USER_ID:
                reply = random.choice(REPLIES_MENTION)
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply))
                return

    if "傻逼" in text:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="我不是"))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
