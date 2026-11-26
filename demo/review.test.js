"use strict";

const assert = require("node:assert/strict");
const { test } = require("node:test");
const { evaluate, snapshots } = require("./review.js");

test("the signed modification applies only once effective", () => {
  assert.equal(evaluate("2025-04-30").agreement.id, "AGR-01");
  assert.equal(evaluate("2025-05-01").agreement.id, "AGR-02");
});

test("the June installment is confirmed before the ledger shows the reversal", () => {
  const result = evaluate(snapshots.before);
  assert.equal(result.agreement.id, "AGR-02");
  assert.equal(result.lastPayment.id, "PAY-02");
  assert.equal(result.lastPayment.due, "2025-06-01");
  assert.equal(result.lastPayment.date, "2025-06-05");
  assert.equal(result.reversal, undefined);
  assert.ok(!result.evidence.some(entry => entry.id === "REV-01"));
});

test("the reversal takes effect on its recorded date and explains the fallback and referral", () => {
  for (const asOf of ["2025-06-12", snapshots.after]) {
    const result = evaluate(asOf);
    assert.equal(result.agreement.id, "AGR-02");
    assert.equal(result.lastPayment.id, "PAY-01");
    assert.equal(result.lastPayment.due, "2025-05-01");
    assert.equal(result.reversal.id, "REV-01");
    assert.equal(result.reversal.paymentId, result.reversedPayment.id);
    assert.equal(result.reversedPayment.id, "PAY-02");
    assert.equal(result.rule, "REV-1 v1.0");
    assert.deepEqual(result.evidence.map(entry => entry.id), [
      "REV-01", "PAY-02", "PAY-01", "AGR-02", "AGR-01",
    ]);
  }
});

test("the conflict case uses the one visible June agreement before the second is signed", () => {
  const result = evaluate(snapshots.before, "ACS-002");
  assert.equal(result.agreement.id, "AGR-04");
  assert.equal(result.lastPayment.id, "PAY-04");
  assert.deepEqual(result.conflict, []);
  assert.ok(!result.evidence.some(entry => entry.id === "AGR-05"));
});

test("conflicting terms trigger review at signing and retain the last independently confirmed installment", () => {
  for (const asOf of ["2025-06-12", snapshots.after]) {
    const result = evaluate(asOf, "ACS-002");
    assert.equal(result.agreement, undefined);
    assert.deepEqual(result.conflict.map(agreement => agreement.id), ["AGR-05", "AGR-04"]);
    assert.deepEqual(result.conflict.map(agreement => agreement.installment), [145000, 135000]);
    assert.ok(result.conflict.every(agreement => agreement.effective === "2025-06-01"));
    assert.equal(result.lastPayment.id, "PAY-03");
    assert.equal(result.lastPayment.due, "2025-05-01");
    assert.ok(result.evidence.some(entry => entry.id === "PAY-04"));
    assert.equal(result.reversal, undefined);
    assert.equal(result.rule, "AGR-1 v1.0");
  }
});
