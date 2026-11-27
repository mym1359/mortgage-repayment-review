# 03. احراز پوشش داده برای ارزیابی | Qualify evaluation data coverage

Status: ready-for-agent

Blocked by: 02

## هدف | What to build

پس از احراز کفایت نمونه در تسک ۰۲، شواهد زمانی را در گروه‌های ماهانه بررسی کنید و با گزارشی تجمیعی مشخص کنید آیا پوشش برای آموزش، اعتبارسنجی و آزمون کافی است.

After ticket 02 establishes sample adequacy, verify timing evidence across monthly cohorts and report whether coverage supports training, validation, and testing.

## معیارهای پذیرش | Acceptance criteria

- [ ] پوشش و دلایل حذف را به تفکیک ماه اثر و بخش زمانی گزارش کنید. ردیف مفقود، گزارش‌نشده، تکراری یا متعارض جداگانه شمارش شود. / Report coverage and exclusions by effective month and partition, with separate counts for missing, unreported, duplicate, and conflicting rows.
- [ ] خروج `Disqualified`، تسویه، سانسور و پیگیری کامل بدون رخداد را با شواهد زمانی طبقه‌بندی کنید. / Classify `Disqualified`, payoff, censoring, and complete event-free follow-up using timing evidence.
- [ ] هیچ وامی در بیش از یک بخش نباشد و آخرین زمان دسترسی به برچسب هر بخش پیش از اولین برش بخش بعدی باشد. در صورت لزوم، دامنهٔ آموزش بر اساس شواهد تأخیر محدود شود. / Verify that loans stay in one partition and that the latest label availability in each partition precedes the next partition's first cutoff. Narrow the training range if required by the timing evidence.
- [ ] تصمیم دربارهٔ آمادگی داده با شمارش‌های بازتولیدپذیر ثبت شود. بازسازی عمومی ۳۰ سلول و جدول ۱۰۲ گروه ماهانه معیار راستی‌آزمایی مستقل دارد و اختلاف حل‌نشده در گزارش قابل مشاهده می‌ماند. / Document the readiness decision with reproducible counts. Retain the independently verifiable public reconstruction of 30 cells and 102 monthly cohorts and its documented unresolved discrepancy.

[مشخصات پروژه / Project spec](../spec.md)
