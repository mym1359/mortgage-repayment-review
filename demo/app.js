"use strict";

const { evaluate, snapshots } = mortgageReview;
const element = id => document.getElementById(id);
const date = value => new Intl.DateTimeFormat("en-US", {
  month: "short", day: "numeric", year: "numeric", timeZone: "UTC",
}).format(new Date(value + "T00:00:00Z"));
const money = cents => new Intl.NumberFormat("en-US", {
  style: "currency", currency: "USD",
}).format(cents / 100);
const dateTime = new Intl.DateTimeFormat("en-US", { dateStyle: "medium", timeStyle: "short" });
const form = element("decision-form");
const outcome = element("outcome");
const notes = element("notes");
const status = element("save-status");
const storageKey = "acs-demo:ACS-001:decisions:v1";
const memory = new Map();

function setText(id, value) {
  element(id).textContent = value;
}

function sourceLink(id, target) {
  const link = element(id);
  link.hidden = !target;
  if (target) link.href = "#" + target;
  else link.removeAttribute("href");
}

function timelineContent(entry) {
  if (entry.type === "agreement") {
    return [
      entry.version === 1 ? "Original agreement signed" : "Modified agreement signed",
      "Effective " + date(entry.effective) + " · " + money(entry.installment) + " monthly installment",
    ];
  }
  if (entry.type === "payment") {
    return [
      money(entry.amount) + " payment posted",
      "Applied to the " + date(entry.due) + " installment under " + entry.agreementId,
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

function getHistory(asOf) {
  if (memory.has(asOf)) return memory.get(asOf);
  try {
    const records = JSON.parse(localStorage.getItem(storageKey + ":" + asOf));
    return Array.isArray(records) ? records : [];
  } catch {
    return [];
  }
}

function renderHistory(asOf) {
  const history = getHistory(asOf);
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
    return item;
  }).reverse());
}

function selectedDate() {
  return snapshots[document.querySelector('input[name="snapshot"]:checked').value];
}

function render() {
  const asOf = selectedDate();
  const { agreement, lastPayment, reversal, reversedPayment, evidence, rule } = evaluate(asOf);
  setText("agreement-value", "Version " + agreement.version);
  setText("agreement-detail", "Effective " + date(agreement.effective) + " · " + money(agreement.installment) + " monthly");
  setText("payment-value", date(lastPayment.due));
  setText("payment-detail", money(lastPayment.amount) + " · Posted " + date(lastPayment.date));
  setText("referral-value", reversal ? "Human review required" : "No reversal referral");
  setText("referral-detail", reversal
    ? "The " + date(reversedPayment.due) + " installment was reversed on " + date(reversal.date) + "."
    : "The ledger shows no reversal through this review date.");
  element("referral-card").classList.toggle("attention", Boolean(reversal));
  setText("rule-version", "Rule " + rule);
  setText("evidence-caption", "Recorded through " + date(asOf) + " · Newest first");
  renderEvidence(evidence);
  sourceLink("agreement-source", agreement.id);
  sourceLink("payment-source", lastPayment.id);
  sourceLink("referral-source", reversal?.id);
  renderHistory(asOf);
  status.textContent = "";
}

const drafts = new Map();
let activeDate = selectedDate();

for (const toggle of document.querySelectorAll('input[name="snapshot"]')) {
  toggle.addEventListener("change", () => {
    drafts.set(activeDate, { outcome: outcome.value, notes: notes.value });
    activeDate = selectedDate();
    outcome.value = drafts.get(activeDate)?.outcome ?? "";
    notes.value = drafts.get(activeDate)?.notes ?? "";
    notes.setCustomValidity("");
    render();
  });
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
  const asOf = selectedDate();
  const records = [...getHistory(asOf), {
    decision: outcome.selectedOptions[0].textContent,
    notes: note,
    savedAt: new Date().toISOString(),
    rule: evaluate(asOf).rule,
  }];
  try {
    localStorage.setItem(storageKey + ":" + asOf, JSON.stringify(records));
    memory.delete(asOf);
    status.textContent = "Decision saved in this browser.";
  } catch {
    memory.set(asOf, records);
    status.textContent = "Decision saved for this tab only. Browser storage is unavailable.";
  }
  form.reset();
  renderHistory(asOf);
});

render();
