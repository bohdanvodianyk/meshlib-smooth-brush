const form = document.getElementById("mesh-form");
const strengthInput = document.getElementById("smoothing-strength");
const strengthValue = document.getElementById("strength-value");
const statusEl = document.getElementById("status");

strengthInput.addEventListener("input", () => {
  strengthValue.textContent = strengthInput.value;
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  statusEl.className = "status";
  statusEl.textContent = "Processing mesh with MeshLib...";

  const formData = new FormData(form);
  formData.set("smoothing_strength", strengthInput.value);

  try {
    const response = await fetch("/api/process", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      const payload = await response.json();
      statusEl.classList.add("error");
      statusEl.textContent = payload.error || "Processing failed.";
      return;
    }

    const blob = await response.blob();
    const downloadUrl = URL.createObjectURL(blob);
    const anchor = document.createElement("a");
    anchor.href = downloadUrl;
    anchor.download = "processed-mesh";
    anchor.click();
    URL.revokeObjectURL(downloadUrl);

    statusEl.classList.add("success");
    statusEl.textContent = "Done! Your processed mesh has been downloaded.";
  } catch (error) {
    statusEl.classList.add("error");
    statusEl.textContent = "Network error. Please try again.";
  }
});
