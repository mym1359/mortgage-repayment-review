# بازبینی بازپرداخت وام مسکن آمریکا | U.S. mortgage repayment review

این پروژه پژوهش بازتولیدپذیر دربارهٔ سابقهٔ بازپرداخت پس از اصلاح وام مسکن را با داده‌های عمومی برنامهٔ هامپ خزانه‌داری آمریکا ثبت می‌کند. واحد تحلیل و محدودیت هر مرحله در گزارش آن آمده است.

Reproducible research on U.S. mortgage repayment after loan modification, using Treasury HAMP data to audit data quality and reconstruct historical delinquency rates. Each stage report states its unit of analysis and limitations.

## مراحل پژوهش | Research stages

- مرحلهٔ صفر، آزمایش نرخ‌های گروه‌های سالانه با دادهٔ تجمیعی. Phase zero benchmarks annual-cohort rates with published aggregates. [روش و دستور اجرا / Method and run instructions](research/phase_zero/README.md)
- بررسی منشأ و کیفیت آرشیو تکمیلی. The supplemental archive audit verifies provenance, coverage, and record quality. [گزارش کیفیت / Data quality report](docs/research/hamp-data-quality.md)
- بازسازی نرخ‌های تاریخی ماه‌های ۶ و ۱۲ با آرشیوهای بازیابی‌شده. The historical reconstruction compares month-six and month-twelve estimates with Treasury's table. [گزارش بازسازی / Reconstruction report](docs/research/hamp-historical-reconstruction.md)
- حسابرسی دسترسی زمانی داده‌ها در ماه ششم و پروتکل ارزیابی مدل. The month-six availability audit documents evidence gaps and the proposed evaluation protocol. [پروتکل و نتایج / Protocol and results](docs/research/hamp-asof-protocol.md)
- کنترل‌های ورود به ارزیابی مدل و بررسی منابع زمان پردازش. Evaluation checks and a review of processing-time sources. [آمادگی داده / Evaluation readiness](docs/research/hamp-evaluation-readiness.md)
- بازیابی نسخهٔ دسامبر ۲۰۱۶ هامپ و بررسی پوشش آن پیش از برش ماه ششم. Recovery and cutoff audit of the December 2016 release. [گزارش نسخهٔ ۲۰۱۶ / 2016 snapshot audit](docs/research/hamp-december-2016-snapshot.md)

کد و گزارش‌های پژوهشی با کمک هوش مصنوعی تهیه شده‌اند. فایل‌های ورودی در سطح وام بیرون از مخزن نگهداری می‌شوند. جزئیات بازتولید و پیوندهای منابع رسمی در گزارش هر مرحله آمده‌اند.

The research code and reports were prepared with AI assistance. Loan-level source files are kept outside the repository. Each stage report provides reproduction instructions and direct source links.
