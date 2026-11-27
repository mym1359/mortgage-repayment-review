# 01. آزمون مستقیم فایل دمو برای ACS-002 | Verify ACS-002 from the local file

Status: ready-for-human

Blocked by: None

## هدف | What to build

پذیرش دموی آفلاین را با بازکردن مستقیم فایل محلی در مرورگری که این کار را مجاز می‌داند، راستی‌آزمایی کنید. نتیجهٔ موفق Chromium روی `localhost` مرجع مقایسه است.

Verify offline demo acceptance by opening the local file directly in a browser that permits it. The successful Chromium run over `localhost` provides a comparison.

## معیارهای پذیرش | Acceptance criteria

- [ ] در نمای ۱۳ ژوئن، `DOC-01` در دسترس نیست، توافق حل‌نشده است و قسط مه آخرین قسط تأییدشده است. / On June 13, `DOC-01` is unavailable, the agreement is unresolved, and May is the last confirmed installment.
- [ ] در نمای ۱۷ ژوئن، `DOC-01` در دسترس است و قسط ژوئن تا ثبت تأیید نسخهٔ دوم همراه با یادداشت معلق می‌ماند. پس از ثبت، قسط ۱ ژوئن به مبلغ ۱٬۳۵۰ دلار تأیید می‌شود. / On June 17, `DOC-01` is available and June remains pending until the reviewer saves the version 2 confirmation with a note. Saving confirms the $1,350 June 1 installment.
- [ ] اصلاحیه ثبت شود. پس از بستن مرورگر و بازکردن همان فایل با `file://` در همان پروفایل، تصمیم اولیه و اصلاحیه با ارجاع به سند بازیابی شوند. در نمای ۱۳ ژوئن همچنان مه آخرین قسط تأییدشده باشد. / Save a revision. After closing the browser and reopening the identical `file://` path in the same profile, verify that both entries and their evidence references persist and that May remains the last confirmed installment on June 13.
- [x] نسخهٔ مرورگر، نتیجه و محدودیت‌های آزمون مستقیم ثبت شوند. / Record the browser version, outcome, and any limitations of the direct-file run.

[مشخصات پروژه / Project spec](../spec.md)

## Comments

نمونهٔ اولیهٔ منطق تصمیم در Chromium روی `localhost` نشان داد که بازکردن `DOC-01` قسط ژوئن را معلق می‌گذارد. ثبت تأیید نسخهٔ دوم قسط را در نمای ۱۷ ژوئن تأیید می‌کند و اصلاحیه به سابقهٔ همان نما افزوده می‌شود. نمای ۱۳ ژوئن همچنان قسط مه را نشان می‌دهد. نمونه تصمیم‌ها را در حافظه نگه می‌دارد. آزمون ماندگاری دموی اصلی با `file://` باز است.

The decision prototype in Chromium over `localhost` showed that opening `DOC-01` leaves the June installment pending. Saving the version 2 decision confirms June in the June 17 view, and a revision appends to that view's history. June 13 still shows May. The prototype keeps decisions in memory. Direct-file persistence in the original demo remains open.

[نمونهٔ اولیه / Prototype](https://github.com/mym1359/mortgage-repayment-review/blob/3ecb10ae2d215db66870285020bb41eadf0e4b4c/demo/prototype-acs-002-decision.html)

بازآزمایی در Chromium نسخهٔ `156.0.8078.79` برای مسیر مستقیم دمو خطای `ERR_BLOCKED_BY_ADMINISTRATOR` داد و فایل بارگیری نشد. سه معیار رفتاری اجرای مستقیم باز می‌مانند و به مرورگری با دسترسی مجاز به فایل‌های محلی نیاز دارند.

Retesting the original demo's direct file path in Chromium `156.0.8078.79` returned `ERR_BLOCKED_BY_ADMINISTRATOR` before page load. The three direct-file behavior checks remain open and require a browser that permits local-file navigation.
