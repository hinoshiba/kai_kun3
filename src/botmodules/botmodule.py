import time
import slackbot_settings
import re
import traceback

from github import Github

def do_res(evt, say, msg):
    say(text=msg, thread_ts=evt["ts"], channel=evt["channel"])

def reply_help(evt, say):
    msg = "これを見な！: https://github.com/hinoshiba/kai_kun3/blob/master/docs/README.md"
    do_res(evt, say, msg)

def reply_unkown(evt, say):
    msg = 'undefined operation. show "@kai help"'
    do_res(evt, say, msg)

def get_msg_without_slackid(evt):
    return re.sub("<@\w+>\s*", "", evt["text"])

def dispacher(app, evt, say, is_mention):
    ch_info = app.client.conversations_info(channel=evt["channel"])
    channel_name = ch_info["channel"]["name"]

    try:
        if channel_name == slackbot_settings.CHANNEL_SHOPPINGLIST:
            shop_dispacher(evt, say, is_mention)
            return
        if not(is_mention):
            return
        if get_msg_without_slackid(evt) == "help":
            reply_help(evt, say)
            return
        reply_unkown(evt, say)
    except Exception as e:
        traceback.print_exc()
        do_res(evt, say, "エラーが起きたから、もうダメぴょん。もう一回試してくれ...。")

def shop_dispacher(evt, say, is_mention):
    args = get_msg_without_slackid(evt).split()

    if not(is_mention):
        if len(args) < 1:
            do_res(evt, say, "operation error.")
            return
        op_open(evt, say, args[0])
        return

    if args[0] in ["help"]:
        reply_help(evt, say)
        return

    if args[0] in ["add", "追加"]:
        if len(args) < 2:
            do_res(evt, say, "operation error. USAGE: @kai add <食材名>")
            return
        op_open(evt, say, args[1])
        return

    if args[0] in ["list", "一覧"]:
        if len(args) < 2:
            op_list(evt, say, "open")
            return

        state = ""
        if args[1] in ["all", "全部"]:
            state = "all"
        elif args[1] in ["closed", "済"]:
            state = "closed"

        if state == "":
            do_res(evt, say, "operation error. USAGE: @kai list [all|close]")
            return

        op_list(evt, say, state)
        return

    if args[0] in ["del", "削除"]:
        if len(args) < 2:
            do_res(evt, say, "operation error. USAGE: @kai del <食材名>")
            return
        op_del(evt, say, args[1])
        return

    if args[0] in ["close", "済"]:
        if len(args) < 2:
            do_res(evt, say, "operation error. USAGE: @kai close <食材名>")
            return
        op_close(evt, say, args[1])
        return

    reply_unkown(evt, say)

def op_list(evt, say, state):
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
        do_res(evt, say, issue.title + location)
        cnt += 1
        if cnt >= 10:
            time.sleep(1)
            cnt = 0

    do_res(evt, say, "以上！")

def op_del(evt, say, target):
    g = Github(slackbot_settings.GITHUB_TOKEN)
    repo = g.get_repo(slackbot_settings.REPO_SHOPPINGLIST)

    open_issues = repo.get_issues(state='all')
    for issue in open_issues:
        if issue.title != target:
            continue
        issue.edit(labels=['destroy'], state='closed')
        do_res(evt, say, '「' + target + '」を消したぜ！')
        return

    do_res(evt, say, '「' + target + '」？ そんなの消しようが無い！')

def op_close(evt, say, target):
    g = Github(slackbot_settings.GITHUB_TOKEN)
    repo = g.get_repo(slackbot_settings.REPO_SHOPPINGLIST)

    open_issues = repo.get_issues(state='open')
    for issue in open_issues:
        if issue.title != target:
            continue
        issue.edit(state='closed')
        do_res(evt, say, '「' + target + '」買った！')
        return

    closed_issues = repo.get_issues(state='closed')
    for issue in closed_issues:
        if issue.title != target:
            continue

        do_res(evt, say, '「' + target + '」もう買った！')
        return

    do_res(evt, say, '「' + target + '」？ そんなの無い！')

def op_open(evt, say, target):
    g = Github(slackbot_settings.GITHUB_TOKEN)
    repo = g.get_repo(slackbot_settings.REPO_SHOPPINGLIST)

    open_issues = repo.get_issues(state='open')
    for issue in open_issues:
        if issue.title != target:
            continue
        do_res(evt, say, '「' + target + '」は、もう買う予定！')
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
        do_res(evt, say, '「' + target + '」を買う予定に変更！')
        return

    repo.create_issue(title=target)
    do_res(evt, say, '「' + target + '」を新しく買い物リストに追加！')

def is_destroy(issue):
    try:
        for lb in issue.labels:
            if lb.name == 'destroy':
                return True
    except AttributeError:
        pass

    return False
