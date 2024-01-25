import env

REPO_SHOPPINGLIST = "hinoshiba/shopping_list"
CHANNEL_SHOPPINGLIST = "shoppinglist"
#REPO_SHOPPINGLIST = "hinoshiba/Test"
#CHANNEL_MENURND = "bot_test"

DEFAULT_REPLY = "その言葉の意味は知りません"

SLACK_APP_TOKEN = env.SlackAppToken
SLACK_BOT_TOKEN = env.SlackBotToken
SLACK_BOT_ID = env.SlackBotId

GITHUB_TOKEN = env.GithubApiToken
PLUGINS = ['slackbot.plugins', 'botmodules']
