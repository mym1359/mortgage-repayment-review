# 02. اعتبارسنجی نخستین نمونهٔ مجاز هامپ | Validate the first authorized HAMP sample

Status: needs-info

Blocked by: None

## هدف | What to build

مسیر بررسی نمونه را آماده کنید و پس از دریافت نمونهٔ مجاز، کفایت شواهد زمانی را با استفاده از اعتبارسنج فرادادهٔ موجود بسنجید. نتیجه باید روشن کند که برای گسترش بررسی به گروه‌های کامل چه شواهدی وجود دارد یا کم است.

Prepare the sample review and use the existing metadata validator once an authorized sample is available. The result must show what timing evidence supports expanding to full cohorts and what evidence is missing.

## معیارهای پذیرش | Acceptance criteria

- [ ] شناسه‌های مستعار وام و اصلاح، منشأ و نسخهٔ گزارش، ماه فعالیت، زمان رویداد و اولین زمان دسترسی یا انتشارِ تأییدشده، و ارتباط نسخه‌های اصلاحی با نسخهٔ پیشین ثبت شوند. / Record pseudonymous loan and modification IDs, report provenance and version, activity month, event time, first availability or verified release time, and links between original and corrected versions.
- [ ] برای همان اصلاح، گزارش ماه ششم، وضعیت فعال در برش، و زمان دسترسی به برچسب پیامد با شواهد منبع تطبیق داده شوند. تاریخ سررسید از تاریخ ثبت پرداخت متمایز بماند. / Verify the month-six report, active status at cutoff, and outcome-label availability for the same modification against source evidence. Keep the due date distinct from the payment posting date.
- [x] اعتبارسنج برای ورودی معتبر، ورودی نامعتبر و شاهد ناکافی نتیجه‌ای قابل توضیح بدهد. گزارش تجمیعی، موارد فاقد شاهد یا دیررس و علت تصمیم دربارهٔ کفایت نمونه را نشان دهد. / Produce explainable results for valid input, invalid input, and insufficient evidence. Report aggregate reasons for missing or late evidence and the decision on sample adequacy.
- [ ] پذیرش نمونه به دریافت شواهد معتبر وابسته است. ریزداده، شناسه‌های پرونده و مکاتبات در مخزن منتشر نشوند. / Sample acceptance depends on receiving verified evidence. Keep microdata, case identifiers, and correspondence outside the repository.

[مشخصات پروژه / Project spec](../spec.md)

## Comments

مسیر خصوصی ثبت شواهد و گزارش تجمیعی به اعتبارسنج موجود وصل شد. آزمون‌های ساختگی، پذیرش یک نمونهٔ تک‌موردی، کمبود یا تأخیر شواهد و ورودی نامعتبر را پوشش می‌دهند. پذیرش نمونهٔ واقعی و شروع بررسی پوشش در انتظار دریافت نمونهٔ مجاز و شواهد منبع است.

Private evidence intake and aggregate reporting now use the existing metadata validator. Synthetic tests cover a supported single-case sample, missing or late evidence, and invalid input. Acceptance of a real sample and coverage qualification await an authorized sample and source evidence.

[راهنمای بررسی نمونه / Sample review guide](../../../docs/research/hamp-sample-review.md)
