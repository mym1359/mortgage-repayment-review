# پروتکل دسترسی به داده در ماه ششم | Month-six data availability protocol

## نتیجهٔ بررسی | Audit result

آرشیوهای عمومی برای بررسی گذشته‌نگر زمان رویداد مناسب‌اند. طرح دادهٔ عمومی زمان اولین دریافت یا دسترس‌پذیری هر رکورد و تاریخچهٔ اصلاح آن را ندارد. بنابراین در این مرحله امکان تأیید اینکه ویژگی‌های مدل در پایان ماه ششم واقعاً در دسترس بوده‌اند، وجود ندارد.

The public archives support retrospective event-time analysis. Their public schema does not provide a record-level first receipt or availability timestamp or revision history. Feature availability as of the end of month six cannot be independently verified with these inputs.

از ۱٬۴۷۳٬۴۳۷ اصلاح دائمی گروه اول هامپ، ۱٬۰۲۸٬۳۲۱ مورد بر اساس قواعد زیر دارای گزارش قابل استفاده برای تحلیل گذشته‌نگر بودند. در ۲۴۱٬۷۰۹ مورد، تاریخ سررسید آخرین قسط کامل اعمال‌شده پس از تاریخ برش بود. این تاریخ می‌تواند با پرداخت پیش از سررسید سازگار باشد. بدون زمان ثبت پرداخت، شواهد کافی برای ورود آن به ویژگی‌های ماه ششم نداریم.

Of 1,473,437 Tier 1 permanent modifications, 1,028,321 had retrospectively usable reports under the rules below. In 241,709 cases, the last applied full installment's due date was after the cutoff. A later due date can be consistent with an advance payment. Without the posting timestamp, its availability as a month-six feature is unverified.

[راهنمای دادهٔ هامپ / HAMP supplemental data guide](https://home.treasury.gov/system/files/136/HAMP%20Performance%20Supplemental%20Data%20File%20User%20Guide%20v1.0.pdf) · [گزارش‌دهی ماهانه و اصلاح داده‌ها / Monthly reporting and corrections](https://home.treasury.gov/system/files/initiatives/financial-stability/reports/Documents/4Q17%20MHA%20Report%20Final.pdf)

## حسابرسی شواهد موجود | Evidence audit

تاریخ برش، پایان ماه ششم است و ماه اثر اصلاح، ماه اول حساب می‌شود. رکورد پرداخت به کمک شناسهٔ وام، شناسهٔ اصلاح، ماه تقویمی و سن شش‌ماهه وصل شد. دسته‌های جدول به ترتیب بررسی اعمال می‌شوند و هر اصلاح در یک دسته شمرده شده است. خروج تا تاریخ برش از وضعیت و تاریخ خروج گزارش‌شده در نسخهٔ مارس ۲۰۲۳ محاسبه شده است. این طبقه‌بندی برای حسابرسی گذشته‌نگر است.

The cutoff is the end of month six, with the effective month counted as month one. A payment row must match the loan ID, modification ID, calendar month, and recorded age of six. The table applies its categories in order and counts each modification once. The exit check uses the March 2023 snapshot and is retrospective.

| وضعیت / Disposition | تعداد اصلاح / Modifications |
|---|---:|
| خروج ثبت‌شده تا تاریخ برش / Retrospectively recorded exit by cutoff | 76,388 |
| ردیف ماه ششم پیدا نشد / No matching month-six row | 2,104 |
| رکوردهای ماه ششم متعارض / Conflicting month-six reports | 0 |
| گزارش یا تاریخ سررسید قابل استفاده موجود نبود / Missing usable report or installment due date | 124,915 |
| تاریخ سررسید پس از برش / Installment due date after cutoff | 241,709 |
| گزارش قابل استفاده برای تحلیل گذشته‌نگر / Retrospectively usable report | 1,028,321 |

در مقایسهٔ ردیف‌های دارای شناسهٔ وام و اصلاح یکسان، نسخهٔ تاریخی و نسخهٔ مارس ۲۰۲۳ برای ۲۹۵ اصلاح دربارهٔ خروج تا برش ماه ششم نتیجهٔ متفاوتی دادند. این اختلاف برای نسخهٔ ماهانهٔ ژوئیهٔ ۲۰۲۰ در برابر مارس ۲۰۲۳، ۱۰۰ مورد بود. در هر دو مقایسه تاریخ برش از نسخهٔ مارس ۲۰۲۳ محاسبه شد. این تغییرها می‌توانند از اصلاح رکورد یا تحول وضعیت در طول زمان ناشی شوند. آرشیوها زمان ثبت تک‌تک تغییرها را مشخص نمی‌کنند.

Among rows paired on loan and modification ID, the historical and March 2023 snapshots disagreed on exit by the month-six cutoff for 295 modifications. July 2020 versus March 2023 disagreed for 100. Both comparisons fixed the cutoff using the March 2023 effective date. Differences can reflect corrections or later changes. The archives do not establish when each change was recorded.

## طرح ارزیابی مدل | Model evaluation design

| تصمیم / Decision | تعریف / Specification |
|---|---|
| جامعهٔ هدف / Target population | اصلاحات دائمی گروه اول هامپ که در پایان ماه ششم بر اساس اطلاعات در دسترس همان زمان فعال باشند. Tier 1 permanent modifications active at the end of month six based on information available at that time. |
| برش ویژگی‌ها / Feature cutoff | پایان تقویمی ماه ششم. برای هر نسخه از هر ورودی، زمان رویداد و زمان ورود آن به سامانه، با منطقهٔ زمانی معلوم، باید تا پایان برش باشد. End of calendar month six. Each feature version needs an event time and a system arrival time, with known time zones, no later than the cutoff. |
| ویژگی‌های اولیه / Initial features | فاصلهٔ ماه سررسید آخرین قسط کامل اعمال‌شده تا ماه برش، الگوی گزارش‌دهی و تغییر وضعیت پرداخت در ماه‌های ۱ تا ۶، مشروط به احراز دسترسی زمانی. Months between the last applied full installment's due month and the cutoff month, reporting pattern, and changes in payment history in months 1–6, subject to verified availability. |
| داده‌های کنارگذاشته‌شده از ویژگی‌ها / Fields excluded from features | وضعیت نهایی، تاریخ و علت خروجِ نسخه‌های بعدی، دادهٔ پرداخت ماه‌های ۷ به بعد و شناسه‌های وام و اصلاح. شناسه‌ها فقط برای اتصال و تفکیک مجموعه‌ها استفاده می‌شوند. Latest final state, exit date and reason, payments in month 7 onward, and loan or modification IDs. IDs are used for joins and partitioning. |
| پیامد / Outcome | خروج مستند `Disqualified` در ماه‌های ۷ تا ۱۲. تسویه رویداد رقیب است. خروج‌های دیگر و پیگیری ناقص به‌عنوان سانسور ثبت می‌شوند. Documented `Disqualified` exit during months 7–12. Payoff is a competing event. Other exits and incomplete follow-up are recorded as censoring. |
| تفکیک زمانی پیشنهادی / Proposed temporal split | ژوئیهٔ ۲۰۰۹ تا ژوئن ۲۰۱۲ آموزش، نیمهٔ دوم ۲۰۱۲ حذف تقویمی، ۲۰۱۳ اعتبارسنجی، ۲۰۱۴ فاصله و ۲۰۱۵ تا ۲۰۱۷ آزمون. پایان پیگیری و زمان دسترسی به پیامد باید پیش از اولین برش بخش بعد باشد. هر وام فقط در یک بخش قرار می‌گیرد. Train on July 2009–June 2012, hold out the second half of 2012, validate on 2013, reserve 2014 as a gap, and test on 2015–2017. Follow-up and label availability must precede the next partition's first cutoff. Each loan belongs to one partition. |

برای عبور به آموزش مدل، باید از منبع داده نسخه‌های ماهانه یا زمان ثبت و تاریخچهٔ اصلاح رکورد تهیه شود. پیش از آموزش، کنترل خودکار باید استفاده از دادهٔ بعد از برش، ورود یک وام به بیش از یک بخش و تعیین پیامد پیش از کامل شدن دورهٔ پیگیری را تشخیص دهد. برای کنترل آخر، سانسور و رویداد رقیب جدا از پیامد اصلی نگهداری می‌شوند.

Model development requires source-level monthly vintages or arrival timestamps with revision history. Before training, automated checks must detect post-cutoff feature use, a loan appearing in multiple partitions, and outcome assignment before follow-up is complete. The last check preserves censoring and competing events as separate dispositions.

حسابرسی تقویمی بعدی، هم‌پوشانی آموزش و اعتبارسنجی را اندازه‌گیری کرد. The follow-up calendar audit quantified the training-to-validation overlap. [نتایج تقویمی / Calendar results](hamp-earlier-vintages.md) · [پوشش پس از اصلاح مرز / Coverage after revising the boundary](hamp-monthly-evaluation-coverage.md)

## بازتولید | Reproduction

پس از مرحله‌بندی سه آرشیو مطابق گزارش بازسازی تاریخی، فرمان زیر را از ریشهٔ پروژه اجرا کنید. خروجی شامل شمارش سالانه و اختلاف نسخه‌هاست.

After staging the three archives as described in the reconstruction report, run this command from the project root. The output includes yearly counts and cross-snapshot differences.

```bash
scratch=../work/mortgage-source/history
"$scratch/venv/bin/python" research/hamp_asof_audit.py \
  --historical-db "$scratch/compact-old.duckdb" \
  --monthly-db "$scratch/compact-monthly.duckdb" \
  --latest-db "$scratch/compact-latest.duckdb"
```

[گزارش بازسازی و مرحله‌بندی آرشیو / Reconstruction and archive staging](hamp-historical-reconstruction.md) · [خروجی تجمیعی / Aggregate audit output](hamp-asof-audit.json) · [کد حسابرسی / Audit script](../../research/hamp_asof_audit.py)
