from __future__ import print_function
import pymysql
import pandas as pd
import requests
import json


# # mostly contributed project - pushEvent and number of commits in the push =distinct_size, PullRequestEvent
# #  commit to a project’s default branch or the gh-pages branch, open an issue, and propose a Pull Request
# # total commit - pushEvent and number of commits in the push =distinct_size
# # total issue report - issuesEvent and action = opened or reopened
# # total issue comment - IssueCommentEvent and action = created or edited

access_token = "xxxxxx" # put you access token here

def main():
    df = pd.read_csv('email_1.csv')

    conn = pymysql.connect(host='127.0.0.1', user='ght', db='ghtorrent')

    active_since_list = []
    total_commits_list = []
    total_issue_report_list = []
    total_issue_comment_list = []
    comment_list = []

    # remove empty logins
    df = df[df.login_id.str.strip() != '']

    for login in df['login_id']:
        print(login)
        active_since, total_commits, total_issue_report, total_issue_comment, comment = Get_stats_for_user(login, conn)
        active_since_list.append(active_since)
        total_commits_list.append(total_commits)
        total_issue_report_list.append(total_issue_report)
        total_issue_comment_list.append(total_issue_comment)
        comment_list.append(comment)

    conn.close()

    if df['login_id'].count() == len(active_since_list):
        df['active_since'] = pd.Series(active_since_list, index=df.index)
    if df['login_id'].count() == len(total_commits_list):
        df['total_commits'] = pd.Series(total_commits_list, index=df.index)
    if df['login_id'].count() == len(total_issue_report_list):
        df['total_issue_report'] = pd.Series(total_issue_report_list, index=df.index)
    if df['login_id'].count() == len(total_issue_comment_list):
        df['total_issue_comment'] = pd.Series(total_issue_comment_list, index=df.index)
    if df['login_id'].count() == len(comment_list):
        df['comment'] = pd.Series(comment_list, index=df.index)

    df.to_csv("full_info_1.csv", sep=',', encoding='utf-8')


def Get_stats_for_user(login_id, db_conn):
    cur = db_conn.cursor()
    # priority
    # platform

    # user id - login
    # already in excel

    # email address
    # already in excel

    # active since
    sql_query_active_since = "select created_at, id from users where login='" + login_id + "'"
    cur.execute(sql_query_active_since)

    first_row = cur.fetchone()
    active_since = first_row[0]
    user_id = first_row[1]
    # print("active since: " + str(active_since))
    # print("user id: " + str(user_id))

    # # most contributed project
    # most_contributed_proj = ""
    # # project and commit count - dict_commit_count: key=project id, value=commit count
    # dict_commit_count = {}
    # sql_query_commit_count = "select project_id, count(*) as cnt from commits where committer_id =" + str(
    #     user_id) + " group by project_id"
    # cur.execute(sql_query_commit_count)
    #
    # for row in cur:
    #     dict_commit_count[row[0]] = row[1]
    #     # print(row)
    #
    # # project and commit contribution
    # # print(dict_commit_count)
    #
    # # repo and pull request proposal count- dict_pull_count: key repo id, value = pull count
    # dict_pull_count = {}
    # sql_query_pull_count = ""
    #
    # # repo and issue opened count - dict_issue_count: key=repo id, value=issue opened count
    # dict_issue_count = {}
    # sql_query_issue_count = "select repo_id, count(*) as cnt from issues where reporter_id =" + str(
    #     user_id) + " group by repo_id;"
    # cur.execute(sql_query_issue_count)
    #
    # for row in cur:
    #     dict_issue_count[row[0]] = row[1]

    # print(dict_issue_count)

    # total commit
    sql_query_total_commit = "select count(*) from commits where committer_id=" + str(user_id)
    cur.execute(sql_query_total_commit)

    first_row = cur.fetchone()
    total_commits = first_row[0]
    # print("total commits: " + str(total_commits))

    # total issue report
    sql_query_total_issue_report = " select count(*) from issues where reporter_id =" + str(user_id)
    cur.execute(sql_query_total_issue_report)

    first_row = cur.fetchone()
    total_issue_report = first_row[0]
    # print("total issue report: " + str(total_issue_report))

    # total issue comment
    sql_query_total_issue_comment = "select count(*) from issue_comments where user_id=" + str(user_id)
    cur.execute(sql_query_total_issue_comment)

    first_row = cur.fetchone()
    total_issue_comment = first_row[0]
    # print("total issue comment: " + str(total_issue_comment))

    # is focus on usability
    # speculated role
    # comments
    # bio information is not in table, have to use GitHub API
    comment = ""
    request_str = "https://api.github.com/users/" + login_id + '?access_token=' + access_token
    r = requests.get(request_str)
    if (r.ok):
        repoItem = json.loads(r.text or r.content)
        comment = repoItem['bio']
    # print(comment)

    cur.close()
    return active_since, total_commits, total_issue_report, total_issue_comment, comment


if __name__ == "__main__":
    main()
