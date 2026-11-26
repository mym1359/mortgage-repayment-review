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
  const snapshots = { before: "2025-06-11", after: "2025-06-13" };
  const rule = "REV-1 v1.0";
  const byLatestDate = (a, b) => b.date.localeCompare(a.date);

  function agreementAt(asOf, due = asOf) {
    return agreements
      .filter(agreement => agreement.signed <= asOf && agreement.effective <= due)
      .sort((a, b) => b.effective.localeCompare(a.effective) || b.version - a.version)[0];
  }

  function evaluate(asOf) {
    const visibleAgreements = agreements.filter(agreement => agreement.signed <= asOf);
    const visibleEvents = events.filter(event => event.date <= asOf);
    const reversals = visibleEvents.filter(event => event.type === "reversal");
    const lastPayment = visibleEvents
      .filter(event => {
        if (event.type !== "payment" || event.due > asOf) return false;
        const agreement = agreementAt(asOf, event.due);
        const reversed = reversals
          .filter(reversal => reversal.paymentId === event.id)
          .reduce((total, reversal) => total + reversal.amount, 0);
        return agreement?.id === event.agreementId && event.amount - reversed >= agreement.installment;
      })
      .sort((a, b) => b.due.localeCompare(a.due) || byLatestDate(a, b))[0];
    const reversal = reversals.sort(byLatestDate)[0];
    return {
      agreement: agreementAt(asOf),
      lastPayment,
      reversal,
      reversedPayment: visibleEvents.find(event => event.id === reversal?.paymentId),
      evidence: [
        ...visibleAgreements.map(agreement => ({ ...agreement, type: "agreement", date: agreement.signed })),
        ...visibleEvents,
      ].sort(byLatestDate),
      rule,
    };
  }

  return { evaluate, snapshots };
})();

if (typeof module !== "undefined") module.exports = mortgageReview;
