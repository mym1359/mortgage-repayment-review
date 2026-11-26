# کیفیت داده‌های تکمیلی هامپ | HAMP supplemental data quality

## دامنه و نتیجه | Scope and result

هدف نخست پژوهش، ثبت منشأ داده و راستی‌آزمایی ساختار، پوشش و کیفیت ریزداده بود. همهٔ ردیف‌های آرشیو بررسی شدند. فایل ماهانه فقط ژانویهٔ ۲۰۲۲ تا فوریهٔ ۲۰۲۳ را پوشش می‌دهد، در حالی که صفحهٔ خزانه‌داری بازهٔ ژانویهٔ ۲۰۱۸ تا فوریهٔ ۲۰۲۳ را اعلام می‌کند. این نتیجه اعتبارسنجی جزئی منبع است.

The first research milestone was to document provenance and verify the structure, coverage, and quality of the loan-level data. The audit profiled every row in the archive. Monthly activity covers January 2022 through February 2023, while Treasury's listing gives January 2018 through February 2023. This is a partial source validation.

## منشأ داده | Provenance

| مشخصه / Item | مقدار / Value |
|---|---|
| تاریخ دریافت به وقت تهران / Retrieval date in Tehran | 2026-11-27 |
| حجم ZIP بر حسب بایت / ZIP bytes | 75,367,977 |
| اثرانگشت ZIP / ZIP SHA-256 | `c3057bee9c947c3cc5ba39ad83d07d36f2137cc8b9cafe14592ccc6c0247076c` |
| فایل داده / CSV member | `HMP_Govt_Agency_Perf_Data_20220101_20230201.csv` |
| حجم CSV بازشده بر حسب بایت / Uncompressed CSV bytes | 1,110,749,182 |
| تعداد رکورد اعلام‌شده در فراداده / Row count in archive metadata | 9,872,074 |

راهنمای خزانه‌داری استفادهٔ عمومیِ مسئولانه را هدف انتشار معرفی می‌کند. در راهنما و صفحهٔ بررسی‌شده، مجوز صریح بازنشر فایل شناسایی نشد. آرشیو و ریزدادهٔ استخراج‌شده بیرون از پوشهٔ پروژه نگهداری شدند. پیوند رسمی HTTP آرشیو ۲۰۰۹ تا ۲۰۱۷ در این محیط پاسخ ۴۰۴ داد و بررسی HTTPS آن پاسخ ۵۰۳ داد.

Treasury's guide describes the data as intended for responsible public use. The guide and listing reviewed did not identify an explicit license for redistribution. The archive and extracted microdata were kept outside the project folder. In this environment, the official HTTP link for the 2009–2017 archive returned HTTP 404 and the HTTPS check returned HTTP 503.

[فهرست رسمی / Official listing](https://home.treasury.gov/data/troubled-assets-relief-program/reports/mha-public-file) · [آرشیو بررسی‌شده / Audited archive](https://home.treasury.gov/system/files/256/HMP_Govt_Agency_Perf_Data.zip) · [راهنمای داده / Data guide](https://home.treasury.gov/system/files/136/HAMP%20Performance%20Supplemental%20Data%20File%20User%20Guide%20v1.0.pdf)

## ساختار و کنترل کیفیت | Structure and quality checks

| نوع رکورد / Record type | ردیف / Rows | وام یکتا / Distinct loans | اصلاح یکتا / Distinct modifications |
|---|---:|---:|---:|
| اطلاعات اصلاح / Modification Information | 1,889,234 | 1,830,654 | 1,889,234 |
| اطلاعات پرداخت / Payment Information | 7,982,840 | 596,480 | 596,480 |

مجموع ردیف‌ها با فراداده برابر بود. تعداد ۵۸٬۵۸۰ وام بیش از یک اصلاح داشتند. هیچ شناسهٔ اصلاح به چند وام وصل نبود و همهٔ رکوردهای پرداخت با جفت شناسهٔ وام و اصلاح به رکورد اصلاح متناظر وصل شدند. کلید رسمی شامل نوع رکورد، شناسهٔ اصلاح و دورهٔ فعالیت است. هیچ کلید تکراری، تکرار کامل یا مقدار متعارض روی یک کلید مشاهده نشد. شناسه‌ها کامل بودند. تاریخ اثر در رکوردهای اصلاح و دورهٔ فعالیت در رکوردهای پرداخت کامل و قابل‌خواندن بودند.

The row count matched the archive metadata. There were 58,580 loans with multiple modifications. Each modification ID mapped to one loan, and all payment rows matched a modification record on both IDs. Treasury's key consists of record type, modification ID, and activity period. The audit found zero repeated keys, exact duplicates, or conflicting rows under that key. IDs were complete. Modification effective dates and payment activity periods were present and parseable in their respective record types.

تاریخ سررسید آخرین قسط کامل اعمال‌شده در ۳٬۲۰۹٬۴۸۲ ردیف پرداخت، معادل ۴۰٫۲۰٪، خالی بود. همهٔ این ردیف‌ها وضعیت «گزارش نشده» داشتند. هر ۴٬۷۷۳٬۳۵۸ ردیف با وضعیت «گزارش شده» تاریخ قابل‌خواندن داشت. شمارش، مقادیر خالی را همان‌طور که ثبت شده‌اند حفظ می‌کند.

The last paid installment date was blank on 3,209,482 payment rows (40.20%). Every such row had the status `Not Reported`. All 4,773,358 rows marked `Reported` had a parseable date. The counts preserve missing values as recorded.

## تطبیق با گزارش رسمی | Comparison with the official report

تعداد یکتای اصلاحات دائمی پس از تفکیک بر اساس نوع برنامه و سال اثر، در هر ۱۵ گروه سالانه با ستون «تعداد اصلاحات دائمی آغازشده» در گزارش رسمی برابر بود. بازهٔ تاریخ اثر اصلاحات در کل فایل ژوئیهٔ ۲۰۰۹ تا دسامبر ۲۰۱۷ است.

Distinct permanent-modification counts by program tier and effective year matched the official report's Permanent Modifications Started column for all 15 annual cohorts. The effective dates in the audited file range from July 2009 through December 2017.

| گروه / Tier | سال / Year | تعداد رسمی و مشاهده‌شده / Official and observed count |
|---|---:|---:|
| 1 | 2009 | 63,359 |
| 1 | 2010 | 532,484 |
| 1 | 2011 | 339,311 |
| 1 | 2012 | 195,894 |
| 1 | 2013 | 147,264 |
| 1 | 2014 | 86,433 |
| 1 | 2015 | 58,369 |
| 1 | 2016 | 37,189 |
| 1 | 2017 | 13,134 |
| 2 | 2012 | 1,356 |
| 2 | 2013 | 37,328 |
| 2 | 2014 | 48,915 |
| 2 | 2015 | 58,640 |
| 2 | 2016 | 53,305 |
| 2 | 2017 | 20,225 |

پوشش ماهانه از ۲۰۲۲ شروع می‌شود و فیلد «ماه‌های سپری‌شده از اصلاح» هیچ رکوردی از ماه‌های ۶ تا ۱۲ ندارد. در نتیجه نرخ‌های تاریخی تأخیر ۹۰روزه در ماه‌های ۶ و ۱۲ و جمعیت واجد شرایط در پایان ماه ۶ با این آرشیو بازسازی‌پذیر نیستند. آزمایش مرحلهٔ صفر همچنان با نرخ‌های تجمیعی رسمی قابل بازتولید است.

Monthly coverage starts in 2022, and the months-after-modification field contained no observations for months 6 through 12. This archive therefore cannot reconstruct historical month-six and month-twelve 90-day delinquency rates or identify the eligible population at the end of month six. The phase-zero benchmark remains reproducible using the published aggregate rates.

[گزارش عملکرد مارس ۲۰۲۳ / March 2023 performance summary](https://home.treasury.gov/system/files/256/129_HAMP_Modification_Performance_Summary_Mar2023_v1.0.pdf)

## بازتولید | Reproduction

از ریشهٔ پروژه، فرمان‌های زیر را با پایتون ۳٫۱۲ اجرا کنید. پوشهٔ موقت را بیرون از پروژه انتخاب کنید و برای ورودی بازشده و فایل کاری پایگاه داده فضای دیسک کافی در نظر بگیرید. تاریخ دریافت را برای دانلود تازه به‌روز کنید و اثرانگشت فایل دریافتی را با مقدار بالا مقایسه کنید.

Run the commands from the project root using Python 3.12. Choose a scratch directory outside the project and allow disk space for the extracted input and working database. For a fresh download, update the retrieval date and compare its fingerprint with the value above.

```bash
mkdir -p ../work/hamp-repro
python3 -m venv ../work/hamp-repro/venv
../work/hamp-repro/venv/bin/python -m pip install duckdb==1.5.0
curl -fLSs https://home.treasury.gov/system/files/256/HMP_Govt_Agency_Perf_Data.zip \
  -o ../work/hamp-repro/source.zip
sha256sum ../work/hamp-repro/source.zip
../work/hamp-repro/venv/bin/python research/hamp_quality.py \
  ../work/hamp-repro/source.zip --work-dir ../work/hamp-repro --retrieved-on 2026-11-27 \
  > ../work/hamp-repro/hamp-data-quality.json
```

خروجی JSON شامل تعداد ردیف‌ها به تفکیک ماه و تعداد اصلاحات یکتا به تفکیک سال و نوع برنامه است. برای بازتولید تطبیق، ردیف‌های `Tier 1 HAMP` و `Tier 2 HAMP` را از بخش `modification_cohorts` با جدول بالا مقایسه کنید.

The JSON output contains monthly row counts and distinct modification counts by program type and year. To reproduce the comparison, match the `Tier 1 HAMP` and `Tier 2 HAMP` entries under `modification_cohorts` against the table above.

[خروجی تجمیعی بررسی / Aggregate audit output](hamp-data-quality.json) · [کد بررسی / Audit script](../../research/hamp_quality.py)
