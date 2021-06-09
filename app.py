import os
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('UixFncuOGHnCLGppaaAfAw+iyhCZsBAIu7FOAY2yMdsPTVQSK+kMrN7wNiBSZnIgKsgocsG6Z+ez4AlpIbxi/X1WdorF40OeB+zdkBf3RGzfSnJ+1qXb268NytL2J4yBV1h5IacPEm1rlpNESmFE5QdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('93ee5830c1026467b3a3a46f6f228118')


@app.route("/callback", methods=['POST'])
def callback():
    # Get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # Get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # Handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    """ Here's all the messages will be handled and processed by the program """
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
