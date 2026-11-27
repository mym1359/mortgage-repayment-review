# بازبینی بازپرداخت وام مسکن آمریکا | U.S. mortgage repayment review

این پروژه پژوهش بازتولیدپذیر دربارهٔ سابقهٔ بازپرداخت پس از اصلاح وام مسکن را با داده‌های عمومی برنامهٔ هامپ خزانه‌داری آمریکا ثبت می‌کند. واحد تحلیل و محدودیت هر مرحله در گزارش آن آمده است.

Reproducible research on U.S. mortgage repayment after loan modification, using Treasury HAMP data to audit data quality and reconstruct historical delinquency rates. Each stage report states its unit of analysis and limitations.

## شروع بازبینی | Start here

[نسخه‌های انتشار / Releases](https://github.com/mym1359/mortgage-repayment-review/releases) · [خلاصهٔ پروژه / Project brief](docs/evaluation/project-brief.md) · [پروتکل ارزیابی مستقل / Independent evaluation protocol](docs/evaluation/protocol.md)

## مراحل پژوهش | Research stages

- مرحلهٔ صفر، آزمایش نرخ‌های گروه‌های سالانه با دادهٔ تجمیعی. Phase zero benchmarks annual-cohort rates with published aggregates. [روش و دستور اجرا / Method and run instructions](research/phase_zero/README.md)
- بررسی منشأ و کیفیت آرشیو تکمیلی. The supplemental archive audit verifies provenance, coverage, and record quality. [گزارش کیفیت / Data quality report](docs/research/hamp-data-quality.md)
- بازسازی نرخ‌های تاریخی ماه‌های ۶ و ۱۲ با آرشیوهای بازیابی‌شده. The historical reconstruction compares month-six and month-twelve estimates with Treasury's table. [گزارش بازسازی / Reconstruction report](docs/research/hamp-historical-reconstruction.md)
- حسابرسی دسترسی زمانی داده‌ها در ماه ششم و پروتکل ارزیابی مدل. The month-six availability audit documents evidence gaps and the proposed evaluation protocol. [پروتکل و نتایج / Protocol and results](docs/research/hamp-asof-protocol.md)
- کنترل‌های ورود به ارزیابی مدل و بررسی منابع زمان پردازش. Evaluation checks and a review of processing-time sources. [آمادگی داده / Evaluation readiness](docs/research/hamp-evaluation-readiness.md)
- بازیابی نسخهٔ دسامبر ۲۰۱۶ هامپ و بررسی پوشش آن پیش از برش ماه ششم. Recovery and cutoff audit of the December 2016 release. [گزارش نسخهٔ ۲۰۱۶ / 2016 snapshot audit](docs/research/hamp-december-2016-snapshot.md)
- بازیابی نسخه‌های منطقه‌ای ۲۰۱۲ و ۲۰۱۳ و بررسی تقویم تفکیک داده. Recovery of 2012 and 2013 regional releases and an audit of the evaluation calendar. [گزارش نسخه‌های قدیمی‌تر / Earlier vintages and calendar](docs/research/hamp-earlier-vintages.md)
- پوشش ماهانه پس از اصلاح مرز آموزش و اعتبارسنجی. Monthly coverage after revising the training-to-validation boundary. [گزارش و جدول پوشش / Coverage report and table](docs/research/hamp-monthly-evaluation-coverage.md)
- وضعیت پژوهش و مشخصات نمونهٔ زمان‌دار مورد نیاز. Research status and the remaining source-evidence requirements. [وضعیت و پیش‌نویس استعلام / Status and draft inquiry](docs/research/hamp-research-status.md)

کد و گزارش‌های پژوهشی با کمک هوش مصنوعی تهیه شده‌اند. فایل‌های ورودی در سطح وام بیرون از مخزن نگهداری می‌شوند. جزئیات بازتولید و پیوندهای منابع رسمی در گزارش هر مرحله آمده‌اند.

The research code and reports were prepared with AI assistance. Loan-level source files are kept outside the repository. Each stage report provides reproduction instructions and direct source links.

## دموی بازبینی آفلاین | Offline reviewer demo

مخزن را دانلود کنید و فایل `demo/index.html` را در مرورگر باز کنید. پرونده را از فهرست انتخاب کنید و تاریخ‌های بازبینی آن را مقایسه کنید.

Download the repository and open `demo/index.html` in a browser. Select a case and compare its review dates.

اگر مرورگر سازمانی مسیر مستقیم فایل را مسدود می‌کند، از ریشهٔ مخزن `python -m http.server 8765 --bind 127.0.0.1` را اجرا و `http://127.0.0.1:8765/demo/index.html` را باز کنید. برای بررسی ماندگاری در این روش، نشانی و پروفایل مرورگر را ثابت نگه دارید.

If a managed browser blocks direct file navigation, run `python -m http.server 8765 --bind 127.0.0.1` from the repository root and open `http://127.0.0.1:8765/demo/index.html`. Use the same URL and browser profile to check restoration in this setup.

| پرونده / Case | سناریو / Scenario |
| --- | --- |
| ACS-001 | برگشت پرداخت ژوئن، آخرین قسط تأییدشده را به مه برمی‌گرداند و پرونده را برای بازبینی انسانی علامت می‌زند. / Reversing the June payment makes May the last confirmed installment and flags the case for human review. |
| ACS-002 | دو نسخهٔ امضاشده مبلغ‌های متفاوتی با تاریخ اجرای یکسان دارند. توافق معتبر و قسط ژوئن تا بازبینی کارشناس معلق می‌مانند و قسط مه همچنان تأییدشده است. در نمای ۱۷ ژوئن، سند تکمیلی را باز کنید و گزینهٔ تأیید نسخهٔ دوم را با یادداشت ذخیره کنید تا قسط ژوئن دوباره ارزیابی شود. / Two signed versions specify different amounts with the same effective date. The applicable agreement and June installment remain unresolved pending human review, while May remains confirmed. In the June 17 view, open the confirmation and record the decision to confirm version 2 with a note to reassess June. |

پیوندهای شواهد به ردیف‌های خط زمانی می‌رسند. تصمیم و یادداشت به پرونده و تاریخ انتخاب‌شده تعلق دارند. ذخیرهٔ دوباره، اصلاحیه‌ای در سابقه ثبت می‌کند. تصمیم‌ها در صورت دسترسی به حافظهٔ محلی در همان مرورگر و همان مسیر فایل باقی می‌مانند. آزمون قواعد با دستور `node --test demo/review.test.js` اجرا می‌شود.

Evidence links point to timeline entries. Decisions and notes are tied to the selected case and date. Saving again adds a revision to the history. Decisions persist in the same browser at the same file path when local storage is available. Run the rule checks with `node --test demo/review.test.js`.
