# 01. آزمون مستقیم فایل دمو برای ACS-002 | Verify ACS-002 from the local file

Status: ready-for-agent

Blocked by: None

## هدف | What to build

پذیرش دموی آفلاین را با بازکردن مستقیم فایل محلی در مرورگری که این کار را مجاز می‌داند، راستی‌آزمایی کنید. نتیجهٔ موفق Chromium روی `localhost` مرجع مقایسه است.

Verify offline demo acceptance by opening the local file directly in a browser that permits it. The successful Chromium run over `localhost` provides a comparison.

## معیارهای پذیرش | Acceptance criteria

- [ ] در نمای ۱۳ ژوئن، `DOC-01` در دسترس نیست، توافق حل‌نشده است و قسط مه آخرین قسط تأییدشده است. / On June 13, `DOC-01` is unavailable, the agreement is unresolved, and May is the last confirmed installment.
- [ ] در نمای ۱۷ ژوئن، `DOC-01` در دسترس است و قسط ژوئن تا ثبت تأیید نسخهٔ دوم همراه با یادداشت معلق می‌ماند. پس از ثبت، قسط ۱ ژوئن به مبلغ ۱٬۳۵۰ دلار تأیید می‌شود. / On June 17, `DOC-01` is available and June remains pending until the reviewer saves the version 2 confirmation with a note. Saving confirms the $1,350 June 1 installment.
- [ ] اصلاحیه ثبت شود. پس از بستن مرورگر و بازکردن همان فایل با `file://` در همان پروفایل، تصمیم اولیه و اصلاحیه با ارجاع به سند بازیابی شوند. در نمای ۱۳ ژوئن همچنان مه آخرین قسط تأییدشده باشد. / Save a revision. After closing the browser and reopening the identical `file://` path in the same profile, verify that both entries and their evidence references persist and that May remains the last confirmed installment on June 13.
- [ ] نسخهٔ مرورگر، نتیجه و محدودیت‌های آزمون مستقیم ثبت شوند. / Record the browser version, outcome, and any limitations of the direct-file run.

[مشخصات پروژه / Project spec](../spec.md)
