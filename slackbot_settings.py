import env

API_TOKEN = env.SlackApiToken
GITHUB_TOKEN = env.GithubApiToken

DEFAULT_REPLY = "その言葉の意味は知りません"
PLUGINS = [
    'slackbot.plugins',
    'botmodules',
]
