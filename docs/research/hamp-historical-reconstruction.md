# بازسازی تاریخی نرخ تأخیر هامپ | Historical HAMP delinquency reconstruction

## نتیجه | Result

آرشیو اصلی سال‌های ۲۰۰۹ تا ۲۰۱۷ و به‌روزرسانی ماهانهٔ ژانویهٔ ۲۰۱۸ تا ژوئیهٔ ۲۰۲۰ از بایگانی وب بازیابی شدند. ترکیب این دو همهٔ ماه‌های تقویمی لازم برای محاسبهٔ ۳۰ نرخ در ۱۵ گروه سالانه را پوشش داد. برآورد ۲۹ نرخ حداکثر ۰٫۲۰ واحد درصد با جدول رسمی مارس ۲۰۲۳ اختلاف داشت. میانگین قدرمطلق اختلاف ۰٫۰۶۷۶ واحد درصد بود. در دقت یک رقم اعشار گزارش، ۱۴ نرخ دقیقاً برابر شدند.

The 2009–2017 archive and January 2018–July 2020 monthly update were recovered from the web archive. Together they covered every calendar month needed for the 30 rates across 15 annual cohorts. Twenty-nine estimates were within 0.20 percentage points of the March 2023 Treasury table. The mean absolute difference was 0.0676 percentage points. Fourteen estimates matched at Treasury's one-decimal display precision.

[گزارش رسمی مارس ۲۰۲۳ / Official March 2023 report](https://home.treasury.gov/system/files/256/129_HAMP_Modification_Performance_Summary_Mar2023_v1.0.pdf)

## منشأ و پوشش | Provenance and coverage

| ورودی / Input | مبنای استفاده / Use | تعداد ردیف‌های پرداخت / Payment rows | فعالیت ماهانهٔ مشاهده‌شده / Observed activity |
|---|---|---:|---|
| آرشیو تاریخی / Historical archive | سوابق پرداخت / Payment history | 85,249,487 | 2009-07 to 2017-12 (102 months) |
| به‌روزرسانی بازیابی‌شده / Recovered update | سوابق پرداخت / Payment history | 25,869,327 | 2018-01 to 2020-07 (31 months) |
| به‌روزرسانی مارس ۲۰۲۳ / March 2023 update | نوع برنامه، تاریخ اثر، وضعیت و تاریخ خروج اصلاح / Modification snapshot | 7,982,840 | 2022-01 to 2023-02 (14 months) |

دو فایل قدیمی در نسخه‌های ۱۶ اکتبر ۲۰۲۰ بایگانی شده بودند. برای دریافت کامل، بازهٔ بایتی هر پاسخ اصلی از فایل WARC استخراج شد و چکیدهٔ محتوا با نمایهٔ بایگانی تطبیق داده شد. کل محتوای هر CSV خوانده شد. اثرانگشت SHA-256، حجم، نام فایل و شمارش رکوردها در خروجی تجمیعی ثبت شده‌اند. آرشیوها و پایگاه‌های کاری در فضای موقت بیرون از پوشهٔ پروژه نگهداری شدند.

Both older files were captured on October 16, 2020. The complete original responses were recovered from their byte ranges in the WARC captures and verified against the archive index payload digests. Every CSV was scanned in full. The aggregate output records SHA-256, byte counts, member names, and record counts. The input archives and working databases were stored in scratch space outside the project.

[فهرست رسمی / Official listing](https://home.treasury.gov/data/troubled-assets-relief-program/reports/mha-public-file) · [آرشیو ۲۰۰۹ تا ۲۰۱۷ / 2009–2017 capture](https://web.archive.org/web/20201016192933id_/http://mhadatafile.treasury.gov/Prod/reports/HMP_Govt_Agency_Perf_Data_20090101_20171201.zip) · [به‌روزرسانی ژوئیهٔ ۲۰۲۰ / July 2020 capture](https://web.archive.org/web/20201016195632id_/http://mhadatafile.treasury.gov/Prod/reports/HMP_Govt_Agency_Perf_Data.zip) · [آرشیو مارس ۲۰۲۳ / March 2023 archive](https://home.treasury.gov/system/files/256/HMP_Govt_Agency_Perf_Data.zip)

## روش | Method

- اطلاعات اصلاح از نسخهٔ مارس ۲۰۲۳ و فعالیت پرداخت از دو فایل قدیمی به هم متصل شدند. اتصال بر اساس شناسهٔ وام، شناسهٔ اصلاح، ماه هدف و سن اصلاح در رکورد پرداخت انجام شد. داده‌ها نشان دادند ماه اثر، ماه اول است. بنابراین ماه ششم و دوازدهم به‌ترتیب پنج و یازده ماه تقویمی پس از ماه اثر هستند.
- رکورد پرداختِ گزارش‌شده زمانی در صورت قرار گرفت که ماه سررسید آخرین قسط کامل اعمال‌شده دست‌کم سه ماه تقویمی پیش از ماه هدف بود. وضعیت خروج به‌دلیل تأخیر تا پایان ماه هدف نیز در صورت و مخرج منظور شد. موارد تسویه یا انصراف تا پایان ماه هدف از مخرج خارج شدند. موارد بدون گزارش پرداخت معتبر و تعارض‌های حل‌نشده نیز از مخرج کنار گذاشته شدند و جداگانه شمرده شدند.
- از ۳٬۳۸۶٬۴۱۲ مشاهدهٔ «اصلاح × افق زمانی»، ۳٬۱۵۷٬۸۲۰ مورد وارد مخرج شدند. ۱۰٬۹۸۴ مورد به‌دلیل تسویه یا انصراف و ۲۱۷٬۶۰۸ مورد به‌دلیل نبود گزارش معتبر از مخرج خارج شدند. در ۷٬۳۰۸ مورد از دستهٔ دوم، هیچ رکورد پرداختی با کلید و ماه هدف پیدا نشد. هیچ کلید پرداخت تکراری یا متعارض در اتصال ماه‌های هدف مشاهده نشد.

- The March 2023 modification snapshot was joined to payment activity in the two older files on loan ID, modification ID, target calendar month, and the recorded modification age. The observed age convention counts the effective month as month one, so months six and twelve are five and eleven calendar months after it.
- Reported activity entered the numerator when the last full installment due month was at least three calendar months before the target month. Disqualification by the end of the target month entered both the numerator and denominator. Payoffs and withdrawals by that cutoff, missing valid reports, and unresolved conflicts were excluded from the denominator and recorded separately.
- Of 3,386,412 modification-horizon observations, 3,157,820 entered the denominator. There were 10,984 payoff or withdrawal exclusions and 217,608 exclusions for missing valid activity. The latter included 7,308 without a payment row on the target key and month. No duplicate or conflicting payment keys were observed among the joined target months.

قاعدهٔ استفاده از اختلاف ماه تقویمی و برش پایان ماه، پیاده‌سازی این پروژه برای مقایسه است. گزارش‌های خزانه‌داری نحوهٔ لحاظ خروج و نبود گزارش را توضیح می‌دهند، اما جزئیات کامل کد محاسبات داخلی در منابع بررسی‌شده در دسترس نبود. استفاده از وضعیت و تاریخ خروج ثبت‌شده در نسخهٔ متأخر برای بازسازی گذشته است. هر ارزیابی مدل آینده‌نگر به تعریف جداگانهٔ زمان دسترسی به داده نیاز دارد.

The calendar-month threshold and end-of-month cutoff are this project's operational choices for the comparison. Treasury reports document the treatment of exits and missing reports, while the full internal calculation code was unavailable in the sources reviewed. Later snapshot status and exit dates are used for retrospective reconstruction. An as-of data-availability protocol is needed before prospective model evaluation.

[راهنمای داده / Data guide](https://home.treasury.gov/system/files/136/HAMP%20Performance%20Supplemental%20Data%20File%20User%20Guide%20v1.0.pdf) · [روش گزارش پرداخت ماهانه / Monthly reporting methodology](https://home.treasury.gov/system/files/initiatives/financial-stability/reports/Documents/4Q17%20MHA%20Report%20Final.pdf)

## مقایسهٔ هر گروه | Cohort comparisons

هر سلول نرخ، برآورد و سپس مقدار رسمی را به درصد نشان می‌دهد. ستون اختلاف بر حسب واحد درصد است.

Each rate cell lists the estimate followed by Treasury's rate in percent. Differences are in percentage points.

| گروه / Tier | سال / Year | ماه ۶ / M6 | اختلاف / Δ | ماه ۱۲ / M12 | اختلاف / Δ |
|---|---:|---:|---:|---:|---:|
| 1 | 2009 | 6.5887 / 6.7 | -0.1113 | 16.1057 / 16.3 | -0.1943 |
| 1 | 2010 | 6.6911 / 6.7 | -0.0089 | 15.4788 / 15.6 | -0.1212 |
| 1 | 2011 | 5.2417 / 5.3 | -0.0583 | 12.6094 / 12.7 | -0.0906 |
| 1 | 2012 | 4.2539 / 4.3 | -0.0461 | 10.2525 / 10.3 | -0.0475 |
| 1 | 2013 | 3.8108 / 3.8 | +0.0108 | 9.4159 / 9.5 | -0.0841 |
| 1 | 2014 | 4.6361 / 4.7 | -0.0639 | 10.5906 / 10.6 | -0.0094 |
| 1 | 2015 | 5.2527 / 5.3 | -0.0473 | 11.7888 / 11.8 | -0.0112 |
| 1 | 2016 | 5.6243 / 5.7 | -0.0757 | 13.0301 / 13.0 | +0.0301 |
| 1 | 2017 | 6.0256 / 6.0 | +0.0256 | 13.6733 / 13.7 | -0.0267 |
| 2 | 2012 | 5.3239 / 5.4 | -0.0761 | 17.1692 / 17.3 | -0.1308 |
| 2 | 2013 | 7.7674 / 7.8 | -0.0326 | 17.1957 / 17.3 | -0.1043 |
| 2 | 2014 | 6.9879 / 7.1 | -0.1121 | 16.0947 / 16.2 | -0.1053 |
| 2 | 2015 | 7.8339 / 7.9 | -0.0661 | 17.4523 / 17.5 | -0.0477 |
| 2 | 2016 | 7.5359 / 7.6 | -0.0641 | 17.6926 / 17.7 | -0.0074 |
| 2 | 2017 | 7.0106 / 7.0 | +0.0106 | 16.4908 / 16.7 | -0.2092 |

## اختلاف گروه دوم در ۲۰۱۷ | Tier 2 in 2017

در ماه دوازدهم، ۳٬۰۷۸ مورد از ۱۸٬۶۶۵ مورد در مخرج، نرخ ۱۶٫۴۹۰۸٪ را می‌دهند. نرخ رسمی ۱۶٫۷٪ و فاصله ۰٫۲۰۹۲ واحد درصد است. از ۲۰٬۲۲۵ اصلاح در این گروه، ۲۵۲ مورد تسویه یا انصراف و ۱٬۳۰۸ مورد فاقد گزارش معتبر بودند. اجرای همان قاعده با وضعیت اصلاحات نسخهٔ ژوئیهٔ ۲۰۲۰، نرخ ۱۶٫۴۹۵۲٪ داد. این تغییر کوچک به‌تنهایی اختلاف را توضیح نمی‌دهد.

At month twelve, 3,078 of 18,665 in the denominator gave 16.4908%, compared with Treasury's 16.7%, a gap of 0.2092 percentage points. Of the 20,225 modifications, 252 were excluded for payoff or withdrawal and 1,308 lacked valid reports. Using the July 2020 modification snapshot under the same rule gave 16.4952%. This small revision does not explain the gap by itself.

## بازتولید | Reproduction

از ریشهٔ پروژه، با پایتون ۳٫۱۲، ابزار `pdftotext` و نسخهٔ `unzip` با پشتیبانی از Deflate64 اجرا کنید. فایل‌های ورودی را با نام‌های زیر در پوشهٔ کاری خارج از پروژه قرار دهید. اثرانگشت ورودی‌ها در فایل خروجی ثبت شده است. اجرای مرحله‌ای از نگهداری CSV بازشدهٔ آرشیو تاریخی در دیسک جلوگیری می‌کند.

Run from the project root with Python 3.12, `pdftotext`, and an `unzip` build supporting Deflate64. Place the source files under the scratch directory with the names below. Their fingerprints are recorded in the aggregate output. The batched import avoids storing the decompressed historical CSV on disk.

```bash
scratch=../work/mortgage-source/history
python3 -m venv "$scratch/venv"
hamp_python="$scratch/venv/bin/python"
"$hamp_python" -m pip install duckdb==1.5.0 pyarrow==21.0.0

"$hamp_python" research/hamp_history_stage.py "$scratch/compact-old.duckdb" historical \
  --archive "$scratch/verified-hamp-2009-2017.zip"
"$hamp_python" research/hamp_history_stage.py "$scratch/compact-monthly.duckdb" monthly_update \
  --archive "$scratch/verified-hamp-monthly-2020.zip"
"$hamp_python" research/hamp_history_stage.py "$scratch/compact-latest.duckdb" latest \
  --archive "$scratch/../hamp-2018-2023.zip"

pdftotext -layout "$scratch/../treasury-hamp.pdf" "$scratch/../treasury-hamp.txt"
"$hamp_python" research/hamp_reconstruct.py \
  --historical-db "$scratch/compact-old.duckdb" --monthly-db "$scratch/compact-monthly.duckdb" \
  --latest-db "$scratch/compact-latest.duckdb" --reference-text "$scratch/../treasury-hamp.txt"
```

[خروجی تجمیعی / Aggregate output](hamp-historical-reconstruction.json) · [کد ورود / Import script](../../research/hamp_history_stage.py) · [کد بازسازی / Reconstruction script](../../research/hamp_reconstruct.py)
