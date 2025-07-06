// background.js
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.type === "analyze_tnc") {
        fetch("http://localhost:8000/analyze", {

            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ text: message.text })
        })
        .then(res => res.json())
        .then(data => {
            chrome.storage.local.set({ summary: data.summary }, () => {
                console.log("Summary saved.");
            });
        });
    }
});
