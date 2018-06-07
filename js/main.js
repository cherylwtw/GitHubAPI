var githubContainer = document.getElementById("github-info");
var contributorContainer = document.getElementById("contributor-info");
var btn1 = document.getElementById("btn1");
var btn2 = document.getElementById("btn2");
var btn3 = document.getElementById("btn3");
var btn4 = document.getElementById("btn4");
var btn5 = document.getElementById("btn5");
var btn6 = document.getElementById("btn6");
var btn7 = document.getElementById("btn7");
var txtPagenum1 = document.getElementById('txtPagenum1');
var txtPagenum2 = document.getElementById('txtPagenum2');
var txtPagenum3 = document.getElementById('txtPagenum3');
var txtPagenum4 = document.getElementById('txtPagenum4');
var txtPagenum5 = document.getElementById('txtPagenum5');
var txtPagenum6 = document.getElementById('txtPagenum6');
var hyperlinkRepoExport = document.getElementById("hyperlinkRepoExport");
var hyperlinkContributorExport = document.getElementById("hyperlinkContributorExport");
var repoData;
var contributorsList = [];
var currentContributorsAdded = 0;
var currentContributorsList = [];
var contributorsDetails = [];
var contributorExportFileName = 'contributorsExport.txt';
var repoExportFileName = 'repoExport.csv';

// Ajax calls to the github server to get data
// this is learned from tutorial, JSON and AJAX Tutorial: With Real Examples on youtube by LearnWebCode - https://www.youtube.com/watch?v=rJesac0_Ftw
btn1.addEventListener("click", function() {
                      var repoRequest = new XMLHttpRequest();
                      requestStr='https://api.github.com/search/repositories?q=stars:%3E=10000&per_page=50' + '&page=' + txtPagenum1.value + '&access_token=4c12cb4a014c24df8301b1ea146afceb4a6626cc'
                      console.log(requestStr);
                      repoRequest.open('GET', requestStr);
                      
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
                      requestStr ='https://api.github.com/search/repositories?q=topic:human-computer-interaction&per_page=50' + '&page=' + txtPagenum2.value + '&access_token=4c12cb4a014c24df8301b1ea146afceb4a6626cc';
                      console.log(requestStr);
                      repoRequest.open('GET', requestStr);
                      
                      repoRequest.onload = function() {
                      if (repoRequest.status >= 200 && repoRequest.status < 400) {
                      repoData = JSON.parse(repoRequest.responseText);
                      
                      GetContributorsData();
                      CreateHTML(repoData);
                      //                      CreateContributorHTML(contributorsList);
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

btn3.addEventListener("click", function() {
                      var repoRequest = new XMLHttpRequest();
                      requestStr ='https://api.github.com/search/repositories?q=topic:hci&per_page=50' + '&page=' + txtPagenum3.value + '&access_token=4c12cb4a014c24df8301b1ea146afceb4a6626cc';
                      console.log(requestStr);
                      repoRequest.open('GET', requestStr);
                      
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

btn4.addEventListener("click", function() {
                      var repoRequest = new XMLHttpRequest();
                      requestStr ='https://api.github.com/search/repositories?q=topic:user-experience&per_page=50' + '&page=' + txtPagenum4.value + '&access_token=4c12cb4a014c24df8301b1ea146afceb4a6626cc';
                      console.log(requestStr);
                      repoRequest.open('GET', requestStr);
                      
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

btn5.addEventListener("click", function() {
                      var repoRequest = new XMLHttpRequest();
                      requestStr ='https://api.github.com/search/repositories?q=topic:ux&per_page=50' + '&page=' + txtPagenum5.value + '&access_token=4c12cb4a014c24df8301b1ea146afceb4a6626cc';
                      console.log(requestStr);
                      repoRequest.open('GET', requestStr);
                      
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


btn6.addEventListener("click", function() {
                      var repoRequest = new XMLHttpRequest();
                      requestStr ='https://api.github.com/search/repositories?q=topic:usability&per_page=50' + '&page=' + txtPagenum6.value + '&access_token=4c12cb4a014c24df8301b1ea146afceb4a6626cc';
                      console.log(requestStr);
                      repoRequest.open('GET', requestStr);
                      
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

btn7.addEventListener("click", function() {
                      currentContributorsAdded = 0;
                      for (i=0; i<currentContributorsList.length; i++) {
                      if (contributorsList.indexOf(currentContributorsList[i]) == -1){
                      contributorsList.push(currentContributorsList[i]);
                      currentContributorsAdded += 1;
                      }
                      }
                      CreateContributorHTML(contributorsList);
                      });


function GetContributorsData() {
    currentContributorsList = [];
    for (i = 0; i < repoData.items.length; i++) {
        var contributors_url = repoData.items[i].contributors_url;
        
        for (j= 1; j<6; j++) {
            var contributorsRequest = new XMLHttpRequest();
            contributors_url = contributors_url + '?per_page=100&' + 'page='+ j + '&access_token=4c12cb4a014c24df8301b1ea146afceb4a6626cc';
            
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
}

function AddContributorsToRepoData(index, contributorsData) {
    if (typeof repoData.items[index]["contributors"] === "undefined") {
        repoData.items[index]["contributors"] = contributorsData
    }
    else {
        repoData.items[index]["contributors"] = repoData.items[index]["contributors"].concat(contributorsData);
    }
    
    // append contributor data to list
    currentContributorsList = currentContributorsList.concat(contributorsData);
}

// Acknowledge: the function to export div content to text/html is taken from answer on StackOverflow https://stackoverflow.com/questions/22084698/how-to-export-source-content-within-div-to-text-html-file
function downloadInnerHtml(filename, elId, mimeType) {
    var elHtml = document.getElementById(elId).innerHTML;
    var strippedElHtml = elHtml.replace(/(<([^>]+)>)/ig,"");
    var trimmedElHtml = strippedElHtml.replace(/\s+/g, '\n');
    var link = document.createElement('a');
    mimeType = mimeType || 'text/plain';
    
    link.setAttribute('download', filename);
    link.setAttribute('href', 'data:' + mimeType  +  ';charset=utf-8,' + encodeURIComponent(trimmedElHtml));
    link.click();
}

// Acknowledge: The function to export table content to csv file is taken from answer on StackOverflow https://stackoverflow.com/questions/16078544/export-to-csv-using-jquery-and-html/16203218
function exportTableToCSV($table, filename) {
    
    var $rows = $table.find('tr:has(td),tr:has(th)'),
    
    // Temporary delimiter characters unlikely to be typed by keyboard
    // This is to avoid accidentally splitting the actual contents
    tmpColDelim = String.fromCharCode(11), // vertical tab character
    tmpRowDelim = String.fromCharCode(0), // null character
    
    // actual delimiter characters for CSV format
    colDelim = '","',
    rowDelim = '"\r\n"',
    
    // Grab text from table into CSV formatted string
    csv = '"' + $rows.map(function(i, row) {
                          var $row = $(row),
                          $cols = $row.find('td,th');
                          
                          return $cols.map(function(j, col) {
                                           var $col = $(col),
                                           text = $col.text();
                                           
                                           return text.replace(/"/g, '""'); // escape double quotes
                                                               
                                                               }).get().join(tmpColDelim);
                                           
                                           }).get().join(tmpRowDelim)
                          .split(tmpRowDelim).join(rowDelim)
                          .split(tmpColDelim).join(colDelim) + '"';
                          
                          // Deliberate 'false', see comment below
                          if (false && window.navigator.msSaveBlob) {
                          
                          var blob = new Blob([decodeURIComponent(csv)], {
                                              type: 'text/csv;charset=utf8'
                                              });
                          
                          // Crashes in IE 10, IE 11 and Microsoft Edge
                          // See MS Edge Issue #10396033
                          // Hence, the deliberate 'false'
                          // This is here just for completeness
                          // Remove the 'false' at your own risk
                          window.navigator.msSaveBlob(blob, filename);
                          
                          }
                          else if (window.Blob && window.URL) {
                          // HTML5 Blob
                          var blob = new Blob([csv], {
                                              type: 'text/csv;charset=utf-8'
                                              });
                          var csvUrl = URL.createObjectURL(blob);
                          
                          $(this)
                          .attr({
                                'download': filename,
                                'href': csvUrl
                                });
                          }
                          else {
                          // Data URI
                          var csvData = 'data:application/csv;charset=utf-8,' + encodeURIComponent(csv);
                          
                          $(this)
                          .attr({
                                'download': filename,
                                'href': csvData,
                                'target': '_blank'
                                });
                          }
                          }
                          
hyperlinkRepoExport.addEventListener("click", function(event) {
                                 // CSV
                                 var args = [$('#github-info>table'), repoExportFileName];
                                 exportTableToCSV.apply(this, args);
                                                           
                               // If CSV, don't do event.preventDefault() or return false
                               // We actually need this to be a typical hyperlink
                                 });
                          
hyperlinkContributorExport.addEventListener("click",function(event){
                                            downloadInnerHtml(contributorExportFileName,
                                                              'contributor-info','text/html');
                                            })
                          
// use Handlebar.js to create html to use on the page
// this is learned from tutorial, Handlebars.js Tutorial on youtube by LearnWebCode - https://www.youtube.com/watch?v=wSNa5b1mS5Y&t=681s
function CreateHTML(repoData) {
                          console.log('# of repo: ' + repoData.items.length);
                          console.log('# of current contributors: ' + currentContributorsList.length);
                          var rawTemplate = document.getElementById("repoTemplate").innerHTML;
                          var compiledTemplate = Handlebars.compile(rawTemplate);
                          var ourGeneratedHTML = compiledTemplate(repoData);
                          
                          githubContainer.innerHTML = ourGeneratedHTML;
                          }
                          
function CreateContributorHTML(contributorsList) {
                          document.getElementById("contributor-sum-info").innerText = currentContributorsAdded + " contributors are added to the list, there are total of " + contributorsList.length + " contributors now";
                          
                          console.log('# of contributors: ' + contributorsList.length);
                          
                          var rawTemplate = document.getElementById("contributorTemplate").innerHTML;
                          var compiledTemplate = Handlebars.compile(rawTemplate);
                          var ourGeneratedHTML = compiledTemplate(contributorsList);
                          
                          contributorContainer.innerHTML = ourGeneratedHTML;
                          }
