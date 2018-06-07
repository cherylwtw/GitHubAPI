const exec = require('child_process').exec;
var fs = require('fs');
var async = require('async');
var csvWriter = require('csv-write-stream')

var loginList = []

const foo = function runGithubEmail(loginId, cb){
    exec('sh ./github-email.sh ' + loginId,
         (error, stdout, stderr) => {
         console.log(`${stdout}`);
         console.log(`${stderr}`);
         cb(null, {stdout,stderr});
         if (error !== null) {
            console.log(`exec error: ${error}`);
         return cb(error);
         }
         });
}

//var parse = require('csv-parse');

async function main() {
    const contributorFilePath='../contributor_info/contributorsExport_1.txt'
    const emailFilePath ='../email_info/email_1.csv'
    
    try {
        var data = fs.readFileSync(contributorFilePath, 'utf8');
        //        console.log(data);
        inputData = data;
        loginList = data.split(/\n/).map(val => val.trim());
        loginList = loginList.filter(function(n){ return n != '' });
    } catch(e) {
        console.log('Error:', e.stack);
    }
    
//    console.log(inputData)
    
    var writer = csvWriter();
    writer.pipe(fs.createWriteStream(emailFilePath, {'flags': 'a'}))
    writer.write({login_id: " ", email_on_github: " ", email_on_npm: " ", email_from_recent_commits: " ", email_from_owned_repo_recent_activity: " " })
    writer.end()
    
//    console.log(loginList.length)
    for (i=0; i<loginList.length;i++) {
        var loginId = loginList[i];
//        console.log(loginId);
        var contributorEmailObject = {};
        
        var loginIdIdx = -1;
        var githubEmailIdx = -1;
        var npmEmailIdx = -1;
        var RecentCommitEmailIdx = -1;
        var OwnedRepoEmailIdx = -1;
        
        foo(loginId, function(error, {stdout,stderr}) {
            stdoutList = stdout.split('\n');
            for (j=0; j<stdoutList.length; j++){
                if (stdoutList[j].includes("Login Id")) {
                    loginIdIdx = j;
                }
                if (stdoutList[j].includes("Email on GitHub")) {
                    githubEmailIdx = j;
                }
                else if (stdoutList[j].includes("Email on npm")) {
                    npmEmailIdx = j
                }
                else if (stdoutList[j].includes("Emails from recent commits")) {
                    RecentCommitEmailIdx = j;
                }
                else if (stdoutList[j].includes("Emails from owned-repo recent activity")) {
                    OwnedRepoEmailIdx = j;
                }
            }
            
            contributorEmailObject["login_id"] = stdoutList.slice(loginIdIdx+1, githubEmailIdx-1).join("\n");
            contributorEmailObject["email_on_github"] = stdoutList.slice(githubEmailIdx+1, npmEmailIdx-1).join("\n");
            contributorEmailObject["email_on_npm"] = stdoutList.slice(npmEmailIdx+1, RecentCommitEmailIdx-1).join("\n");
            contributorEmailObject["email_from_recent_commits"] = stdoutList.slice(RecentCommitEmailIdx+1, OwnedRepoEmailIdx-1).join("\n");
            contributorEmailObject["email_from_owned_repo_recent_activity"] = stdoutList.slice(OwnedRepoEmailIdx+1, stdoutList.length-1).join("\n");
            
            console.log(contributorEmailObject);
            
            var writer = csvWriter({sendHeaders: false});
            writer.pipe(fs.createWriteStream(emailFilePath, {'flags': 'a'}))
            writer.write(contributorEmailObject)
            writer.end()
            });
    }
}



main();
