# GitHubAPI
### Description
1. Retrieve GitHub contributor logins to repos that satisfy different search criteria
2. Get emails of GitHub logins - this is using resources (github-email.sh)provided by Paulirish, in his repo github-email (https://github.com/paulirish/github-email)

### Acknowledgement
1. Source code and methods are used and learned from youtube tutorial, JSON and AJAX Tutorial: With Real Examples and Handlebars.js Tutorial provided by LearnWebCode. I highly recommend this channel - series of videos can be found at https://www.youtube.com/user/LearnWebCode.
2. Some helpful stackOverflow answers are used, including
https://stackoverflow.com/questions/22084698/how-to-export-source-content-within-div-to-text-html-file,
https://stackoverflow.com/questions/16078544/export-to-csv-using-jquery-and-html/16203218

### Usage
Retrieve GitHub contributor logins to repos that satisfy different search criteria
Before executing: replace accessToken with your own token in main.js, this allows increasing in github request rate limit
1. Click "search" button next to the repo search criteria you want
2. When table shows in the result section, click on "export repo data into excel" to export the repo data shown in the table, click on "add shown contributors to list" to add contributors to the "list of unque contributors" window on the right.
3. After all contributors are added based on searched repos, "export contributor data into text" will export the final contributors list into a text file

 Get emails of GitHub logins - this is using resources provided by Paulirish, in his repo github-email (https://github.com/paulirish/github-email)
 1. run node contributors_email.js to get emails for logins in contirbutor_info/contributorExport_1.txt into email_info/emailExport_1.txt

