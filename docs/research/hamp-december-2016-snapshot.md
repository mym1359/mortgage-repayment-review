# بررسی نسخهٔ دسامبر ۲۰۱۶ هامپ | HAMP December 2016 snapshot audit

## نتیجه | Result

نسخهٔ دسامبر ۲۰۱۶ فایل اصلاحات وام را از بایگانی وب بازیابی و هر ۶٬۸۴۳٬۶۲۹ ردیف آن را بررسی کردیم. در ۱۱٬۶۴۵ اصلاح از گروه اول، تاریخ ثبت این نسخه در بایگانی پیش از برش ماه ششم بود. در ۹٬۸۲۰ مورد از این اصلاحات، نسخه وضعیت فعال، تاریخ سررسید آخرین قسط کامل و تاریخ پردازش گزارش ماهانه را نشان می‌داد. همهٔ این موارد به گروه سال ۲۰۱۶ تعلق داشتند. این شواهد نشان می‌دهد این نسخه از مقادیر پیش از برش وجود داشته است. وضعیت دقیق پرونده و گزارش مربوط به خودِ ماه ششم در پایان آن ماه به شواهد بیشتری نیاز دارد.

We recovered the December 2016 loan-modification release and scanned all 6,843,629 rows. For 11,645 Tier 1 modifications, the archive capture preceded the month-six cutoff. Of these, 9,820 had an active state, a last full installment due date, and an official monthly report processing date in the capture. All were in the 2016 cohort. This establishes that this version of those values existed before the cutoff. Establishing state and activity for month six at its close requires additional evidence.

## منشأ و ساختار | Provenance and structure

| مشخصه / Item | مقدار / Value |
|---|---|
| زمان ثبت در بایگانی / Archive capture UTC | 2016-12-16T03:02:03Z |
| نام فایل عضو / CSV member | `HMP_Public_User_Mod_Data_All_20161117.csv` |
| حجم ZIP بر حسب بایت / ZIP bytes | 858,396,013 |
| چکیدهٔ محتوا در نمایهٔ بایگانی / Archive payload SHA-1, Base32 | `S7YAOKBAH7R3A4XTVEZ4URDF7ER6LXDE` |
| اثرانگشت ZIP / ZIP SHA-256 | `e4439053801776a4404c3b9b32e1306c8e08aef2eaf191f96c218c67ddf2a293` |
| تعداد ردیف‌های دارای تاریخ پردازش / Rows with a processing date | 1,764,243 |
| بازهٔ تاریخ‌های پردازش مشاهده‌شده / Observed processing date range | 2009-11-02 – 2016-11-10 |

محتوای پاسخ بایگانی‌شده از یک بازهٔ بایتی در فایل WARC پروژهٔ بایگانی پایان دورهٔ ریاست‌جمهوری بازیابی شد. چکیدهٔ ZIP با نمایهٔ بایگانی و تعداد ردیف‌های خوانده‌شده با فرادادهٔ خود آرشیو مطابقت داشت. زمان ثبت در بایگانی، شاهد محافظه‌کارانهٔ وجود نسخه است. `DD493` تاریخ پردازش آخرین گزارش را در همان نسخه نشان می‌دهد و فقط دقت روزانه دارد. فایل ستون صریح ماه فعالیت ندارد که این پردازش را به گزارش ماه ششم وصل کند. بیشترین تاریخ پردازش، ۱۰ نوامبر ۲۰۱۶، پیش از ماه ثبت در بایگانی است.

The original response was recovered from one byte range in an End of Term WARC. The ZIP digest matched the archive index and the parsed row count matched the ZIP metadata. The capture time is conservative evidence that the release existed. `DD493` gives the date, at day precision, of the latest monthly report represented in the release. The CSV lacks an explicit activity-period column to link that processing date to the month-six report. The maximum processing date, November 10, 2016, precedes the capture month.

[نسخهٔ بایگانی‌شده / Captured release](https://web.archive.org/web/20161216030203id_/http://mhadatafile.treasury.gov/Prod/reports/HMP_Public_User_Mod_Data_All.zip) · [مجموعهٔ بایگانی ۲۰۱۶ / End of Term 2016 dataset](https://eotarchive.s3.amazonaws.com/crawl-data/EOT-2016/index.html) · [تعریف تاریخ پردازش / Processing date definition](https://home.treasury.gov/system/files/136/MHA%20Data%20File%20Handbook%20Data%20Dictionary%2011-4-2011.pdf)

## تطبیق با گروه اول هامپ | Matching to Tier 1 HAMP

جامعهٔ مرجع، اصلاحات گروه اول در فایل مارس ۲۰۲۳ است. از نسخهٔ ۲۰۱۶ فقط رکوردهای `Official Modification` را با هر دو شناسهٔ وام و اصلاح به مرجع وصل کردیم. ۱٬۴۵۰٬۶۷۵ اصلاح تطبیق یافتند. تاریخ اثر در ۷۰۳ مورد متفاوت بود. در کلیدهای تطبیق‌یافته رکورد رسمی تکراری یا متعارض دیده نشد. با کنار گذاشتن تاریخ‌های اثر متفاوت، ۱٬۴۳۸٬۳۲۷ مورد نسخه‌ای داشتند که در زمان برش یا پس از آن ثبت شده بود. از ۱۱٬۶۴۵ مورد ثبت‌شده پیش از برش، ۲٬۸۷۶ مورد در خود ماه ششم ثبت شده بودند.

The March 2023 file defines the retrospective Tier 1 reference cohort. We matched only `Official Modification` rows in the 2016 release on both loan and modification ID. We matched 1,450,675 modifications, and 703 had different effective dates. The matched official records contained no duplicate or conflicting keys. After removing effective-date disagreements, 1,438,327 cases had a release captured at or after the cutoff. The 11,645 earlier cases included 2,876 whose capture occurred during month six itself.

| بخش پیشنهادی / Proposed partition | سال اثر / Effective years | نسخه ثبت‌شده پیش از برش / Capture before cutoff |
|---|---|---:|
| آموزش / Training | 2009–2012 | 0 |
| اعتبارسنجی / Validation | 2013 | 0 |
| فاصله / Gap | 2014 | 0 |
| آزمون / Test | 2015–2017 | 11,645 |

بنابراین این فایل برای یک زیرمجموعه از دورهٔ آزمون شاهدی دربارهٔ مقادیر قابل مشاهده پیش از برش فراهم می‌کند. برای اجرای پروتکل ارزیابی، نسخه‌های معتبر پیش از برش در دوره‌های آموزش و اعتبارسنجی، و شواهد زمان‌دار کافی برای وضعیت و گزارش در ماه ششم، همچنان لازم‌اند.

This release provides evidence of pre-cutoff values for a subset of the proposed test period. Executing the evaluation protocol still requires substantiated pre-cutoff releases for training and validation and dated evidence of month-six state and reporting.

## بازتولید | Reproduction

آرشیو تکمیلی مارس ۲۰۲۳ را طبق راهنمای بازسازی تاریخی مرحله‌بندی کنید. از ریشهٔ پروژه، این بازهٔ فشرده را در پوشه‌ای بیرون از مخزن دریافت کنید. اسکریپت زمان ثبت، نشانی پاسخ بایگانی‌شده و چکیدهٔ ZIP را بررسی می‌کند. مسیر محیط پایتون باید وابستگی‌های مرحلهٔ بازسازی، یعنی DuckDB و PyArrow، را داشته باشد.

Stage the March 2023 archive using the historical reconstruction instructions. From the project root, download the compressed byte range to scratch space outside the repository. The script checks the capture time, archived response URL, and ZIP digest. Use the reconstruction Python environment with DuckDB and PyArrow installed.

```bash
scratch=../work/mortgage-source/availability/recovery
mkdir -p "$scratch"
warc='https://eotarchive.s3.amazonaws.com/crawl-data/EOT-2016/segments/LOC-000/warc/LOC-QUARTERLY-006-20161216025938404-06679-06686-wbgrp-crawl202_LOC-QUARTERLY-006-20161216030211652-06681-29402~wbgrp-crawl202.us.archive.org~8443.warc.gz'
curl -fLSs --range 648023793-1506627522 --max-filesize 858603730 \
  -o "$scratch/candidate.warc.gz" "$warc"
../work/mortgage-source/history/venv/bin/python research/hamp_2016_snapshot.py \
  --warc "$scratch/candidate.warc.gz" --work-dir "$scratch" \
  --latest-db ../work/mortgage-source/history/compact-latest.duckdb
```

[خروجی تجمیعی / Aggregate audit](hamp-december-2016-snapshot.json) · [راهنمای مرحله‌بندی / Staging instructions](hamp-historical-reconstruction.md)
