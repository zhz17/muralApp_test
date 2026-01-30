document.addEventListener("DOMContentLoaded", () => {
  const tabs = document.querySelectorAll(".tab-btn");
  const tabContents = document.querySelectorAll(".tab-content");
  const form = document.getElementById("generatorForm");
  const submitBtn = document.getElementById("submitBtn");
  const logsContainer = document.getElementById("logs");
  const fileInput = document.getElementById("jsonFile");
  const fileLabel = document.querySelector(".file-upload-label");

  // Tab switching
  tabs.forEach((tab) => {
    tab.addEventListener("click", () => {
      tabs.forEach((t) => t.classList.remove("active"));
      tabContents.forEach((c) => c.classList.remove("active"));
      tab.classList.add("active");
      document.getElementById(tab.dataset.tab).classList.add("active");
    });
  });

  // File input change
  fileInput.addEventListener("change", (e) => {
    if (e.target.files.length > 0) {
      fileLabel.textContent = `SELECTED: ${e.target.files[0].name}`;
      fileLabel.style.color = "var(--secondary-accent)";
    }
  });

  // Logging function
  function log(message, type = "info") {
    const entry = document.createElement("div");
    entry.className = `log-entry log-${type}`;
    entry.textContent = `> ${message}`;
    logsContainer.appendChild(entry);
    logsContainer.scrollTop = logsContainer.scrollHeight;
  }

  // Form submission
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    submitBtn.disabled = true;
    submitBtn.textContent = "PROCESSING...";
    log("Initiating generation sequence...", "info");

    const formData = new FormData(form);
    const activeTab = document.querySelector(".tab-btn.active").dataset.tab;

    // Validation based on active tab
    if (activeTab === "text-input") {
      const text = formData.get("json_text");
      if (!text || text.trim() === "") {
        log("ERROR: JSON Text is empty.", "error");
        submitBtn.disabled = false;
        submitBtn.textContent = "INITIATE GENERATION";
        return;
      }
      // Clear file input from formData if we're using text
      formData.delete("json_file");
    } else {
      const file = fileInput.files[0];
      if (!file) {
        log("ERROR: No file selected.", "error");
        submitBtn.disabled = false;
        submitBtn.textContent = "INITIATE GENERATION";
        return;
      }
      // Clear text input from formData if we're using file
      formData.delete("json_text");
    }

    try {
      const response = await fetch("/api/generate", {
        method: "POST",
        body: formData,
      });

      const result = await response.json();

      if (response.ok) {
        log("Generation sequence completed successfully.", "success");
        if (result.results && result.results.length > 0) {
          result.results.forEach((res) => log(res, "success"));
        } else {
          log("No actions performed.", "info");
        }
      } else {
        log(`ERROR: ${result.detail || "Unknown error occurred"}`, "error");
      }
    } catch (error) {
      log(`CRITICAL ERROR: ${error.message}`, "error");
    } finally {
      submitBtn.disabled = false;
      submitBtn.textContent = "INITIATE GENERATION";
    }
  });
});
