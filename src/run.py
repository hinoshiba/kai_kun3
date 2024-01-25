from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from github import Github

import slackbot_settings
import botmodules

app = App(token=slackbot_settings.SLACK_BOT_TOKEN)

@app.event("app_mention")
def men_reply(event, say):
    print("mention", event)
    botmodules.dispacher(app, event, say, True)

@app.event("message")
def msg_reply(event, say):
    print("just msg", event)
    if has_mention_to_bot(event):
        print("has mention")
        return
    botmodules.dispacher(app, event, say, False)

def has_mention_to_bot(evt):
    print(slackbot_settings.SLACK_BOT_ID)
    print(evt["text"])
    return slackbot_settings.SLACK_BOT_ID in evt["text"]

def main():
    handler = SocketModeHandler(
        app,
        slackbot_settings.SLACK_APP_TOKEN,
    )
    handler.start()

if __name__ == "__main__":
    print('starting slackbot')
    main()
