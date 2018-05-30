var pageCounter = 1;
var githubContainer = document.getElementById("github-info");
var btn = document.getElementById("btn");

btn.addEventListener("click", function() {
                     var ourRequest = new XMLHttpRequest();
                     ourRequest.open('GET', 'https://api.github.com/search/repositories?q=stars:%3E=10000&sort=stars&order=de');
                    
                     ourRequest.onload = function() {
                     if (ourRequest.status >= 200 && ourRequest.status < 400) {
                     var ourData = JSON.parse(ourRequest.responseText);
                     renderHTML(ourData);
                     } else {
                     console.log("We connected to the server, but it returned an error.");
                     }
                     
                     };
                     
                     ourRequest.onerror = function() {
                     console.log("Connection error");
                     };
                     
                     ourRequest.send();
                     pageCounter++;
                     if (pageCounter > 3) {
                     btn.classList.add("hide-me");
                     }
                     });

function renderHTML(data) {
    var htmlString = "";
    
    githubContainer.insertAdjacentHTML('beforeend', "Total number of item: " + data.items.length);
    
    for (i = 0; i < data.items.length; i++) {
        htmlString += "<p>" + data.items[i].id;

        htmlString += '</p>';

    }

    githubContainer.insertAdjacentHTML('beforeend', htmlString);
}
