document.getElementById("summarizeBtn").addEventListener("click", async () => {
  document.getElementById("summary").innerText = "⏳ Extracting selection...";

  try {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

    // Inject script to get selected text
    const [{ result }] = await chrome.scripting.executeScript({
      target: { tabId: tab.id },
      func: () => window.getSelection().toString(),
    });

    if (!result || result.trim() === "") {
      document.getElementById("summary").innerText = "⚠️ No text selected. Please highlight the T&C first.";
      return;
    }

    // Send selected text to backend
    document.getElementById("summary").innerText = "🧠 Summarizing...";
    const response = await fetch("http://127.0.0.1:8000/analyze/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: result })
    });

    const data = await response.json();

    if (data.summary) {
      document.getElementById("summary").innerText = data.summary;
      const risksEl = document.getElementById("risks");
      risksEl.innerHTML = "";
      if (data.risks && data.risks.length > 0) {
        data.risks.forEach(risk => {
          const tag = document.createElement("span");
          tag.className = "risk-tag";
          tag.textContent = "⚠️ " + risk;
          risksEl.appendChild(tag);
        });
      }
    } else {
      document.getElementById("summary").innerText = "⚠️ Summary not received.";
    }

  } catch (err) {
    console.error(err);
    document.getElementById("summary").innerText = "❌ Error occurred. Check console.";
  }
});
