(() => {
  const forms = document.querySelectorAll("[data-operation-form]");
  forms.forEach((form) => {
    form.addEventListener("submit", () => {
      const button = form.querySelector("button[type='submit']");
      if (!button || button.disabled) return;
      button.dataset.originalText = button.textContent;
      button.textContent = "Starting…";
      button.disabled = true;
    });
  });

  const container = document.querySelector("[data-operation-id]");
  if (!container) return;

  const operationId = container.dataset.operationId;
  const status = container.querySelector(".operation-status");
  const started = container.querySelector("[data-operation-started]");
  const completed = container.querySelector("[data-operation-completed]");
  const output = container.querySelector("[data-operation-output]");
  const progress = container.querySelector("[data-operation-progress]");

  const applyStatusClass = (value) => {
    status.classList.remove("good", "bad", "warn");
    if (value === "completed") status.classList.add("good");
    else if (value === "failed") status.classList.add("bad");
    else status.classList.add("warn");
  };

  const poll = async () => {
    try {
      const response = await fetch(`/api/operations/${operationId}`, {
        headers: { Accept: "application/json" },
        cache: "no-store",
      });
      if (!response.ok) return;
      const operation = await response.json();
      status.textContent = operation.status;
      applyStatusClass(operation.status);
      started.textContent = operation.started_at || "waiting";
      completed.textContent = operation.completed_at || "—";
      if (operation.error) output.textContent = operation.error;
      else if (operation.summary) output.textContent = operation.summary;
      else output.textContent = `Operation is ${operation.status}. This page updates automatically.`;

      if (operation.status === "completed" || operation.status === "failed") {
        progress.classList.add("finished");
        return;
      }
      window.setTimeout(poll, 1200);
    } catch (_) {
      window.setTimeout(poll, 2200);
    }
  };

  poll();
})();
