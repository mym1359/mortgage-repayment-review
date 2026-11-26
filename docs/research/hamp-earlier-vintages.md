# نسخه‌های قدیمی هامپ و تقویم ارزیابی | Earlier HAMP vintages and evaluation calendar

## یافتهٔ اصلی | Main finding

تمام ۱۱ فایل منطقه‌ای نسخهٔ سپتامبر ۲۰۱۲ بازیابی و با اثرانگشت نمایهٔ بایگانی راستی‌آزمایی شدند. این نسخه برای بخشی از گروه آموزش شاهدی دربارهٔ وجود داده پیش از برش فراهم می‌کند. حسابرسی تقویم نیز نشان داد که پنجرهٔ پیگیری ۹۶٬۳۷۰ اصلاح پیشنهادی برای آموزش، حتی با فرض صفر روز تأخیر در گزارش، در زمان اولین برش اعتبارسنجی کامل نشده بود.

All 11 regional files from the September 2012 release were recovered and verified against the web archive's payload digests. This release provides pre-cutoff evidence for part of the training cohort. The calendar audit also found 96,370 proposed training modifications whose full follow-up would not finish before the first validation cutoff, even with zero reporting delay.

## انتشار و جست‌وجوی نسخه‌ها | Publication and vintage search

صفحه‌های بایگانی‌شدهٔ خزانه‌داری در سال‌های ۲۰۱۱ تا ۲۰۱۶، نشانی فایل‌های منطقه‌ای رهن اول را در مسیرهای قدیمی `results/Documents`، `reports/Reports` و میزبان `mhadatafile.treasury.gov` نشان دادند. پیوند صفحهٔ فهرست و ثبت هر فایل داده جداگانه بررسی شدند. علاوه بر نمایه و بازپخش Wayback، بلوک‌های مرتبط در نمایه‌های بایگانی پایان دورهٔ ۲۰۰۸، ۲۰۱۲ و ۲۰۱۶ بررسی شدند. این جست‌وجو محدودهٔ مشخصی داشت و نبودن یک فایل در نتایج، نبودن آن در سایر مجموعه‌ها را ثابت نمی‌کند.

Archived Treasury landing pages from 2011 through 2016 revealed first-lien regional files under `results/Documents`, `reports/Reports`, and `mhadatafile.treasury.gov`. We checked the listing pages and the data captures separately, using Wayback availability and the relevant End of Term 2008, 2012, and 2016 index blocks. The search was scoped to these sources and paths.

[فهرست اکتبر ۲۰۱۱ / October 2011 listing](https://web.archive.org/web/20111023102428/http://www.treasury.gov/initiatives/financial-stability/results/Pages/mha_publicfile.aspx) · [فهرست دسامبر ۲۰۱۲ / December 2012 listing](https://web.archive.org/web/20121210002240/http://www.treasury.gov/initiatives/financial-stability/reports/Pages/mha_publicfile.aspx) · [فهرست مه ۲۰۱۳ / May 2013 listing](https://web.archive.org/web/20130512183244/http://www.treasury.gov/initiatives/financial-stability/reports/Pages/mha_publicfile.aspx) · [مجموعهٔ بایگانی ۲۰۱۲ / End of Term 2012 dataset](https://eotarchive.s3.amazonaws.com/crawl-data/EOT-2012/index.html)

## حسابرسی نسخهٔ سپتامبر ۲۰۱۲ | September 2012 audit

فایل‌های ۱۱ منطقه در ۲۶ سپتامبر ۲۰۱۲ در بایگانی ثبت شدند. همهٔ **۴٬۶۴۳٬۸۶۵ ردیف** خوانده شدند. در **۱٬۰۵۵٬۸۱۵ ردیف** تاریخ پردازش آخرین گزارش ماهانه وجود داشت و تازه‌ترین تاریخ پردازش ۱۰ اوت ۲۰۱۲ بود. شناسهٔ اصلاح در فایل موجود بود و شناسهٔ وام در طرح این نسخه وجود نداشت. بنابراین فقط پس از احراز یکتایی شناسهٔ اصلاح در کل مرجع مارس ۲۰۲۳، دو منبع با همان شناسه تطبیق داده شدند. تاریخ اثرهای متفاوت جداگانه شمارش و از ارزیابی زمان کنار گذاشته شدند.

The 11 regional files were captured on September 26, 2012. The audit scanned all **4,643,865 rows**. It found a latest monthly processing date on **1,055,815 rows**, with a maximum date of August 10, 2012. The release provides a modification ID and has no loan ID column. We joined on modification ID after confirming global uniqueness in the March 2023 reference, and counted effective-date disagreements separately from timing evidence.

| شاخص / Measure | تعداد / Count |
|---|---:|
| اصلاح رسمی گروه اول با تطبیق شناسه / Matched official Tier 1 modifications | 1,049,623 |
| تاریخ اثر متفاوت / Effective-date disagreements | 2,058 |
| ثبت نسخه پیش از برش / Capture before cutoff | 70,688 |
| ثبت نسخه در خود ماه ششم و پیش از برش / Capture during month six and before cutoff | 15,533 |
| قبل از برش با وضعیت فعال، تاریخ سررسید و تاریخ پردازش / Pre-cutoff active state with due and processing dates | 59,556 |

تمام ۷۰٬۶۸۸ مورد پیش از برش به گروه اثر سال ۲۰۱۲ تعلق داشتند. مقدار ثبت‌شده در نسخه، شاهد دادهٔ قابل مشاهده پیش از برش است. ستون تاریخ پردازش به‌تنهایی ماه فعالیت یا وضعیت پرونده را در آخرین روز ماه ششم مشخص نمی‌کند.

All 70,688 pre-cutoff cases were in the 2012 effective-year cohort. An archived value establishes that the value was observable before the cutoff. The processing date alone does not identify the activity month or the state at the end of month six.

## حسابرسی سه فایل ثبت‌شده در ژوئن ۲۰۱۳ | June 2013 three-file audit

سه فایل منطقه‌ای ۱، ۶ و ۷ که در ۲۵ ژوئن ۲۰۱۳ بایگانی شده بودند، با بازه‌های بایتی بازپخش Wayback بازیابی و با نمایه تطبیق داده شدند. نام اعضای ZIP به ۱۷ آوریل ۲۰۱۳ اشاره دارد. مجموع **۳٬۱۴۱٬۹۱۶ ردیف** بررسی شد و تازه‌ترین تاریخ پردازش ماهانه ۱۰ آوریل ۲۰۱۳ بود. این نسخه هر دو شناسهٔ وام و اصلاح را داشت. آمار زیر فقط همین سه منطقه را پوشش می‌دهد.

The regional files 1, 6, and 7 captured on June 25, 2013 were recovered via Wayback byte ranges and verified against index digests. Their ZIP member names identify April 17, 2013. We scanned all **3,141,916 rows**. The latest monthly report processing date was April 10, 2013. Both loan and modification IDs were available. The counts cover the three recovered regions.

| شاخص / Measure | تعداد / Count |
|---|---:|
| اصلاح رسمی گروه اول با تطبیق هر دو شناسه / Matched official Tier 1 modifications | 756,657 |
| تاریخ اثر متفاوت / Effective-date disagreements | 1,306 |
| ثبت نسخه پیش از برش / Capture before cutoff | 29,863 |
| ثبت نسخه در خود ماه ششم و پیش از برش / Capture during month six and before cutoff | 8,249 |
| قبل از برش با وضعیت فعال، تاریخ سررسید و تاریخ پردازش / Pre-cutoff active state with due and processing dates | 24,591 |

تمام ۲۹٬۸۶۳ مورد پیش از برش از گروه سال ۲۰۱۳ در بخش اعتبارسنجی‌اند. در کنار نسخه‌های سپتامبر ۲۰۱۲ و دسامبر ۲۰۱۶، اکنون برای زیرمجموعه‌هایی از هر سه بخش شواهد وجود نسخه پیش از برش داریم. برای تعیین وضعیت در پایان ماه ششم و سنجش مدل، همچنان باید برچسب زمانی گزارش همان ماه و زمان دسترسی به پیامد از منبع تأیید شود. نمایه یازده فایل دیگر از اکتبر ۲۰۱۱ را نشان داد. این مرحله فقط ثبت آن‌ها را در نمایه بررسی کرد.

All 29,863 pre-cutoff cases fall in the 2013 validation cohort. Together with September 2012 and December 2016, the captures now attest to pre-cutoff values for subsets of all three partitions. Evaluation still requires verified month-six reporting and outcome availability. We identified 11 additional October 2011 captures in the index. This stage checked their index entries.

[نمونهٔ فایل ژوئن ۲۰۱۳ / June 2013 regional capture](https://web.archive.org/web/20130625100040/http://www.treasury.gov:80/initiatives/financial-stability/reports/Reports/HMP_Public_User_Mod_Data_1.zip) · [حسابرسی دسامبر ۲۰۱۶ / December 2016 audit](hamp-december-2016-snapshot.md)

## بررسی تقویم بخش‌ها | Partition calendar audit

آغاز پنجرهٔ پیامد، ابتدای ماه هفتم و پایان آن، ابتدای ماه سیزدهم است. برای مقایسهٔ منصفانه، یک قاعدهٔ یکنواخت را برای همهٔ اصلاحات در نظر گرفتیم که در آن کل پنجره باید پیش از برش بعدی تمام شود. فرض صفر روز تأخیر خوش‌بینانه است. زمان واقعی دسترسی به برچسب‌ها همچنان باید بررسی شود.

The outcome window begins at the start of month seven and ends at the start of month thirteen. For this audit, the entire window must close before the next partition's first cutoff under a uniform follow-up rule. Assuming zero reporting delay makes the calendar check optimistic. Actual label availability still needs verification.

| بخش / Partition | اصلاح / Modifications | نخستین تا آخرین برش / First to last cutoff |
|---|---:|---|
| آموزش / Training | 1,131,048 | 2010-01-01 – 2013-06-01 |
| اعتبارسنجی / Validation | 147,264 | 2013-07-01 – 2014-06-01 |
| فاصله / Gap | 86,433 | 2014-07-01 – 2015-06-01 |
| آزمون / Test | 108,692 | 2015-07-01 – 2018-06-01 |

پنجرهٔ کامل پیامد برای **۹۶٬۳۷۰ اصلاح از ژوئیه تا دسامبر ۲۰۱۲** در تاریخ ۲۰۱۳-۰۷-۰۱ یا بعد از آن پایان می‌یابد. این گروه‌ها با قاعدهٔ پیگیری کامل نمی‌توانند در آموزش پیش از اولین برش اعتبارسنجی بمانند. از اعتبارسنجی تا آزمون، در این بررسی تقویمی هم‌پوشانی دیده نشد. در شناسه‌های فایل مرجع نیز وام مشترک بین سه بخش تحلیلی مشاهده نشد.

Full outcome observation for **96,370 July–December 2012 modifications** ends on or after July 1, 2013. Under the uniform follow-up rule, those cohorts cannot remain in training before the first validation cutoff. The calendar audit found no validation-to-test overlap and no shared loan IDs across the three analysis partitions in the reference snapshot.

## بازتولید | Reproduction

فایل‌های منطقه‌ای باید در پوشهٔ کاری بیرون از مخزن قرار گیرند. بخش `sources` در خروجی تجمیعی، راهنمای فایل ورودی هر نسخه است و نشانی، زمان ثبت و اثرانگشت هر فایل را ثبت می‌کند. ردیف‌های بازیابی‌شده از WARC، نشانی و بازهٔ بایتی فشرده را نیز دارند. پس از مرحله‌بندی فایل مارس ۲۰۲۳، فرمان‌ها را از ریشهٔ پروژه در محیط پایتون مرحلهٔ بازسازی اجرا کنید.

Keep regional payloads in scratch space outside the repository. Each release's `sources` array in the aggregate output is the input manifest. It records capture times, source URLs, and payload digests. WARC-recovered entries also include the compressed record location and byte range. After staging March 2023, run the commands from the project root using the reconstruction Python environment.

```bash
scratch=../work/mortgage-source/vintage-survey
history=../work/mortgage-source/history
mkdir -p "$scratch"
python3 - "$scratch" <<'PYMANIFEST'
import json
from pathlib import Path
import sys

root = Path(sys.argv[1])
release_audits = json.loads(Path("docs/research/hamp-earlier-vintages.json").read_text())["release_audits"]
for name, audit in release_audits.items():
    (root / f"{name}-manifest.json").write_text(json.dumps(audit["sources"]))
PYMANIFEST
for vintage in september_2012 june_2013; do
  "$history/venv/bin/python" research/hamp_recover_regional.py \
    --manifest "$scratch/$vintage-manifest.json" --source-dir "$scratch/$vintage"
  "$history/venv/bin/python" research/hamp_regional_snapshots.py \
    --manifest "$scratch/$vintage-manifest.json" --source-dir "$scratch/$vintage" \
    --work-dir "$scratch" --latest-db "$history/compact-latest.duckdb"
done
"$history/venv/bin/python" research/hamp_partition_calendar.py \
  --latest-db "$history/compact-latest.duckdb"
```

[خروجی تجمیعی و مسیرهای بازیابی / Aggregate output and capture locations](hamp-earlier-vintages.json) · [پروتکل ماه ششم / Month-six protocol](hamp-asof-protocol.md) · [راهنمای مرحله‌بندی / Archive staging](hamp-historical-reconstruction.md)
