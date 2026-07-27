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

function renderDashboard(data) {
  renderWorkspace(data.workspace || {});
  renderEngines(data.engines);
  renderStats(data.execution_stats);
  renderHistory(data.recent_history);
  renderReliability(data.reliability_stats);
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

document.addEventListener("DOMContentLoaded", () => {
  tickClock();
  setInterval(tickClock, 1000);
  fetchInitialDashboard();
  connectWebSocket();
});
