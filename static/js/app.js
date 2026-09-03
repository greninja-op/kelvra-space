/**
 * KelvraSpace — Hub Client & Live Ecosystem Status Poller
 */

async function refreshTelemetry() {
  try {
    const res = await fetch("/api/overview");
    const data = await res.json();
    const services = data.services || {};

    // 1. Voice
    const voice = services.voice || {};
    const voiceBadge = document.getElementById("voiceStatusBadge");
    const voiceMeta = document.getElementById("voiceMeta");
    if (voice.online) {
      voiceBadge.className = "card-status-badge online";
      voiceBadge.innerText = "ONLINE";
      voiceMeta.innerText = `Engine: ${voice.engine || "Whisper"} · Air-Gap: ${voice.local_only ? "Active" : "Off"}`;
    } else {
      voiceBadge.className = "card-status-badge offline";
      voiceBadge.innerText = "STANDBY";
      voiceMeta.innerText = "Service awaiting launch on port 8765";
    }

    // 2. Bench
    const bench = services.bench || {};
    const benchBadge = document.getElementById("benchStatusBadge");
    const benchMeta = document.getElementById("benchMeta");
    if (bench.online) {
      benchBadge.className = "card-status-badge online";
      benchBadge.innerText = "ONLINE";
      benchMeta.innerText = `Guard: ${bench.prompt_guard_status || "ARMED"} · Collision Engine: Ready`;
    } else {
      benchBadge.className = "card-status-badge offline";
      benchBadge.innerText = "STANDBY";
      benchMeta.innerText = "Service awaiting launch on port 8099";
    }

    // 3. Security
    const sec = services.security || {};
    const secBadge = document.getElementById("securityStatusBadge");
    const secMeta = document.getElementById("securityMeta");
    if (sec.online) {
      secBadge.className = "card-status-badge online";
      secBadge.innerText = "ONLINE";
      secMeta.innerText = `Capabilities: ${(sec.capabilities || []).slice(0, 2).join(", ")}`;
    } else {
      secBadge.className = "card-status-badge offline";
      secBadge.innerText = "STANDBY";
      secMeta.innerText = "Service awaiting launch on port 8100";
    }
  } catch (e) {
    console.debug("Telemetry refresh error:", e);
  }
}

// Initial fetch and 5s polling loop
document.addEventListener("DOMContentLoaded", () => {
  refreshTelemetry();
  setInterval(refreshTelemetry, 5000);
});
