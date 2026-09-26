const navGroups = [
  { label: "OPERATIONS", items: [["Dashboard","▦"],["Risk Analysis & Scanner","⌕"],["Repositories","⑂"],["Deployment Health","⌁"]] },
  { label: "CRYPTO INTELLIGENCE", items: [["Cryptographic Scanner","◈"],["Dependency Graph","⌘"],["Blast Radius","◎"],["AI Investigation","✳"],["Migration Planner","⇢"],["Remediation Center","⚒"],["Crypto-Agility","◌"],["Crypto Timeline","↗"]] },
  { label: "POLICY & GOVERNANCE", items: [["Policy Center","⛨"],["Reports","▤"],["Evaluation","◫"],["Audit Logs","☷"],["Settings","⚙"],["Sample Data","▧"]] }
];
const navItems = navGroups.flatMap(group => group.items.map(item => ({ title: item[0], icon: item[1], count: item[2] })));
const assets = [
  { algorithm:"RSA", library:"OpenSSL", version:"3.0.13", role:"TLS certificate", file:"services/gateway/tls.py", line:84, key:"2048", protocol:"TLS 1.2", cert:"api.northstar.internal", service:"api-gateway", environment:"Production", classification:"Quantum-vulnerable", confidence:96, priority:"Critical", status:"Open", language:"Python" },
  { algorithm:"ECDSA", library:"cryptography", version:"42.0", role:"JWT signing", file:"services/auth/tokens.py", line:126, key:"P-256", protocol:"OIDC", cert:"auth-signing-2024", service:"identity-service", environment:"Production", classification:"Quantum-vulnerable", confidence:94, priority:"High", status:"Open", language:"Python" },
  { algorithm:"AES-256-GCM", library:"BouncyCastle", version:"1.77", role:"Data encryption", file:"src/main/java/crypto/Envelope.java", line:51, key:"256", protocol:"Internal", cert:"—", service:"vault-service", environment:"Production", classification:"Approved", confidence:99, priority:"Safe", status:"Verified", language:"Java" },
  { algorithm:"SHA-1", library:"OpenSSL", version:"3.0.13", role:"Certificate signature", file:"deploy/certs/legacy-chain.pem", line:1, key:"2048", protocol:"TLS 1.2", cert:"legacy-partner-chain", service:"partner-adapter", environment:"Staging", classification:"Deprecated", confidence:98, priority:"Critical", status:"Open", language:"Config" },
  { algorithm:"ML-KEM-768", library:"liboqs", version:"0.12.0", role:"Key encapsulation", file:"pqc/kem_provider.py", line:33, key:"—", protocol:"Hybrid TLS", cert:"—", service:"pqc-edge", environment:"Development", classification:"PQC candidate", confidence:91, priority:"Safe", status:"Pilot", language:"Python" },
  { algorithm:"3DES", library:"JCE", version:"17", role:"Legacy data decryption", file:"batch/ImportJob.java", line:203, key:"168", protocol:"Internal", cert:"—", service:"ledger-import", environment:"Production", classification:"Deprecated", confidence:89, priority:"High", status:"Open", language:"Java" },
  { algorithm:"AES-128-CBC", library:"OpenSSL", version:"3.0.13", role:"Session encryption", file:"services/session/crypto.py", line:68, key:"128", protocol:"TLS 1.2", cert:"—", service:"session-service", environment:"Production", classification:"Review required", confidence:86, priority:"Medium", status:"Review", language:"Python" },
  { algorithm:"SHA-256", library:"Go crypto", version:"1.22", role:"Integrity hash", file:"pkg/audit/digest.go", line:44, key:"—", protocol:"Internal", cert:"—", service:"audit-service", environment:"Production", classification:"Approved", confidence:99, priority:"Safe", status:"Verified", language:"Go" }
];
const findings = [
  { id:"CRY-2481", title:"RSA-2048 certificate on external API gateway", algorithm:"RSA", severity:"Critical", service:"api-gateway", file:"services/gateway/tls.py:84", confidence:"96%", age:"2h ago" },
  { id:"CRY-2474", title:"SHA-1 signature in partner certificate chain", algorithm:"SHA-1", severity:"Critical", service:"partner-adapter", file:"deploy/certs/legacy-chain.pem:1", confidence:"98%", age:"5h ago" },
  { id:"CRY-2462", title:"ECDSA signing key requires migration assessment", algorithm:"ECDSA", severity:"Medium", service:"identity-service", file:"services/auth/tokens.py:126", confidence:"94%", age:"1d ago" },
  { id:"CRY-2459", title:"AES-128-CBC configuration needs policy review", algorithm:"AES-128-CBC", severity:"Medium", service:"session-service", file:"services/session/crypto.py:68", confidence:"86%", age:"1d ago" }
];
const remediationJobs = [
  { id:"REM-1082", title:"Migrate gateway certificate to hybrid TLS profile", finding:"CRY-2481", status:"Approval Required", risk:"High", owner:"M. Chen", updated:"12 min ago", tests:"12 / 12 passed", before:"RSA-2048", after:"Hybrid ML-KEM + ECDHE" },
  { id:"REM-1079", title:"Replace SHA-1 partner certificate chain", finding:"CRY-2474", status:"Sandbox Testing", risk:"Medium", owner:"S. Patel", updated:"38 min ago", tests:"8 / 9 passed", before:"SHA-1 signature", after:"SHA-256 certificate chain" },
  { id:"REM-1071", title:"Provider abstraction for identity signing", finding:"CRY-2462", status:"Pending", risk:"Medium", owner:"A. Rivera", updated:"2 hours ago", tests:"Not run", before:"Hardcoded ECDSA", after:"Config-driven signing provider" },
  { id:"REM-1055", title:"AES-GCM profile deployed to vault service", finding:"CRY-2401", status:"Deployed", risk:"Low", owner:"M. Chen", updated:"Yesterday", tests:"24 / 24 passed", before:"AES-128-CBC", after:"AES-256-GCM" },
  { id:"REM-1038", title:"Rollback legacy partner cipher profile", finding:"CRY-2314", status:"Rolled Back", risk:"High", owner:"S. Patel", updated:"Sep 24", tests:"Compatibility regression", before:"TLS 1.3 only", after:"Reverted with exception" }
];
const firewallEvents = [
  { time:"13:14:22", decision:"REVIEW", tls:"TLS 1.2", cipher:"ECDHE-RSA-AES128-GCM-SHA256", source:"203.0.113.24", destination:"api.northstar.io:443", service:"api-gateway", reason:"Below policy minimum; client compatibility review required." },
  { time:"13:12:09", decision:"ALLOW", tls:"TLS 1.3", cipher:"TLS_AES_256_GCM_SHA384", source:"10.24.8.18", destination:"vault.svc:443", service:"vault-service", reason:"Meets active policy. Known service-to-service route." },
  { time:"13:08:51", decision:"MONITOR", tls:"TLS 1.3", cipher:"TLS_CHACHA20_POLY1305_SHA256", source:"10.24.5.9", destination:"auth.svc:443", service:"identity-service", reason:"Approved cipher observed; monitor certificate rotation." },
  { time:"12:59:17", decision:"WARN", tls:"TLS 1.1", cipher:"AES128-SHA", source:"198.51.100.17", destination:"partner.northstar.io:443", service:"partner-adapter", reason:"Deprecated protocol; grandfathered exception expires in 6 days." },
  { time:"12:54:31", decision:"BLOCK", tls:"TLS 1.0", cipher:"DES-CBC3-SHA", source:"192.0.2.44", destination:"api.northstar.io:443", service:"api-gateway", reason:"Blocked protocol and cipher; policy enforcement applied." }
];
const sampleData = {
  repositories: [
    { name:"payments-platform", branch:"main", provider:"GitHub", language:"Java · Python", findings:6, health:"Needs review", scan:"8 min ago" },
    { name:"identity-services", branch:"main", provider:"GitLab", language:"Go · TypeScript", findings:4, health:"At risk", scan:"24 min ago" },
    { name:"customer-portal", branch:"release/4.2", provider:"GitHub", language:"TypeScript", findings:2, health:"Healthy", scan:"1 hour ago" },
    { name:"ledger-batch", branch:"main", provider:"GitLab", language:"Java", findings:8, health:"At risk", scan:"3 hours ago" }
  ],
  deployments: [
    { name:"api-gateway · prod-eu", status:"Degraded", issue:"TLS handshake failures increased 18%", correlate:"tls.py:84 → OpenSSL 3.0 → api-gateway", time:"13:02 UTC" },
    { name:"identity-service · prod-us", status:"Healthy", issue:"No runtime errors detected", correlate:"Certificate rotation verified", time:"12:47 UTC" },
    { name:"partner-adapter · prod-eu", status:"Warning", issue:"Partner negotiated TLS 1.1", correlate:"legacy-chain.pem → partner-adapter", time:"12:31 UTC" }
  ]
};

const page = document.getElementById("page-content");
const titleElement = document.getElementById("breadcrumb-current");
const apiStatus = document.getElementById("api-status");
const API = "/api/v1";
const DEMO_SESSION_KEY = "pqc_migrate_demo_session";
const ORG_PROFILE_KEY = "pqc_migrate_demo_organization";
const SCAN_HISTORY_KEY = "pqc_migrate_scan_history";
let currentScan = null;
let activePage = "Dashboard";
let currentAssets = assets.slice();
let currentProjectProfile = null;
let selectedProjectFile = null;

function escapeHtml(value) {
  return String(value ?? "").replace(/[&<>"']/g, ch => ({ "&":"&amp;", "<":"&lt;", ">":"&gt;", '"':"&quot;", "'":"&#39;" }[ch]));
}
function badge(label, kind = "") { return `<span class="badge ${kind || badgeKind(label)}">${escapeHtml(label)}</span>`; }
function badgeKind(label) {
  const normalized = String(label).toLowerCase();
  if (normalized.includes("critical") || normalized === "block" || normalized === "rolled back") return "critical";
  if (normalized.includes("medium") || normalized.includes("high") || normalized === "review" || normalized === "warn" || normalized.includes("approval")) return "medium";
  if (normalized.includes("safe") || normalized.includes("healthy") || normalized.includes("allow") || normalized.includes("deployed") || normalized.includes("pass") || normalized.includes("verified")) return "safe";
  if (normalized.includes("pqc") || normalized.includes("monitor") || normalized.includes("testing")) return "info";
  return "neutral";
}
function button(label, action, kind = "", icon = "") {
  return `<button class="button ${kind}" data-action="${escapeHtml(action)}">${icon ? `<span>${icon}</span>` : ""}${escapeHtml(label)}</button>`;
}
function heading(name, subtitle, actions = "") {
  return `<div class="page-heading"><div><p class="eyebrow">PQC-MIGRATE / SECURITY OPERATIONS</p><h1>${escapeHtml(name)}</h1><p>${escapeHtml(subtitle)}</p></div><div class="heading-actions">${actions}</div></div>`;
}
function panel(title, content, subtitle = "", action = "") {
  return `<section class="panel"><div class="panel-header"><div><h2 class="panel-title">${title}</h2>${subtitle ? `<p class="panel-subtitle">${subtitle}</p>` : ""}</div>${action}</div>${content}</section>`;
}
function metric(label, value, detail, icon, trend = "trend-up") {
  return `<article class="metric-card"><div class="metric-top"><span>${label}</span><span class="metric-icon">${icon}</span></div><div class="metric-value">${value}</div><div class="metric-foot"><span class="${trend}">↗ ${detail.split(" · ")[0]}</span>${detail.includes(" · ") ? `<span>· ${detail.split(" · ")[1]}</span>` : ""}</div></article>`;
}
function makeTable(columns, rows, emptyMessage = "No records match this view.") {
  return `<div class="table-wrap"><table class="data-table"><thead><tr>${columns.map(c => `<th>${c}</th>`).join("")}</tr></thead><tbody>${rows || `<tr><td colspan="${columns.length}"><div class="empty-state">${escapeHtml(emptyMessage)}</div></td></tr>`}</tbody></table></div>`;
}
function showToast(message, error = false) {
  const toast = document.createElement("div"); toast.className = `toast${error ? " error" : ""}`; toast.textContent = message;
  document.getElementById("toast-region").appendChild(toast); setTimeout(() => toast.remove(), 3800);
}
async function request(path, options = {}) {
  const response = await fetch(path, options);
  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    throw new Error(body.detail || `Request failed (${response.status})`);
  }
  return response.json();
}
function navRender() {
  const nav = document.getElementById("primary-nav");
  nav.innerHTML = navGroups.map(group => `<div class="nav-label">${group.label}</div>${group.items.map(([name, icon, count]) => `<button class="nav-item ${activePage === name ? "active" : ""}" data-page="${escapeHtml(name)}"><span class="nav-icon">${icon}</span><span>${escapeHtml(name)}</span>${count ? `<span class="nav-count">${count}</span>` : ""}</button>`).join("")}`).join("");
}
function setPage(name) {
  activePage = name; titleElement.textContent = name; navRender(); renderPage(name); page.focus();
  document.getElementById("sidebar").classList.remove("open");
}
function renderPage(name) {
  const renderers = {
    Dashboard: renderDashboard, "Cryptographic Scanner": renderInventory, "Crypto Inventory": renderInventory, "Crypto Findings": renderFindings,
    "Risk Analysis & Scanner": renderProjectScanner, "Project Scanner": renderProjectScanner, Repositories: renderRepositories, "Deployment Health": renderDeployments,
    "Dependency Graph": renderGraph, "Blast Radius": renderBlastRadius, "AI Investigation": renderInvestigation,
    "Migration Planner": renderMigration, "Remediation Center": renderRemediations, "Crypto-Agility": renderAgility,
    "Crypto Firewall": renderPolicyCenter, "Firewall Events": renderPolicyCenter, "Secure Data": renderPolicyCenter,
    "CI/CD Guard": renderPolicyCenter, "Policy Center": renderPolicyCenter, "Crypto Timeline": renderTimeline, Reports: renderReports, Evaluation: renderEvaluation,
    "Audit Logs": renderAudit, Settings: renderSettings, "Sample Data": renderSampleData
  };
  (renderers[name] || renderDashboard)();
  bindPageEvents();
}
function renderDashboard() {
  const org = readLocal(ORG_PROFILE_KEY, null);
  const history = readLocal(SCAN_HISTORY_KEY, []);
  const latest = history.at(-1);
  page.innerHTML = `${heading("Security overview",org ? `Cryptographic migration assessment for ${org.name}. Metrics below reflect scans saved in this browser only.` : "Set up your organization and run a scan to begin an evidence-backed assessment.",button("Run a scan","Risk Analysis & Scanner","primary","＋"))}
    <div class="grid metrics-grid">
      ${metric("Scans recorded",String(history.length),"In this browser · not server-persisted","⌕")}
      ${metric("Crypto assets detected",String(latest?.asset_count ?? "—"),latest ? "Latest scan only" : "No scan evidence yet","◈")}
      ${metric("Algorithms observed",String(latest?.algorithms?.length ?? "—"),latest ? "Latest scan only" : "Awaiting source evidence","⚙")}
      ${metric("Organization",org ? escapeHtml(org.name) : "Not set up",org ? escapeHtml(org.location) : "Complete workspace setup","▦")}
    </div>
    ${panel("Assessment activity",history.length ? `<div class="timeline">${history.slice(-2).map((s,i)=>`<article class="timeline-card"><div class="timeline-dot"></div><strong>${i===0&&history.length>1?"Previous scan":"Latest scan"}</strong><small>${escapeHtml(new Date(s.created_at).toLocaleString())}</small><p>${escapeHtml(s.filename)} · ${s.asset_count} candidate evidence items</p>${badge(s.status||"Completed")}</article>`).join("")}</div>` : `<div class="empty-state"><strong>No scan evidence yet</strong>Upload a project PDF, repository ZIP, configuration, or SBOM in Risk Analysis & Scanner. Dashboard metrics will stay empty until you run a scan.</div>`,`Only actual local scan results are shown`)}
    <div class="grid section-grid" style="margin-top:14px">${panel("Quick actions",`<div class="panel-body" style="display:flex;gap:8px;flex-wrap:wrap">${button("Upload a project PDF","Risk Analysis & Scanner","primary")}${button("Review the combined crypto scanner","Cryptographic Scanner","quiet")}${button("Build project policy","Policy Center","quiet")}${button("Report a deployment issue","Deployment Health","quiet")}</div>`,"Start with evidence; sample records are separated under Sample Data")}${panel("Assessment principles",`<div class="panel-body"><p style="color:#a9b7bf;line-height:1.7;font-size:10px">Evidence first. Unknown fields remain unknown. Scanner matches are candidates until validated. Risk assessments are not guarantees of quantum safety. Proposed policies and changes do not modify production.</p>${badge("No production deployment","safe")}</div>`,"Controlled workflow")}</div>`;
}

const inventoryColumns = ["ALGORITHM","LIBRARY / VERSION","ROLE","FILE : LINE","KEY SIZE","PROTOCOL","SERVICE","ENVIRONMENT","CLASSIFICATION","CONFIDENCE","PRIORITY"];
function inventoryRows(list) {
  return list.map(a=>`<tr data-asset="${escapeHtml(a.algorithm)}"><td class="table-primary">${escapeHtml(a.algorithm)}</td><td>${escapeHtml(a.library)} <span style="color:var(--dim)">· ${escapeHtml(a.version)}</span></td><td>${escapeHtml(a.role)}</td><td class="code">${escapeHtml(a.file)}:${a.line}</td><td>${escapeHtml(a.key)}</td><td>${escapeHtml(a.protocol)}</td><td>${escapeHtml(a.service)}</td><td>${escapeHtml(a.environment)}</td><td>${badge(a.classification)}</td><td>${escapeHtml(a.confidence)}%</td><td>${badge(a.priority)}</td></tr>`).join("");
}
function renderInventory() {
  const actions = currentScan ? `${button("Export report","export-scan-pdf","quiet","↓")}${button("Export JSON","export-scan-json","quiet","{ }")}${button("Export CSV","export-scan-csv","primary","↓")}` : "";
  page.innerHTML = `${heading("Cryptographic scanner","One evidence-backed inventory and findings view. Scan source bundles, configuration, certificates, SBOM/CBOM files, and project repositories.",actions)}
    <section class="panel"><div class="panel-header"><div><h2 class="panel-title">Scan source material</h2><p class="panel-subtitle">Files are never executed. Maximum upload size: 10 GB per file. ZIPs are inspected without extraction.</p></div>${badge("Text and metadata scan","info")}</div>
      <label class="upload-zone" id="scanner-drop"><input type="file" id="scanner-files" multiple accept=".pdf,.zip,.json,.yaml,.yml,.crt,.pem,.sbom,.cbom,.py,.java,.js,.jsx,.ts,.tsx,.go,.rs,.cs,.c,.cc,.cpp,.h,.hpp,.rb,.kt,.tf,.xml,.gradle,.kts,.mod,.sum,.lock,.toml,.txt,.cfg,.ini,.conf,.properties,.md,.sh,.sql" hidden><span class="upload-icon">↑</span><strong>Drop software, source files, or project data here</strong><p>ZIP · source code · PDF · JSON/YAML · PEM/CRT · SBOM/CBOM · up to 10 GB each</p><small>Candidate matches include exact file/line evidence. Uploaded software is analyzed statically and never executed.</small></label>
      <div class="toolbar" style="border:0"><span id="scanner-selection" style="color:var(--muted);font-size:9px;flex:1">No files selected</span>${button("Load sample software ZIP","load-sample-software","quiet")}${button("Start full analysis","start-file-scan","primary","⌕")}<progress id="scan-progress" max="100" value="0" hidden></progress></div>
    </section>${costAssumptionControls()}<div id="scan-result" style="margin-top:14px">${currentScan ? assessmentMarkup(currentScan) : `<div class="panel empty-state"><strong>Inventory and findings will appear here</strong>No source data has been scanned in this session. Sample records are isolated under Sample Data.</div>`}</div>`;
}
function filterInventory() {
  const query = (document.getElementById("inventory-search")?.value || "").toLowerCase();
  const algorithm = document.getElementById("filter-alg")?.value || "";
  const priority = document.getElementById("filter-priority")?.value || "";
  const env = document.getElementById("filter-env")?.value || "";
  const status = document.getElementById("filter-status")?.value || "";
  currentAssets = assets.filter(a=>(!query || Object.values(a).join(" ").toLowerCase().includes(query)) && (!algorithm || a.algorithm === algorithm) && (!priority || a.priority === priority) && (!env || a.environment === env) && (!status || a.status === status));
  const tbody = page.querySelector("tbody"); if (tbody) tbody.innerHTML = inventoryRows(currentAssets) || `<tr><td colspan="${inventoryColumns.length}"><div class="empty-state">No assets match these filters.</div></td></tr>`;
  const footer = page.querySelector(".table-footer span"); if (footer) footer.textContent = `Showing ${currentAssets.length} sample assets · Demonstration workspace data`;
}
function renderFindings() {
  page.innerHTML = `${heading("Crypto findings","Prioritized, evidence-backed risk findings across scanned environments.",`${button("Filter findings","toggle-filters","quiet","☷")}${button("Investigate finding","open-finding","primary","✳")}`)}
  <div class="stat-strip panel" style="margin-bottom:14px"><div><small>Open findings</small><strong>14</strong></div><div><small>Critical</small><strong style="color:var(--red)">4</strong></div><div><small>Evidence uncertain</small><strong style="color:var(--amber)">7</strong></div><div><small>Resolved this month</small><strong style="color:var(--green)">19</strong></div><div><small>Mean confidence</small><strong>91%</strong></div></div>
  <section class="panel"><div class="toolbar"><input class="search-input" id="findings-search" placeholder="⌕  Search findings…"><select class="filter-select" id="finding-severity"><option value="">All severity</option><option>Critical</option><option>Medium</option></select><select class="filter-select"><option>All classifications</option><option>Quantum-vulnerable</option><option>Deprecated</option></select><select class="filter-select"><option>All statuses</option><option>Open</option><option>Review</option></select></div>
  ${makeTable(["FINDING","CLASSIFICATION","SERVICE","EVIDENCE","CONFIDENCE","AGE","STATUS"],findings.map(f=>`<tr data-finding="${f.id}"><td class="table-primary">${escapeHtml(f.title)}<br><span style="color:var(--dim);font-weight:400">${f.id} · ${f.algorithm}</span></td><td>${badge(f.severity === "Critical" ? "Quantum-vulnerable":"Review required",f.severity === "Critical"?"critical":"medium")}</td><td>${escapeHtml(f.service)}</td><td class="code">${escapeHtml(f.file)}</td><td>${escapeHtml(f.confidence)}</td><td>${escapeHtml(f.age)}</td><td>${badge("Open")}</td></tr>`).join(""))}<div class="table-footer"><span>Showing 4 representative findings</span><span>Report · Export</span></div></section>`;
}
function findingDetail(f) {
  const selected = f || findings[0];
  page.innerHTML = `${heading(selected.id,"Cryptographic risk assessment · Evidence verified",`${button("Investigate","investigate","quiet","✳")}${button("Generate fix","generate-fix","quiet","⚒")}${button("Run sandbox","run-sandbox","primary","▶")}`)}
  <div class="detail-layout"><div>
   <section class="panel"><div class="detail-section"><div style="display:flex;justify-content:space-between;gap:12px;align-items:flex-start"><div><h3>${escapeHtml(selected.title)}</h3><div style="color:var(--muted);font-size:9px">${escapeHtml(selected.id)} · ${escapeHtml(selected.service)} · Detected by repository scanner</div></div>${badge(selected.severity)}</div></div>
   <div class="detail-section"><h3>Verified evidence</h3><div class="evidence-box"><p><span class="code" style="color:#70dac7">84</span> &nbsp; <span style="color:#bcc7cf">context.load_cert_chain(</span><span style="color:#f0be6a">"certs/api-rsa-2048.pem"</span><span style="color:#bcc7cf">)</span><br><span style="color:#91a0aa">Certificate metadata confirms RSA-2048 public key, observed on the production TLS listener.</span></p><div class="evidence-meta"><span>services/gateway/tls.py · line 84</span><span>Scanner confidence 96% · SHA-256 evidence hash recorded</span></div></div></div>
   <div class="detail-section"><h3>Assessment</h3><div class="kv-grid"><div class="kv"><small>Algorithm</small><strong>RSA-2048 · TLS certificate</strong></div><div class="kv"><small>Cryptographic role</small><strong>Server authentication</strong></div><div class="kv"><small>Dependency</small><strong>OpenSSL 3.0.13 → api-gateway</strong></div><div class="kv"><small>Certificate relationship</small><strong>api.northstar.internal · expires 2027-03-12</strong></div></div></div>
   <div class="detail-section"><h3>Migration recommendation</h3><p style="color:#b4c1c9;font-size:10px;line-height:1.7">Plan a hybrid key-establishment migration with a supported TLS termination profile. Verify client compatibility and certificate trust-chain behavior in an isolated sandbox before approval. Do not treat a PQC assessment as a guarantee of quantum safety.</p><div style="display:flex;gap:8px;flex-wrap:wrap">${button("Create migration task","create-migration","quiet")}${button("Request approval","request-approval","quiet")}${button("Apply approved fix","apply-fix","primary")}</div></div>
   </section>
   </div><div>
    <section class="panel"><div class="detail-section"><h3>Risk dimensions</h3>${riskRow("Classical risk","Medium")}${riskRow("Quantum risk","Critical")}${riskRow("Implementation risk","Low")}${riskRow("Configuration risk","Medium")}</div><div class="detail-section"><h3>Blast radius</h3><div class="kv-grid"><div class="kv"><small>Affected services</small><strong>3 services</strong></div><div class="kv"><small>Repositories</small><strong>2 repositories</strong></div><div class="kv"><small>Certificates</small><strong>1 certificate</strong></div><div class="kv"><small>Dependency distance</small><strong>4 hops</strong></div></div><p style="color:var(--muted);font-size:9px">api-gateway → payments-platform → OpenSSL → TLS listener</p></div><div class="detail-section"><h3>Validation requirements</h3><div class="risk-row">Build and unit tests ${badge("Required","info")}</div><div class="risk-row">Crypto scan rescan ${badge("Required","info")}</div><div class="risk-row">Client compatibility ${badge("Required","info")}</div><div class="risk-row">Security policy review ${badge("Approval","medium")}</div></div><div class="detail-section"><h3>Rollback plan</h3><p style="color:#a4b1b9;font-size:9px;line-height:1.6">Retain the prior approved certificate profile and configuration snapshot. Roll back if handshake errors exceed the deployment threshold or compatibility tests fail.</p></div></section>
   </div></div>`;
}
function riskRow(label, level) { return `<div class="risk-row"><span>${label}</span><span class="risk-level ${level.toLowerCase()}">${level}</span></div>`; }

function costAssumptionControls() {
  return `<section class="panel cost-assumptions"><div class="panel-header"><div><h2 class="panel-title">Editable cost assumptions</h2><p class="panel-subtitle">USD engineering estimate; adjust the blended rate and expected hours per distinct file/algorithm finding.</p></div>${badge("Estimate · not a quote","medium")}</div><div class="panel-body policy-form">
    <div class="form-field"><label for="cost-hourly-rate">Blended rate · USD/hour</label><input id="cost-hourly-rate" class="form-control" type="number" min="1" max="5000" step="1" value="150"></div>
    <div class="form-field"><label for="cost-legacy-hours">Legacy crypto fix · hours/finding</label><input id="cost-legacy-hours" class="form-control" type="number" min="0" max="1000" step="1" value="8"></div>
    <div class="form-field"><label for="cost-quantum-hours">Classical public-key migration · hours/finding</label><input id="cost-quantum-hours" class="form-control" type="number" min="0" max="1000" step="1" value="16"></div>
    <div class="form-field"><label for="cost-review-hours">Other crypto review · hours/finding</label><input id="cost-review-hours" class="form-control" type="number" min="0" max="1000" step="1" value="3"></div>
  </div><p class="panel-subtitle" style="padding:0 14px 12px">Includes a 2-hour baseline analysis and a 75%–150% effort range. Excludes licenses, infrastructure, vendor costs, testing, and deployment.</p></section>`;
}

function assessmentMarkup(scan) {
  const report = scan?.report || {};
  const profile = report.project_profile || {};
  const items = report.crypto_assets || [];
  const knowledge = report.knowledge_recommendations || [];
  const secrets = report.potential_secret_findings || [];
  const cost = report.cost_analysis || {};
  const software = report.software_analysis;
  const rows = items.map(item=>`<tr><td class="table-primary">${escapeHtml(item.algorithms.join(", "))}</td><td class="code">${escapeHtml(item.file)}:${item.line}</td><td>${escapeHtml(item.evidence)}</td><td class="code">${escapeHtml(item.evidence_hash.slice(0,16))}…</td><td>${badge("Candidate · verify","medium")}</td></tr>`).join("");
  const category = value => value && value !== "unknown" ? escapeHtml(value) : "INSUFFICIENT_EVIDENCE";
  const money = value => Number.isFinite(Number(value)) ? new Intl.NumberFormat("en-US",{style:"currency",currency:"USD",maximumFractionDigits:0}).format(Number(value)) : "Not calculated";
  const costBreakdown = Object.entries(cost.finding_counts || {}).map(([name,count])=>`<div class="risk-row"><span>${escapeHtml(name.replaceAll("_"," "))} · ${count} finding(s)</span><span>${escapeHtml(String((cost.assumptions||{})[`${name==="legacy_crypto"?"legacy_fix":name==="quantum_vulnerable_public_key"?"quantum_migration":"crypto_review"}_hours_per_finding`] ?? 0))} h each</span></div>`).join("");
  const softwareSection = software ? panel("Software analysis",`<div class="panel-body kv-grid">
    ${[["Text files analyzed",software.source_files_analyzed],["Source lines analyzed",software.total_text_lines_analyzed],["Dependencies identified",software.dependencies_identified],["Crypto candidate matches",software.crypto_candidate_matches],["Potential secrets",software.potential_secret_findings],["Dependency vulnerability scan",software.dependency_vulnerability_status],["Build and tests",software.build_and_tests]].map(([label,value])=>`<div class="kv"><small>${escapeHtml(label)}</small><strong>${escapeHtml(String(value ?? "Not available"))}</strong></div>`).join("")}
    <div class="kv"><small>Languages detected</small><strong>${escapeHtml(Object.entries(software.languages_detected||{}).map(([name,count])=>`${name} (${count})`).join(", ")||"None detected")}</strong></div>
    <div class="kv" style="grid-column:1/-1"><small>Dependency names · versions/advisories not verified</small><strong>${escapeHtml((software.dependency_names||[]).join(", ")||"No supported package manifest found")}</strong></div>
    <div class="kv" style="grid-column:1/-1"><small>Analysis limitations</small><strong>${escapeHtml((software.limitations||[]).join(" "))}</strong></div>
  </div>`,"Static inspection only · software was not executed") : "";
  return `<div class="grid section-grid">
    <section class="panel"><div class="panel-header"><div><h2 class="panel-title">Assessment summary</h2><p class="panel-subtitle">${escapeHtml(scan.filename || "Uploaded document")} · ${escapeHtml(scan.scan_id || "scan")} · SHA-256 ${escapeHtml((scan.sha256||"").slice(0,18))}…</p></div>${badge(report.classification || scan.status || "review")}</div>
      <div class="panel-body kv-grid">${[["Project scope",profile.scope],["Technology stack",profile.technology],["Timeline",profile.timeline],["Budget source",profile.budget],["Vendors",profile.vendors],["Dependencies",profile.dependencies],["Security requirements",profile.security_requirements],["Risks stated in source",profile.risks]].map(([label,value])=>`<div class="kv"><small>${label}</small><strong>${escapeHtml(Array.isArray(value)?value.join(", ")||"INSUFFICIENT_EVIDENCE":value||"INSUFFICIENT_EVIDENCE")}</strong></div>`).join("")}</div>
    </section>
    <section class="panel"><div class="panel-header"><div><h2 class="panel-title">Risk dimensions</h2><p class="panel-subtitle">Calculated from crypto matches and controlled knowledge results.</p></div>    </div><div class="panel-body">${[["Classical",report.risk?.classical],["Quantum",report.risk?.quantum],["Implementation",report.risk?.implementation],["Configuration",report.risk?.configuration],["Compliance",report.risk?.compliance],["Operational",report.risk?.operational]].map(([label,value])=>riskRow(label,category(value))).join("")}</div></section>
    </div>
    <div class="grid section-grid" style="margin-top:14px">${panel("Total estimated engineering cost",`<div class="panel-body"><div class="risk-row"><span>Expected total · USD</span><strong>${money(cost.total_cost_usd)}</strong></div><div class="risk-row"><span>Estimated range</span><strong>${money(cost.cost_range_usd?.low)} – ${money(cost.cost_range_usd?.high)}</strong></div><div class="risk-row"><span>Expected effort</span><strong>${escapeHtml(String(cost.estimated_hours?.expected ?? "—"))} h · ${escapeHtml(String(cost.assumptions?.hourly_rate_usd ?? "—"))} USD/h</strong></div>${costBreakdown}<p style="color:#a1afb8;font-size:9px">${escapeHtml(cost.estimate_type||"Assumption-based estimate; not a quote.")} ${escapeHtml((cost.exclusions||[]).join(" "))}</p></div>`,"Based on editable assumptions and unique file/algorithm matches")}${panel("Controlled knowledge and model status",`<div class="panel-body"><div class="risk-row"><span>Generative LLM</span>${badge(report.llm_status?.configured ? "Configured" : "Not configured","medium")}</div><p style="color:#a1afb8;font-size:9px;line-height:1.6">${escapeHtml(report.llm_status?.reason || "Model configuration status unavailable.")}</p>${knowledge.map(k=>`<div class="evidence-box" style="margin-top:8px"><strong style="font-size:9px">${escapeHtml(k.algorithm)} · ${escapeHtml(k.knowledge_version)}</strong><p>${escapeHtml(k.reasoning)}</p><div class="evidence-meta"><span>${escapeHtml(k.knowledge_source)}</span><span>Confidence ${Math.round((k.confidence||0)*100)}%</span></div></div>`).join("")||`<p style="color:var(--muted);font-size:9px">No algorithm-specific knowledge retrieved from available evidence.</p>`}</div>`,"Recommendations cite knowledge source, version, and evidence")}</div>
    ${softwareSection}
    ${panel(`Crypto evidence · ${items.length} candidate match${items.length===1?"":"es"}`,makeTable(["ALGORITHM","FILE / LINE","SOURCE EVIDENCE","LINE HASH","VALIDATION"],rows||"", "No cryptographic algorithm matches found in scanned text."),"Matches are inventory candidates; presence does not establish exploitability or runtime use")}
    ${secrets.length ? panel(`Potential secret markers · ${secrets.length}`,makeTable(["TYPE","FILE / LINE","EVIDENCE","HASH"],secrets.map(s=>`<tr><td>${escapeHtml(s.type)}</td><td class="code">${escapeHtml(s.file)}:${s.line}</td><td>[REDACTED]</td><td class="code">${escapeHtml(s.evidence_hash.slice(0,18))}…</td></tr>`).join("")),"Secret values are never rendered") : ""}
    <section class="panel" style="margin-top:14px"><div class="panel-body"><strong style="font-size:10px">Evidence limitations</strong><ul style="color:#96a5ae;font-size:9px;line-height:1.7">${(report.uncertainties||[]).map(x=>`<li>${escapeHtml(x)}</li>`).join("")||"<li>Further validation is needed before remediation or policy actions.</li>"}</ul></div></section>`;
}

function renderProjectScanner() {
  page.innerHTML = `${heading("Project risk analysis","Upload one project-specification PDF for evidence-based risks and an editable USD engineering-cost estimate.",currentScan ? `${button("Export PDF","export-scan-pdf","quiet","↓")}${button("Export JSON","export-scan-json","quiet","{ }")}${button("Export CSV","export-scan-csv","primary","↓")}` : "")}
    <section class="panel"><div class="panel-header"><div><h2 class="panel-title">Project document scanner</h2><p class="panel-subtitle">Text-only PDF parsing. No uploaded code is executed. Maximum size: 10 GB.</p></div>${badge("Evidence-based","info")}</div>
      <label class="upload-zone" id="project-drop"><input type="file" id="project-file" accept=".pdf" hidden><span class="upload-icon">↑</span><strong>Drop a project PDF here or browse</strong><p>PDF · Maximum 10 GB per file</p><small>Values absent from the source remain marked as insufficient evidence.</small></label>
      <div class="toolbar" style="border:0"><span id="project-upload-name" style="color:var(--muted);font-size:9px;flex:1">No document selected</span>${button("Load sample project PDF","load-sample-project","quiet")}${button("Analyze risk + total cost","analyze-project","primary","⌕")}<progress id="project-progress" max="100" value="0" hidden></progress></div>
    </section>${costAssumptionControls()}
    <div id="project-results" style="margin-top:14px">${currentScan ? assessmentMarkup(currentScan) : `<div class="panel empty-state"><strong>Ready for a project PDF</strong>The report includes evidence-based risks and a clearly labeled estimate based on adjustable USD rates and effort assumptions.</div>`}</div>
    <section class="panel" style="margin-top:14px"><div class="panel-header"><div><h2 class="panel-title">Analysis method and limitations</h2><p class="panel-subtitle">The current service is not a trained generative LLM.</p></div></div><div class="panel-body"><p style="color:#aab8c0;font-size:10px;line-height:1.7">Risk is based on text evidence and controlled recommendations. The USD total is an engineering effort estimate using the editable rate and hours above—not an exact project quote. Licenses, vendors, performance, compatibility, deployment, and compliance require separate validated inputs.</p></div></section>`;
}
function renderRepositories() {
  page.innerHTML = `${heading("Repositories","Connect source control and review repository health, crypto use, secrets, builds, and dependencies.",`${button("Connect GitLab","connect-gitlab","quiet","＋")}${button("Connect GitHub","connect-github","primary","＋")}`)}
  <div class="grid metrics-grid" style="grid-template-columns:repeat(4,minmax(0,1fr));margin-bottom:14px">${metric("Connected","24","GitHub + GitLab","⑂")}${metric("Need review","6","Open crypto findings","⚑","trend-warn")}${metric("Secret alerts","2","Credential-like evidence","⌑","trend-warn")}${metric("Build errors","3","Last scan window","×","trend-warn")}</div>
  <section class="panel">${makeTable(["REPOSITORY","PROVIDER","DEFAULT BRANCH","LANGUAGES","CRYPTO FINDINGS","HEALTH","LAST SCAN"],sampleData.repositories.map(r=>`<tr><td class="table-primary">${escapeHtml(r.name)}</td><td>${badge(r.provider,"info")}</td><td class="code">${escapeHtml(r.branch)}</td><td>${escapeHtml(r.language)}</td><td>${r.findings}</td><td>${badge(r.health)}</td><td>${escapeHtml(r.scan)}</td></tr>`).join(""))}<div class="table-footer"><span>4 repositories shown · sample workspace inventory</span>${button("Scan repository","run-scan","quiet")}</div></section>
  <div class="grid section-grid" style="margin-top:14px">${panel("Repository health checks",`<div class="finding-list">${["Dependency vulnerabilities · 4 require triage","Cryptographic API usage · 28 assets discovered","Secret scanning · 2 potential exposures (masked)","Build status · 3 failures correlate with config changes","Outdated dependencies · 11 package updates available"].map((x,i)=>`<div class="finding-item"><span class="finding-indicator" style="background:${i<2?"var(--amber)":"var(--teal)"}"></span><div class="finding-content"><strong>${x.split(" · ")[0]}</strong><p>${x.split(" · ")[1]}</p></div>${badge(i<2?"Review":"Monitored")}</div>`).join("")}</div>`,"Latest aggregated scanner summary")}${panel("Provider connections",`<div class="detail-section"><div class="risk-row"><span>GitHub Enterprise</span>${badge("Connected","safe")}</div><div class="risk-row"><span>GitLab</span>${badge("Connected","safe")}</div><p style="color:var(--muted);font-size:9px">Tokens are managed server-side. OAuth credentials are not displayed in this interface.</p></div>`,"Source control integrations")}</div>`;
}
function renderDeployments() {
  page.innerHTML = `${heading("Deployment health","Correlate deployment telemetry with source, dependencies, services, and cryptographic assets.",button("Analyze deployment log","deployment-scan","primary","＋"))}<div class="grid metrics-grid" style="grid-template-columns:repeat(4,minmax(0,1fr));margin-bottom:14px">${metric("Environments","18","Across 6 services","⌂")}${metric("Build failures","3","Last 24 hours","×","trend-warn")}${metric("Runtime alerts","8","2 crypto-correlated","⚑","trend-warn")}${metric("Performance warnings","2","Within observation window","◷","trend-warn")}</div><div class="grid section-grid">${panel("Recent deployment telemetry",`<div class="finding-list">${sampleData.deployments.map(d=>`<div class="finding-item"><span class="finding-indicator" style="background:${d.status==="Healthy"?"var(--green)":d.status==="Warning"?"var(--amber)":"var(--red)"}"></span><div class="finding-content"><strong>${escapeHtml(d.name)} ${badge(d.status)}</strong><p>${escapeHtml(d.issue)}</p><small>Correlation: ${escapeHtml(d.correlate)} · ${escapeHtml(d.time)}</small></div></div>`).join("")}</div>`,"Telemetry correlation · illustrative sample data")}${panel("Submit deployment event",`<div class="panel-body"><div class="form-field"><label for="deploy-id">Deployment ID</label><input id="deploy-id" class="form-control" value="deploy-prod-eu-042"></div><div class="form-field"><label for="deploy-error">Runtime error or log excerpt</label><textarea id="deploy-error" class="form-control" style="width:100%;height:80px">TLS handshake failure due to certificate signature algorithm</textarea></div>${button("Correlate event","submit-deployment","primary")}</div>`,"Analysis is advisory; evidence is retained with the assessment")}</div>`;
}
function renderGraph() {
  const nodes = [["Repository","payments-platform"],["Application","payments-api"],["Service","api-gateway"],["Package","cryptography"],["Crypto library","OpenSSL 3.0"],["Algorithm","RSA-2048"],["Certificate","api.northstar"],["Protocol","TLS 1.2"],["Data asset","payment records"]];
  page.innerHTML = `${heading("Dependency graph","Explore verified cryptographic dependencies and trace affected services and data.",button("Recalculate blast radius","recalc-graph","primary","◎"))}<section class="panel"><div class="panel-header"><div><h2 class="panel-title">Cryptographic dependency path</h2><p class="panel-subtitle">Select a node to inspect relationships. Graph edges represent observed dependencies, not inferred certainty.</p></div>${badge("9 nodes","info")}</div><div class="graph-canvas"><div class="graph-flow">${nodes.map((n,i)=>`${i?'<span class="graph-arrow">→</span>':""}<button class="graph-node ${i===5?"selected":""}" data-node="${escapeHtml(n[0])}" data-node-name="${escapeHtml(n[1])}"><span>${escapeHtml(n[0])}</span><strong>${escapeHtml(n[1])}</strong></button>`).join("")}</div></div><div class="node-details" id="node-details"><h3>Algorithm · RSA-2048</h3><p>Observed from services/gateway/tls.py:84 and certificate metadata. Linked path reaches 3 services, 2 repositories, and 1 data asset; impact remains subject to owner validation.</p></div></section><div class="grid section-grid" style="margin-top:14px">${panel("Blast radius summary",`<div class="panel-body kv-grid">${[["Affected services","3"],["Repositories","2"],["Certificate paths","1"],["Dependency distance","4 hops"]].map(([a,b])=>`<div class="kv"><small>${a}</small><strong>${b}</strong></div>`).join("")}</div>`,"Based on current graph snapshot")}${panel("Relationship legend",`<div class="panel-body chart-legend" style="display:grid;grid-template-columns:1fr 1fr;gap:14px">${["USES","DEPENDS_ON","CONFIGURES","CERTIFICATE_FOR","COMMUNICATES_WITH","PROTECTS"].map(x=>`<span>${badge(x,"info")} &nbsp; verified graph relation</span>`).join("")}</div>`,"Typed relationships are recorded with provenance")}</div>`;
}
function renderBlastRadius() {
  page.innerHTML = `${heading("Blast radius","Prioritize affected systems based on verified dependency paths and service criticality.",button("Export impact report","export-report","quiet","↓"))}<div class="grid metrics-grid" style="grid-template-columns:repeat(4,minmax(0,1fr));margin-bottom:14px">${metric("Affected services","12","Across 5 findings","◎","trend-warn")}${metric("Critical paths","3","External-facing","⚑","trend-warn")}${metric("Repositories","7","In dependency chain","⑂")}${metric("Business data assets","4","Owner review required","▣","trend-warn")}</div>${panel("Impact paths",makeTable(["FINDING","ENTRY POINT","DEPENDENCY PATH","SERVICES","CRITICALITY","DISTANCE"],findings.slice(0,4).map((f,i)=>`<tr><td class="table-primary">${f.id}<br>${escapeHtml(f.algorithm)}</td><td>${escapeHtml(f.service)}</td><td class="code">${i===0?"payments-platform → OpenSSL → RSA → TLS":i===1?"partner-adapter → cert chain → SHA-1":i===2?"identity-services → cryptography → ECDSA":"session-service → OpenSSL → AES-CBC"}</td><td>${i===0?"3":i===1?"2":"1"}</td><td>${badge(i<2?"High":"Medium")}</td><td>${i+2} hops</td></tr>`).join("")),"Paths require service-owner validation before production changes")}`;
}
function renderInvestigation() {
  page.innerHTML = `${heading("Agentic investigation","Structured agent activity with evidence references and concise audit-safe decision summaries.",button("Start investigation","start-investigation","primary","▶"))}<div class="grid detail-layout"><div><section class="panel"><div class="panel-header"><div><h2 class="panel-title">CRY-2481 · RSA certificate on API gateway</h2><p class="panel-subtitle">Investigation INV-5802 · Running against scan SCN-22091</p></div>${badge("Approval pending","medium")}</div><div class="panel-body"><div class="agent-timeline">${[
    ["Discovery Agent","Completed","Identified RSA certificate loading call in the supplied repository scan evidence.","Input: scanner finding CRY-2481 · Output: candidate crypto asset and source location.","96%"],
    ["Evidence Agent","Completed","Validated file path and line against scan snapshot; certificate metadata confirms RSA-2048.","Evidence: services/gateway/tls.py:84 · certificate fingerprint recorded.","96%"],
    ["Risk Agent","Completed","Classified as quantum-vulnerable for key establishment exposure; not a claim of system-wide safety.","Knowledge: approved crypto reference v1.2 · Output: migration assessment.","93%"],
    ["Dependency Agent","Completed","Connected gateway to OpenSSL package and two downstream services; four-hop impact path.","Graph snapshot DG-2409 · Affected services require owner review.","88%"],
    ["Migration Agent","Completed","Proposed a hybrid migration sequence with client compatibility gates and rollback checkpoint.","Output: plan MPL-0084 · Human approval required.","87%"],
    ["Sandbox Agent","Completed","Build and unit suite passed. One legacy client compatibility case remains under review.","Sandbox SBX-1901 · No production changes made.","92%"],
    ["Verification Agent","Completed","Rescan confirms candidate profile in sandbox. Deployment verification is not yet performed.","Output: sandbox verification only · Not a deployment success claim.","94%"],
    ["Human Approval","Waiting","Security lead approval is required before any deployment action.","Requested from: Security Lead · No production action taken.","—"]
  ].map(([agent,status,summary,evidence,confidence],i)=>`<details class="agent-step ${i===7?"waiting":""}" ${i===0?"open":""}><summary>${agent}<span style="float:right;color:${status==="Waiting"?"var(--amber)":"var(--green)"}">${status}</span></summary><div class="agent-output"><span class="confidence">Confidence ${confidence}</span><strong>Audit-safe reasoning summary</strong><br>${summary}<br><br><strong>Evidence / output</strong><br>${evidence}</div></details>`).join("")}</div></div></section></div><div><section class="panel"><div class="detail-section"><h3>Investigation context</h3>${riskRow("Finding","CRY-2481")}${riskRow("Evidence status","Verified")}${riskRow("Current phase","Approval")}${riskRow("Production changes","None")}</div><div class="detail-section"><h3>Controls</h3><p style="color:#9ba9b2;font-size:9px;line-height:1.6">Agents exchange structured state. Hidden chain-of-thought is not displayed or stored. Recommendations remain advisory and require validated evidence and human approval.</p>${button("Open finding details","open-finding","quiet")}</div></section></div></div>`;
}
function renderMigration() {
  page.innerHTML = `${heading("Migration planner","Sequence cryptographic migration work with dependency ordering, compatibility gates, and rollback plans.",button("Create migration plan","create-migration","primary","＋"))}<div class="grid metrics-grid" style="grid-template-columns:repeat(4,minmax(0,1fr));margin-bottom:14px">${metric("Active plans","8","3 awaiting approval","⇢")}${metric("Tasks in progress","23","5 sandbox validation","⚒")}${metric("Blocked by dependency","4","Owner input needed","⌁","trend-warn")}${metric("Verified complete","17","+4 this month","✓")}</div><div class="grid section-grid">${panel("Active migration plans",makeTable(["PLAN","REPOSITORY","SCOPE","PHASE","TASKS","STATUS"],[["MPL-0084","payments-platform","Gateway hybrid TLS","Sandbox","4 / 7","Approval required"],["MPL-0079","identity-services","Provider abstraction","Planning","2 / 5","In progress"],["MPL-0071","ledger-batch","3DES removal","Compatibility","3 / 4","In progress"]].map(([id,repo,scope,phase,tasks,status])=>`<tr><td class="table-primary">${id}</td><td>${repo}</td><td>${scope}</td><td>${phase}</td><td>${tasks}</td><td>${badge(status)}</td></tr>`).join("")),"Dependency-aware tasks; production deployment is always gated")}${panel("Recommended sequence",`<div class="finding-list">${["Inventory certificate consumers and client support","Introduce provider abstraction behind configuration","Run hybrid profile in isolated compatibility sandbox","Request owner and security approval","Deploy staged rollout with telemetry guardrails","Verify rescan and maintain rollback checkpoint"].map((s,i)=>`<div class="finding-item"><span class="workspace-icon" style="width:22px;height:22px;font-size:9px">${i+1}</span><div class="finding-content"><strong>${s}</strong><p>Gate ${i+1} · ${i<2?"Evidence":"Validation and approval required"}</p></div></div>`).join("")}</div>`,"Plan order is advisory and evidence-driven")}</div>`;
}
function renderRemediations() {
  const statuses=["Pending","Sandbox Testing","Approval Required","Approved","Deployed","Rolled Back"];
  page.innerHTML = `${heading("Remediation center","Proposed fixes move through sandbox verification and human approval before deployment.",button("Propose remediation","generate-fix","primary","＋"))}<div class="grid section-grid three">${statuses.map(s=>`<article class="panel"><div class="panel-header"><h2 class="panel-title">${s}</h2>${badge(remediationJobs.filter(j=>j.status===s).length,"info")}</div><div class="panel-body">${remediationJobs.filter(j=>j.status===s).map(j=>`<div class="evidence-box" style="margin-bottom:9px"><div style="display:flex;justify-content:space-between;gap:6px"><strong style="font-size:9px">${escapeHtml(j.title)}</strong>${badge(j.risk)}</div><p style="margin-top:7px">${j.id} · ${j.finding}<br>Owner ${j.owner} · ${j.updated}</p><div class="risk-row"><span>Test status</span><span>${escapeHtml(j.tests)}</span></div><div class="risk-row"><span>Before → proposed</span><span>${escapeHtml(j.before)} → ${escapeHtml(j.after)}</span></div><div style="margin-top:8px">${button("Review details","open-remediation","quiet small")}</div></div>`).join("") || `<div class="empty-state">No jobs in this state.</div>`}</div></article>`).join("")}</div><p style="color:var(--muted);font-size:9px">Sample workflow data. High-risk changes are never deployed automatically; deployment requires approval and active monitoring.</p>`;
}
function renderAgility() {
  const indicators=[["Algorithm abstraction",56,"Hardcoded RSA/ECDSA call sites remain"],["Provider abstraction",48,"Provider selection is partially centralized"],["Configuration-driven crypto",71,"Most services use external profiles"],["Dependency coupling",39,"Three services bind to provider-specific APIs"],["Certificate coupling",52,"Manual certificate references found"],["Protocol flexibility",63,"TLS profiles configurable for 4 of 6 services"],["PQC readiness",34,"Two isolated PQC pilot integrations"],["Migration complexity",58,"Moderate; compatibility evidence incomplete"]];
  page.innerHTML = `${heading("Crypto-agility assessment","Evidence-backed indicators of how readily cryptographic mechanisms can be replaced.",button("Compare history","Crypto Timeline","quiet","↗"))}<section class="panel"><div class="agility-score"><div class="score-ring"><strong>48</strong></div><div class="score-copy"><h3>Crypto-agility score · Developing</h3><p>Composite assessment from repository evidence, configuration, dependency coupling, and test signals. This is not a security guarantee; 8 services have incomplete evidence and need owner validation.</p></div>${badge("Evidence coverage 82%","info")}</div></section><div class="grid section-grid" style="margin-top:14px">${panel("Agility indicators",`<div class="panel-body progress-list">${indicators.map(([n,v,d])=>`<div><div class="progress-row" style="grid-template-columns:165px 1fr 30px"><span>${n}</span><div class="progress-track"><span style="width:${v}%;background:${v<40?"var(--amber)":"var(--teal)"}"></span></div><strong>${v}</strong></div><p style="margin:4px 0 0 173px;color:var(--dim);font-size:8px">${d}</p></div>`).join("")}</div>`,"Score dimensions and evidence limitations")}${panel("Historical trend",`<div class="panel-body"><div class="bars">${[["Apr",32],["May",35],["Jun",37],["Jul",39],["Aug",44],["Sep",48]].map(([m,v])=>`<div class="bar-group"><i class="bar" style="height:${v*1.7}%;width:20px;background:var(--teal)"></i></div>`).join("")}</div><div class="bar-labels"><span>Apr</span><span>May</span><span>Jun</span><span>Jul</span><span>Aug</span><span>Sep</span></div></div>`,"Assessment trend · monthly snapshots")}</div>`;
}
function renderFirewall() {
  page.innerHTML = `${heading("Crypto firewall","Policy decisions and telemetry for runtime cryptographic behavior.",`${button("Rollback active policy","rollback-policy","quiet")}${button("Save policy draft","save-policy","primary")}`)}<div class="grid metrics-grid" style="grid-template-columns:repeat(4,minmax(0,1fr));margin-bottom:14px">${metric("Blocked","18","TLS 1.0 or prohibited cipher","⊘","trend-warn")}${metric("Allowed","2,481","Policy-compliant flows","✓")}${metric("Monitored","314","No automatic block","◷")}${metric("Review required","23","Human assessment queued","⚑","trend-warn")}</div>
  <div class="grid section-grid"><section class="panel"><div class="panel-header"><div><h2 class="panel-title">Enforcement architecture</h2><p class="panel-subtitle">Policy decisions use inspection metadata from managed gateway components.</p></div><span class="pulse-dot"></span></div><div class="firewall-flow">${[["Internet","◉"],["WAF","▤"],["Crypto Firewall","⛨"],["API Gateway","⌘"],["Application Services","▦"]].map(([n,i],k)=>`${k?'<span class="firewall-connector">→</span>':""}<div class="firewall-hop ${k===2?"active":""}"><div class="hop-icon">${i}</div><strong>${n}</strong><small>${k===2?"Policy decision":k===0?"External":"Managed"}</small></div>`).join("")}</div></section>${panel("Live policy events",`<div class="finding-list">${firewallEvents.slice(0,3).map(e=>`<div class="finding-item"><span class="finding-indicator" style="background:${e.decision==="BLOCK"?"var(--red)":e.decision==="REVIEW"||e.decision==="WARN"?"var(--amber)":"var(--green)"}"></span><div class="finding-content"><strong>${e.decision} · ${e.tls} · ${escapeHtml(e.service)}</strong><p>${escapeHtml(e.cipher)} · ${escapeHtml(e.time)}</p><small>${escapeHtml(e.reason)}</small></div></div>`).join("")}</div>`,"Recent gateway observations")}</div>
  <section class="panel" style="margin-top:14px"><div class="panel-header"><div><h2 class="panel-title">Policy-as-code editor</h2><p class="panel-subtitle">Draft → Test → Approve → Deploy. High-impact changes require approval.</p></div>${badge("v12 · Active","safe")}</div><div class="panel-body"><div class="policy-form"><div class="form-field"><label for="minimum-tls">Minimum TLS version</label><select id="minimum-tls" class="form-control"><option>TLS 1.3</option><option selected>TLS 1.2</option><option>TLS 1.1 (not recommended)</option></select></div><div class="form-field"><label for="minimum-rsa">Minimum RSA key size</label><select id="minimum-rsa" class="form-control"><option>2048</option><option selected>3072</option><option>4096</option></select></div><div class="form-field"><label for="allowed-ciphers">Allowed ciphers</label><textarea id="allowed-ciphers" class="form-control">TLS_AES_256_GCM_SHA384
TLS_CHACHA20_POLY1305_SHA256
ECDHE-RSA-AES256-GCM-SHA384</textarea></div><div class="form-field"><label for="blocked-algorithms">Blocked algorithms</label><textarea id="blocked-algorithms" class="form-control">MD5, 3DES, DES, RC4, SHA-1</textarea></div><div class="form-field"><label for="pqc-policy">PQC policy</label><select id="pqc-policy" class="form-control"><option>Monitor hybrid readiness</option><option>Require approved hybrid profile</option><option>Not applicable</option></select></div><div class="form-field"><label for="exceptions">Exception policy</label><select id="exceptions" class="form-control"><option>Expiry required · max 30 days</option><option>Expiry required · max 7 days</option></select></div></div><div class="policy-actions">${button("Test draft","test-policy","quiet")}${button("Request approval","approve-policy","quiet")}${button("Deploy approved policy","deploy-policy","primary")}</div></div></section>`;
}
function renderFirewallEvents() {
  page.innerHTML = `${heading("Firewall events","Inspect decisions and observed TLS metadata. TLS 1.2 is evaluated in context, not blocked by version alone.",button("Export events","export-csv","quiet","↓"))}<div class="stat-strip panel" style="margin-bottom:14px">${[["Blocked","18"],["Allowed","2,481"],["Monitored","314"],["Warn","9"],["Review","23"]].map(([a,b])=>`<div><small>${a}</small><strong>${b}</strong></div>`).join("")}</div><section class="panel"><div class="toolbar"><input class="search-input" id="firewall-search" placeholder="⌕ Search service, cipher, address…"><select class="filter-select" id="firewall-decision"><option value="">All decisions</option><option>ALLOW</option><option>MONITOR</option><option>WARN</option><option>REVIEW</option><option>BLOCK</option></select><select class="filter-select"><option>Last 24 hours</option><option>7 days</option><option>30 days</option></select></div>${makeTable(["TIME","DECISION","TLS","CIPHER","SOURCE","DESTINATION","SERVICE","POLICY REASON"],firewallEvents.map(e=>`<tr><td class="code">${e.time}</td><td>${badge(e.decision)}</td><td>${e.tls}</td><td class="code">${e.cipher}</td><td>${e.source}</td><td>${e.destination}</td><td class="table-primary">${e.service}</td><td>${e.reason}</td></tr>`).join(""))}<div class="table-footer"><span>5 sample events shown · Live event feed connects when available</span>${button("Connect event stream","connect-ws","quiet")}</div></section>`;
}
function renderSecureData() {
  page.innerHTML = `${heading("Secure data","Access is role-scoped and audited. Private encryption keys are never displayed.",button("Request access","request-data-access","primary","＋"))}<div class="grid section-grid"><section class="panel"><div class="panel-header"><div><h2 class="panel-title">Secure data objects</h2><p class="panel-subtitle">Encrypted payloads at rest · organization boundaries enforced</p></div>${badge("Envelope encryption","safe")}</div>${makeTable(["OBJECT","TYPE","CLASSIFICATION","ACCESS VIEW","KEY HOLDER","UPDATED"],[["SDO-0081","Project specification","Confidential","Masked view","KMS-managed","Today, 09:14"],["SDO-0079","Certificate metadata","Internal","Metadata only","Security Lead","Yesterday"],["SDO-0072","Migration evidence","Restricted","Redacted view","KMS-managed","Sep 24"]].map(([a,b,c,d,e,f])=>`<tr><td class="table-primary">${a}</td><td>${b}</td><td>${badge(c)}</td><td>${d}</td><td>${e}</td><td>${f}</td></tr>`).join(""))}</section><section class="panel"><div class="panel-header"><div><h2 class="panel-title">Role-based access</h2><p class="panel-subtitle">Illustrative access policy</p></div></div><div class="panel-body">${[["Non-organization","Encrypted payload only"],["General staff","Masked / redacted view"],["Main Lead","Full decrypted view with approval"],["Key holder","KMS-mediated key operation; key material hidden"]].map(([a,b])=>`<div class="risk-row"><span>${a}</span><strong style="font-size:9px;color:#c5d0d6">${b}</strong></div>`).join("")}<div style="margin-top:12px;padding:10px;border:1px solid #3b5149;border-radius:7px;background:#1a2b26;color:#a6cbb8;font-size:9px;line-height:1.6">Production use requires a configured KMS/HSM integration, authenticated identity, and transport encryption. This interface never reveals private keys.</div></div></section></div><section class="panel" style="margin-top:14px">${panel("Access log",makeTable(["TIME","USER","ROLE","OBJECT","ACTION","RESULT"],[["13:02:15","a.rivera","Security Lead","SDO-0081","View masked","Allowed"],["12:41:09","m.chen","Analyst","SDO-0079","Read metadata","Allowed"],["11:17:30","unknown","External","SDO-0081","Read content","Denied"]].map(([a,b,c,d,e,f])=>`<tr><td>${a}</td><td>${b}</td><td>${c}</td><td>${d}</td><td>${e}</td><td>${badge(f)}</td></tr>`).join("")),"Sensitive access actions are recorded for audit review")}</section>`;
}
function renderCiGuard() {
  page.innerHTML = `${heading("CI/CD guard","Evaluate newly introduced crypto against policy and the existing inventory before merge.",button("Configure policy","Crypto Firewall","quiet","⚙"))}<div class="grid section-grid"><section class="panel"><div class="panel-header"><div><h2 class="panel-title">Pull request crypto scan</h2><p class="panel-subtitle">Submit a diff excerpt for a policy decision. Evidence and rationale are returned.</p></div>${badge("POST /api/v1/ci/scan","info")}</div><div class="panel-body"><div class="form-field"><label for="pr-repo">Repository</label><input id="pr-repo" class="form-control" value="northstar/payments-platform"></div><div class="form-field"><label for="pr-commit">Commit hash</label><input id="pr-commit" class="form-control" value="a41bf03"></div><div class="form-field"><label for="pr-diff">Changed code / diff excerpt</label><textarea id="pr-diff" class="form-control" style="width:100%;height:110px">cipher = AES.new(key, AES.MODE_CBC, iv)
signature = hashlib.sha1(payload).digest()</textarea></div>${button("Scan pull request","scan-pr","primary","⌕")}</div></section><section class="panel" id="ci-result"><div class="panel-header"><div><h2 class="panel-title">Decision workflow</h2><p class="panel-subtitle">Rules and approved policy are authoritative; AI assists evidence interpretation.</p></div></div><div class="panel-body"><div class="agent-timeline">${["Diff scanner","Policy evaluator","Inventory comparison","Review decision"].map((x,i)=>`<details class="agent-step" ${i===0?"open":""}><summary>${x}<span style="float:right;color:${i<3?"var(--green)":"var(--amber)"}">${i<3?"Ready":"Awaiting scan"}</span></summary><div class="agent-output">Stage ${i+1} · Scans file-level evidence, policy context, and baseline inventory.</div></details>`).join("")}</div><p style="color:var(--muted);font-size:9px">Possible outcomes: PASS · REVIEW · BLOCK. Decisions include the matched policy and evidence.</p></div></section></div><section class="panel" style="margin-top:14px">${panel("Recent CI decisions",makeTable(["PULL REQUEST","REPOSITORY","CRYPTO CHANGES","POLICY VIOLATIONS","DECISION","TIME"],[["#1842 · Add new session crypto","payments-platform","AES-128-CBC, SHA-1","2","REVIEW","13:04"],["#1839 · PQC provider pilot","identity-services","ML-KEM-768","0","PASS","11:22"],["#1834 · Update TLS defaults","customer-portal","TLS 1.0 removed","0","PASS","Yesterday"]].map(([a,b,c,d,e,f])=>`<tr><td class="table-primary">${a}</td><td>${b}</td><td>${c}</td><td>${d}</td><td>${badge(e)}</td><td>${f}</td></tr>`).join("")),"Sample decisions illustrate policy outcomes")}</section>`;
}
function renderTimeline() {
  page.innerHTML = `${heading("Crypto timeline","Compare historical inventory snapshots to identify migration progress and changes.",button("Compare scans","compare-scans","primary","↗"))}<section class="panel"><div class="panel-header"><div><h2 class="panel-title">Repository crypto state</h2><p class="panel-subtitle">payments-platform · 4 snapshots · lineage retained for comparisons</p></div><select class="filter-select"><option>payments-platform</option><option>identity-services</option></select></div><div class="panel-body"><div class="timeline">${[["Scan 1","Jun 18 · Baseline","RSA 2048 · ECDSA · TLS 1.2","8 findings"],["Scan 2","Jul 22","3DES removed · new dependency: liboqs","7 findings"],["Scan 3","Aug 27","PQC pilot added · 2 issues resolved","5 findings"],["Scan 4","Sep 26 · Current","SHA-1 chain newly detected · 38% migration","4 open findings"]].map(([a,b,c,d])=>`<article class="timeline-card"><div class="timeline-dot"></div><strong>${a}</strong><small>${b}</small><p>${c}</p>${badge(d)}</article>`).join("")}</div></div></section><div class="grid section-grid" style="margin-top:14px">${panel("Changes since previous scan",`<div class="finding-list">${[["New crypto","AES-128-CBC in session-service","medium"],["Removed crypto","3DES removed from batch importer","safe"],["New vulnerability","SHA-1 partner chain detected","critical"],["Resolved","CBC mode finding closed after verified GCM migration","safe"],["New dependency","liboqs 0.12.0 added for PQC pilot","info"],["Exceptions","TLS 1.1 partner exception remains · expires Oct 2","medium"]].map(([a,b,c])=>`<div class="finding-item"><span class="finding-indicator" style="background:var(--${c==="critical"?"red":c==="medium"?"amber":"teal"})"></span><div class="finding-content"><strong>${a}</strong><p>${b}</p></div>${badge(c==="critical"?"Critical":c==="medium"?"Review":c==="safe"?"Resolved":"New",c)}</div>`).join("")}</div>`,"Snapshot comparison is based on recorded scan data")}${panel("Comparison summary",`<div class="panel-body kv-grid">${[["Algorithms removed","2"],["New dependencies","1"],["Resolved vulnerabilities","3"],["Exceptions remaining","4"],["PQC assets added","+6"],["Migration progress","+8%"]].map(([a,b])=>`<div class="kv"><small>${a}</small><strong>${b}</strong></div>`).join("")}</div>`,"Scan 3 compared with Scan 4")}</div>`;
}
function renderReports() {
  const reports=[["Executive Report","Leadership summary of risk, migration status, and approvals","PDF"],["Crypto Inventory","Asset inventory with provenance and classification","CSV"],["CBOM","Cryptographic bill of materials snapshot","JSON"],["Migration Plan","Dependency-ordered task and validation export","PDF"],["Firewall Report","Policy decisions, exceptions, and event summaries","CSV"],["AI Investigation Report","Evidence references and audit-safe decisions","PDF"],["Audit Report","Sensitive operations, approvals, and outcomes","JSON"]];
  page.innerHTML = `${heading("Reports","Generate evidence-linked exports for security, engineering, and governance stakeholders.")}<div class="grid section-grid three">${reports.map(([a,b,c])=>`<section class="panel"><div class="panel-body"><span class="metric-icon">${c==="PDF"?"▤":c==="CSV"?"▦":"{ }"}</span><h3 style="font:600 12px 'Space Grotesk';margin:12px 0 5px">${a}</h3><p style="min-height:30px;color:var(--muted);font-size:9px;line-height:1.5">${b}</p><div style="display:flex;justify-content:space-between;align-items:center">${badge(c,"info")}${button("Export","export-report","quiet small","↓")}</div></div></section>`).join("")}</div><p style="color:var(--muted);font-size:9px">Exports include assessment scope, evidence references, and limitations. No report can claim a system is quantum-safe.</p>`;
}
function renderEvaluation() {
  page.innerHTML = `${heading("Evaluation","Compare Rules, LLM, and Hybrid Agentic AI using measured test outcomes.",button("Record evaluation","record-evaluation","primary","＋"))}<div class="grid section-grid">${panel("Approach comparison",makeTable(["APPROACH","PRECISION","RECALL","F1","FALSE POSITIVE RATE","UNCERTAINTY DETECTION","REMEDIATION SUCCESS"],[["Rules","0.91","0.74","0.81","0.06","Limited","0.68"],["LLM","0.78","0.89","0.83","0.17","0.72","0.61"],["Hybrid Agentic AI","0.93","0.91","0.92","0.05","0.94","0.84"]].map((r,i)=>`<tr>${r.map((v,j)=>`<td class="${j===0?"table-primary":""}">${j===0?v:j===1||j===2||j===3||j===4?badge(v,i===2?"safe":"info"):v}</td>`).join("")}</tr>`).join("")),"Illustrative dataset results · replace with measured evaluation runs")}${panel("Evaluation coverage",`<div class="panel-body progress-list">${[["Legacy algorithms",92],["PQC detection",86],["Wrapper API resolution",64],["Dynamic configuration",58],["False positive review",81],["Rollback scenarios",73]].map(([a,b])=>`<div class="progress-row" style="grid-template-columns:135px 1fr 28px"><span>${a}</span><div class="progress-track"><span style="width:${b}%"></span></div><strong>${b}%</strong></div>`).join("")}</div>`,"Evidence benchmark dimensions")}</div>`;
}
function renderAudit() {
  const rows=[["13:11:40","Alex Rivera","Crypto finding","Requested approval","approval=required","Recorded"],["12:54:31","FirewallAgent","Firewall event","Decision BLOCK","TLS 1.0 · DES-CBC3-SHA","Success"],["12:43:02","MigrationAgent","Remediation REM-1082","Created proposal","Sandbox required; no production change","Success"],["11:20:12","M. Chen","Secure data SDO-0081","Read masked view","Role=Analyst","Allowed"],["10:48:39","VerificationAgent","Sandbox SBX-1901","Completed tests","8/9 pass; compatibility review pending","Completed"]];
  page.innerHTML = `${heading("Audit logs","Trace user and agent actions, evidence references, approvals, and remediation outcomes.",button("Export audit report","export-report","quiet","↓"))}<div class="stat-strip panel" style="margin-bottom:14px">${[["Events today","1,842"],["Agent actions","312"],["Approvals pending","4"],["Access denials","3"]].map(([a,b])=>`<div><small>${a}</small><strong>${b}</strong></div>`).join("")}</div><section class="panel"><div class="toolbar"><input class="search-input" id="audit-search" placeholder="⌕ Search user, resource, action…"><select class="filter-select"><option>All actors</option><option>Users</option><option>Agents</option></select><select class="filter-select"><option>Last 24 hours</option><option>7 days</option></select></div>${makeTable(["TIMESTAMP","ACTOR","RESOURCE","ACTION","DECISION / EVIDENCE","RESULT"],rows.map(r=>`<tr>${r.map((v,i)=>`<td class="${i===1?"table-primary":""}">${escapeHtml(v)}</td>`).join("")}</tr>`).join(""))}<div class="table-footer"><span>Immutable audit retention configured by organization policy</span></div></section>`;
}
function renderSettings() {
  page.innerHTML = `${heading("Settings","Workspace preferences, integrations, and security controls.")}<div class="grid section-grid"><section class="panel"><div class="panel-header"><h2 class="panel-title">Workspace configuration</h2></div><div class="panel-body">${[["Organization","Northstar Financial"],["Workspace region","US East · us-east-1"],["Data retention","365 days"],["Default assessment policy","Northstar Crypto Baseline v12"],["Identity provider","OIDC · MFA enabled"]].map(([a,b])=>`<div class="risk-row"><span>${a}</span><strong style="font-size:9px">${b}</strong></div>`).join("")}</div></section><section class="panel"><div class="panel-header"><h2 class="panel-title">Security controls</h2></div><div class="panel-body">${[["Role-based access","Enabled"],["Audit events","Enabled"],["Secure transport","Required"],["Production deployment approval","Required"],["KMS/HSM integration","Configured by deployment"]].map(([a,b])=>`<div class="risk-row"><span>${a}</span>${badge(b,b==="Enabled"||b==="Required"?"safe":"medium")}</div>`).join("")}<p style="color:var(--muted);font-size:9px">Secrets and KMS credentials are managed outside this browser session.</p></div></section></div>`;
}

function readLocal(key, fallback) {
  try { const value=localStorage.getItem(key);return value?JSON.parse(value):fallback; }
  catch { return fallback; }
}
function saveLocal(key, value) { localStorage.setItem(key,JSON.stringify(value)); }
function currentRole() { return readLocal(DEMO_SESSION_KEY,null)?.role || null; }
function isAdministrator() { return currentRole()==="administrator"; }
function setWorkspaceIdentity() {
  const profile=readLocal(ORG_PROFILE_KEY,null);const session=readLocal(DEMO_SESSION_KEY,null);
  document.getElementById("workspace-name").textContent=profile?.name||"Organization not set up";
  document.getElementById("workspace-subtitle").textContent=profile?.location||"Local demo workspace";
  document.getElementById("workspace-initial").textContent=(profile?.name||"·").slice(0,1).toUpperCase();
  document.getElementById("profile-name").textContent=session?.name||"Demo user";
  document.getElementById("profile-role").textContent=session?.role==="administrator"?"Administrator · demo":session?.role==="accessor"?"Accessor · read-only":"Not signed in";
  document.getElementById("profile-initial").textContent=(session?.name||"D").split(/\s+/).map(x=>x[0]).join("").slice(0,2).toUpperCase();
  const latest=readLocal(SCAN_HISTORY_KEY,[]).at(-1);
  document.getElementById("last-assessment").textContent=latest?`Last scan · ${new Date(latest.created_at).toLocaleString()}`:"No scan recorded";
  document.getElementById("topbar-date").textContent=new Date().toLocaleDateString(undefined,{weekday:"long",month:"long",day:"numeric"});
}
function renderLanding() {
  document.body.classList.add("public-view");
  page.innerHTML=`<div class="landing-shell"><div class="landing-nav"><a class="brand" href="#"><span class="brand-mark"><span></span><span></span><span></span></span><span><strong>PQC<span class="brand-accent">·</span>Migrate</strong><small>CRYPTOGRAPHIC MIGRATION OPERATIONS</small></span></a><span class="landing-chip"><i></i> Local product demo</span></div>
    <div class="landing-body"><div class="landing-copy"><p class="eyebrow">CRYPTO-AGILITY · POST-QUANTUM READINESS</p><h1>Make cryptographic change <span>observable and controlled.</span></h1><p>Discover cryptography. Verify evidence. Plan migration. Test in isolation. Require approval before production change.</p><div class="landing-points"><div><b>01</b><span>Evidence-led risk and inventory scanning</span></div><div><b>02</b><span>Project-specific crypto policy workflows</span></div><div><b>03</b><span>Sandbox and approval-oriented remediation</span></div></div></div>
    <section class="login-card"><p class="eyebrow">DEMO ACCESS</p><h2>Enter your workspace</h2><p class="login-copy">Select a local demonstration role. This is not production authentication and must not be used to protect real data.</p><div class="form-field"><label for="demo-name">Display name</label><input id="demo-name" class="form-control" maxlength="80" placeholder="e.g. Alex Rivera" value="Demo Operator"></div><button class="button primary login-role" data-role="administrator">Continue as Administrator <span>→</span></button><button class="button login-role" data-role="accessor">Continue as Accessor (read-only) <span>→</span></button><div class="demo-security-note">Demo-only roles are stored in this browser. Configure OIDC, server-enforced RBAC, and MFA before deployment.</div></section></div>
    <div class="landing-footer"><span>Assessment language: PQC readiness · quantum risk · crypto-agility</span><span>No “quantum-safe” guarantee is made.</span></div></div>`;
}
function startDemoSession(role) {
  const name=(document.getElementById("demo-name")?.value||"Demo Operator").trim()||"Demo Operator";
  saveLocal(DEMO_SESSION_KEY,{name,role,mode:"local-demo"});
  document.body.classList.remove("public-view");
  setWorkspaceIdentity();
  if(role==="administrator"&&!readLocal(ORG_PROFILE_KEY,null)){renderOrganizationSetup();bindPageEvents();}
  else setPage("Dashboard");
}
function renderOrganizationSetup() {
  document.body.classList.remove("public-view");
  page.innerHTML=`<div class="onboarding-wrap"><div class="onboarding-head"><p class="eyebrow">FIRST-RUN WORKSPACE SETUP</p><h1>Tell us about your organization</h1><p>These local demo settings identify the workspace; profile data is stored only in this browser and is not sent to a production database.</p></div><form id="organization-form" class="panel onboarding-card"><div class="policy-form"><div class="form-field"><label for="org-name">Organization name *</label><input id="org-name" class="form-control" required maxlength="180" placeholder="Organization name"></div><div class="form-field"><label for="org-location">Location *</label><input id="org-location" class="form-control" required maxlength="180" placeholder="City, country or region"></div><div class="form-field"><label for="org-industry">Industry</label><input id="org-industry" class="form-control" maxlength="120" placeholder="e.g. Financial services"></div><div class="form-field"><label for="org-contact">Security contact</label><input id="org-contact" class="form-control" maxlength="180" placeholder="Name or team email"></div><div class="form-field"><label for="org-project">Initial project (optional)</label><input id="org-project" class="form-control" maxlength="180" placeholder="Project name"></div><div class="form-field"><label for="org-reporting">Report cadence preference (scheduler not connected)</label><select id="org-reporting" class="form-control"><option value="manual">Manual</option><option value="weekly">Weekly draft preference</option><option value="monthly">Monthly draft preference</option></select></div></div><div class="policy-actions"><button class="button primary" type="submit">Save workspace and continue</button><button class="button quiet" type="button" data-action="skip-onboarding">Continue without saving</button></div><p class="demo-security-note">Administrator privileges in this prototype are only a client-side demonstration and do not constitute authorization.</p></form></div>`;
}
function saveOrganizationForm() {
  const name=document.getElementById("org-name").value.trim();
  const location=document.getElementById("org-location").value.trim();
  if(!name||!location)return showToast("Organization name and location are required.",true);
  saveLocal(ORG_PROFILE_KEY,{name,location,industry:document.getElementById("org-industry").value.trim(),contact:document.getElementById("org-contact").value.trim(),project:document.getElementById("org-project").value.trim(),reporting:document.getElementById("org-reporting").value,updated_at:new Date().toISOString()});
  setWorkspaceIdentity();setPage("Dashboard");showToast("Local demo workspace profile saved in this browser.");
}
function renderRepositories() {
  const profile=readLocal(ORG_PROFILE_KEY,null);
  page.innerHTML=`${heading("Repositories","Register a GitHub/GitLab source URL, or upload a repository archive in the scanner. External cloning is not enabled until a secure provider connector is configured.",button("Upload repository archive","Cryptographic Scanner","primary","↑"))}<div class="grid section-grid">
  <section class="panel"><div class="panel-header"><div><h2 class="panel-title">Register source repository</h2><p class="panel-subtitle">The URL is recorded as a reference only. No unauthenticated clone or remote code execution occurs.</p></div></div><div class="panel-body"><div class="form-field"><label for="repo-url">GitHub or GitLab HTTPS URL</label><input class="form-control" id="repo-url" placeholder="https://github.com/org/repository"></div><div class="form-field"><label for="repo-project">Project</label><input class="form-control" id="repo-project" value="${escapeHtml(profile?.project||"")}" placeholder="Project name"></div><div class="form-field"><label for="repo-branch">Branch or commit</label><input class="form-control" id="repo-branch" placeholder="main or commit SHA"></div>${button("Register repository","register-repo","primary")}</div></section>
  ${panel("Connector state",`<div class="panel-body"><div class="risk-row"><span>GitHub App / OAuth</span>${badge("Not configured","medium")}</div><div class="risk-row"><span>GitLab OAuth</span>${badge("Not configured","medium")}</div><p style="color:var(--muted);font-size:9px;line-height:1.6">Connectors require server-side OAuth, webhook verification, scoped installation permissions, and a secure worker. Until then, scan a local ZIP through the scanner.</p></div>`,"No fabricated repository health or vulnerability counts")}</div><div id="repo-result" style="margin-top:14px"></div>`;
}
function renderDeployments() {
  page.innerHTML=`${heading("Deployment health","Report a deployment issue and optionally provide a GitHub/GitLab URL. Source and dependency correlation remains unknown until a connector verifies it.")}<div class="grid section-grid"><section class="panel"><div class="panel-header"><div><h2 class="panel-title">Report deployment issue</h2><p class="panel-subtitle">Participants submit symptoms, service, environment, and source repository reference.</p></div></div><div class="panel-body"><div class="form-field"><label for="deployment-issue">Issue description *</label><textarea id="deployment-issue" class="form-control" style="width:100%;min-height:110px" maxlength="2000" placeholder="Describe the observed build/runtime/performance/configuration issue"></textarea></div><div class="form-field"><label for="deployment-repo">GitHub/GitLab URL (optional)</label><input id="deployment-repo" class="form-control" placeholder="https://github.com/org/repo"></div><div class="policy-form"><div class="form-field"><label for="deployment-service">Service</label><input id="deployment-service" class="form-control" placeholder="Unknown unless supplied"></div><div class="form-field"><label for="deployment-environment">Environment</label><input id="deployment-environment" class="form-control" placeholder="e.g. staging"></div></div>${button("Submit issue for correlation","report-deployment-issue","primary")}</div></section><section id="deployment-report" class="panel"><div class="panel-header"><div><h2 class="panel-title">Correlation output</h2><p class="panel-subtitle">Only supplied and verified data is populated.</p></div></div><div class="empty-state"><strong>No deployment issue reported</strong>Source file, crypto dependency, and affected service will not be guessed.</div></section></div>`;
}
function renderPolicyCenter() {
  const selected=window.policyView||"Firewall Builder";
  const tabs=["Firewall Builder","Events","CI/CD Guard","Secure Data"];
  if(selected==="Events")return renderFirewallEvents();
  if(selected==="CI/CD Guard")return renderCiGuard();
  if(selected==="Secure Data")return renderSecureData();
  page.innerHTML=`${heading("Policy center","Create a project-scoped crypto firewall policy, review policy events, and manage CI/CD guardrails.",isAdministrator()?button("Save policy draft","save-custom-policy","primary","＋"):badge("Accessor · read-only","info"))}<div class="toolbar">${tabs.map(t=>`<button class="button ${selected===t?"primary":"quiet"}" data-policy-view="${escapeHtml(t)}">${escapeHtml(t)}</button>`).join("")}</div>
  <div class="grid section-grid"><section class="panel"><div class="panel-header"><div><h2 class="panel-title">Build a firewall policy for a project</h2><p class="panel-subtitle">Generate a reviewable policy artifact from explicit project inputs. This does not deploy a network firewall.</p></div>${badge("Draft only","medium")}</div><div class="panel-body"><div class="policy-form">
  <div class="form-field"><label for="fw-project">Project name *</label><input class="form-control" id="fw-project" required placeholder="Project to protect"></div>
  <div class="form-field"><label for="fw-service">Service / gateway</label><input class="form-control" id="fw-service" placeholder="Service name"></div>
  <div class="form-field"><label for="fw-environment">Target environment</label><select class="form-control" id="fw-environment"><option>Development</option><option>Staging</option><option>Production</option></select></div>
  <div class="form-field"><label for="fw-min-tls">Minimum TLS</label><select id="fw-min-tls" class="form-control"><option>TLS 1.3</option><option>TLS 1.2</option></select></div>
  <div class="form-field"><label for="fw-algorithms">Allowed algorithms / ciphers</label><textarea id="fw-algorithms" class="form-control">AES-256-GCM, SHA-256, TLS_AES_256_GCM_SHA384</textarea></div>
  <div class="form-field"><label for="fw-blocked">Prohibited algorithms</label><textarea id="fw-blocked" class="form-control">MD5, SHA-1, DES, 3DES, RC4</textarea></div>
  <div class="form-field"><label for="fw-key">Minimum RSA key size</label><select id="fw-key" class="form-control"><option>2048</option><option selected>3072</option><option>4096</option></select></div>
  <div class="form-field"><label for="fw-pqc">PQC policy</label><select id="fw-pqc" class="form-control"><option>Monitor readiness</option><option>Require approved hybrid profile</option><option>Not in scope</option></select></div>
  <div class="form-field"><label for="fw-provider">Approved crypto providers</label><input id="fw-provider" class="form-control" value="OpenSSL, BoringSSL"></div>
  <div class="form-field"><label for="fw-expires">Exception expiry (days)</label><select id="fw-expires" class="form-control"><option>7</option><option selected>30</option><option>60</option></select></div></div>
  <div class="policy-actions">${button("Preview policy","preview-policy","quiet")}${isAdministrator()?button("Save draft to policy API","save-custom-policy","primary"):`<span style="align-self:center;color:var(--muted);font-size:9px">Administrator role required to save a draft.</span>`}</div>
  <div id="firewall-policy-output" style="margin-top:12px"></div></div></section>
  <section class="panel"><div class="panel-header"><div><h2 class="panel-title">Enforcement pipeline</h2><p class="panel-subtitle">Generated rules require integration with a supported gateway such as Envoy/OPA.</p></div></div><div class="firewall-flow">${[["Internet","◉"],["WAF","▤"],["Policy","⛨"],["Gateway","⌘"],["Project service","▦"]].map(([n,i],k)=>`${k?'<span class="firewall-connector">→</span>':""}<div class="firewall-hop ${k===2?"active":""}"><div class="hop-icon">${i}</div><strong>${n}</strong><small>${k===2?"Generated rules":k===0?"Source":"Connector required"}</small></div>`).join("")}</div><div class="panel-body"><div class="risk-row"><span>Policy status</span>${badge("Draft · not deployed","medium")}</div><div class="risk-row"><span>Production approval</span>${badge("Required","medium")}</div><p style="color:var(--muted);font-size:9px;line-height:1.6">Policy decision options: ALLOW, MONITOR, WARN, REVIEW, BLOCK. TLS 1.2 alone does not automatically imply BLOCK. High-impact blocking requires approval and client compatibility review.</p></div></section></div>`;
}
function renderTimeline() {
  const history=readLocal(SCAN_HISTORY_KEY,[]);
  const first=history[0],last=history.at(-1);
  const before=new Set(first?.algorithms||[]),after=new Set(last?.algorithms||[]);
  const added=[...after].filter(a=>!before.has(a));const removed=[...before].filter(a=>!after.has(a));
  page.innerHTML=`${heading("Crypto timeline","Compare the initial scan with the latest scan. History stores scan metadata in this browser only; it is not a shared database.")}${panel("Initial → current inventory graph",history.length>=2?`<div class="timeline two-stage"><article class="timeline-card"><div class="timeline-dot"></div><strong>Initial scan</strong><small>${escapeHtml(new Date(first.created_at).toLocaleString())}</small><p>${first.asset_count} candidate matches<br>${escapeHtml(first.algorithms.join(", ")||"No algorithms detected")}</p>${badge("Baseline","info")}</article><article class="timeline-card"><div class="timeline-dot"></div><strong>Latest scan</strong><small>${escapeHtml(new Date(last.created_at).toLocaleString())}</small><p>${last.asset_count} candidate matches<br>${escapeHtml(last.algorithms.join(", ")||"No algorithms detected")}</p>${badge("Current","safe")}</article></div><div class="panel-body kv-grid">${[["New algorithms",added],["Removed algorithms",removed],["Scan count",history.length],["Latest file",last.filename]].map(([k,v])=>`<div class="kv"><small>${k}</small><strong>${escapeHtml(Array.isArray(v)?v.join(", ")||"None recorded":v)}</strong></div>`).join("")}</div>`:`<div class="empty-state"><strong>Initial and final graph appear after two scans</strong>Run at least two scans to compare the observed algorithm sets.</div>`,"Only observations actually saved from scan results are compared")}`;
}
function renderAgility() {
  page.innerHTML=`${heading("Crypto-agility assessment","Assess changeability from source and configuration evidence; no synthetic score is shown.",button("Scan source evidence","Cryptographic Scanner","primary","⌕"))}<div class="grid section-grid"><section class="panel"><div class="panel-header"><div><h2 class="panel-title">Assessment dimensions</h2><p class="panel-subtitle">Each indicator needs validated source/configuration evidence and test signals.</p></div></div><div class="panel-body">${["Algorithm abstraction","Provider abstraction","Configuration-driven crypto","Dependency coupling","Certificate coupling","Protocol flexibility","PQC readiness","Migration complexity"].map(x=>`<div class="risk-row"><span>${x}</span>${badge("INSUFFICIENT_EVIDENCE","medium")}</div>`).join("")}</div></section>${panel("How to assess",`<div class="panel-body"><p style="font-size:10px;color:#aab8c0;line-height:1.7">Upload repository source or configuration under Cryptographic Scanner. The current scanner detects candidate crypto references but does not infer architectural substitutability from a keyword alone. A defensible score requires call-site and dependency evidence, configuration, certificate/protocol coupling, and test coverage.</p>${button("Open scanner","Cryptographic Scanner","primary")}</div>`,"No data-derived assessment is available yet")}</div>`;
}
function renderSampleData() {
  page.innerHTML=`${heading("Sample Data","Synthetic examples are isolated here and are not shown as organization findings or dashboard metrics.",button("Back to workspace","Dashboard","quiet"))}<section class="panel"><div class="panel-header"><div><h2 class="panel-title">Demonstration records</h2><p class="panel-subtitle" id="sample-notice">Loading separate sample database…</p></div>${badge("Synthetic","medium")}</div><div class="toolbar">${button("Algorithms and assets","samples-assets","quiet")}${button("Findings","samples-findings","quiet")}${button("Firewall events","samples-firewall","quiet")}${button("Repositories","samples-repositories","quiet")}</div><div id="sample-table"><div class="empty-state">Loading isolated sample records.</div></div></section>`;
  showSampleTable("assets");
}
function buildFirewallPolicy() {
  return {
    project_name:document.getElementById("fw-project")?.value.trim()||"",
    service:document.getElementById("fw-service")?.value.trim()||"",
    environment:document.getElementById("fw-environment")?.value||"Development",
    rules:{
      minimum_tls:document.getElementById("fw-min-tls")?.value||"TLS 1.3",
      allowed_ciphers:(document.getElementById("fw-algorithms")?.value||"").split(/[,\n]/).map(x=>x.trim()).filter(Boolean),
      blocked_algorithms:(document.getElementById("fw-blocked")?.value||"").split(/[,\n]/).map(x=>x.trim()).filter(Boolean),
      minimum_rsa_key_size:Number(document.getElementById("fw-key")?.value||3072),
      approved_providers:(document.getElementById("fw-provider")?.value||"").split(",").map(x=>x.trim()).filter(Boolean),
      pqc_policy:{mode:document.getElementById("fw-pqc")?.value||"Monitor readiness"},
      exception_expiry:Number(document.getElementById("fw-expires")?.value||30),
      certificate_requirements:{sha2_required:true}
    }
  };
}

function renderGraph() {
  const scan=currentScan?.report;
  if(!scan){page.innerHTML=`${heading("Dependency graph","Graph relationships are only available when supported by repository/package scanner evidence.")}<section class="panel"><div class="empty-state"><strong>No verified dependency graph yet</strong>Upload a repository archive or SBOM to scan candidate assets. This scanner does not currently resolve full transitive package/service relationships.</div></section>`;return;}
  const nodes=(scan.crypto_assets||[]).slice(0,100).map(asset=>`<tr><td>${escapeHtml(asset.file)}:${asset.line}</td><td>${escapeHtml(asset.algorithms.join(", "))}</td><td>${escapeHtml(asset.evidence)}</td></tr>`).join("");
  page.innerHTML=`${heading("Dependency evidence","Crypto reference edges from the latest scan only; unverified service/package edges are not invented.",button("Cryptographic scanner","Cryptographic Scanner","quiet"))}${panel("Observed source-to-algorithm relationships",makeTable(["SOURCE LOCATION","ALGORITHM","OBSERVED EVIDENCE"],nodes),"Candidate references; not a complete dependency graph")}`;
}
function renderBlastRadius() {
  page.innerHTML=`${heading("Blast radius","Affected services cannot be estimated until dependency relationships are verified.",button("Scan source evidence","Cryptographic Scanner","primary"))}<section class="panel"><div class="empty-state"><strong>INSUFFICIENT_EVIDENCE</strong>Upload a repository plus package metadata and service ownership to calculate dependency distance and affected services. Source keyword matches alone are not a blast-radius graph.</div></section>`;
}
function renderInvestigation() {
  page.innerHTML=`${heading("AI investigation","Evidence-first structured orchestration. The local demo has no configured generative LLM endpoint.",button("Open scanner","Cryptographic Scanner","primary"))}<div class="grid section-grid"><section class="panel"><div class="panel-header"><div><h2 class="panel-title">Agent run status</h2><p class="panel-subtitle">No agent run is recorded for this browser session.</p></div>${badge("No active investigation","neutral")}</div><div class="panel-body"><div class="agent-timeline">${["Discovery Agent","Evidence Agent","Risk Agent","Dependency Agent","Migration Agent","Sandbox Agent","Verification Agent","Human approval"].map(x=>`<details class="agent-step"><summary>${x}<span style="float:right;color:var(--muted)">Not run</span></summary><div class="agent-output">No input evidence supplied for this step.</div></details>`).join("")}</div></div></section>${panel("Model configuration",`<div class="panel-body"><p style="color:#aab8c0;font-size:10px;line-height:1.7">The current codebase’s LocalCryptoLLM uses a pretrained SentenceTransformer embedding model to retrieve chunks. It does not train/fine-tune a language model and does not generate original prose: answers concatenate retrieved text and a fixed template. The assessment API currently uses deterministic pattern extraction and a versioned local recommendation table. A generative LLM is not configured.</p></div>`,"Do not treat model output as authoritative evidence")}</div>`;
}
function renderMigration() {
  page.innerHTML=`${heading("Migration planner","Create plans only from findings and dependency relationships that have been verified.",button("Scan for findings","Cryptographic Scanner","primary"))}<section class="panel"><div class="empty-state"><strong>No migration tasks have been created</strong>Run a scan, review evidence, and define owner-approved dependencies and compatibility requirements. Production work requires an explicit approval workflow.</div></section>`;
}
function renderRemediations() {
  page.innerHTML=`${heading("Remediation center","Proposed changes are sandbox-first and approval-gated. This local demo does not apply code patches or deploy to production.")}<div class="grid section-grid three">${["Pending","Sandbox testing","Approval required","Approved","Deployed","Rolled back"].map(state=>`<section class="panel"><div class="panel-header"><h2 class="panel-title">${state}</h2></div><div class="empty-state">No persisted remediation jobs in this status.</div></section>`).join("")}</div>`;
}
function renderFirewallEvents() {
  page.innerHTML=`${heading("Policy events","Event entries will appear after a configured gateway or the server event API supplies real telemetry.")}<section class="panel"><div class="empty-state"><strong>No firewall events recorded</strong>Connect Envoy/OPA or another managed gateway to populate events. Sample events are available separately under Sample Data.</div></section>`;
}
function renderSecureData() {
  page.innerHTML=`${heading("Secure data","This local demo stores no sensitive payload and displays no private keys.")}<div class="grid section-grid">${panel("Secure data access",`<div class="panel-body"><div class="risk-row"><span>Organization role</span>${badge(currentRole()||"not signed in","info")}</div><div class="risk-row"><span>Local data encryption / KMS</span>${badge("Not configured","medium")}</div><p style="color:var(--muted);font-size:9px">Production secure-data access requires server-side RBAC, organization isolation, envelope encryption backed by a KMS/HSM, and immutable access logging. This browser demo provides no decrypted view.</p></div>`,"No secure records are seeded")}${panel("Access log",`<div class="empty-state">No persistent secure-data access records are available.</div>`,"Connect the production audit store to view access events")}</div>`;
}
function renderCiGuard() {
  page.innerHTML=`${heading("CI/CD guard","Submit a change only when an authenticated repository integration is configured. No sample PRs are presented as live decisions.",button("Open scanner","Cryptographic Scanner","primary"))}<section class="panel"><div class="empty-state"><strong>Repository webhook integration not configured</strong>After connecting GitHub/GitLab with verified webhook signatures, CI scans can return PASS, REVIEW, or BLOCK alongside file/line evidence and matched policy.</div></section>`;
}
function renderSettings() {
  const profile=readLocal(ORG_PROFILE_KEY,{});
  const disabled=isAdministrator()?"":"disabled";
  page.innerHTML=`${heading("Settings","Organization profile and report preferences for this local demo.",isAdministrator()?button("Save changes","save-organization","primary"):badge("Accessor · read-only","info"))}<form id="organization-form" class="panel onboarding-card"><div class="policy-form">${[["Organization name","org-name",profile.name||""],["Location","org-location",profile.location||""],["Industry","org-industry",profile.industry||""],["Security contact","org-contact",profile.contact||""],["Initial project","org-project",profile.project||""]].map(([label,id,value])=>`<div class="form-field"><label for="${id}">${label}</label><input id="${id}" class="form-control" maxlength="180" value="${escapeHtml(value)}" ${disabled}></div>`).join("")}<div class="form-field"><label for="org-reporting">Report cadence preference (scheduler not connected)</label><select id="org-reporting" class="form-control" ${disabled}><option value="manual" ${profile.reporting==="manual"?"selected":""}>Manual</option><option value="weekly" ${profile.reporting==="weekly"?"selected":""}>Weekly draft preference</option><option value="monthly" ${profile.reporting==="monthly"?"selected":""}>Monthly draft preference</option></select></div></div><div class="policy-actions">${isAdministrator()?`<button class="button primary" type="submit">Save local demo profile</button>`:""}</div><p class="demo-security-note">Profile is stored in browser local storage, not PostgreSQL. Production organization onboarding and role enforcement require server authentication and persistence.</p></form>`;
}
function renderEvaluation() {
  page.innerHTML=`${heading("Evaluation","Track measured detector and remediation evaluation runs. No benchmark results have been recorded.",button("Record evaluation","record-evaluation","primary","＋"))}<section class="panel"><div class="empty-state"><strong>No evaluation runs recorded</strong>Compare Rules, LLM, and Hybrid Agentic AI only after running the same versioned dataset and capturing measured precision, recall, F1, false-positive rate, uncertainty detection, remediation success, and rollback success.</div></section>`;
}
async function renderAudit() {
  page.innerHTML=`${heading("Audit logs","Sensitive operations and agent decisions from the active backend process.",button("Refresh","refresh-audit","quiet","↻"))}<section class="panel"><div id="audit-content" class="empty-state">Loading audit events…</div></section>`;
  try{const rows=await request(`${API}/audit`);const target=document.getElementById("audit-content");if(!target)return;target.outerHTML=rows.length?makeTable(["TIME","USER","AGENT","RESOURCE","ACTION","APPROVAL","RESULT"],rows.map(r=>`<tr><td>${escapeHtml(r.timestamp||r.time||"")}</td><td>${escapeHtml(r.user||"")}</td><td>${escapeHtml(r.agent||"")}</td><td>${escapeHtml(r.resource||"")}</td><td>${escapeHtml(r.action||"")}</td><td>${escapeHtml(r.approval||"")}</td><td>${escapeHtml(r.result||"")}</td></tr>`).join("")):`<div class="empty-state"><strong>No audit events recorded</strong>Actions will appear when supported backend routes are used.</div>`;}
  catch(error){const target=document.getElementById("audit-content");if(target)target.textContent=`Audit API unavailable: ${error.message}`;}
}

function bindPageEvents() {
  const input=document.getElementById("scanner-files");const drop=document.getElementById("scanner-drop");
  if(input){input.addEventListener("change",()=>updateScannerSelection(input.files));drop?.addEventListener("dragover",e=>{e.preventDefault();drop.classList.add("dragging");});drop?.addEventListener("dragleave",()=>drop.classList.remove("dragging"));drop?.addEventListener("drop",e=>{e.preventDefault();drop.classList.remove("dragging");input.files=e.dataTransfer.files;updateScannerSelection(input.files);});}
  const pdfInput=document.getElementById("project-file");const pdfDrop=document.getElementById("project-drop");
  if(pdfInput){pdfInput.addEventListener("change",()=>{selectedProjectFile=pdfInput.files[0]||null;document.getElementById("project-upload-name").textContent=selectedProjectFile?`${selectedProjectFile.name} · ${(selectedProjectFile.size/1024/1024).toFixed(1)} MB`:"No document selected";});pdfDrop?.addEventListener("dragover",e=>{e.preventDefault();pdfDrop.classList.add("dragging");});pdfDrop?.addEventListener("dragleave",()=>pdfDrop.classList.remove("dragging"));pdfDrop?.addEventListener("drop",e=>{e.preventDefault();pdfDrop.classList.remove("dragging");const file=e.dataTransfer.files[0];if(file&&file.name.toLowerCase().endsWith(".pdf")){selectedProjectFile=file;document.getElementById("project-upload-name").textContent=`${file.name} · ${(file.size/1024/1024).toFixed(1)} MB`;}else showToast("Choose a PDF file.",true);});}
  const orgForm=document.getElementById("organization-form");orgForm?.addEventListener("submit",e=>{e.preventDefault();saveOrganizationForm();});
  document.querySelectorAll("[data-policy-view]").forEach(button=>button.addEventListener("click",()=>{window.policyView=button.dataset.policyView;renderPolicyCenter();bindPageEvents();}));
  document.querySelectorAll("[data-role]").forEach(button=>button.addEventListener("click",()=>startDemoSession(button.dataset.role)));
  document.querySelectorAll("[data-sample-view]").forEach(button=>button.addEventListener("click",()=>showSampleTable(button.dataset.sampleView)));
}
function updateScannerSelection(files) {
  const list=[...files];const total=list.reduce((sum,file)=>sum+file.size,0);
  document.getElementById("scanner-selection").textContent=list.length?`${list.length} file(s) · ${(total/1024/1024).toFixed(1)} MiB selected`:"No files selected";
  if(total>10*1024**3)showToast("Combined selection exceeds the 10 GiB request limit.",true);
  if(list.some(file=>file.size>10*1024**3))showToast("A selected file exceeds the 10 GiB per-file limit.",true);
}
function readCostAssumptions() {
  const fields={
    hourly_rate_usd:"cost-hourly-rate",
    legacy_fix_hours_per_finding:"cost-legacy-hours",
    quantum_migration_hours_per_finding:"cost-quantum-hours",
    crypto_review_hours_per_finding:"cost-review-hours"
  };
  const assumptions={};
  for(const [key,id] of Object.entries(fields)){
    const input=document.getElementById(id);const value=Number(input?.value);
    const max=key==="hourly_rate_usd"?5000:1000;
    if(!Number.isFinite(value)||value<(key==="hourly_rate_usd"?1:0)||value>max){
      throw new Error(`Enter a valid ${id.replace("cost-","").replaceAll("-"," ")} value.`);
    }
    assumptions[key]=value;
  }
  return assumptions;
}
function aggregateCostAnalysis(results) {
  const reports=results.map(item=>item.report?.cost_analysis).filter(Boolean);
  if(!reports.length)return null;
  const sumValues=(section,key)=>reports.reduce((total,item)=>total+Number(item[section]?.[key]||0),0);
  const counts={};
  for(const report of reports)for(const [name,count] of Object.entries(report.finding_counts||{}))counts[name]=(counts[name]||0)+Number(count);
  const hours={low:sumValues("estimated_hours","low"),expected:sumValues("estimated_hours","expected"),high:sumValues("estimated_hours","high")};
  const costs={low:sumValues("cost_range_usd","low"),expected:sumValues("cost_range_usd","expected"),high:sumValues("cost_range_usd","high")};
  return {...reports.at(-1),total_cost_usd:costs.expected,estimated_hours:hours,cost_range_usd:costs,finding_counts:counts};
}
async function runUploadScan(inputId,resultId,progressId,projectOnly=false) {
  const input=document.getElementById(inputId);const files=projectOnly?(selectedProjectFile?[selectedProjectFile]:[]):[...(input?.files||[])];
  if(!files.length)return showToast("Select at least one supported input file.",true);
  if(projectOnly&&files[0].name.toLowerCase().split(".").at(-1)!=="pdf")return showToast("Project risk analysis accepts PDF only.",true);
  const total=files.reduce((sum,file)=>sum+file.size,0);if(total>10*1024**3)return showToast("Combined input exceeds the 10 GiB limit.",true);
  let assumptions;try{assumptions=readCostAssumptions();}catch(error){return showToast(error.message,true);}
  const progress=document.getElementById(progressId);progress.hidden=false;progress.value=0;
  const results=[];
  try {
    for(let i=0;i<files.length;i++){
      const file=files[i];const form=new FormData();form.append("file",file,file.name);for(const [key,value] of Object.entries(assumptions))form.append(key,String(value));
      const result=await request(`${API}/scans/upload`,{method:"POST",body:form});results.push(result);progress.value=Math.round((i+1)/files.length*100);
    }
    const result=results.at(-1);currentScan=result;
    const aggregateAssets=results.flatMap(r=>r.report?.crypto_assets||[]);
    if(results.length>1){
      const softwareReports=results.map(r=>r.report?.software_analysis).filter(Boolean);
      const languages={};for(const item of softwareReports)for(const [name,count] of Object.entries(item.languages_detected||{}))languages[name]=(languages[name]||0)+count;
      const packageManifests=softwareReports.flatMap(item=>item.package_manifests||[]);
      const dependencyNames=[...new Set(softwareReports.flatMap(item=>item.dependency_names||[]))].sort();
      const secrets=results.flatMap(r=>r.report?.potential_secret_findings||[]);
      const risks=results.map(r=>r.report?.risk||{});
      const rank={unknown:0,low:1,medium:2,high:3,critical:4};
      const mergedRisk={};for(const key of ["classical","quantum","implementation","configuration","compliance","operational"]){mergedRisk[key]=risks.map(item=>item[key]||"unknown").sort((a,b)=>(rank[b]||0)-(rank[a]||0))[0]||"unknown";}
      const softwareAnalysis=softwareReports.length?{...softwareReports.at(-1),source_files_analyzed:softwareReports.reduce((n,item)=>n+item.source_files_analyzed,0),total_text_lines_analyzed:softwareReports.reduce((n,item)=>n+item.total_text_lines_analyzed,0),languages_detected:languages,package_manifests:packageManifests,dependencies_identified:dependencyNames.length,dependency_names:dependencyNames.slice(0,500),crypto_candidate_matches:aggregateAssets.length,potential_secret_findings:secrets.length}:undefined;
      const report={...result.report,crypto_assets:aggregateAssets,algorithms:[...new Set(results.flatMap(r=>r.report?.algorithms||[]))],risk:mergedRisk,potential_secret_findings:secrets,cost_analysis:aggregateCostAnalysis(results),uncertainties:[...new Set(results.flatMap(r=>r.report?.uncertainties||[]))]};
      if(softwareAnalysis)report.software_analysis=softwareAnalysis;
      currentScan={...result,filename:`${results.length} uploaded files`,report};
    }
    const history=readLocal(SCAN_HISTORY_KEY,[]);history.push({scan_id:result.scan_id,created_at:new Date().toISOString(),filename:results.length>1?`${results.length} files`:result.filename,asset_count:aggregateAssets.length,algorithms:[...new Set(results.flatMap(r=>r.report?.algorithms||[]))],status:result.status});saveLocal(SCAN_HISTORY_KEY,history.slice(-50));
    const resultContainer=document.getElementById(resultId);if(resultContainer)resultContainer.innerHTML=assessmentMarkup(currentScan);
    const headingActions=page.querySelector(".heading-actions");
    if(headingActions)headingActions.innerHTML=`${button("Export PDF","export-scan-pdf","quiet","↓")}${button("Export JSON","export-scan-json","quiet","{ }")}${button("Export full CSV","export-scan-csv","primary","↓")}`;
    if(input)input.value="";
    if(projectOnly)selectedProjectFile=null;
    showToast(`Scan completed for ${results.length} input file(s). Review evidence and uncertainty before acting.`);
  } catch(error){showToast(`Scan failed: ${error.message}`,true);}
  finally{progress.hidden=true;progress.value=0;}
}
async function showSampleTable(view) {
  const target=document.getElementById("sample-table");if(!target)return;
  try{
    const data=await request(`${API}/demo/samples`);const notice=document.getElementById("sample-notice");
    if(notice)notice.textContent=`${data.notice} · Source: ${data.database}`;
    if(view==="findings")target.innerHTML=makeTable(["FINDING","ALGORITHM","SERVICE","SOURCE","CONFIDENCE"],data.findings.map(f=>`<tr><td>${escapeHtml(f.title)}</td><td>${escapeHtml(f.algorithm)}</td><td>${escapeHtml(f.service)}</td><td class="code">${escapeHtml(f.file)}</td><td>${escapeHtml(f.confidence)}</td></tr>`).join(""));
    else if(view==="firewall")target.innerHTML=makeTable(["TIME","DECISION","TLS","CIPHER","SERVICE"],data.firewall_events.map(e=>`<tr><td>${escapeHtml(e.time)}</td><td>${badge(e.decision)}</td><td>${escapeHtml(e.tls)}</td><td>${escapeHtml(e.cipher)}</td><td>${escapeHtml(e.service)}</td></tr>`).join(""));
    else if(view==="repositories")target.innerHTML=makeTable(["REPOSITORY","PROVIDER","BRANCH","LANGUAGE","SAMPLE FINDINGS"],data.repositories.map(r=>`<tr><td>${escapeHtml(r.name)}</td><td>${escapeHtml(r.provider)}</td><td>${escapeHtml(r.branch)}</td><td>${escapeHtml(r.language)}</td><td>${r.findings}</td></tr>`).join(""));
    else target.innerHTML=makeTable(["ID","ALGORITHM","LIBRARY","ROLE","FILE / LINE","KEY SIZE","PROTOCOL","SERVICE","CLASSIFICATION","CONFIDENCE"],data.crypto_assets.map(a=>`<tr><td>${escapeHtml(a.id)}</td><td class="table-primary">${escapeHtml(a.algorithm)}</td><td>${escapeHtml(a.library)} · ${escapeHtml(a.version)}</td><td>${escapeHtml(a.role)}</td><td class="code">${escapeHtml(a.file)}:${a.line}</td><td>${escapeHtml(a.key_size)}</td><td>${escapeHtml(a.protocol)}</td><td>${escapeHtml(a.service)}</td><td>${badge(a.classification)}</td><td>${a.confidence}%</td></tr>`).join(""));
  }catch(error){target.innerHTML=`<div class="empty-state"><strong>Sample database unavailable</strong>${escapeHtml(error.message)}</div>`;}
}

function selectProjectFile(file) {
  if(!file.name.toLowerCase().endsWith(".pdf")) return showToast("Select a PDF project specification.",true);
  if(file.size > 50*1024*1024) return showToast("PDF exceeds the 50 MB upload limit.",true);
  selectedProjectFile=file;
  document.getElementById("project-upload-name").textContent=`${file.name} · ${(file.size/1024/1024).toFixed(1)} MB`;
}
async function analyzeProject() {
  const file=selectedProjectFile;
  if(!file) return showToast("Choose a PDF before starting the project assessment.",true);
  const form=new FormData();form.append("file",file);
  try {
    const result=await request(`${API}/ingest`,{method:"POST",body:form});
    currentProjectProfile={profile:result.profile||{},risk_score:result.risk_score,status:result.assessment_status||result.status};
    showProjectResult(currentProjectProfile,result);showToast("PDF processed. Review extracted fields and evidence gaps.");
  } catch(error) { showToast(`Project scan failed: ${error.message}`,true); }
}
function showProjectResult(result,ingest) {
  const profile=result.profile||{};const set=(id,value)=>{const el=document.getElementById(id);if(el)el.textContent=Array.isArray(value)?value.join(", ")||"Unknown":value||"Unknown";};
  set("project-scope",profile.scope);set("project-technology-stack",profile.technology);set("project-timeline",profile.timeline);set("project-budget",profile.budget);set("project-vendors",profile.vendors);set("project-dependencies",profile.dependencies);set("project-security-requirements",profile.security_requirements);
  document.getElementById("project-results").innerHTML=`<section class="panel"><div class="panel-header"><div><h2 class="panel-title">Project assessment result</h2><p class="panel-subtitle">Upload receipt ${escapeHtml(ingest.hash||"recorded")} · Fields are extracted from document text; absent fields remain unknown.</p></div>${badge(result.status||"review")}</div><div class="panel-body kv-grid">${[["Scope",profile.scope],["Technology",profile.technology],["Timeline",profile.timeline],["Budget",profile.budget],["Vendors",profile.vendors],["Dependencies",profile.dependencies],["Security requirements",profile.security_requirements],["Risks",profile.risks]].map(([n,v])=>`<div class="kv"><small>${n}</small><strong>${escapeHtml(Array.isArray(v)?v.join(", ")||"INSUFFICIENT_EVIDENCE":v||"INSUFFICIENT_EVIDENCE")}</strong></div>`).join("")}<p style="grid-column:1/-1;color:var(--muted);font-size:9px">Risk score: ${result.risk_score==null?"Not calculated":result.risk_score}. Uploaded code is never executed; document text is processed within configured upload and extraction limits.</p></div></section>`;
}
function modal(title, description, content = "") {
  const dialog=document.getElementById("action-modal");document.getElementById("modal-content").innerHTML=`<p class="eyebrow">PQC-MIGRATE / ACTION</p><h2>${escapeHtml(title)}</h2><p>${escapeHtml(description)}</p>${content}`;dialog.showModal();
}
function csvDownload(filename, headers, rows) {
  const quote=v=>`"${String(v??"").replaceAll('"','""')}"`;
  const csv=[headers,...rows].map(row=>row.map(quote).join(",")).join("\r\n");
  downloadBlob(filename,new Blob([csv],{type:"text/csv"}));
}
function downloadBlob(filename, blob) {
  const url=URL.createObjectURL(blob);
  const link=document.createElement("a");
  link.href=url;link.download=filename;document.body.append(link);link.click();link.remove();
  setTimeout(()=>URL.revokeObjectURL(url),1000);
}
async function action(name) {
  const dialog=document.getElementById("action-modal");if(name==="close-modal"){dialog.close();return;}
  const adminOnly=["save-custom-policy","deploy-policy","rollback-policy","save-organization","register-repo","approve-policy","apply-fix"];
  if(adminOnly.includes(name)&&!isAdministrator()){showToast("This action is administrator-only in the local demo. Production permissions must be enforced by the server.",true);return;}
  if(name==="skip-onboarding"){setPage("Dashboard");return;}
  if(name==="logout"){localStorage.removeItem(DEMO_SESSION_KEY);dialog.close();document.body.classList.add("public-view");renderLanding();bindPageEvents();return;}
  if(name==="start-file-scan"){await runUploadScan("scanner-files","scan-result","scan-progress");return;}
  if(name==="analyze-project"){await runUploadScan("project-file","project-results","project-progress",true);return;}
  if(name==="load-sample-project"||name==="load-sample-software"){
    const project=name==="load-sample-project";
    const input=document.getElementById(project?"project-file":"scanner-files");
    try{
      const response=await fetch(`${API}/demo/sample-files/${project?"project.pdf":"software.zip"}`);
      if(!response.ok)throw new Error(`Sample download failed (${response.status}).`);
      const blob=await response.blob();
      const sample=new File([blob],project?"pqc-demo-project-spec.pdf":"pqc-demo-software.zip",{type:blob.type});
      const transfer=new DataTransfer();transfer.items.add(sample);input.files=transfer.files;
      if(project){selectedProjectFile=sample;document.getElementById("project-upload-name").textContent=`${sample.name} · ${(sample.size/1024).toFixed(1)} KB`;}
      else updateScannerSelection(input.files);
      showToast("Synthetic sample loaded. Review the cost assumptions, then run the scan.");
    }catch(error){showToast(`Could not load sample input: ${error.message}`,true);}
    return;
  }
  if(name==="export-scan-json"){
    if(!currentScan)return showToast("Run a scan before exporting a report.",true);
    downloadBlob(`pqc-assessment-${currentScan.scan_id}.json`,new Blob([JSON.stringify(currentScan,null,2)],{type:"application/json"}));return;
  }
  if(name==="export-scan-csv"){
    if(!currentScan)return showToast("Run a scan before exporting an inventory.",true);
    const report=currentScan.report||{};const cost=report.cost_analysis||{};const software=report.software_analysis||{};
    const rows=[
      ["Assessment","Status",report.classification||currentScan.status,"","",""],
      ["Cost","Expected total USD",cost.total_cost_usd??"","","",""],
      ["Cost","Low estimate USD",cost.cost_range_usd?.low??"","","",""],
      ["Cost","High estimate USD",cost.cost_range_usd?.high??"","","",""],
      ["Cost","Expected effort hours",cost.estimated_hours?.expected??"","","",""],
      ["Cost","Hourly rate USD",cost.assumptions?.hourly_rate_usd??"","","",""],
      ...Object.entries(report.risk||{}).map(([name,value])=>["Risk",name,value,"","",""]),
      ...Object.entries(software.languages_detected||{}).map(([name,count])=>["Software language",name,count,"","",""]),
      ...(software.package_manifests||[]).map(item=>["Package manifest",item.file,`${item.dependency_count} dependencies`,"","",""]),
      ...(software.dependency_names||[]).map(name=>["Dependency",name,"Inventory only; vulnerabilities not checked","","",""]),
      ...(report.crypto_assets||[]).flatMap(item=>item.algorithms.map(algorithm=>["Crypto evidence",algorithm,item.file,item.line,item.evidence,item.evidence_hash])),
      ...(report.potential_secret_findings||[]).map(item=>["Potential secret",item.type,item.file,item.line,"[REDACTED]",item.evidence_hash])
    ];
    csvDownload("pqc-full-analysis.csv",["Type","Category","Value","File","Line","Evidence / SHA-256"],rows);return;
  }
  if(name==="export-scan-pdf"){
    if(!currentScan)return showToast("Run a scan before exporting a PDF.",true);
    const w=window.open("","_blank");if(!w)return showToast("Allow pop-ups to open the printable PDF report.",true);
    const printable=`<!doctype html><html><head><title>PQC-Migrate Assessment</title><style>body{font:14px Arial,sans-serif;color:#17232d;margin:36px}h1,h2{color:#123b3b}small{color:#586a74}table{width:100%;border-collapse:collapse}td,th{border:1px solid #bcc7cc;padding:6px;text-align:left;font-size:11px}section{page-break-inside:avoid;margin:18px 0}pre{white-space:pre-wrap;word-break:break-word;font:11px monospace}</style></head><body><h1>Cryptographic migration assessment</h1><small>Evidence-based report · ${escapeHtml(currentScan.scan_id)} · ${escapeHtml(new Date().toLocaleString())}</small><p>Assessment is not a claim of quantum safety. Candidate matches require validation.</p><h2>Project profile</h2><pre>${escapeHtml(JSON.stringify(currentScan.report.project_profile,null,2))}</pre><h2>Risk dimensions</h2><pre>${escapeHtml(JSON.stringify(currentScan.report.risk,null,2))}</pre><h2>Estimated cost and effort · USD</h2><pre>${escapeHtml(JSON.stringify(currentScan.report.cost_analysis,null,2))}</pre><h2>Software analysis</h2><pre>${escapeHtml(JSON.stringify(currentScan.report.software_analysis||{status:"Not a software archive"},null,2))}</pre><h2>Cryptographic evidence</h2><table><tr><th>Algorithms</th><th>File</th><th>Line</th><th>Evidence hash</th></tr>${(currentScan.report.crypto_assets||[]).map(x=>`<tr><td>${escapeHtml(x.algorithms.join(", "))}</td><td>${escapeHtml(x.file)}</td><td>${x.line}</td><td>${escapeHtml(x.evidence_hash)}</td></tr>`).join("")}</table><h2>Potential secret findings</h2><pre>${escapeHtml(JSON.stringify(currentScan.report.potential_secret_findings||[],null,2))}</pre><h2>Knowledge recommendations</h2><pre>${escapeHtml(JSON.stringify(currentScan.report.knowledge_recommendations,null,2))}</pre><h2>Uncertainties</h2><ul>${(currentScan.report.uncertainties||[]).map(x=>`<li>${escapeHtml(x)}</li>`).join("")}</ul><small>Model status: ${escapeHtml(currentScan.report.llm_status?.reason||"not available")}</small></body></html>`;
    w.document.write(printable);w.document.close();w.focus();setTimeout(()=>w.print(),250);return;
  }
  if(name==="preview-policy"){document.getElementById("firewall-policy-output").innerHTML=`<div class="evidence-box"><strong>Policy preview · not deployed</strong><pre style="white-space:pre-wrap;color:#cbd7dd">${escapeHtml(JSON.stringify(buildFirewallPolicy(),null,2))}</pre></div>`;return;}
  if(name==="save-custom-policy"){
    const policy=buildFirewallPolicy();if(!policy.project_name)return showToast("Enter a project name before building its firewall policy.",true);
    try{const response=await request(`${API}/firewall/policies`,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(policy.rules)});const record={...policy,api_response:response,saved_at:new Date().toISOString()};saveLocal("pqc_demo_firewall_policy",record);document.getElementById("firewall-policy-output").innerHTML=`<div class="evidence-box"><strong>Draft created · ${escapeHtml(response.id||"policy")}</strong><p>Policy JSON is saved locally for this demo. This is not a network firewall and has not been deployed.</p><pre style="white-space:pre-wrap;color:#cbd7dd">${escapeHtml(JSON.stringify(record,null,2))}</pre></div>`;showToast("Project policy draft created; deployment still requires an approved gateway integration.");}
    catch(error){showToast(`Could not create policy draft: ${error.message}`,true);}return;
  }
  if(name==="report-deployment-issue"){
    const issue=document.getElementById("deployment-issue")?.value.trim();if(!issue)return showToast("Describe the deployment issue before submitting.",true);
    try{const result=await request(`${API}/deployments/report-issue`,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({issue,repository_url:document.getElementById("deployment-repo").value.trim(),service:document.getElementById("deployment-service").value.trim(),environment:document.getElementById("deployment-environment").value.trim()})});document.getElementById("deployment-report").innerHTML=`<div class="panel-header"><div><h2 class="panel-title">Issue received · ${escapeHtml(result.issue_id)}</h2><p class="panel-subtitle">Source and dependency relationships are unverified without connector evidence.</p></div>${badge(result.status,"safe")}</div><div class="panel-body kv-grid">${Object.entries(result.correlation||{}).map(([k,v])=>`<div class="kv"><small>${escapeHtml(k.replaceAll("_"," "))}</small><strong>${escapeHtml(Array.isArray(v)?v.join(", "):v)}</strong></div>`).join("")}<div class="kv" style="grid-column:1/-1"><small>Uncertainties</small><strong>${escapeHtml((result.uncertainties||[]).join(" · "))}</strong></div></div>`;showToast("Deployment report received; no source correlation was invented.");}
    catch(error){showToast(`Issue submission failed: ${error.message}`,true);}return;
  }
  if(name==="register-repo"){
    const url=document.getElementById("repo-url").value.trim();if(!/^https:\/\/(github\.com|gitlab\.com)\/[^/]+\/[^/]+/.test(url))return showToast("Enter a valid GitHub or GitLab repository HTTPS URL.",true);
    const repositories=readLocal("pqc_demo_repository_refs",[]);repositories.push({url,project:document.getElementById("repo-project").value.trim()||"unknown",branch:document.getElementById("repo-branch").value.trim()||"default branch",added_at:new Date().toISOString()});saveLocal("pqc_demo_repository_refs",repositories);
    document.getElementById("repo-result").innerHTML=`<section class="panel"><div class="panel-body"><strong>Repository reference saved in this browser</strong><p style="color:var(--muted);font-size:9px">No clone or scan was performed. Configure a Git provider connector before requesting repository contents.</p><span class="code">${escapeHtml(url)}</span></div></section>`;return;
  }
  if(name==="samples-assets"){showSampleTable("assets");return;}
  if(name==="samples-findings"){showSampleTable("findings");return;}
  if(name==="samples-firewall"){showSampleTable("firewall");return;}
  if(name==="save-organization"){saveOrganizationForm();return;}
  if(name==="export-csv"){
    if(activePage==="Sample Data"){
      try{const sample=await request(`${API}/demo/samples`);const headers=["ID","Algorithm","Library","Role","File","Line","Classification","Confidence"];csvDownload("pqc-demo-sample-assets.csv",headers,sample.crypto_assets.map(a=>[a.id,a.algorithm,a.library,a.role,a.file,a.line,a.classification,a.confidence]));}
      catch(error){showToast(`Sample export unavailable: ${error.message}`,true);}return;
    }
    if(!currentScan)return showToast("Run an organization scan first. Synthetic records are available separately under Sample Data.",true);
    const rows=(currentScan.report?.crypto_assets||[]).flatMap(item=>item.algorithms.map(algorithm=>[algorithm,item.file,item.line,item.evidence,item.evidence_hash]));
    csvDownload("pqc-crypto-evidence.csv",["Algorithm","File","Line","Evidence","SHA-256"],rows);return;
  }
  if(name==="export-report"){
    if(!currentScan){modal("No organization scan to export","Run a project or cryptographic scan first. Sample records are isolated from organization reports.");return;}
    modal("Export assessment","Export only the current scan evidence.",`<div style="display:flex;gap:8px;margin-top:14px">${button("PDF / Print","export-scan-pdf","quiet")}${button("JSON","export-scan-json","quiet")}${button("CSV","export-scan-csv","primary")}</div>`);return;
  }
  if(name==="export-json"){if(!currentScan)return showToast("Run a scan before exporting. Sample records are available in their separate view.",true);downloadBlob(`pqc-assessment-${currentScan.scan_id}.json`,new Blob([JSON.stringify(currentScan,null,2)],{type:"application/json"}));return;}
  if(name==="export-pdf"){dialog.close();window.print();return;}
  if(navItems.some(item=>item.title===name)){dialog.close();setPage(name);return;}
  if(name==="run-scan"){
    try{const result=await request(`${API}/repositories/scan`,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({repository_id:"repo-demo-1",scan_type:"full"})});showToast(`Repository scan ${result.status||"completed"}.`);}
    catch(error){showToast(`Repository scan unavailable: ${error.message}`,true);}return;
  }
  if(name==="scan-pr"){
    try{const diff=document.getElementById("pr-diff").value;const result=await request(`${API}/ci/scan`,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({repository:document.getElementById("pr-repo").value,commit_hash:document.getElementById("pr-commit").value,diff,source_text:diff})});document.getElementById("ci-result").innerHTML=`<div class="panel-header"><div><h2 class="panel-title">Pull request decision</h2><p class="panel-subtitle">Server response · evidence-led policy evaluation</p></div>${badge(result.decision,result.decision==="PASS"?"safe":result.decision==="BLOCK"?"critical":"medium")}</div><div class="panel-body"><div class="risk-row"><span>Finding</span><strong>${escapeHtml(result.finding||"No finding returned")}</strong></div><div class="risk-row"><span>File and line</span><strong>${escapeHtml(result.file||"Not provided")}:${escapeHtml(result.line||"—")}</strong></div><div class="risk-row"><span>Algorithm</span><strong>${escapeHtml(result.algorithm||"Not resolved")}</strong></div><div class="risk-row"><span>Policy</span><strong>${escapeHtml(result.policy||"Not returned")}</strong></div><div class="evidence-box" style="margin-top:12px"><p>${escapeHtml((result.evidence||[]).join(" · "))}</p><div class="evidence-meta"><span>Recommended fix: ${escapeHtml(result.recommended_fix||"Review evidence")}</span></div></div><p style="color:var(--muted);font-size:9px">This decision is from the configured server policy endpoint. Confirm scanner evidence before acting.</p></div>`;showToast(`CI scan returned ${result.decision}.`);}
    catch(error){showToast(`CI scan failed: ${error.message}`,true);}return;
  }
  if(name==="submit-deployment"){
    try{const result=await request(`${API}/deployments/scan`,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({deployment_id:document.getElementById("deploy-id").value,runtime_error:document.getElementById("deploy-error").value})});modal("Deployment correlation",`Status: ${result.status}. Runtime event is mapped to its reported source, dependency, and service.`, `<div class="evidence-box"><p>${escapeHtml(JSON.stringify(result.correlation||result,null,2))}</p></div>`);}
    catch(error){showToast(`Deployment analysis failed: ${error.message}`,true);}return;
  }
  if(name==="test-policy"){
    try{const policy={minimum_tls:document.getElementById("minimum-tls").value,allowed_ciphers:document.getElementById("allowed-ciphers").value.split(/\n/).map(s=>s.trim()).filter(Boolean),blocked_algorithms:document.getElementById("blocked-algorithms").value.split(",").map(s=>s.trim()).filter(Boolean),minimum_rsa_key_size:Number(document.getElementById("minimum-rsa").value),pqc_policy:{mode:document.getElementById("pqc-policy").value}};const result=await request(`${API}/firewall/policies`,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(policy)});showToast(`Policy draft validated by API: ${result.status||"created"}. Approval required before deployment.`);}
    catch(error){showToast(`Policy test failed: ${error.message}`,true);}return;
  }
  if(name==="connect-ws"){
    try{const url=`${location.protocol==="https:"?"wss":"ws"}://${location.host}/ws/events`;const ws=new WebSocket(url);ws.onmessage=event=>{try{const data=JSON.parse(event.data);showToast(`Event stream: ${data.message||data.status||"event received"}`);}catch{showToast("Event received.");}};ws.onopen=()=>showToast("WebSocket event stream connected.");ws.onerror=()=>showToast("Could not connect to the WebSocket event stream.",true);ws.onclose=()=>{};}
    catch(error){showToast(error.message,true);}return;
  }
  const copy={
    "open-finding":["Crypto finding details","A representative, evidence-backed finding is shown. File and line references are tied to the sample scan snapshot."],
    "investigate":["Start evidence-based investigation","Discovery → evidence validation → risk classification → dependency correlation. Agent outputs are structured and audit-safe."],
    "generate-fix":["Generate remediation proposal","A proposed patch requires repository evidence, sandbox validation, and approval. No production file will be modified."],
    "run-sandbox":["Create isolated sandbox run","A sandbox run uses an isolated repository snapshot. Production deployment is not part of this action."],
    "create-migration":["Create migration task","Migration tasks include prerequisites, compatibility checks, validation, approval, and rollback."],
    "request-approval":["Request human approval","Approval will be recorded against the remediation proposal and its evidence."],
    "apply-fix":["Apply approved fix","Production changes require an approved proposal, successful sandbox verification, and configured deployment controls."],
    "open-remediation":["Remediation review","Review original configuration, proposed diff, sandbox test results, compatibility status, and rollback plan before approval."],
    "approve-policy":["Request policy approval","High-impact firewall policy changes require authorized reviewer approval before deployment."],
    "deploy-policy":["Deploy approved policy","Only approved policies can be deployed. The active policy remains unchanged in this interface."],
    "rollback-policy":["Rollback policy","A policy rollback must reference a previous approved version and be auditable."],
    "save-policy":["Policy draft saved","Draft policy changes are reviewable; this interface does not silently activate production policy."],
    "start-investigation":["Investigation queued","Structured evidence and approved cryptographic knowledge are required for agent conclusions."],
    "recalc-graph":["Blast radius recalculation","Use current graph evidence to recompute affected services. No unstated relationships will be inferred."],
    "compare-scans":["Crypto inventory comparison","Select two completed snapshots to compare additions, removals, risks, and exception changes."],
    "record-evaluation":["Record evaluation run","Enter a labeled dataset and measured metrics; results should not be treated as production assurance."],
    "request-data-access":["Secure data access request","Role-based approval and KMS-mediated decryption are required. No key material is shown."],
    "connect-github":["Connect GitHub Enterprise","Integration credentials must be configured server-side using an approved secret manager."],
    "connect-gitlab":["Connect GitLab","Integration credentials must be configured server-side using an approved secret manager."],
    "toggle-filters":["Filter findings","Use the search and filter controls to narrow findings by severity, status, and classification."]
  };
  const item=copy[name];if(item)modal(item[0],item[1]);
}

document.getElementById("primary-nav").addEventListener("click",e=>{const item=e.target.closest("[data-page]");if(item)setPage(item.dataset.page);});
page.addEventListener("click",e=>{
  const buttonEl=e.target.closest("[data-action]");
  if(buttonEl){action(buttonEl.dataset.action);return;}
  const row=e.target.closest("[data-finding]");
  if(row){findingDetail(findings.find(f=>f.id===row.dataset.finding));return;}
});
document.getElementById("modal-content").addEventListener("click",e=>{const buttonEl=e.target.closest("[data-action]");if(buttonEl)action(buttonEl.dataset.action);});
document.querySelector(".modal-close").addEventListener("click",e=>{e.preventDefault();document.getElementById("action-modal").close();});
document.getElementById("menu-toggle").addEventListener("click",()=>document.getElementById("sidebar").classList.toggle("open"));
document.getElementById("help-button").addEventListener("click",()=>modal("PQC-Migrate help","Evidence-led cryptographic migration assessment, policy enforcement, and controlled remediation. AI outputs are advisory; validated evidence and approved policy remain authoritative."));
document.getElementById("notification-button").addEventListener("click",()=>modal("Notifications","Notifications are empty until live scan, approval, and event data sources are configured."));
document.getElementById("profile-button").addEventListener("click",()=>modal("Local demo session","This browser demo has no real login or server-side authorization.",button("Sign out of demo","logout","quiet")));
async function checkApi() {
  try { const result=await request("/health");apiStatus.textContent=result.status==="ok"?"Connected":"Unavailable"; }
  catch { apiStatus.textContent="Offline"; }
}
function renderInitial() {
  setWorkspaceIdentity();
  const session=readLocal(DEMO_SESSION_KEY,null);
  if(!session){renderLanding();bindPageEvents();return;}
  if(session.role==="administrator"&&!readLocal(ORG_PROFILE_KEY,null)){renderOrganizationSetup();bindPageEvents();return;}
  document.body.classList.remove("public-view");navRender();renderPage("Dashboard");
}
renderInitial();checkApi();
const eventProtocol=location.protocol==="https:"?"wss":"ws";
try {
  const ws=new WebSocket(`${eventProtocol}://${location.host}/ws/events`);
  ws.onmessage=event=>{try{const data=JSON.parse(event.data);if(data.type==="scan_status")apiStatus.textContent="Connected · scan active";}catch{}};
  ws.onerror=()=>{};
} catch {}
