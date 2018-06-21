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

access_token = "xxxxxxxxx" # place your own access token here

def main():
    df = pd.read_csv('email_short.csv')

    conn = pymysql.connect(host='127.0.0.1', user='ght', db='ghtorrent')

    active_since_list = []
    total_commits_list = []
    total_issue_report_list = []
    total_issue_comment_list = []
    project_info_commit_output_list = []
    project_info_pull_request_proposal_output_list = []
    project_info_issue_report_output_list = []
    comment_list = []

    # remove empty logins
    df = df[df.login_id.str.strip() != '']

    for login in df['login_id']:
        print(login)
        active_since, total_commits, total_issue_report, total_issue_comment, project_info_commit_output, project_info_pull_request_proposal_output, project_info_issue_report_output, comment = Get_stats_for_user(login, conn)
        active_since_list.append(active_since)
        total_commits_list.append(total_commits)
        total_issue_report_list.append(total_issue_report)
        total_issue_comment_list.append(total_issue_comment)
        project_info_commit_output_list.append(project_info_commit_output)
        project_info_pull_request_proposal_output_list.append(project_info_pull_request_proposal_output)
        project_info_issue_report_output_list.append(project_info_issue_report_output)
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
    if df['login_id'].count() == len(project_info_commit_output_list):
        df['project_info_commit_output'] = pd.Series(project_info_commit_output_list, index=df.index)
    if df['login_id'].count() == len(project_info_pull_request_proposal_output_list):
        df['project_info_pull_request_proposal_output'] = pd.Series(project_info_pull_request_proposal_output_list, index=df.index)
    if df['login_id'].count() == len(project_info_issue_report_output_list):
        df['project_info_issue_report_output'] = pd.Series(project_info_issue_report_output_list, index=df.index)
    if df['login_id'].count() == len(comment_list):
        df['comment'] = pd.Series(comment_list, index=df.index)

    df.to_csv("full_info_short.csv", sep=',', encoding='utf-8')


def Get_stats_for_user(login_id, db_conn):
    cur = db_conn.cursor()
    # priority
    # platform

    # user id - login
    # already in excel

    # email address
    # already in excel

    # active since
    active_since = -1
    sql_query_active_since = "select created_at, id from users where login='" + login_id + "'"
    cur.execute(sql_query_active_since)

    first_row = cur.fetchone()
    active_since = first_row[0]
    user_id = first_row[1]
    # print("active since: " + str(active_since))
    # print("user id: " + str(user_id))

    # total commit - OK
    total_commits = -1
    sql_query_total_commit = "select count(*) from commits where author_id=" + str(user_id)
    cur.execute(sql_query_total_commit)

    first_row = cur.fetchone()
    total_commits = first_row[0]
    # print("total commits: " + str(total_commits))

    # total issue report
    total_issue_report = -1
    sql_query_total_issue_report = " select count(*) from issues where reporter_id =" + str(user_id)
    cur.execute(sql_query_total_issue_report)

    first_row = cur.fetchone()
    total_issue_report = first_row[0]
    # print("total issue report: " + str(total_issue_report))

    # total issue comment
    total_issue_comment = -1
    sql_query_total_issue_comment = "select count(*) from issue_comments where user_id=" + str(user_id)
    cur.execute(sql_query_total_issue_comment)

    first_row = cur.fetchone()
    total_issue_comment = first_row[0]
    # print("total issue comment: " + str(total_issue_comment))

    # PROJECT BASED
    # number of commits
    project_info_commit_list = []
    sql_query_project_commit = "select project_id, count(*) as commit_count from commits where author_id=" + str(user_id) + " group by project_id order by commit_count desc"
    cur.execute(sql_query_project_commit)

    project_commits_list = cur.fetchall()
    for project_based_commit in project_commits_list:
        if project_based_commit[0] is not None:
            sql_query_project = "select id, name, url from projects where id =" + str(project_based_commit[0])
            cur.execute(sql_query_project)

            first_row = cur.fetchone()
            project_info_commit_str = "project_id: " + str(first_row[0]) + " ," + \
                                      "project_name: " + str(first_row[1]) + " ," + \
                                      "url: " + str(first_row[2]) + " ," + \
                                      "commit_count: " + str(project_based_commit[1])
            project_info_commit_list.append(project_info_commit_str)

    project_info_commit_output = '\n'.join(project_info_commit_list)


    # number of pull request proposals
    # 37447015
    # select forked_from, count(*) as pull_request_proposal_count from projects inner join (select tableA.*, tableB.id as tableB_id from (select * from pull_request_commits inner join commits on pull_request_commits.commit_id = commits.id where commits.author_id = 8389) as tableA left join  (select * from pull_request_history where action = 'merged') as tableB on tableA.pull_request_id = tableB.pull_request_id and tableA.author_id = tableB.actor_id where tableB.id is NULL) as tableC on projects.id = tableC.project_id group by forked_from order by pull_request_proposal_count desc;
    # select forked_from, count(*) as pull_request_proposal_count from projects inner join (select tableC.*, tableD.id as tableD_id from (select tableA.* from (select * from pull_request_commits inner join commits on pull_request_commits.commit_id = commits.id where commits.author_id = 8389) as tableA left join (select * from pull_request_commits inner join commits on pull_request_commits.commit_id = commits.id where commits.author_id = 8389) as tableB on tableA.commit_id = tableB.commit_id and tableA.pull_request_id < tableB.pull_request_id where tableB.pull_request_id is NULL) as tableC left join  (select * from pull_request_history where action = 'merged') as tableD on tableC.pull_request_id = tableD.pull_request_id and tableC.author_id = tableD.actor_id where tableD.id is NULL) as tableE on projects.id = tableE.project_id group by forked_from order by pull_request_proposal_count desc;
    #  project_info_pull_request_proposals_list = []
    sql_query_project_pull_requset_proposals = "select forked_from, count(*) as pull_request_proposal_count " + \
                                               "from projects inner join " + \
                                               "(select tableA.*, tableB.id as tableB_id from " + \
                                               "(select * from pull_request_commits inner join commits " + \
                                               "on pull_request_commits.commit_id = commits.id " + \
                                               "where commits.author_id = " + str(user_id) + ") as tableA left join" + \
                                               " (select * from pull_request_history where action = 'merged') as tableB" + \
                                               " on tableA.pull_request_id = tableB.pull_request_id " + \
                                               "and tableA.author_id = tableB.actor_id" + \
                                               " where tableB.id is NULL) as tableC " + \
                                               "on projects.id = tableC.project_id " + \
                                               "group by forked_from order by pull_request_proposal_count desc"

    cur.execute(sql_query_project_pull_requset_proposals)

    project_pull_request_proposals_list = cur.fetchall()
    for project_based_pull_request_proposal in project_pull_request_proposals_list:
        if project_based_pull_request_proposal[0] is not None:
            sql_query_project = "select id, name, url from projects where id =" + str(project_based_pull_request_proposal[0])
            cur.execute(sql_query_project)

            first_row = cur.fetchone()
            project_info_pull_request_proposal_str = "project_id: " + str(first_row[0]) + " ," + \
                                                     "project_name: " + str(first_row[1]) + " ," + \
                                                     "url: " + str(first_row[2]) + " ," + \
                                                     "commit_count: " + str(project_based_pull_request_proposal[1])
            project_info_pull_request_proposals_list.append(project_info_pull_request_proposal_str)

    project_info_pull_request_proposal_output = '\n'.join(project_info_pull_request_proposals_list)


    # REPO BASED
    # issue report
    # select repo_id, count(*) issue_reported_count from issues where reporter_id = 8389 group by repo_id;
    project_info_issue_report_list = []
    sql_query_project_issue_report = "select repo_id, count(*) issue_reported_count from issues where reporter_id = " + str(user_id) + " group by repo_id order by issue_reported_count desc"
    cur.execute(sql_query_project_issue_report)

    project_issue_reports_list = cur.fetchall()
    for project_based_issue_report in project_issue_reports_list:
        if project_based_issue_report[0] is not None:
            sql_query_project = "select id, name, url from projects where id =" + str(project_based_issue_report[0])
            cur.execute(sql_query_project)

            first_row = cur.fetchone()
            project_info_issue_report_str = "project_id: " + str(first_row[0]) + " ," + \
                                            "project_name: " + str(first_row[1]) + " ," + \
                                            "url" + str(first_row[2]) + " ," + \
                                            "commit_count: " + str(project_based_issue_report[1])
            project_info_issue_report_list.append(project_info_issue_report_str)

    project_info_issue_report_output = '\n'.join(project_info_issue_report_list)

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
    return active_since, total_commits, total_issue_report, total_issue_comment, project_info_commit_output, project_info_pull_request_proposal_output, project_info_issue_report_output, comment


if __name__ == "__main__":
    main()
