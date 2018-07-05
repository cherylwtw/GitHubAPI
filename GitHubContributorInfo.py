from __future__ import print_function
import pandas as pd
import requests
import json
import subprocess
import os
import time


access_token = "xxxxxx" #put your access token here

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def stepOne():
    # read repo list
    df = pd.read_csv('repo_list.csv')

    df = df[df.repo_name.str.strip() != '']

    owner_list = []
    html_url_list = []
    description_list = []
    contributor_list = []

    total_contributor_list = []

    for repo in df['repo_name']:
        print(repo)
        # get repo data
        request_str = "https://api.github.com/repos/" + repo + "?access_token=" + access_token
        r = requests.get(request_str)
        repoItem = json.loads(r.text or r.content)

        repo_owner = repoItem['owner']['login']
        repo_html_url = repoItem['html_url']
        repo_description = repoItem['description']

        # get contributor data
        repo_contributor_list = []
        for page in range(1, 11):
            if page == 10:
                print(bcolors.WARNING + repo + "needs more contributor page" + bcolors.ENDC)

            request_str = "https://api.github.com/repos/" + repo + "/contributors?per_page=100&page=" + str(page) + "&access_token=" + access_token
            r = requests.get(request_str)
            if (r.ok):
                contributors = json.loads(r.text or r.content)

                if len(contributors) == 0:
                    break

                for contributor in contributors:
                    contributor_login = contributor['login']
                    if contributor_login not in repo_contributor_list:
                        repo_contributor_list.append(contributor_login)
                    if contributor_login not in total_contributor_list:
                        total_contributor_list.append(contributor_login)

        repo_contributors = '\n'.join(repo_contributor_list)

        owner_list.append(repo_owner)
        html_url_list.append(repo_html_url)
        contributor_list.append(repo_contributors)
        description_list.append(repo_description)

    if df['repo_name'].count() == len(owner_list):
        df['owner'] = pd.Series(owner_list, index=df.index)
    if df['repo_name'].count() == len(html_url_list):
        df['html_url'] = pd.Series(html_url_list, index=df.index)
    if df['repo_name'].count() == len(contributor_list):
        df['contributors'] = pd.Series(contributor_list, index=df.index)
    if df['repo_name'].count() == len(description_list):
        df['description'] = pd.Series(description_list, index=df.index)

    # output a repo data excel
    df.to_csv("repo_info.csv", sep=',', encoding='utf-8', index=False)

    # output contributors list
    composite_list = [total_contributor_list[x:x + 1000] for x in range(0, len(total_contributor_list), 1000)]
    print(composite_list)

    # split it into sub-files, cause only 5k/h requests allowed
    for idx, val in enumerate(composite_list):
        df_contributor = pd.DataFrame({'contributor': val})
        df_contributor.drop(df_contributor.columns[0], axis=1)
        df_contributor.to_csv("contributor_list_" + str(idx+1) + ".csv", sep=',', encoding='utf-8', index=False)

    # write the entire list for result checking
    df_total = pd.DataFrame({'contributor': total_contributor_list})
    df_total.drop(df_total.columns[0], axis=1)
    df_total.to_csv("contributor_list_total.csv", sep=',', encoding='utf-8', index=False)

# getting emails
def stepTwo(sub_file_num):
    # set access token envrionment variable
    os.environ["GH_EMAIL_TOKEN"] = access_token
    print(os.environ["GH_EMAIL_TOKEN"])

    # read contributor list
    df = pd.read_csv('contributor_list_' + str(sub_file_num) + '.csv')
    df = df[df.contributor.str.strip() != '']

    email_on_github_list = []
    email_on_npm_list = []
    email_from_recent_commits_list = []
    emails_from_owned_repo_recent_activity_list = []

    for contributor in df['contributor']:
        print(contributor)

        try:
            stdout = subprocess.check_output(["./github-email.sh", contributor])
        except subprocess.CalledProcessError as stdexc:
            print("error code", stdexc.returncode, stdexc.output)
            stdout = ""

        if stdout != "":
            stdoutList = stdout.decode("utf-8").split('\n')

            for idx, val in enumerate(stdoutList):
                if "Email on GitHub" in val:
                    githubEmailIdx = idx
                elif "Email on npm" in val:
                    npmEmailIdx = idx
                elif "Emails from recent commits" in val:
                    RecentCommitEmailIdx = idx
                elif "Emails from owned-repo recent activity" in val:
                    OwnedRepoEmailIdx = idx

            email_on_github_list.append('\n'.join(stdoutList[githubEmailIdx+1: npmEmailIdx-1]))
            email_on_npm_list.append('\n'.join(stdoutList[npmEmailIdx+1: RecentCommitEmailIdx-1]))
            email_from_recent_commits_list.append('\n'.join(stdoutList[RecentCommitEmailIdx+1: OwnedRepoEmailIdx-1]))
            emails_from_owned_repo_recent_activity_list.append('\n'.join(stdoutList[OwnedRepoEmailIdx+1: len(stdoutList)-1]))
        else:
            email_on_github_list.append("")
            email_on_npm_list.append("")
            email_from_recent_commits_list.append("")
            emails_from_owned_repo_recent_activity_list.append("")

    if df['contributor'].count() == len(email_on_github_list):
        df['email_on_github'] = pd.Series(email_on_github_list, index=df.index)
    if df['contributor'].count() == len(email_on_npm_list):
        df['email_on_npm'] = pd.Series(email_on_npm_list, index=df.index)
    if df['contributor'].count() == len(email_from_recent_commits_list):
        df['email_from_recent_commits'] = pd.Series(email_from_recent_commits_list, index=df.index)
    if df['contributor'].count() == len(emails_from_owned_repo_recent_activity_list):
        df['emails_from_owned_repo_recent_activity'] = pd.Series(emails_from_owned_repo_recent_activity_list, index=df.index)

    df.to_csv("email_info_" + str(sub_file_num) + ".csv", sep=',', encoding='utf-8', index=False)

# get personal info
def stepThree(sub_file_num):
    # read email info list
    df = pd.read_csv('email_info_' + str(sub_file_num) + '.csv')

    df = df[df.contributor.str.strip() != '']

    active_since_list = []
    company_list = []
    location_list = []
    bio_list = []

    for contributor in df['contributor']:
        print(contributor)
        request_str = "https://api.github.com/users/" + contributor + "?access_token=" + access_token
        r = requests.get(request_str)
        contributorItem = json.loads(r.text or r.content)

        active_since = contributorItem['created_at']
        company = contributorItem['company']
        location = contributorItem['location']
        bio = contributorItem['bio']

        active_since_list.append(active_since)
        company_list.append(company)
        location_list.append(location)
        bio_list.append(bio)

    if df['contributor'].count() == len(active_since_list):
        df['active_since'] = pd.Series(active_since_list, index=df.index)
    if df['contributor'].count() == len(company_list):
        df['company'] = pd.Series(company_list, index=df.index)
    if df['contributor'].count() == len(location_list):
        df['location'] = pd.Series(location_list, index=df.index)
    if df['contributor'].count() == len(bio_list):
        df['bio'] = pd.Series(bio_list, index=df.index)

    df.to_csv("bio_info_" + str(sub_file_num) + ".csv", sep=',', encoding='utf-8', index=False)



# get commit stats
# def stepFour(sub_file_num):
#     # read repo list
#     df_repo = pd.read_csv('repo_list.csv')
#     df_contributor = pd.read_csv('contributor_list_' + str(sub_file_num) + '.csv')
#
#     df_repo = df_repo[df_repo.repo_name.str.strip() != '']
#     df_contributor = df_contributor[df_contributor.contributor.str.strip() != '']
#
#     for repo in df_repo['repo_name']:
#         repo_commit_list = []
#
#         contribution_dict = {}
#         # TODO: need to go through all pages of contributors
#         request_str = "https://api.github.com/repos/" + repo + "/stats/contributors?access_token=" + access_token
#         r = requests.get(request_str)
#         contributorsItem = json.loads(r.text or r.content)
#         commit_count = contributorsItem['total']
#         contributor = contributorsItem['author']['login']
#         contribution_dict[contributor] = commit_count
#
#         for contributor in df_contributor['contributor']:
#             commit_count = contribution_dict.get(contributor, "")
#             repo_commit_list.append(commit_count)
#
#         if df_contributor['contributor'].count() == len(repo_commit_list):
#             df_contributor[repo] = pd.Series(repo_commit_list, index=df_contributor.index)
#
#     df_contributor.to_csv("stats_info_" + str(sub_file_num) + ".csv", sep=',', encoding='utf-8', index=False)

# get commit from user for each repo
def stepFive(stat_type, sub_file_num):
    df_repo = pd.read_csv('repo_list.csv')
    df_contributor = pd.read_csv('contributor_list_' + str(sub_file_num) + '.csv')

    df_repo = df_repo[df_repo.repo_name.str.strip() != '']
    df_contributor = df_contributor[df_contributor.contributor.str.strip() != '']

    for repo in df_repo['repo_name']:
        print(repo)
        repo_count_list = []
        for contributor in df_contributor['contributor']:
            print(contributor)
            # time.sleep(2)
            # commit count for a specific user on a specific repo
            try:
                if stat_type == "commit":
                    request_str = "https://api.github.com/search/commits?q=author:" + \
                                     contributor + "+merge:false+repo:" + \
                                     repo + "&access_token=" + access_token

                    r = requests.get(request_str, headers={"Accept": "application/vnd.github.cloak-preview"})
                elif stat_type == "issue":
                    request_str = "https://api.github.com/search/issues?q=type:issue+involves:" + \
                                        contributor + "+repo:" + \
                                        repo + "&access_token=" + access_token
                    r = requests.get(request_str, headers={"Accept": "application/vnd.github.symmetra-preview+jason"})
                elif stat_type == "pr":
                    request_str = "https://api.github.com/search/issues?q=type:pr+involves:" + \
                                     contributor + "+repo:" + \
                                     repo + "&access_token=" + access_token
                    r = requests.get(request_str, headers={"Accept": "application/vnd.github.symmetra-preview+jason"})

                item = json.loads(r.text or r.content)
                count = item['total_count']
            except:
                time.sleep(10)
                count = -1
                print(bcolors.WARNING + "ERROR in getting count: " + repo + " and " + contributor + bcolors.ENDC)

            repo_count_list.append(count)

        if df_contributor['contributor'].count() == len(repo_count_list):
            df_contributor[repo] = pd.Series(repo_count_list, index=df_contributor.index)

    df_contributor.to_csv(stat_type + "_info_" + str(sub_file_num) + ".csv", sep=',', encoding='utf-8', index=False)

def stepSix(stat_type, sub_file_num):
    # get the -1 ones, re-run the request
    df_commit = pd.read_csv(stat_type + "_info_" + str(sub_file_num) + ".csv")

    for row_index, row_value in df_commit.iterrows():
        contributor = row_value['contributor']
        for column in df_commit:
            repo = column
            if row_value[column] == -1:
                # send request
                try:
                    if stat_type == "commit":
                        request_str = "https://api.github.com/search/commits?q=author:" + \
                                      contributor + "+merge:false+repo:" + \
                                      repo + "&access_token=" + access_token

                        r = requests.get(request_str, headers={"Accept": "application/vnd.github.cloak-preview"})
                    elif stat_type == "issue":
                        request_str = "https://api.github.com/search/issues?q=type:issue+involves:" + \
                                      contributor + "+repo:" + \
                                      repo + "&access_token=" + access_token
                        r = requests.get(request_str,
                                         headers={"Accept": "application/vnd.github.symmetra-preview+jason"})
                    elif stat_type == "pr":
                        request_str = "https://api.github.com/search/issues?q=type:pr+involves:" + \
                                      contributor + "+repo:" + \
                                      repo + "&access_token=" + access_token
                        r = requests.get(request_str,
                                         headers={"Accept": "application/vnd.github.symmetra-preview+jason"})

                    item = json.loads(r.text or r.content)
                    count = item['total_count']
                except:
                    time.sleep(10)
                    count = -1
                    print(bcolors.WARNING + "ERROR in getting count: " + repo + " and " + contributor + bcolors.ENDC)

                df_commit.loc[row_index, column] = count

    df_commit.to_csv(stat_type + "_info_" + str(sub_file_num) + "_new.csv", sep=',', encoding='utf-8', index=False)

# get commit from user for each repo
def stepFive_2(stat_type, sub_file_num):
    df_repo = pd.read_csv('repo_list.csv')
    df_contributor = pd.read_csv('contributor_list_' + str(sub_file_num) + '.csv')

    repo_contributor_dict = {}
    df_repo_info = pd.read_csv('repo_info.csv')
    for row_index, row_value in df_repo_info.iterrows():
        repo_name = row_value['repo_name']
        contributors = row_value['contributors']
        contributor_list = contributors.splitlines()
        repo_contributor_dict[repo_name] = contributor_list


    df_repo = df_repo[df_repo.repo_name.str.strip() != '']
    df_contributor = df_contributor[df_contributor.contributor.str.strip() != '']

    for repo in df_repo['repo_name']:
        print(repo)
        repo_count_list = []
        for contributor in df_contributor['contributor']:
            print(contributor)
            # do the following if contributor is a repo's contributor
            contributor_list = repo_contributor_dict[repo]
            if contributor in contributor_list:
                # time.sleep(2)
                # commit count for a specific user on a specific repo
                try:
                    if stat_type == "commit":
                        request_str = "https://api.github.com/search/commits?q=author:" + \
                                         contributor + "+merge:false+repo:" + \
                                         repo + "&access_token=" + access_token

                        r = requests.get(request_str, headers={"Accept": "application/vnd.github.cloak-preview"})
                    elif stat_type == "issue":
                        request_str = "https://api.github.com/search/issues?q=type:issue+involves:" + \
                                            contributor + "+repo:" + \
                                            repo + "&access_token=" + access_token
                        r = requests.get(request_str, headers={"Accept": "application/vnd.github.symmetra-preview+jason"})
                    elif stat_type == "pr":
                        request_str = "https://api.github.com/search/issues?q=type:pr+involves:" + \
                                         contributor + "+repo:" + \
                                         repo + "&access_token=" + access_token
                        r = requests.get(request_str, headers={"Accept": "application/vnd.github.symmetra-preview+jason"})

                    item = json.loads(r.text or r.content)
                    count = item['total_count']
                except:
                    time.sleep(10)
                    count = -1
                    print(bcolors.FAIL + "ERROR in getting count: " + repo + " and " + contributor + bcolors.ENDC)
            else:
                count = 0
                print(bcolors.WARNING + "not contributor: " + repo + " and " + contributor + bcolors.ENDC)

            repo_count_list.append(count)

        if df_contributor['contributor'].count() == len(repo_count_list):
            df_contributor[repo] = pd.Series(repo_count_list, index=df_contributor.index)

    df_contributor.to_csv(stat_type + "_info_" + str(sub_file_num) + ".csv", sep=',', encoding='utf-8', index=False)

def stepSix_2(stat_type, sub_file_num):
    # get the -1 ones, re-run the request
    df_commit = pd.read_csv(stat_type + "_info_" + str(sub_file_num) + ".csv")

    for row_index, row_value in df_commit.iterrows():
        contributor = row_value['contributor']
        for column in df_commit:
            repo = column
            if row_value[column] == -1:
                print(repo + ", " + contributor)
                try:
                    if stat_type == "commit":
                        request_str = "https://api.github.com/search/commits?q=author:" + \
                                      contributor + "+merge:false+repo:" + \
                                      repo + "&access_token=" + access_token

                        r = requests.get(request_str, headers={"Accept": "application/vnd.github.cloak-preview"})
                    elif stat_type == "issue":
                        request_str = "https://api.github.com/search/issues?q=type:issue+involves:" + \
                                      contributor + "+repo:" + \
                                      repo + "&access_token=" + access_token
                        r = requests.get(request_str,
                                         headers={"Accept": "application/vnd.github.symmetra-preview+jason"})
                    elif stat_type == "pr":
                        request_str = "https://api.github.com/search/issues?q=type:pr+involves:" + \
                                      contributor + "+repo:" + \
                                      repo + "&access_token=" + access_token
                        r = requests.get(request_str,
                                         headers={"Accept": "application/vnd.github.symmetra-preview+jason"})

                    item = json.loads(r.text or r.content)
                    count = item['total_count']
                except:
                    time.sleep(10)
                    count = -1
                    print(bcolors.WARNING + "ERROR in getting count: " + repo + " and " + contributor + bcolors.ENDC)

                df_commit.loc[row_index, column] = count

    df_commit.to_csv(stat_type + "_info_" + str(sub_file_num) + "_new.csv", sep=',', encoding='utf-8', index=False)

def stepSeven(sub_file_num):
    df_repo = pd.read_csv('repo_list.csv')
    df_contributor = pd.read_csv('contributor_list_' + str(sub_file_num) + '.csv')

    df_repo = df_repo[df_repo.repo_name.str.strip() != '']
    df_contributor = df_contributor[df_contributor.contributor.str.strip() != '']

    commit_list = []
    issue_list = []
    pr_list = []
    for contributor in df_contributor['contributor']:
        print(contributor)
        time.sleep(5)
        # commit count for a specific user
        try:
            commit_request_str = "https://api.github.com/search/commits?q=author:" + \
                                 contributor + "+merge:false" + "&access_token=" + access_token
            commit_r = requests.get(commit_request_str, headers={"Accept": "application/vnd.github.cloak-preview"})
            commit_item = json.loads(commit_r.text or commit_r.content)
            commit_count = commit_item['total_count']
        except:
            commit_count = -1
            print(bcolors.WARNING + "ERROR in commit_count: " + contributor + bcolors.ENDC)
        commit_list.append(commit_count)

        # issue involved count for specific user
        try:
            issue_request_str = "https://api.github.com/search/issues?q=type:issue+involves:" + \
                                contributor + "&access_token=" + access_token
            issue_r = requests.get(issue_request_str, headers={"Accept": "application/vnd.github.symmetra-preview+jason"})
            issue_item = json.loads(issue_r.text or issue_r.content)
            issue_count = issue_item['total_count']
        except:
            issue_count = -1
            print(bcolors.WARNING + "ERROR in issue_count: " + contributor + bcolors.ENDC)
        issue_list.append(issue_count)

        # pr involved count for specific user
        try:
            pr_request_str = "https://api.github.com/search/issues?q=type:pr+involves:" + \
                                contributor + "&access_token=" + access_token
            pr_r = requests.get(pr_request_str, headers={"Accept": "application/vnd.github.symmetra-preview+jason"})
            pr_item = json.loads(pr_r.text or pr_r.content)
            pr_count = pr_item['total_count']
        except:
            pr_count = -1
            print(bcolors.WARNING + "ERROR in cpr_count: " + contributor + bcolors.ENDC)
        pr_list.append(pr_count)


    if df_contributor['contributor'].count() == len(commit_list):
        df_contributor['commit_count'] = pd.Series(commit_list, index=df_contributor.index)
    if df_contributor['contributor'].count() == len(issue_list):
        df_contributor['issue_count'] = pd.Series(issue_list, index=df_contributor.index)
    if df_contributor['contributor'].count() == len(pr_list):
        df_contributor['pr_count'] = pd.Series(pr_list, index=df_contributor.index)

    df_contributor.to_csv("stats_info_" + str(sub_file_num) + ".csv", sep=',', encoding='utf-8', index=False)

def concatenate_files(stat_type):
    directory = 'final_repo_' + stat_type + '_stats/'
    file = stat_type + '_info'
    df_1 = pd.read_csv(directory + file + '_' + str(1) + '.csv')
    df_2 = pd.read_csv(directory + file + '_' + str(2) + '.csv')
    df_3 = pd.read_csv(directory + file + '_' + str(3) + '.csv')
    df_4 = pd.read_csv(directory + file + '_' + str(4) + '.csv')
    df_5 = pd.read_csv(directory + file + '_' + str(5) + '.csv')
    df_6 = pd.read_csv(directory + file + '_' + str(6) + '.csv')
    df_7 = pd.read_csv(directory + file + '_' + str(7) + '.csv')

    frames = [df_1, df_2, df_3, df_4, df_5, df_6, df_7]
    df_result = pd.concat(frames)
    df_result.to_csv(directory + file + ".csv", sep=',', encoding='utf-8', index=False)


def find_top_contributor_for_repo(stat_type, top_num):
    df_contributor_list = []
    df_repo_list = []
    df_count_list = []
    directory = 'final_repo_' + stat_type + '_stats/'
    file = stat_type + '_info.csv'
    output_file = stat_type + '_contributor_top'
    df = pd.read_csv(directory + file)
    # get all repos
    repo_list = list(df.columns.values)
    repo_list.remove('contributor')
    for repo in repo_list:
        df_sort = df.sort_values([repo], ascending=[0])
        top_5_row = df_sort.head(top_num)
        for index, row in top_5_row.iterrows():
            contributor = row['contributor']
            count = row[repo]
            if count != 0:
                if contributor not in df_contributor_list:
                    df_contributor_list.append(contributor)
                    df_repo_list.append(repo)
                    df_count_list.append(count)
                else:
                    print("already exist: " + repo + " and " + contributor)
            else:
                print("less than " + str(top_num) + " contributors: " + repo)

    if len(df_repo_list) == len(df_contributor_list) and len(df_repo_list) == len(df_count_list):
        df = pd.DataFrame({'repo': df_repo_list})
        df['contributor'] = df_contributor_list
        df['contribution_count'] = df_count_list
        df['contribution_type'] = [stat_type] * len(df_repo_list)
        df.to_csv(directory + output_file + str(top_num) + '.csv', sep=',', encoding='utf-8', index=False)


# getting emails
def get_contributor_info(stat_type, top_num):
    # set access token envrionment variable
    os.environ["GH_EMAIL_TOKEN"] = access_token
    print(os.environ["GH_EMAIL_TOKEN"])

    directory = 'final_repo_' + stat_type + '_stats/'
    file = stat_type + '_contributor_top' + str(top_num) + '.csv'

    # read contributor list
    df = pd.read_csv(directory + file)

    email_on_github_list = []
    email_on_npm_list = []
    email_from_recent_commits_list = []
    emails_from_owned_repo_recent_activity_list = []

    name_list = []
    active_since_list = []
    company_list = []
    location_list = []
    bio_list = []

    for contributor in df['contributor']:
        print(contributor)

        try:
            stdout = subprocess.check_output(["./github-email.sh", contributor])
        except subprocess.CalledProcessError as stdexc:
            print("error code", stdexc.returncode, stdexc.output)
            stdout = ""

        if stdout != "":
            stdoutList = stdout.decode("utf-8").split('\n')

            for idx, val in enumerate(stdoutList):
                if "Email on GitHub" in val:
                    githubEmailIdx = idx
                elif "Email on npm" in val:
                    npmEmailIdx = idx
                elif "Emails from recent commits" in val:
                    RecentCommitEmailIdx = idx
                elif "Emails from owned-repo recent activity" in val:
                    OwnedRepoEmailIdx = idx

            email_on_github_list.append('\n'.join(stdoutList[githubEmailIdx+1: npmEmailIdx-1]))
            email_on_npm_list.append('\n'.join(stdoutList[npmEmailIdx+1: RecentCommitEmailIdx-1]))
            email_from_recent_commits_list.append('\n'.join(stdoutList[RecentCommitEmailIdx+1: OwnedRepoEmailIdx-1]))
            emails_from_owned_repo_recent_activity_list.append('\n'.join(stdoutList[OwnedRepoEmailIdx+1: len(stdoutList)-1]))
        else:
            email_on_github_list.append("")
            email_on_npm_list.append("")
            email_from_recent_commits_list.append("")
            emails_from_owned_repo_recent_activity_list.append("")

        try:
            request_str = "https://api.github.com/users/" + contributor + "?access_token=" + access_token
            r = requests.get(request_str)
            contributorItem = json.loads(r.text or r.content)

            name = contributorItem['name']
            active_since = contributorItem['created_at']
            company = contributorItem['company']
            location = contributorItem['location']
            bio = contributorItem['bio']
        except:
            name = ""
            active_since = ""
            company = ""
            location = ""
            bio = ""

        name_list.append(name)
        active_since_list.append(active_since)
        company_list.append(company)
        location_list.append(location)
        bio_list.append(bio)

    if df['contributor'].count() == len(email_on_github_list):
        df['email_on_github'] = pd.Series(email_on_github_list, index=df.index)
    if df['contributor'].count() == len(email_on_npm_list):
        df['email_on_npm'] = pd.Series(email_on_npm_list, index=df.index)
    if df['contributor'].count() == len(email_from_recent_commits_list):
        df['email_from_recent_commits'] = pd.Series(email_from_recent_commits_list, index=df.index)
    if df['contributor'].count() == len(emails_from_owned_repo_recent_activity_list):
        df['emails_from_owned_repo_recent_activity'] = pd.Series(emails_from_owned_repo_recent_activity_list, index=df.index)

    if df['contributor'].count() == len(name_list):
        df['name'] = pd.Series(name_list, index=df.index)
    if df['contributor'].count() == len(active_since_list):
        df['active_since'] = pd.Series(active_since_list, index=df.index)
    if df['contributor'].count() == len(company_list):
        df['company'] = pd.Series(company_list, index=df.index)
    if df['contributor'].count() == len(location_list):
        df['location'] = pd.Series(location_list, index=df.index)
    if df['contributor'].count() == len(bio_list):
        df['bio'] = pd.Series(bio_list, index=df.index)

    df.to_csv(directory + file + "_info.csv", sep=',', encoding='utf-8', index=False)

def validate(row):
    email = row['Email'].strip().lower()
    if email == 'extra' or email == 'no name' or email == 'no email':
        return False
    else:
        return True

# combine all user list from commit, issue and pr. remove duplicates
def combineUserlist():
    df_commit = pd.read_csv('final_repo_commit_stats/commit_contributor_top10.csv_info_fixed.csv')
    df_issue = pd.read_csv('final_repo_issue_stats/issue_contributor_top10.csv_info_fixed.csv')
    df_pr = pd.read_csv('final_repo_pr_stats/pr_contributor_top10.csv_info_fixed.csv')

    # remove the rows with 'extra'/'no email'/ 'no name' as email
    df_commit['valid'] = df_commit.apply(lambda row: validate(row), axis=1)
    df_commit = df_commit[df_commit.valid]
    df_issue['valid'] = df_issue.apply(lambda row: validate(row), axis=1)
    df_issue = df_issue[df_issue.valid]
    df_pr['valid'] = df_pr.apply(lambda row: validate(row), axis=1)
    df_pr = df_pr[df_pr.valid]

    frames = [df_commit, df_issue, df_pr]
    df_result = pd.concat(frames)

    # df_non_duplicate = df_result.drop_duplicates(subset=['repo', 'contributor', 'Email',
    #                                                      'name', 'active_since', 'company',
    #                                                      'location', 'bio'], keep='first')
    df_non_duplicate = df_result

    df_sort = df_non_duplicate.sort_values(['repo', 'contributor', 'contribution_count'],
                                           ascending=[1, 1, 0])

    df_sort.to_csv('final_user_list_top5.csv', sep=',',
                            columns=['contributor', 'name', 'Email', 'repo', 'contribution_type',
                                     'contribution_count', 'active_since', 'company', 'location', 'bio'],
                            encoding='utf-8', index=False)


def remove_non_valid_rows():
    df = pd.read_csv('final_user_list_top5_email.csv')

    df = df[df['Final recipient'] != '0']

    df_sort = df.sort_values(['repo', 'contributor', 'contribution_count'],
                                           ascending=[1, 1, 0])

    df_sort.to_csv('final_user_list_top5_valid.csv', sep=',',
                            columns=['contributor', 'name', 'Email', 'repo', 'contribution_type',
                                     'contribution_count', 'active_since', 'company', 'location',
                                     'bio', 'Final recipient', 'Contribution sentence', 'Contribution count < 5'],
                            encoding='utf-8', index=False)


if __name__ == "__main__":
    # stepOne()
    # stepTwo(7)
    # stepThree(6)
    # stepFive(1)
    # stepFive(2)
    # stepFive(3)
    # stepFive(4)
    # stepFive(5)
    # stepFive(6)
    # stepFive_2("commit", 1)
    # stepFive_2("commit", 2)
    # stepFive_2("commit", 3)
    # stepFive_2("commit", 4)
    # stepFive_2("commit", 5)
    # stepFive_2("commit", 6)
    # stepFive_2("commit", 7)
    # stepSix_2("commit", 1)
    # stepSix_2("commit", 2)
    # stepSix_2("commit", 3)
    # stepSix_2("commit", 4)
    # stepSix_2("commit", 5)
    # stepSix_2("commit", 6)
    # stepSix_2("commit", 7)
    # stepFive_2("issue", 1)
    # stepFive_2("issue", 2)
    # stepFive_2("issue", 3)
    # stepFive_2("issue", 4)
    # stepFive_2("issue", 5)
    # stepFive_2("issue", 6)
    # stepFive_2("issue", 7)
    # stepSix_2("issue", 1)
    # stepSix_2("issue", 2)
    # stepSix_2("issue", 3)
    # stepSix_2("issue", 4)
    # stepSix_2("issue", 5)
    # stepSix_2("issue", 6)
    # stepSix_2("issue", 7)
    # stepFive_2("pr", 1)
    # stepFive_2("pr", 2)
    # stepFive_2("pr", 3)
    # stepFive_2("pr", 4)
    # stepFive_2("pr", 5)
    # stepFive_2("pr", 6)
    # stepFive_2("pr", 7)
    # stepSix_2("pr", 1)
    # stepSix_2("pr", 2)
    # stepSix_2("pr", 3)
    # stepSix_2("pr", 4)
    # stepSix_2("pr", 5)
    # stepSix_2("pr", 6)
    # stepSix_2("pr", 7)
    # stepSeven(1)
    # stepSeven(2)
    # stepSeven(3)
    # stepSeven(4)
    # stepSeven(5)
    # stepSeven(6)
    # stepSeven(7)
    # stepFour(1)

    # concatenate_files("commit")
    # concatenate_files("issue")
    # concatenate_files("pr")

    # find_top_contributor_for_repo('commit', 10)
    # find_top_contributor_for_repo('issue', 10)
    # find_top_contributor_for_repo('pr', 10)

    # get_contributor_info("commit", 10)
    # get_contributor_info("issue", 10)
    # get_contributor_info("pr", 10)
    # combineUserlist()
    # remove_non_valid_rows()
