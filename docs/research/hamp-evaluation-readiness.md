# آمادگی داده برای ارزیابی مدل هامپ | HAMP evaluation readiness

## شواهد دسترسی زمانی | Evidence of data availability

فایل تکمیلی عمومی زمان اولین دسترسی به نسخهٔ هر رکورد را نشان نمی‌دهد. در فرهنگ دادهٔ قدیمی اصلاحات رهن اول، فیلد `DD493` تاریخ پردازش آخرین گزارش رسمی ماهانه در نسخهٔ منتشرشده را نشان می‌دهد. این تاریخ می‌تواند برای همان نسخه شاهدی دربارهٔ پردازش باشد. برای بازسازی زمان دسترسی همهٔ ماه‌ها، خود نسخه‌های متوالی و ارتباط هر گزارش با ماه فعالیت لازم‌اند. گزارش عملکرد خزانه‌داری هم به اصلاح داده‌های قبلی اشاره می‌کند.

The supplemental public file lacks a first-availability timestamp for each record version. The older first-lien data dictionary defines `DD493` as the processing date of the latest official monthly report represented in a release. That date can provide processing evidence for that release. Establishing availability across months also requires the releases themselves and a link between each report and its activity month. Treasury's performance report notes that servicer corrections can change previously reported data.

[فرهنگ دادهٔ رهن اول / First-lien data dictionary](https://home.treasury.gov/system/files/136/MHA%20Data%20File%20Handbook%20Data%20Dictionary%2011-4-2011.pdf) · [راهنمای فایل تکمیلی / Supplemental file guide](https://home.treasury.gov/system/files/136/HAMP%20Performance%20Supplemental%20Data%20File%20User%20Guide%20v1.0.pdf) · [گزارش عملکرد / Performance report](https://home.treasury.gov/system/files/initiatives/financial-stability/reports/Documents/4Q17%20MHA%20Report%20Final.pdf)

در جست‌وجوی نشانی‌های اصلی خزانه‌داری برای سال‌های ۲۰۰۹ تا ۲۰۱۸، نمایهٔ بایگانی یک نسخهٔ نامزد از فایل کامل اصلاحات را در ۱۶ دسامبر ۲۰۱۶ نشان داد. درخواست بررسی دسترسی به فایل در این محیط به پایان نرسید و محتوای آن بررسی نشد. نسخه‌های عمومی شناسایی‌شده برای اثبات زمان دسترسی در هر سه بخش زمانی پژوهش کافی نبودند. گزارش‌های عملکرد پیوندخورده نیز نرخ‌های تجمیعی ارائه می‌کنند.

A search of the original Treasury addresses for 2009–2018 identified a candidate capture of the all-modifications file on December 16, 2016. The availability probe timed out, so the payload was not inspected. The identified public releases did not establish availability across all three research partitions. The linked performance reports provide aggregate rates.

[نمایهٔ نسخهٔ نامزد دسامبر ۲۰۱۶ / December 2016 candidate capture](https://web.archive.org/web/20161216030203id_/http://mhadatafile.treasury.gov/Prod/reports/HMP_Public_User_Mod_Data_All.zip) · [فهرست رسمی داده‌ها / Official data listing](https://home.treasury.gov/data/troubled-assets-relief-program/reports/mha-public-file) · [گزارش‌های تجمیعی / Aggregate reports](https://home.treasury.gov/data/troubled-assets-relief-program/reports/making-home-affordable-program-performance-report)

این فایل در مرحلهٔ بعد بازیابی و بررسی شد. The next stage recovered and audited this file. [گزارش نسخهٔ دسامبر ۲۰۱۶ / December 2016 snapshot audit](hamp-december-2016-snapshot.md)

## کنترل‌های ورود به ارزیابی | Evaluation checks

اعتبارسنج دو فایل فراداده را بررسی می‌کند. برش پایان ماه ششم در ورودی برابر با ابتدای ماه هفتم است. این مرز در ویژگی‌ها انحصاری و در پنجرهٔ پیامد فراگیر است. پایان پنجره ابتدای ماه سیزدهم است. زمان‌ها با آفست صریح ثبت و بر اساس لحظهٔ واقعی مقایسه می‌شوند.

The validator checks two metadata files. The end-of-month-six cutoff is encoded as the start of month seven. It is exclusive for features and inclusive for the outcome window. The outcome window ends at the exclusive start of month thirteen. Timestamps require explicit offsets and are compared as instants.

| فایل / File | ستون‌ها / Columns |
|---|---|
| فرادادهٔ گروه پژوهش / Cohort metadata | `loan_id,modification_id,split,cutoff_at,horizon_end_at,disposition,evidence_at,label_available_at` |
| شواهد ویژگی‌ها / Feature evidence | `modification_id,feature,event_at,available_at` |

- **ویژگی‌ها.** برای هر ورودی به‌کاررفته در ساخت ویژگی، یک ردیف شواهد ثبت شود. زمان رویداد و اولین دسترسی به نسخهٔ استفاده‌شده باید پیش از برش باشند. نام‌های پذیرفته‌شده `last_installment_month_gap`، `reporting_pattern` و `payment_history_change` هستند.
- **پیامد.** برای `disqualified` و `paid_off`، زمان شواهد، زمان رویداد داخل پنجره است. برای `censored`، زمان شواهد پایان مشاهده درون پنجره است. برای `no_event`، شواهد باید تا پایان کامل پنجره ادامه داشته باشد. برچسب باید هم‌زمان با شواهد یا پس از آن در دسترس قرار گیرد.
- **تفکیک.** هر اصلاح فقط یک بار در ورودی گروه می‌آید. هر وام فقط در یکی از بخش‌های `train`، `validation` و `test` قرار می‌گیرد. آخرین زمان دسترسی به برچسب هر بخش باید پیش از اولین برش بخش بعدی باشد.

- **Features.** Supply an evidence row for every input used to derive a feature. Event time and first availability of the input version must both precede the cutoff. Accepted feature names are `last_installment_month_gap`, `reporting_pattern`, and `payment_history_change`.
- **Outcome.** For `disqualified` and `paid_off`, evidence time is the event time within the window. For `censored`, it is the end of observation inside the window. For `no_event`, evidence must extend through the full window. The label must be available at or after its evidence time.
- **Partitions.** Each modification appears once. Each loan belongs to one of `train`, `validation`, and `test`. The last label availability time in each partition must precede the next partition's first cutoff.

عبور از این بررسی سازگاری فراداده را تأیید می‌کند. پیش از استفاده از دادهٔ واقعی، اصالت زمان‌ها، کامل بودن شواهد ورودی‌ها، فعال بودن اصلاح در ماه ششم و ثبت درست رویدادها باید در منبع بررسی شوند. کنترل‌ها با دادهٔ ساختگی اجرا شده‌اند. آموزش و آزمون مدل با ریزدادهٔ واقعی در انتظار همین شواهد است.

A passing check verifies metadata consistency. Before real-data use, timestamp provenance, complete input lineage, active status at month six, and outcome ascertainment must be verified against the source. The checks were exercised with synthetic data. Real-data model development remains gated on source evidence.

## اجرا و راستی‌آزمایی | Usage and verification

فرمان اول ۹ آزمون ساختگی را اجرا می‌کند. فرمان دوم فقط شمارش‌ها و نوع مغایرت را به‌شکل JSON برمی‌گرداند. کد خروج `0` به معنی عبور، `1` به معنی نقض یک قاعده و `2` به معنی ورودی نامعتبر است. فایل‌های ورودی واقعی بیرون از مخزن نگهداری شوند.

The first command runs nine synthetic tests. The second reports aggregate counts and violation categories as JSON. Exit code `0` means pass, `1` a policy violation, and `2` invalid input. Keep real input files outside the repository.

```bash
python3 -m unittest discover -s research -p 'test_hamp_evaluation_gate.py'
python3 research/hamp_evaluation_gate.py \
  --cohort ../work/cohort.csv --features ../work/feature-evidence.csv
```

[پروتکل ماه ششم / Month-six protocol](hamp-asof-protocol.md) · [کد اعتبارسنج / Validator](../../research/hamp_evaluation_gate.py) · [آزمون‌های ساختگی / Synthetic tests](../../research/test_hamp_evaluation_gate.py)
