console.log("AI Prompt Privacy Protector background script loaded.");

// Initialize extension state on install
chrome.runtime.onInstalled.addListener(function() {
  chrome.storage.sync.set({enabled: true}, function() {
    console.log("AI Prompt Privacy Protector has been enabled by default.");
  });
});