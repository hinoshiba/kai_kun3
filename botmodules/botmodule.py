from slackbot.bot import respond_to
from slackbot.bot import listen_to
from slackbot.bot import default_reply
import slackbot_settings

from github import Github

# メンションあり応答
@respond_to('こんにちは')
def greeting(message):
    # メンションして応答
    message.reply('こんにちは!')

# メンションなし応答
@listen_to('もうかりまっか')
def greeting(message):
    message.send('ぼちぼちでんな')

@listen_to('いっしゅ')
def greeting(message):
    g = Github(slackbot_settings.GITHUB_TOKEN)
    repo = g.get_repo("hinoshiba/shopping_list")
    open_issues = repo.get_issues(state='open')
    for issue in open_issues:
        message.send(issue.title)

#@default_reply
@listen_to(r'^.*$')
def default(message):
    text = message.body['text']
    channel = message.channel._client.channels[message.body['channel']]
    channel_name = channel['name']
    print(text)
    print(channel_name)

    g = Github(slackbot_settings.GITHUB_TOKEN)
    repo = g.get_repo("hinoshiba/Test")

    open_issues = repo.get_issues(state='open')
    for issue in open_issues:
        if issue.title == text:
            message.reply(text + 'は、既に買う予定です！')
            return

    closed_issues = repo.get_issues(state='closed')
    for issue in closed_issues:
        if issue.title != text:
            continue

        issue.edit(state='open')
        message.reply(text + 'を買う予定にしました！')
        return

    repo.create_issue(title=text)
    message.reply(text + 'を買い物リストに追加しました')
