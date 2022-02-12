from slackbot.bot import respond_to
from slackbot.bot import listen_to
from slackbot.bot import default_reply
import time
import random
import slackbot_settings

from github import Github

@respond_to(r'^.*$')
def response_run_dispacher(message):
    channel_name = get_channelName(message)
    dispacher(channel_name, False, message)

@listen_to(r'^.*$')
def listen_run_dispacher(message):
    channel_name = get_channelName(message)
    dispacher(channel_name, True, message)

def dispacher(channel_name, default, message):
    if channel_name == slackbot_settings.CHANNEL_SHOPPINGLIST:
        shop_dispacher(default, message)
        return
    elif channel_name == slackbot_settings.CHANNEL_MENURND:
        menurand_dispacher(default, message)
        return
    elif get_args(message)[0] == "help":
        message.reply("これを見な！: https://github.com/hinoshiba/kai_kun3/blob/master/docs/README.md")

    else:
        reply_unkown(message)
        return

def menurand_dispacher(default, message):
    if default:
        search_menu(message, False)
        return
    search_menu(message, True)
    return

def search_menu(message, absolutely):
    if absolutely:
        message.send("その材料で作れるのは....")
        time.sleep(0.5)
    else:
        message.send("その材料+アルファで作れるのは....")
        time.sleep(0.5)

    g = Github(slackbot_settings.GITHUB_TOKEN)
    repo = g.get_repo(slackbot_settings.REPO_MENURND)

    issues = []
    kw = message.body['text']
    if slackbot_settings.MAGICWORD in kw:
        message.send("anyモードで探すぜ")
        for word in kw.split():
            issues.extend(repo.legacy_search_issues(state="open", keyword=word))
    else:
        issues.extend(repo.legacy_search_issues(state="open", keyword=kw))

    checked = []
    menues = []
    for issue in issues:
        if issue.number in checked:
            continue
        if issue.state != "open":
            checked.append(issue.number)
            continue
        try:
            name = issue.assignee.login
        except:
            checked.append(issue.number)
            continue
        if not name in slackbot_settings.TRUSTED_USERNAME:
            checked.append(issue.number)
            continue

        url = slackbot_settings.URL_GITHUB + issue.url.replace('https://api.github.com/repos', '')
        menu = issue.title + " : " + url
        if absolutely:
            match = True
            for com in issue.get_comments():
                c_user = com.user.login
                if not c_user in slackbot_settings.TRUSTED_USERNAME:
                    continue
                if not com.body in kw:
                    match = False
                    break
            if match:
                menues.append(menu)

            checked.append(issue.number)
            continue
        checked.append(issue.number)
        menues.append(menu)

    if len(menues) < 1:
        message.send("....なにも...ない....。\n https://github.com/hinoshiba/iCH1f-menues/issues に、メニューを追加するんだ!!")
        time.sleep(0.5)
        return

    for menu in random.sample(menues, len(menues)):
        message.send(menu)
        time.sleep(0.5)
    message.send("....だぜ！")

    if len(menues) < 2:
        return
    time.sleep(0.5)
    message.send("今回のオレのおすすめは....\n" + random.choice(menues) + " だ！")

def shop_dispacher(default, message):
    args = get_args(message)

    if default:
        if len(args) < 1:
            message.reply("operation error.")
            return
        op_open(message, args[0])
        return

    if args[0] in ["help"]:
        message.reply("これを見な！: https://github.com/hinoshiba/kai_kun3/blob/master/docs/README.md")
        return

    if args[0] in ["add", "追加"]:
        if len(args) < 2:
            message.reply("operation error. USAGE: @kai add <食材名>")
            return
        op_open(message, args[1])
        return

    elif args[0] in ["list", "一覧"]:
        if len(args) < 2:
            op_list(message, "open")
            return

        state = ""
        if args[1] in ["all", "全部"]:
            state = "all"
        elif args[1] in ["closed", "済"]:
            state = "closed"

        if state == "":
            message.reply("operation error. USAGE: @kai list [all|close]")
            return

        op_list(message, state)
        return

    elif args[0] in ["del", "削除"]:
        if len(args) < 2:
            message.reply("operation error. USAGE: @kai del <食材名>")
            return
        op_del(message, args[1])
        return

    elif args[0] in ["close", "済"]:
        if len(args) < 2:
            message.reply("operation error. USAGE: @kai close <食材名>")
            return
        op_close(message, args[1])
        return

    reply_unkown(message)

def op_list(message, state):
    g = Github(slackbot_settings.GITHUB_TOKEN)
    repo = g.get_repo(slackbot_settings.REPO_SHOPPINGLIST)

    cnt = 0
    issues = repo.get_issues(state=state)
    for issue in issues:
        if is_destroy(issue):
            continue

        location = ""
        try:
            for label in issue.labels:
                if location == "":
                    location = "＠"
                else:
                    location += ", "
                location += label.name
        except AttributeError:
            pass

        time.sleep(0.5)
        message.send(issue.title + location)
        cnt += 1
        if cnt >= 10:
            time.sleep(1)
            cnt = 0

    message.reply("以上！")

def op_del(message, target):
    g = Github(slackbot_settings.GITHUB_TOKEN)
    repo = g.get_repo(slackbot_settings.REPO_SHOPPINGLIST)

    open_issues = repo.get_issues(state='all')
    for issue in open_issues:
        if issue.title != target:
            continue
        issue.edit(labels=['destroy'], state='closed')
        message.reply('「' + target + '」を消したぜ！')
        return

    message.reply('「' + target + '」？ そんなの消しようが無い！')

def op_close(message, target):
    g = Github(slackbot_settings.GITHUB_TOKEN)
    repo = g.get_repo(slackbot_settings.REPO_SHOPPINGLIST)

    open_issues = repo.get_issues(state='open')
    for issue in open_issues:
        if issue.title != target:
            continue
        issue.edit(state='closed')
        message.reply('「' + target + '」買った！')
        return

    closed_issues = repo.get_issues(state='closed')
    for issue in closed_issues:
        if issue.title != target:
            continue

        message.reply('「' + target + '」もう買った！')
        return

    message.reply('「' + target + '」？ そんなの無い！')

def op_open(message, target):
    g = Github(slackbot_settings.GITHUB_TOKEN)
    repo = g.get_repo(slackbot_settings.REPO_SHOPPINGLIST)

    open_issues = repo.get_issues(state='open')
    for issue in open_issues:
        if issue.title != target:
            continue
        message.reply('「' + target + '」は、もう買う予定！')
        return

    closed_issues = repo.get_issues(state='closed')
    for issue in closed_issues:
        if issue.title != target:
            continue

        if is_destroy(issue):
            issue.delete_labels()
            issue.edit(state='open')
        else:
            issue.edit(state='open')
        message.reply('「' + target + '」を買う予定に変更！')
        return

    repo.create_issue(title=target)
    message.reply('「' + target + '」を新しく買い物リストに追加！')

def reply_unkown(message):
    message.reply('undefined operation. show "@kai help"')

def get_channelName(message):
    try:
        text = message.body['text']
        channel = message.channel._client.channels[message.body['channel']]
        return channel['name']
    except:
        return ""

def get_args(message):
    text = message.body['text']
    return text.split()

def is_destroy(issue):
    try:
        for lb in issue.labels:
            if lb.name == 'destroy':
                return True
    except AttributeError:
        pass

    return False
