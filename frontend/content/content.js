chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === "getCurrentPage") {
        sendResponse({ url: window.location.href });
    }
});
