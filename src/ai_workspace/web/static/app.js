let workspaceStartedAt = null;

function pad(n) {
  return String(n).padStart(2, "0");
}

function formatClock(date) {
  return `${pad(date.getHours())}:${pad(date.getMinutes())}:${pad(date.getSeconds())}`;
}

function formatElapsed(startedAt) {
  if (!startedAt) {
    return "-";
  }
  const start = new Date(startedAt).getTime();
  const now = Date.now();
  let seconds = Math.max(0, Math.floor((now - start) / 1000));
  const hours = Math.floor(seconds / 3600);
  seconds -= hours * 3600;
  const minutes = Math.floor(seconds / 60);
  seconds -= minutes * 60;
  return `${pad(hours)}:${pad(minutes)}:${pad(seconds)}`;
}

function tickClock() {
  document.getElementById("clock").textContent = formatClock(new Date());
  document.getElementById("elapsed-time").textContent = formatElapsed(workspaceStartedAt);
}

function renderWorkspace(workspace) {
  workspaceStartedAt = workspace.started_at || null;
  document.getElementById("project-name").textContent = workspace.project_name || "-";
  document.getElementById("current-task").textContent = workspace.current_task_title || "-";
  document.getElementById("workspace-status").textContent = workspace.status_label || "-";
  document.getElementById("elapsed-time").textContent = formatElapsed(workspaceStartedAt);
}

function renderEngines(engines) {
  const list = document.getElementById("engine-list");
  list.innerHTML = "";
  (engines || []).forEach((engine) => {
    const li = document.createElement("li");
    li.textContent = `${engine.name}: ${engine.status_label}`;
    list.appendChild(li);
  });
}

function renderStats(stats) {
  const list = document.getElementById("stats-list");
  list.innerHTML = "";
  if (!stats) {
    return;
  }
  const rows = [
    ["전체", stats.total],
    ["성공", stats.success],
    ["실패", stats.failure],
    ["취소", stats.cancelled],
    ["시간 초과", stats.timed_out],
  ];
  rows.forEach(([label, value]) => {
    const li = document.createElement("li");
    li.textContent = `${label}: ${value}`;
    list.appendChild(li);
  });
}

function renderHistory(history) {
  const list = document.getElementById("history-list");
  list.innerHTML = "";
  (history || []).forEach((entry) => {
    const li = document.createElement("li");
    li.textContent = `[${entry.executed_at}] ${entry.engine} - ${entry.result_label}`;
    list.appendChild(li);
  });
}

function renderReliability(reliability) {
  const list = document.getElementById("reliability-list");
  list.innerHTML = "";
  if (!reliability) {
    return;
  }
  const rows = [
    ["재시도 횟수", reliability.retry_count],
    ["시간 초과 횟수", reliability.timeout_count],
    ["취소 횟수", reliability.cancelled_count],
    ["인증 실패 횟수", reliability.authentication_failure_count],
  ];
  rows.forEach(([label, value]) => {
    const li = document.createElement("li");
    li.textContent = `${label}: ${value}`;
    list.appendChild(li);
  });
}

function renderAutomationSummary(automationStatus) {
  const list = document.getElementById("automation-summary-list");
  list.innerHTML = "";
  if (!automationStatus) {
    return;
  }
  const rows = [
    ["등록된 Rule 수", automationStatus.registered_rule_count],
    ["활성 Rule 수", automationStatus.enabled_rule_count],
    ["마지막 실행", automationStatus.last_execution_at || "-"],
    ["다음 실행 예정", automationStatus.next_execution_at || "-"],
  ];
  rows.forEach(([label, value]) => {
    const li = document.createElement("li");
    li.textContent = `${label}: ${value}`;
    list.appendChild(li);
  });
}

const HEALTH_STATUS_LABELS = {
  healthy: "정상",
  degraded: "저하",
  unhealthy: "비정상",
};

function formatUptime(uptimeSeconds) {
  if (uptimeSeconds === null || uptimeSeconds === undefined) {
    return "-";
  }
  let seconds = Math.max(0, Math.floor(uptimeSeconds));
  const hours = Math.floor(seconds / 3600);
  seconds -= hours * 3600;
  const minutes = Math.floor(seconds / 60);
  seconds -= minutes * 60;
  return `${pad(hours)}:${pad(minutes)}:${pad(seconds)}`;
}

function renderProduction(productionStatus, config) {
  const list = document.getElementById("production-list");
  list.innerHTML = "";
  if (!productionStatus) {
    return;
  }
  const rows = [
    ["Server 상태", HEALTH_STATUS_LABELS[productionStatus.health_status] || productionStatus.health_status],
    ["Version", productionStatus.version],
    ["시작 시각", productionStatus.started_at || "-"],
    ["Uptime", formatUptime(productionStatus.uptime_seconds)],
  ];
  (productionStatus.components || []).forEach((component) => {
    const label = HEALTH_STATUS_LABELS[component.status] || component.status;
    rows.push([`  - ${component.name}`, label]);
  });
  if (config) {
    rows.push([
      "Configuration",
      `${config.host}:${config.port}, log_level=${config.log_level}, dashboard=${config.dashboard_enabled}, automation=${config.automation_enabled}`,
    ]);
  }
  rows.forEach(([label, value]) => {
    const li = document.createElement("li");
    li.textContent = `${label}: ${value}`;
    list.appendChild(li);
  });
}

function renderDashboard(data) {
  renderWorkspace(data.workspace || {});
  renderEngines(data.engines);
  renderStats(data.execution_stats);
  renderHistory(data.recent_history);
  renderReliability(data.reliability_stats);
  renderAutomationSummary(data.automation_status);
  renderProduction(data.production_status, window.__productionConfig);
}

async function fetchProductionConfig() {
  const response = await fetch("/api/config");
  if (!response.ok) {
    return;
  }
  window.__productionConfig = await response.json();
}

async function fetchInitialDashboard() {
  const response = await fetch("/api/dashboard");
  const data = await response.json();
  renderDashboard(data);
}

function connectWebSocket() {
  const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
  const socket = new WebSocket(`${protocol}//${window.location.host}/ws/dashboard`);
  socket.onmessage = (event) => {
    renderDashboard(JSON.parse(event.data));
  };
  socket.onclose = () => {
    setTimeout(connectWebSocket, 2000);
  };
}

function describeTrigger(trigger) {
  if (trigger.kind === "time") {
    const day = trigger.day_of_week || (trigger.day_of_month ? `매월 ${trigger.day_of_month}일` : "매일");
    return `Time: ${day} ${trigger.time_of_day}`;
  }
  if (trigger.kind === "interval") {
    return `Interval: ${trigger.interval_seconds}초마다`;
  }
  if (trigger.kind === "event") {
    return `Event: ${trigger.event_type}`;
  }
  return "Startup";
}

function describeAction(action) {
  if (action.kind === "run_task") {
    return `Task 실행: ${action.task_title || "-"}`;
  }
  if (action.kind === "run_workflow") {
    return `Workflow 실행: ${action.workflow_id || "-"}`;
  }
  if (action.kind === "notification") {
    return `Notification: ${action.notification_message || "-"}`;
  }
  return "Dashboard Refresh";
}

async function fetchAutomationRules() {
  const response = await fetch("/api/automation");
  if (!response.ok) {
    return;
  }
  const rules = await response.json();
  renderAutomationRules(rules);
}

function renderAutomationRules(rules) {
  const tbody = document.getElementById("automation-rule-list");
  tbody.innerHTML = "";
  (rules || []).forEach((rule) => {
    const tr = document.createElement("tr");

    const cells = [
      rule.name,
      describeTrigger(rule.trigger),
      describeAction(rule.action),
      rule.enabled ? "활성" : "비활성",
      rule.last_executed_at || "-",
      rule.next_execution_at || "-",
    ];
    cells.forEach((text) => {
      const td = document.createElement("td");
      td.textContent = text;
      tr.appendChild(td);
    });

    const actionsTd = document.createElement("td");
    actionsTd.appendChild(
      makeRuleButton(rule.enabled ? "비활성화" : "활성화", "", () => toggleRule(rule))
    );
    actionsTd.appendChild(makeRuleButton("삭제", "danger", () => deleteRule(rule)));
    tr.appendChild(actionsTd);

    tbody.appendChild(tr);
  });
}

function makeRuleButton(label, extraClass, onClick) {
  const button = document.createElement("button");
  button.type = "button";
  button.className = extraClass ? `rule-action ${extraClass}` : "rule-action";
  button.textContent = label;
  button.addEventListener("click", onClick);
  return button;
}

async function refreshAutomationSummary() {
  const response = await fetch("/api/summary");
  if (!response.ok) {
    return;
  }
  const data = await response.json();
  renderAutomationSummary(data.automation_status);
}

async function toggleRule(rule) {
  const endpoint = rule.enabled ? "disable" : "enable";
  await fetch(`/api/automation/${rule.rule_id}/${endpoint}`, { method: "POST" });
  fetchAutomationRules();
  refreshAutomationSummary();
}

async function deleteRule(rule) {
  await fetch(`/api/automation/${rule.rule_id}`, { method: "DELETE" });
  fetchAutomationRules();
  refreshAutomationSummary();
}

function updateVisibleFields(selectId, fieldClass, prefix) {
  const select = document.getElementById(selectId);
  document.querySelectorAll(`.${fieldClass}`).forEach((el) => el.classList.remove("visible"));
  document
    .querySelectorAll(`.${prefix}-${select.value}`)
    .forEach((el) => el.classList.add("visible"));
}

function buildTriggerFromForm() {
  const kind = document.getElementById("rule-trigger-kind").value;
  const trigger = { kind };
  if (kind === "time") {
    trigger.time_of_day = document.getElementById("rule-trigger-time-of-day").value;
  } else if (kind === "interval") {
    trigger.interval_seconds = Number(
      document.getElementById("rule-trigger-interval-seconds").value
    );
  } else if (kind === "event") {
    trigger.event_type = document.getElementById("rule-trigger-event-type").value;
  }
  return trigger;
}

function buildActionFromForm() {
  const kind = document.getElementById("rule-action-kind").value;
  const action = { kind };
  if (kind === "run_task") {
    action.project_id = document.getElementById("rule-action-project-id").value;
    action.task_title = document.getElementById("rule-action-task-title").value;
  } else if (kind === "run_workflow") {
    action.workflow_id = document.getElementById("rule-action-workflow-id").value;
  } else if (kind === "notification") {
    action.notification_message = document.getElementById(
      "rule-action-notification-message"
    ).value;
  }
  return action;
}

async function submitAutomationForm(event) {
  event.preventDefault();
  const body = {
    name: document.getElementById("rule-name").value,
    description: document.getElementById("rule-description").value,
    trigger: buildTriggerFromForm(),
    action: buildActionFromForm(),
  };
  await fetch("/api/automation", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  document.getElementById("automation-form").reset();
  fetchAutomationRules();
  refreshAutomationSummary();
}

function setupAutomationForm() {
  document
    .getElementById("rule-trigger-kind")
    .addEventListener("change", () => updateVisibleFields("rule-trigger-kind", "trigger-field", "trigger"));
  document
    .getElementById("rule-action-kind")
    .addEventListener("change", () => updateVisibleFields("rule-action-kind", "action-field", "action"));
  document.getElementById("automation-form").addEventListener("submit", submitAutomationForm);

  updateVisibleFields("rule-trigger-kind", "trigger-field", "trigger");
  updateVisibleFields("rule-action-kind", "action-field", "action");
}

document.addEventListener("DOMContentLoaded", async () => {
  tickClock();
  setInterval(tickClock, 1000);
  await fetchProductionConfig();
  fetchInitialDashboard();
  connectWebSocket();
  setupAutomationForm();
  fetchAutomationRules();
});
