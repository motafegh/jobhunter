(() => {
  const forms = document.querySelectorAll("[data-operation-form]");
  forms.forEach((form) => {
    form.addEventListener("submit", (event) => {
      const button = event.submitter || form.querySelector("button[type='submit']");
      if (!button || button.disabled) return;
      button.dataset.originalText = button.textContent;
      button.textContent = "Starting…";
      button.disabled = true;
    });
  });

  const syncForm = document.querySelector("[data-sync-form]");
  const presets = {
    light: {
      search_limit: 12,
      request_budget: 12,
      missing_limit: 3,
      refresh_limit: 2,
      refresh_after_hours: 24,
    },
    normal: {
      search_limit: 40,
      request_budget: 40,
      missing_limit: 10,
      refresh_limit: 5,
      refresh_after_hours: 24,
    },
    thorough: {
      search_limit: 80,
      request_budget: 80,
      missing_limit: 20,
      refresh_limit: 10,
      refresh_after_hours: 72,
    },
  };

  document.querySelectorAll("[data-sync-preset]").forEach((button) => {
    button.addEventListener("click", () => {
      if (!syncForm) return;
      const preset = presets[button.dataset.syncPreset];
      if (!preset) return;
      Object.entries(preset).forEach(([name, value]) => {
        const field = syncForm.elements.namedItem(name);
        if (field) field.value = value;
      });
      document.querySelectorAll("[data-sync-preset]").forEach((item) => {
        item.classList.toggle("active", item === button);
      });
    });
  });

  const container = document.querySelector("[data-operation-id]");
  if (!container) return;

  const operationId = container.dataset.operationId;
  const returnUrl = container.dataset.returnUrl || "";
  const autoReturn = container.dataset.autoReturn === "true";
  const status = container.querySelector(".operation-status");
  const started = container.querySelector("[data-operation-started]");
  const completed = container.querySelector("[data-operation-completed]");
  const output = container.querySelector("[data-operation-output]");
  const progress = container.querySelector("[data-operation-progress]");
  const returnMessage = container.querySelector("[data-operation-return]");

  const isTerminal = (value) =>
    value === "completed" || value === "completed_with_failures" || value === "failed";

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

      if (isTerminal(operation.status)) {
        progress.classList.add("finished");
        if (operation.status === "completed" && returnUrl && autoReturn) {
          if (returnMessage) returnMessage.textContent = "Completed. Returning to the previous screen…";
          window.setTimeout(() => window.location.assign(returnUrl), 900);
        } else if (returnMessage && returnUrl) {
          returnMessage.textContent = "Operation finished. Use the return button above to continue.";
        }
        return;
      }
      window.setTimeout(poll, 1200);
    } catch (_) {
      window.setTimeout(poll, 2200);
    }
  };

  poll();
})();
