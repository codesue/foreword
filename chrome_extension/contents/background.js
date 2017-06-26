
var articleUrl = "";
  
chrome.tabs.query({active: true, currentWindow: true}, function(arrayOfTabs) {
	// since only one tab should be active and in the current window at once
	// the return variable should only have one entry
	var activeTab = arrayOfTabs[0];
	articleUrl = activeTab.url;

});

chrome.browserAction.onClicked.addListener(function(tab) {
	chrome.tabs.create({ url: "https://codesue-foreword.herokuapp.com/sort-words/?url_to_clean=" + articleUrl });
});