"use strict";

const mortgageReview = (() => {
  // All amounts are integer cents, and dates are date-only ISO strings.
  const agreements = [
    { id: "AGR-01", version: 1, signed: "2025-03-01", effective: "2025-04-01", installment: 140000 },
    { id: "AGR-02", version: 2, signed: "2025-04-24", effective: "2025-05-01", installment: 125000 },
  ];
  const events = [
    { id: "PAY-01", type: "payment", date: "2025-05-03", due: "2025-05-01", agreementId: "AGR-02", amount: 125000 },
    { id: "PAY-02", type: "payment", date: "2025-06-05", due: "2025-06-01", agreementId: "AGR-02", amount: 125000 },
    { id: "REV-01", type: "reversal", date: "2025-06-12", paymentId: "PAY-02", amount: 125000 },
  ];
  const snapshots = { before: "2025-06-11", after: "2025-06-13", resolution: "2025-06-17" };
  const cases = {
    "ACS-001": {
      title: "Payment reversal review",
      rule: "REV-1 v1.0",
      description: "Compare the repayment record before and after a posted payment was reversed.",
      phases: { before: "Before reversal", after: "After reversal" },
      agreements,
      events,
    },
    "ACS-002": {
      title: "Agreement conflict review",
      rule: "AGR-1 v1.1",
      description: "Review two competing signed modifications and confirm which applies when supporting evidence arrives.",
      phases: { before: "Before conflict", after: "After conflict" },
      agreements: [
        { id: "AGR-03", version: 1, signed: "2025-03-11", effective: "2025-04-01", installment: 155000 },
        { id: "AGR-04", version: 2, signed: "2025-05-22", effective: "2025-06-01", installment: 135000 },
        { id: "AGR-05", version: 3, signed: "2025-06-12", effective: "2025-06-01", installment: 145000 },
      ],
      confirmation: { id: "DOC-01", type: "confirmation", date: "2025-06-16",
        agreementId: "AGR-04", otherAgreementId: "AGR-05" },
      events: [
        { id: "PAY-03", type: "payment", date: "2025-05-05", due: "2025-05-01", agreementId: "AGR-03", amount: 155000 },
        { id: "PAY-04", type: "payment", date: "2025-06-05", due: "2025-06-01", agreementId: "AGR-04", amount: 135000 },
      ],
    },
  };
  const byLatestDate = (a, b) => b.date.localeCompare(a.date);

  function agreementAt(visibleAgreements, due, resolution) {
    const eligible = visibleAgreements
      .filter(agreement => agreement.effective <= due)
      .sort((a, b) => b.effective.localeCompare(a.effective) || b.version - a.version);
    const latest = eligible[0];
    if (!latest) return { agreement: undefined, conflict: [] };
    const candidates = eligible.filter(agreement => agreement.effective === latest.effective);
    const conflict = candidates.some(agreement => agreement.installment !== latest.installment)
      ? candidates
      : [];
    if (!conflict.length) return { agreement: latest, conflict };
    const confirmed = conflict.find(agreement => agreement.id === resolution?.agreementId);
    return { agreement: confirmed, conflict: confirmed ? [] : conflict };
  }

  function evaluate(asOf, caseId = "ACS-001", decision) {
    const selected = cases[caseId];
    const visibleAgreements = selected.agreements.filter(agreement => agreement.signed <= asOf);
    const visibleEvents = selected.events.filter(event => event.date <= asOf);
    const unresolved = agreementAt(visibleAgreements, asOf);
    const confirmation = selected.confirmation?.date <= asOf ? selected.confirmation : undefined;
    const resolutionEvidence = confirmation && [confirmation.agreementId, confirmation.otherAgreementId]
      .every(id => unresolved.conflict.some(agreement => agreement.id === id))
      ? confirmation
      : undefined;
    const resolution = resolutionEvidence && decision?.evidenceId === resolutionEvidence.id
      && decision.agreementId === resolutionEvidence.agreementId ? resolutionEvidence : undefined;
    const { agreement, conflict } = resolution
      ? agreementAt(visibleAgreements, asOf, resolution)
      : unresolved;
    const reversals = visibleEvents.filter(event => event.type === "reversal");
    const lastPayment = visibleEvents
      .filter(event => {
        if (event.type !== "payment" || event.due > asOf) return false;
        const { agreement } = agreementAt(visibleAgreements, event.due, resolution);
        const reversed = reversals
          .filter(reversal => reversal.paymentId === event.id)
          .reduce((total, reversal) => total + reversal.amount, 0);
        return agreement?.id === event.agreementId && event.amount - reversed >= agreement.installment;
      })
      .sort((a, b) => b.due.localeCompare(a.due) || byLatestDate(a, b))[0];
    const reversal = reversals.sort(byLatestDate)[0];
    return {
      agreement,
      conflict,
      resolutionEvidence,
      resolution,
      lastPayment,
      reversal,
      reversedPayment: visibleEvents.find(event => event.id === reversal?.paymentId),
      evidence: [
        ...visibleAgreements.map(agreement => ({ ...agreement, type: "agreement", date: agreement.signed })),
        ...visibleEvents,
        ...(confirmation ? [confirmation] : []),
      ].sort(byLatestDate),
      rule: selected.rule,
    };
  }

  return { cases, evaluate, snapshots };
})();

if (typeof module !== "undefined") module.exports = mortgageReview;
