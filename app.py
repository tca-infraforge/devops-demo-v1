from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
import socket
import time

STARTED = time.time()
REQUESTS = 0


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        global REQUESTS
        REQUESTS += 1

        if self.path == "/healthz":
            self.reply(
                json.dumps(
                    {
                        "status": "ok",
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                    }
                ),
                "application/json",
            )
            return

        if self.path == "/api/status":
            self.reply(
                json.dumps(
                    {
                        "version": os.getenv("APP_VERSION", "local"),
                        "hostname": socket.gethostname(),
                        "uptime": round(time.time() - STARTED, 1),
                        "requests": REQUESTS,
                        "status": "healthy",
                    }
                ),
                "application/json",
            )
            return

        if self.path == "/metrics":
            uptime = time.time() - STARTED
            metrics = (
                "# HELP devops_clock_http_requests_total Total HTTP requests served.\n"
                "# TYPE devops_clock_http_requests_total counter\n"
                f"devops_clock_http_requests_total {REQUESTS}\n"
                "# HELP devops_clock_uptime_seconds Application uptime in seconds.\n"
                "# TYPE devops_clock_uptime_seconds gauge\n"
                f"devops_clock_uptime_seconds {uptime:.2f}\n"
            )
            self.reply(metrics, "text/plain; version=0.0.4")
            return

        version = os.getenv("APP_VERSION", "local")
        hostname = socket.gethostname()
        environment = os.getenv("ENVIRONMENT", "development")

        page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>DevOps Deployment Clock</title>

<style>
:root {{
    --paper: #f7f1e7;
    --ink: #23231f;
    --muted: #777166;
    --line: #d5c8b7;
    --panel: #f0d9b5;
    --panel-dark: #243630;
    --olive: #71836b;
    --brass: #d09a42;
    --rust: #d96f49;
    --ok: #4f8f73;
}}

* {{ box-sizing: border-box; }}

html, body {{
    margin: 0;
    min-height: 100%;
}}

body {{
    min-height: 100vh;
    background:
        linear-gradient(180deg, #fff8ef 0%, #f7f1e7 58%, #efe3d6 100%);
    color: var(--ink);
    font-family: "Avenir Next", Avenir, "Helvetica Neue", Arial, sans-serif;
}}

.shell {{
    width: min(1480px, calc(100% - 56px));
    margin: 0 auto;
    padding: 34px 0 44px;
}}

.topline {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1px solid var(--line);
    padding-bottom: 18px;
}}

.brand {{
    display: flex;
    align-items: baseline;
    gap: 14px;
}}

.brand h1 {{
    margin: 0;
    font-family: Georgia, "Times New Roman", serif;
    font-size: clamp(1.8rem, 3.5vw, 3.6rem);
    font-weight: 500;
    letter-spacing: -0.035em;
}}

.brand span {{
    color: var(--muted);
    font-size: .78rem;
    letter-spacing: .18em;
    text-transform: uppercase;
}}

.health {{
    display: flex;
    align-items: center;
    gap: 10px;
    color: var(--muted);
    font-size: .86rem;
}}

.health-dot {{
    width: 9px;
    height: 9px;
    border-radius: 50%;
    background: var(--ok);
}}

.hero {{
    display: grid;
    grid-template-columns: 1.6fr 1fr;
    gap: 18px;
    margin-top: 18px;
}}

.time-block {{
    min-height: 270px;
    padding: 28px 30px 24px;
    border: 1px solid var(--line);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}}

.time-block.local {{
    background:
        linear-gradient(135deg, #1f3b34 0%, #31574b 62%, #5b7f69 100%);
    color: #fffaf2;
    border-color: #2f584d;
}}

.time-block.utc {{
    background:
        linear-gradient(135deg, #f4d7a6 0%, #eebf73 100%);
}}

.eyebrow {{
    display: flex;
    justify-content: space-between;
    gap: 20px;
    font-size: .75rem;
    text-transform: uppercase;
    letter-spacing: .15em;
    opacity: .72;
}}

.big-time {{
    font-family: "Courier New", ui-monospace, monospace;
    font-size: clamp(3rem, 8vw, 7.6rem);
    line-height: .9;
    letter-spacing: -.08em;
    font-variant-numeric: tabular-nums;
}}

.date-line {{
    display: flex;
    justify-content: space-between;
    align-items: end;
    gap: 20px;
    color: inherit;
    opacity: .76;
    font-size: .95rem;
}}

.section-head {{
    display: flex;
    align-items: end;
    justify-content: space-between;
    margin: 34px 0 14px;
}}

.section-head h2 {{
    margin: 0;
    font-family: Georgia, "Times New Roman", serif;
    font-weight: 500;
    font-size: clamp(1.5rem, 2.5vw, 2.5rem);
}}

.section-head p {{
    margin: 0;
    max-width: 620px;
    color: var(--muted);
    text-align: right;
    font-size: .9rem;
}}

.world-grid {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    border-top: 1px solid var(--line);
    border-left: 1px solid var(--line);
}}

.world-clock {{
    min-height: 360px;
    padding: 24px 22px 22px;
    border-right: 1px solid var(--line);
    border-bottom: 1px solid var(--line);
    background: #fffaf2;
    display: flex;
    flex-direction: column;
    align-items: center;
}}

.city-row {{
    width: 100%;
    display: flex;
    justify-content: space-between;
    gap: 12px;
}}

.city {{
    font-family: Georgia, "Times New Roman", serif;
    font-size: 1.25rem;
}}

.zone {{
    color: var(--muted);
    font-size: .74rem;
    line-height: 1.35;
    text-align: right;
}}

.analog {{
    width: min(190px, 70vw);
    aspect-ratio: 1;
    border: 2px solid var(--ink);
    border-radius: 50%;
    margin: 26px 0 20px;
    position: relative;
    background:
        radial-gradient(circle at center, var(--ink) 0 4px, transparent 4.5px),
        var(--paper);
}}

.tick {{
    position: absolute;
    left: 50%;
    top: 50%;
    width: 1px;
    height: 47%;
    transform-origin: 50% 0%;
}}

.tick::before {{
    content: "";
    display: block;
    width: 1px;
    height: 7px;
    background: var(--ink);
}}

.hand {{
    position: absolute;
    left: 50%;
    bottom: 50%;
    transform-origin: 50% 100%;
    border-radius: 999px;
}}

.hour {{
    width: 4px;
    height: 27%;
    background: var(--ink);
}}

.minute {{
    width: 2px;
    height: 36%;
    background: var(--ink);
}}

.second {{
    width: 1px;
    height: 40%;
    background: var(--rust);
}}

.digital {{
    font-family: "Courier New", ui-monospace, monospace;
    font-size: 1.6rem;
    font-variant-numeric: tabular-nums;
    letter-spacing: -.04em;
}}

.world-date {{
    color: var(--muted);
    font-size: .76rem;
    margin-top: 4px;
}}

.telemetry {{
    margin-top: 28px;
    border-top: 1px solid var(--line);
    border-bottom: 1px solid var(--line);
    display: grid;
    grid-template-columns: 1.4fr repeat(4, 1fr);
}}

.telemetry > div {{
    padding: 18px 16px;
    border-right: 1px solid var(--line);
}}

.telemetry > div:last-child {{
    border-right: 0;
}}

.telemetry .label {{
    color: var(--muted);
    font-size: .68rem;
    text-transform: uppercase;
    letter-spacing: .14em;
    margin-bottom: 8px;
}}

.telemetry .value {{
    font-size: .95rem;
    overflow-wrap: anywhere;
}}

.actions {{
    display: flex;
    gap: 10px;
    margin-top: 18px;
}}

button, .button {{
    appearance: none;
    border: 1px solid var(--ink);
    background: transparent;
    color: var(--ink);
    padding: 10px 14px;
    font: inherit;
    font-size: .82rem;
    text-decoration: none;
    cursor: pointer;
}}

button:hover, .button:hover {{
    background: var(--ink);
    color: var(--paper);
}}

#message {{
    margin-left: auto;
    align-self: center;
    color: var(--muted);
    font-size: .78rem;
}}

footer {{
    margin-top: 24px;
    color: var(--muted);
    font-size: .72rem;
    letter-spacing: .08em;
    text-transform: uppercase;
}}

@media (max-width: 1000px) {{
    .hero {{
        grid-template-columns: 1fr;
    }}

    .world-grid {{
        grid-template-columns: repeat(2, 1fr);
    }}

    .telemetry {{
        grid-template-columns: repeat(2, 1fr);
    }}

    .telemetry > div:first-child {{
        grid-column: 1 / -1;
    }}
}}

@media (max-width: 640px) {{
    .shell {{
        width: min(100% - 28px, 1480px);
        padding-top: 20px;
    }}

    .topline,
    .section-head,
    .date-line,
    .actions {{
        align-items: flex-start;
        flex-direction: column;
    }}

    .section-head p {{
        text-align: left;
    }}

    .world-grid,
    .telemetry {{
        grid-template-columns: 1fr;
    }}

    .telemetry > div:first-child {{
        grid-column: auto;
    }}

    .big-time {{
        font-size: clamp(3rem, 18vw, 5.5rem);
    }}

    #message {{
        margin-left: 0;
    }}
}}
</style>
</head>

<body>
<main class="shell">
    <header class="topline">
        <div class="brand">
            <h1>Deployment Clock</h1>
            <span>Live release surface</span>
        </div>

        <div class="health">
            <span class="health-dot"></span>
            <span>Application healthy</span>
        </div>
    </header>

    <section class="hero">
        <article class="time-block local">
            <div class="eyebrow">
                <span>Local time</span>
                <span id="local-zone">Detecting timezone</span>
            </div>

            <div id="local-clock" class="big-time">--:--:--</div>

            <div class="date-line">
                <span id="local-date">Loading...</span>
                <span>Your browser timezone</span>
            </div>
        </article>

        <article class="time-block utc">
            <div class="eyebrow">
                <span>UTC</span>
                <span>Coordinated Universal Time</span>
            </div>

            <div id="utc-clock" class="big-time">--:--:--</div>

            <div class="date-line">
                <span id="utc-date">Loading...</span>
                <span>UTC +00:00</span>
            </div>
        </article>
    </section>

    <div class="section-head">
        <h2>World clock wall</h2>
        <p>Four reference markets, kept intentionally visible during the deployment demo.</p>
    </div>

    <section class="world-grid" id="world-grid"></section>

    <section class="telemetry">
        <div>
            <div class="label">Application version</div>
            <div class="value">🚀 {version}</div>
        </div>
        <div>
            <div class="label">Pod / host</div>
            <div class="value">📦 {hostname}</div>
        </div>
        <div>
            <div class="label">Environment</div>
            <div class="value">⚙ {environment}</div>
        </div>
        <div>
            <div class="label">Requests</div>
            <div class="value" id="requests">{REQUESTS}</div>
        </div>
        <div>
            <div class="label">Uptime</div>
            <div class="value" id="uptime">0 sec</div>
        </div>
    </section>

    <div class="actions">
        <button onclick="refreshStatus()">Refresh status</button>
        <button onclick="checkHealth()">Run health check</button>
        <a class="button" href="/metrics" target="_blank">Open metrics</a>
        <div id="message"></div>
    </div>

    <footer>DevOps Deployment Clock · Python HTTP Server</footer>
</main>

<script>
const clocks = [
    {{
        city: "Toronto",
        subtitle: "North America",
        timeZone: "America/Toronto",
        short: "ET"
    }},
    {{
        city: "Mumbai",
        subtitle: "India",
        timeZone: "Asia/Kolkata",
        short: "IST"
    }},
    {{
        city: "Tokyo",
        subtitle: "Japan",
        timeZone: "Asia/Tokyo",
        short: "JST"
    }},
    {{
        city: "Lagos",
        subtitle: "Nigeria",
        timeZone: "Africa/Lagos",
        short: "WAT"
    }}
];

function makeTicks() {{
    return Array.from({{ length: 12 }}, (_, i) =>
        `<span class="tick" style="transform: rotate(${{i * 30}}deg) translateY(-50%);"></span>`
    ).join("");
}}

function buildWorldClocks() {{
    const grid = document.getElementById("world-grid");

    grid.innerHTML = clocks.map((clock, index) => `
        <article class="world-clock">
            <div class="city-row">
                <div>
                    <div class="city">${{clock.city}}</div>
                    <div class="world-date">${{clock.subtitle}}</div>
                </div>
                <div class="zone">
                    ${{clock.short}}<br>
                    ${{clock.timeZone}}
                </div>
            </div>

            <div class="analog">
                ${{makeTicks()}}
                <div class="hand hour" id="hour-${{index}}"></div>
                <div class="hand minute" id="minute-${{index}}"></div>
                <div class="hand second" id="second-${{index}}"></div>
            </div>

            <div class="digital" id="digital-${{index}}">--:--:--</div>
            <div class="world-date" id="date-${{index}}">Loading...</div>
        </article>
    `).join("");
}}

function partsForZone(date, timeZone) {{
    const parts = new Intl.DateTimeFormat("en-CA", {{
        timeZone,
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
        hour12: false
    }}).formatToParts(date);

    const result = {{}};
    for (const p of parts) {{
        if (p.type !== "literal") result[p.type] = p.value;
    }}
    return result;
}}

function renderWorldClocks() {{
    const now = new Date();

    clocks.forEach((clock, index) => {{
        const parts = partsForZone(now, clock.timeZone);
        const hour = Number(parts.hour) % 12;
        const minute = Number(parts.minute);
        const second = Number(parts.second);

        const hourDeg = (hour * 30) + (minute * 0.5);
        const minuteDeg = (minute * 6) + (second * 0.1);
        const secondDeg = second * 6;

        document.getElementById(`hour-${{index}}`).style.transform =
            `translateX(-50%) rotate(${{hourDeg}}deg)`;

        document.getElementById(`minute-${{index}}`).style.transform =
            `translateX(-50%) rotate(${{minuteDeg}}deg)`;

        document.getElementById(`second-${{index}}`).style.transform =
            `translateX(-50%) rotate(${{secondDeg}}deg)`;

        document.getElementById(`digital-${{index}}`).textContent =
            new Intl.DateTimeFormat("en-CA", {{
                timeZone: clock.timeZone,
                hour: "2-digit",
                minute: "2-digit",
                second: "2-digit",
                hour12: false
            }}).format(now);

        document.getElementById(`date-${{index}}`).textContent =
            new Intl.DateTimeFormat("en-US", {{
                timeZone: clock.timeZone,
                weekday: "short",
                month: "short",
                day: "numeric"
            }}).format(now);
    }});
}}

function updatePrimaryClocks() {{
    const now = new Date();
    const localZone = Intl.DateTimeFormat().resolvedOptions().timeZone || "Local";

    document.getElementById("local-zone").textContent = localZone;

    document.getElementById("local-clock").textContent =
        new Intl.DateTimeFormat("en-CA", {{
            hour: "2-digit",
            minute: "2-digit",
            second: "2-digit",
            hour12: false
        }}).format(now);

    document.getElementById("local-date").textContent =
        new Intl.DateTimeFormat("en-US", {{
            weekday: "long",
            year: "numeric",
            month: "long",
            day: "numeric"
        }}).format(now);

    document.getElementById("utc-clock").textContent =
        new Intl.DateTimeFormat("en-CA", {{
            timeZone: "UTC",
            hour: "2-digit",
            minute: "2-digit",
            second: "2-digit",
            hour12: false
        }}).format(now);

    document.getElementById("utc-date").textContent =
        new Intl.DateTimeFormat("en-US", {{
            timeZone: "UTC",
            weekday: "long",
            year: "numeric",
            month: "long",
            day: "numeric"
        }}).format(now);

    renderWorldClocks();
}}

async function refreshStatus() {{
    const message = document.getElementById("message");
    message.textContent = "Refreshing deployment status...";

    try {{
        const response = await fetch("/api/status");
        const data = await response.json();

        document.getElementById("requests").textContent = data.requests;
        document.getElementById("uptime").textContent = formatUptime(data.uptime);

        message.textContent = "Deployment information refreshed";
    }} catch (error) {{
        message.textContent = "Could not refresh application status";
    }}
}}

async function checkHealth() {{
    const message = document.getElementById("message");
    message.textContent = "Running health check...";

    try {{
        const response = await fetch("/healthz");
        const data = await response.json();
        message.textContent = data.status === "ok"
            ? "Health check passed"
            : "Health check returned an unexpected state";
    }} catch (error) {{
        message.textContent = "Health check failed";
    }}
}}

function formatUptime(seconds) {{
    seconds = Math.floor(seconds);

    if (seconds < 60) return `${{seconds}} sec`;

    const minutes = Math.floor(seconds / 60);
    if (minutes < 60) return `${{minutes}} min ${{seconds % 60}} sec`;

    const hours = Math.floor(minutes / 60);
    return `${{hours}} hr ${{minutes % 60}} min`;
}}

buildWorldClocks();
updatePrimaryClocks();
setInterval(updatePrimaryClocks, 1000);

refreshStatus();
setInterval(refreshStatus, 5000);
</script>
</body>
</html>"""

        self.reply(page, "text/html")

    def reply(self, body, content_type):
        data = body.encode()

        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()

        self.wfile.write(data)


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8000), Handler)

    print("🚀 DevOps Deployment Clock")
    print("🌐 http://localhost:8000")
    print("❤️  http://localhost:8000/healthz")
    print("📊 http://localhost:8000/metrics")
    print("\nPress Ctrl+C to stop.\n")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped.")
    finally:
        server.server_close()
