var githubContainer = document.getElementById("github-info");
var btn1 = document.getElementById("btn1");
var btn2 = document.getElementById("btn2");
var repoData;

btn1.addEventListener("click", function() {
                     var repoRequest = new XMLHttpRequest();
                     repoRequest.open('GET', 'https://api.github.com/search/repositories?q=stars:%3E=10000&sort=stars&order=de');
                    
                     repoRequest.onload = function() {
                     if (repoRequest.status >= 200 && repoRequest.status < 400) {
                     repoData = JSON.parse(repoRequest.responseText);

                      GetContributorsData();
                      CreateHTML(repoData);
                     } else {
                     console.log("We connected to the server, but it returned an error.");
                     }
                     
                     };
                     
                     repoRequest.onerror = function() {
                     console.log("Connection error");
                     };
                     
                     repoRequest.send();
                     });

btn2.addEventListener("click", function() {
                      var repoRequest = new XMLHttpRequest();
                      repoRequest.open('GET', 'https://api.github.com/search/repositories?q=topic:human-computer-interaction&sort=stars&order=de');
                      
                      repoRequest.onload = function() {
                          if (repoRequest.status >= 200 && repoRequest.status < 400) {
                              repoData = JSON.parse(repoRequest.responseText);

                              GetContributorsData();
                              CreateHTML(repoData);
                          }
                          else {
                            console.log("We connected to the server, but it returned an error.");
                          }
                      };
                      
                      repoRequest.onerror = function() {
                        console.log("Connection error");
                      };
                      
                      repoRequest.send();
                      });

function GetContributorsData() {
    for (i = 0; i < repoData.items.length; i++) {
        var contributors_url = repoData.items[i].contributors_url;
        
        var contributorsRequest = new XMLHttpRequest();
        var contributors_url = contributors_url;
        
        // TODO: force process is handled synchronously
        contributorsRequest.open('GET', contributors_url, false);
        
        contributorsRequest.onload = function() {
            if (contributorsRequest.status >= 200 && contributorsRequest.status < 400) {
                var contributorsData = JSON.parse(contributorsRequest.responseText);
                console.log(contributorsData);
                
                AddContributorsToRepoData(i, contributorsData);

            }
            else {
                console.log("We connected to the server, but it returned an error.");
            }
        };
        
        contributorsRequest.onerror = function() {
            console.log("Connection error");
        };
        
        contributorsRequest.send();
    }
}

function AddContributorsToRepoData(index, contributorsData) {
    repoData.items[index]["contributors"] = contributorsData;
//    CreateHTML(repoData);
}

//function AddContributorsToRepoData(repoData) {
//    for (i = 0; i < 1; i++) {
//        var contributors_url = repoData.items[i].contributors_url;
//        var contributorsData = GetContributorsData(i, contributors_url);
//        repoData.items[i]["contributors"] = contributorsData;
//    }
//    return repoData;
//}

    
//function renderHTML(data) {
//    var htmlString = "";
//
//    githubContainer.innerHTML = ""
//    githubContainer.insertAdjacentHTML('beforeend', "Total number of item: " + data.items.length);
//
//    for (i = 0; i < data.items.length; i++) {
//        htmlString += "<p>" + data.items[i].id;
//
//        htmlString += '</p>';
//
//    }
//
//    githubContainer.insertAdjacentHTML('beforeend', htmlString);
//}

function CreateHTML(repoData) {
    var rawTemplate = document.getElementById("repoTemplate").innerHTML;
    var compiledTemplate = Handlebars.compile(rawTemplate);
    var ourGeneratedHTML = compiledTemplate(repoData);
    
    githubContainer.innerHTML = ourGeneratedHTML;
}
