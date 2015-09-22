(function() {
  var proxied = window.alert;
  window.alert = function() {
    console.log("\nURL: " + window.location.href+ " Executed Payload: " + arguments[0]);
    var http = new XMLHttpRequest();
	var url = "http://localhost:8787/?b64="+window.btoa(window.location.href);
	http.open("GET", url, true);
	http.onreadystatechange = function() {
    if(http.readyState == 4 && http.status == 200) {
        console.log(http.responseText);
    }
}
http.send();
  };

var proxied = window.prompt;
  window.prompt = function() {
    console.log("\nURL: " + window.location.href+ " Executed Payload: " + arguments[0]);
    var http = new XMLHttpRequest();
	var url = "http://localhost:8787/?b64="+window.btoa(window.location.href);
	http.open("GET", url, true);
	http.onreadystatechange = function() {
    if(http.readyState == 4 && http.status == 200) {
        console.log(http.responseText);
    }
}
http.send();
  };

var proxied = window.confirm;
  window.confirm = function() {
    console.log("\nURL: " + window.location.href+ " Executed Payload: " + arguments[0]);
    var http = new XMLHttpRequest();
	var url = "http://localhost:8787/?b64="+window.btoa(window.location.href);
	http.open("GET", url, true);
	http.onreadystatechange = function() {
    if(http.readyState == 4 && http.status == 200) {
        console.log(http.responseText);
    }
}
http.send();
  };



})();
