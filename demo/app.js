"use strict";

const { cases, evaluate, snapshots } = mortgageReview;
const element = id => document.getElementById(id);
const date = value => new Intl.DateTimeFormat("en-US", {
  month: "short", day: "numeric", year: "numeric", timeZone: "UTC",
}).format(new Date(value + "T00:00:00Z"));
const money = cents => new Intl.NumberFormat("en-US", {
  style: "currency", currency: "USD",
}).format(cents / 100);
const dateTime = new Intl.DateTimeFormat("en-US", { dateStyle: "medium", timeStyle: "short" });
const picker = element("case-picker");
const form = element("decision-form");
const outcome = element("outcome");
const notes = element("notes");
const resolveOutcome = element("resolve-outcome");
const resolutionPhase = element("resolution-phase");
const resolutionDate = resolutionPhase.querySelector("input");
const status = element("save-status");
const memory = new Map();

function setText(id, value) {
  element(id).textContent = value;
}

function sourceLink(id, target, label) {
  const link = element(id);
  link.hidden = !target;
  if (label) link.textContent = label;
  if (target) link.href = "#" + target;
  else link.removeAttribute("href");
}

function timelineContent(entry) {
  if (entry.type === "agreement") {
    return [
      entry.version === 1 ? "Original agreement signed" : "Modified agreement v" + entry.version + " signed",
      "Effective " + date(entry.effective) + " · " + money(entry.installment) + " monthly installment",
    ];
  }
  if (entry.type === "payment") {
    return [
      money(entry.amount) + " payment posted",
      "Applied to the " + date(entry.due) + " installment under " + entry.agreementId,
    ];
  }
  if (entry.type === "confirmation") {
    return [
      "Signed agreement confirmation received",
      "Confirms " + entry.agreementId + " as the controlling modification and withdraws " + entry.otherAgreementId,
    ];
  }
  return [
    money(entry.amount) + " payment reversed",
    "Reversed posted payment " + entry.paymentId,
  ];
}

function renderEvidence(entries) {
  const items = entries.map(entry => {
    const item = document.createElement("li");
    item.id = entry.id;
    item.tabIndex = -1;
    item.dataset.type = entry.type;
    const meta = document.createElement("div");
    meta.className = "entry-meta";
    const time = document.createElement("time");
    time.dateTime = entry.date;
    time.textContent = date(entry.date);
    const code = document.createElement("span");
    code.textContent = entry.id;
    meta.append(time, code);
    const [title, description] = timelineContent(entry);
    const heading = document.createElement("h3");
    heading.textContent = title;
    const detail = document.createElement("p");
    detail.textContent = description;
    item.append(meta, heading, detail);
    return item;
  });
  element("timeline").replaceChildren(...items);
}

function getHistory(key) {
  if (memory.has(key)) return memory.get(key);
  try {
    const records = JSON.parse(localStorage.getItem(key));
    return Array.isArray(records) ? records : [];
  } catch {
    return [];
  }
}

function renderHistory(history) {
  element("no-decisions").hidden = history.length > 0;
  element("decision-history").replaceChildren(...history.map((record, index) => {
    const item = document.createElement("li");
    const label = document.createElement("strong");
    label.textContent = index ? "Revision " + index + " · " + record.decision : record.decision;
    const timestamp = document.createElement("time");
    timestamp.dateTime = record.savedAt;
    timestamp.textContent = dateTime.format(new Date(record.savedAt)) + " · Rule " + record.rule;
    const note = document.createElement("p");
    note.textContent = record.notes;
    item.append(label, timestamp, note);
    if (record.resolution) {
      const evidenceLink = document.createElement("a");
      evidenceLink.href = "#" + record.resolution.evidenceId;
      evidenceLink.textContent = "Evidence " + record.resolution.evidenceId;
      item.append(evidenceLink);
    }
    return item;
  }).reverse());
}

function selectedDate() {
  return snapshots[document.querySelector('input[name="snapshot"]:checked').value];
}

function decisionKey() {
  return "acs-demo:" + picker.value + ":decisions:v1:" + selectedDate();
}

function renderAgreement(agreement, conflict) {
  if (conflict.length) {
    const [first, second] = conflict;
    setText("agreement-value", "Agreement unresolved");
    setText("agreement-detail", "Effective " + date(first.effective) + " · v" + first.version + " "
      + money(first.installment) + " vs. v" + second.version + " " + money(second.installment));
    sourceLink("agreement-source", first.id, "View version " + first.version);
    sourceLink("agreement-other-source", second.id, "View version " + second.version);
    return;
  }
  setText("agreement-value", "Version " + agreement.version);
  setText("agreement-detail", "Effective " + date(agreement.effective) + " · " + money(agreement.installment) + " monthly");
  sourceLink("agreement-source", agreement.id, "View agreement evidence");
  sourceLink("agreement-other-source", null);
}

function renderReferral({ rule, conflict, reversal, reversedPayment, resolutionEvidence, resolution }) {
  const needsReview = conflict.length > 0 || Boolean(reversal);
  let value = needsReview ? "Human review required" : "No reversal referral";
  let detail = "The ledger shows no reversal through this review date.";
  let source = reversal?.id;
  let label = "View reversal evidence";
  if (resolution) {
    value = "Agreement conflict resolved";
    detail = "Reviewer confirmed " + resolution.agreementId + " using " + resolution.id + ".";
    source = resolution.id;
    label = "View confirmation";
  } else if (picker.value === "ACS-002") {
    if (!needsReview) value = "No agreement conflict";
    detail = "Only one signed version applies to the current installment.";
    if (resolutionEvidence) {
      detail = "A signed confirmation is available. Review it and record a decision to resolve the conflict.";
      source = resolutionEvidence.id;
      label = "View confirmation";
    } else if (conflict.length) {
      detail = "Two signed versions have different monthly amounts and the same effective date. Review both documents to establish which applies.";
      source = conflict[0].id;
      label = "View conflict evidence";
    }
  } else if (reversal) {
    detail = "The " + date(reversedPayment.due) + " installment was reversed on " + date(reversal.date) + ".";
  }
  setText("referral-value", value);
  setText("referral-detail", detail);
  element("referral-card").classList.toggle("attention", needsReview);
  setText("rule-version", "Rule " + rule);
  sourceLink("referral-source", source, label);
}

function reviewResult(history) {
  const resolution = history.findLast(record => record.resolution)?.resolution;
  return evaluate(selectedDate(), picker.value, resolution);
}

function render() {
  const asOf = selectedDate();
  const { title, description, phases } = cases[picker.value];
  const history = getHistory(decisionKey());
  const result = reviewResult(history);
  const { agreement, conflict, lastPayment, evidence, resolutionEvidence } = result;
  resolveOutcome.hidden = resolveOutcome.disabled = !resolutionEvidence;
  if (resolutionEvidence) {
    const confirmed = evidence.find(entry => entry.id === resolutionEvidence.agreementId);
    resolveOutcome.textContent = "Resolve conflict · Confirm version " + confirmed.version;
  }
  setText("case-id", "Case " + picker.value);
  setText("case-title", title);
  setText("case-description", description);
  setText("before-phase", phases.before);
  setText("after-phase", phases.after);
  renderAgreement(agreement, conflict);
  setText("payment-value", date(lastPayment.due));
  setText("payment-detail", money(lastPayment.amount) + " · Posted " + date(lastPayment.date)
    + (conflict.length ? " · June installment pending agreement review" : ""));
  renderReferral(result);
  setText("evidence-caption", "Recorded through " + date(asOf) + " · Newest first");
  renderEvidence(evidence);
  sourceLink("payment-source", lastPayment.id);
  renderHistory(history);
  status.textContent = "";
}

function syncDates() {
  const hasConfirmation = Boolean(cases[picker.value].confirmation);
  if (!hasConfirmation && resolutionDate.checked) {
    document.querySelector('input[name="snapshot"][value="after"]').checked = true;
  }
  resolutionPhase.hidden = resolutionDate.disabled = !hasConfirmation;
}

syncDates();
const drafts = new Map();
let activeKey = decisionKey();

function switchReview() {
  drafts.set(activeKey, { outcome: outcome.value, notes: notes.value });
  syncDates();
  activeKey = decisionKey();
  outcome.value = drafts.get(activeKey)?.outcome ?? "";
  notes.value = drafts.get(activeKey)?.notes ?? "";
  notes.setCustomValidity("");
  render();
}

picker.addEventListener("change", switchReview);
for (const toggle of document.querySelectorAll('input[name="snapshot"]')) {
  toggle.addEventListener("change", switchReview);
}

notes.addEventListener("input", () => notes.setCustomValidity(""));
form.addEventListener("submit", event => {
  event.preventDefault();
  const note = notes.value.trim();
  if (!note) {
    notes.setCustomValidity("Enter the reason for your decision.");
    notes.reportValidity();
    return;
  }
  const key = decisionKey();
  const history = getHistory(key);
  const { resolutionEvidence } = reviewResult(history);
  const resolving = outcome.value === resolveOutcome.value;
  if (resolving && !resolutionEvidence) return;
  const records = [...history, {
    decision: outcome.selectedOptions[0].textContent,
    notes: note,
    savedAt: new Date().toISOString(),
    rule: cases[picker.value].rule,
    ...(resolving ? { resolution: {
      evidenceId: resolutionEvidence.id,
      agreementId: resolutionEvidence.agreementId,
    } } : {}),
  }];
  let message;
  try {
    localStorage.setItem(key, JSON.stringify(records));
    memory.delete(key);
    message = "Decision saved in this browser.";
  } catch {
    memory.set(key, records);
    message = "Decision saved for this tab only. Browser storage is unavailable.";
  }
  form.reset();
  render();
  status.textContent = message;
});

render();
