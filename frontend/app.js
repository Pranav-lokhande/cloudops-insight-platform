const $ = (s) => document.querySelector(s);
async function api(path, options={}) {
  const response = await fetch(path, {headers:{"Content-Type":"application/json"}, ...options});
  const data = await response.json().catch(()=>({}));
  if (!response.ok) throw new Error(data.error || `Request failed (${response.status})`);
  return data;
}
function esc(value) {
  return String(value ?? "").replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#039;"}[c]));
}
function renderServices(services) {
  $("#service-count").textContent = services.length;
  if (!services.length) { $("#service-list").innerHTML='<div class="empty">No services yet. Add your first component using the form.</div>'; return; }
  $("#service-list").innerHTML=services.map(s=>`<article class="service-row"><div><h4>${esc(s.name)}</h4><p>${esc(s.description||"No description provided")}<br>${esc(s.environment)} · ${esc(s.created_at)}</p></div><div class="service-meta"><span>${esc(s.category)}</span><small>#${s.id}</small></div></article>`).join("");
}
async function loadServices() {
  try { const data=await api("/api/services"); renderServices(data.services||[]); }
  catch { $("#service-list").innerHTML='<div class="empty">Could not load records. Check API and database containers.</div>'; $("#service-count").textContent="—"; }
}
async function health() {
  try { const d=await api("/api/health"); $("#api-status").textContent=d.status==="healthy"?"Healthy":"Degraded"; $("#api-detail").textContent=d.database==="connected"?"API + database connected":"Database unavailable"; $("#footer-api").textContent="API healthy"; }
  catch { $("#api-status").textContent="Offline"; $("#api-detail").textContent="Backend unavailable"; $("#footer-api").textContent="API unavailable"; }
}
$("#service-form").addEventListener("submit",async e=>{
  e.preventDefault(); const msg=$("#form-message"); const button=e.currentTarget.querySelector("button");
  const body=Object.fromEntries(new FormData(e.currentTarget).entries()); msg.textContent="Saving to MySQL…"; button.disabled=true;
  try { await api("/api/services",{method:"POST",body:JSON.stringify(body)}); msg.textContent="Service saved successfully."; e.currentTarget.reset(); await loadServices(); }
  catch(err) { msg.textContent=err.message; msg.style.color="#c34343"; }
  finally { button.disabled=false; }
});
$("#refresh").addEventListener("click",loadServices);
health(); loadServices();
