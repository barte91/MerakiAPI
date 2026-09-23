const logContent = document.getElementById("log-content");
const logPanel = document.getElementById("log-panel");
const logStatus = document.getElementById("log-status");
const autoscrollLbl = document.getElementById("autoscroll-label");

let autoscroll = true;
let evtSource = null;

/* ── Avvia la connessione SSE ─────────────────────────── */
function startLogStream() {
    evtSource = new EventSource("/api/log-stream");

    evtSource.onopen = function () {
        logStatus.textContent = "● Connesso";
        logStatus.className = "connected";
    };

    evtSource.onmessage = function (e) {
        if (!e.data || !e.data.trim()) return; // heartbeat vuoto

        const line = document.createElement("div");
        const msg = e.data;

        // Assegna classe CSS in base al livello
        if (msg.includes("[ERROR]")) line.className = "log-error";
        else if (msg.includes("[WARNING]")) line.className = "log-warning";
        else if (msg.includes("[INFO]")) line.className = "log-info";
        else line.className = "log-debug";

        line.textContent = msg;
        logContent.appendChild(line);

        if (autoscroll) {
            logPanel.scrollTop = logPanel.scrollHeight;
        }
    };

    evtSource.onerror = function () {
        logStatus.textContent = "● Disconnesso — riconnessione...";
        logStatus.className = "disconnected";
        // Il browser riprova automaticamente dopo ~3s
    };
}

/* ── Pulisce il pannello ──────────────────────────────── */
function clearLog() {
    logContent.innerHTML = "";
}

/* ── Toggle autoscroll ────────────────────────────────── */
function toggleAutoscroll() {
    autoscroll = !autoscroll;
    autoscrollLbl.textContent = autoscroll ? "ON" : "OFF";
}

// Avvia subito al caricamento della pagina
startLogStream();