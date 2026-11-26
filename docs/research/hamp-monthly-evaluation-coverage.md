# پوشش ماهانه پس از اصلاح تقویم ارزیابی | Monthly coverage after the partition change

## مرز اصلاح‌شده | Revised boundary

برش آغاز اعتبارسنجی را در ۱ ژوئیهٔ ۲۰۱۳ حفظ کردیم. تاریخ اثر آخرین گروه مجاز آموزش ژوئن ۲۰۱۲ است. گروه‌های ژوئیه تا دسامبر ۲۰۱۲، شامل **۹۶٬۳۷۰ اصلاح وام**، کنار گذاشته شدند تا پایان پنجرهٔ پیگیری آن‌ها وارد دورهٔ اعتبارسنجی نشود. با مرز جدید، آخرین پنجرهٔ آموزش در ۱ ژوئن ۲۰۱۳ پایان می‌یابد. دسترسی واقعی به برچسب باید پیش از ۱ ژوئیه تأیید شود و تأخیر گزارش می‌تواند دامنهٔ آموزش را باز هم کوچک کند.

The first validation cutoff remains July 1, 2013. June 2012 is the last permitted training effective month. The **96,370 July–December 2012 modifications** are held out because their complete follow-up windows overlap the first validation cutoff. Under the revised boundary, the last training follow-up window ends June 1, 2013. Actual label availability must precede July 1. Reporting delays could move the latest eligible training month earlier.

[حسابرسی تقویم اولیه / Original calendar audit](hamp-earlier-vintages.md)

## پوشش هر بخش | Coverage by partition

| بخش / Partition | ماه‌های اثر / Effective months | اصلاحات مرجع / Reference modifications | گزارش ماه ششم قابل استفادهٔ گذشته‌نگر / Retrospectively usable month-six report | نسخهٔ پیش از برش با وضعیت فعال و اطلاعات پرداخت / Earlier snapshot with active status and payment fields | گزارش ماه ششم و برچسب با دسترسی اثبات‌شده / Month-six report and label with verified availability |
|---|---:|---:|---:|---:|---:|
| آموزش / Training | 36 | 1,034,678 | 716,772 | 43,606 | 0 |
| حذف تقویمی / Embargo | 6 | 96,370 | 69,305 | 15,950 | 0 |
| اعتبارسنجی / Validation | 12 | 147,264 | 103,853 | 24,591 | 0 |
| فاصلهٔ ۲۰۱۴ / 2014 gap | 12 | 86,433 | 60,918 | 0 | 0 |
| آزمون / Test | 36 | 108,692 | 77,473 | 9,820 | 0 |

جدول کامل بر اساس **۱۰۲ گروه ماهانهٔ تاریخ اثر** تهیه شده است. شمارش‌های گزارش گذشته‌نگر و نسخهٔ پیش از برش از دو منبع متفاوت می‌آیند. اشتراک این دو شمارش اندازه‌گیری نشده و آن‌ها را نمی‌توان با هم جمع کرد. شمارش‌های مرجع، جمعیت مرحله‌بندی‌شدهٔ گروه اول هستند و فعال بودن در زمان تصمیم را به‌تنهایی اثبات نمی‌کنند.

The detailed table covers **102 effective-month cohorts**. Retrospective payment counts and earlier snapshot counts come from different sources. Their intersection was not measured and the counts should not be added. Reference counts describe the staged Tier 1 population. They do not establish active status as of the cutoff.

[جدول ماهانهٔ CSV / Monthly coverage CSV](hamp-monthly-evaluation-coverage.csv)

## شواهد لازم برای ارزیابی | Evidence needed for evaluation

رکوردهای تکمیلی عمومی به کمک ماه فعالیت و سن اصلاح به خودِ ماه ششم نسبت داده می‌شوند. این فایل‌ها زمان دسترسی به نسخهٔ هر گزارش را مشخص نمی‌کنند. نسخه‌های ۲۰۱۲، ۲۰۱۳ و ۲۰۱۶ زمان بایگانی مشخص دارند، اما تاریخ پردازش آخرین گزارش در آن‌ها به‌صورت صریح به ماه فعالیت وصل نشده است. نسخه‌های نهایی نیز زمان نخستین دسترسی به پیامد یا نسخهٔ برچسب را ثبت نکرده‌اند.

The public supplemental records identify month six through activity month and modification age, but do not timestamp access to each report version. The 2012, 2013, and 2016 snapshots have dated archive captures, but their latest processing date is not explicitly linked to an activity month. Final snapshots do not establish when the outcome or label version first became available.

عدد صفر در ستون‌های شواهد زمان‌دار یعنی **در منابع بررسی‌شده مورد قابل‌اثبات پیدا نشد**. تعداد واقعی گزارش‌ها یا پیامدهای موجود در سامانهٔ مؤسسه نامعلوم است. برای ساخت مجموعهٔ ارزیابی، به شواهدی نیاز داریم که شناسهٔ اصلاح، ماه فعالیت، نسخه و زمان دسترسی گزارش را به هم وصل کند و زمان دسترسی به برچسب را هم ثبت کند.

A zero in a verified-availability column means **no case could be substantiated in the audited sources**. Actual availability within servicer systems is unknown. Building the evaluation set requires evidence linking modification ID, activity month, report version, availability time, and outcome label availability.

[پروتکل ارزیابی / Evaluation protocol](hamp-asof-protocol.md) · [نسخه‌های ۲۰۱۲ و ۲۰۱۳ / 2012 and 2013 vintages](hamp-earlier-vintages.md) · [نسخهٔ ۲۰۱۶ / 2016 vintage](hamp-december-2016-snapshot.md)

## بازتولید | Reproduction

سه آرشیو تکمیلی و سه نسخهٔ قدیمی را طبق گزارش‌های لینک‌شده آماده کنید. برای ممیزی پرداخت، هر دو ممیزی منطقه‌ای و ممیزی ۲۰۱۶، همان فرمان‌های گزارش‌های قبلی را با گزینهٔ `--monthly` اجرا کنید. خروجی‌ها را به‌ترتیب در فایل‌های نمونهٔ زیر ذخیره کنید و ترکیب نهایی را از ریشهٔ پروژه اجرا کنید.

Stage the three supplemental archives and prepare the three older snapshots as described in the linked reports. Run the previous payment, regional, and December 2016 audit commands with `--monthly`, writing their JSON outputs to the example paths below, then combine them from the project root.

```bash
scratch=../work/mortgage-source/vintage-survey
python3 research/hamp_evaluation_coverage.py \
  --payment-audit "$scratch/asof-monthly.json" \
  --snapshot "$scratch/monthly-2012.json" \
  --snapshot "$scratch/monthly-2013.json" \
  --snapshot "$scratch/monthly-2016.json" \
  --monthly-csv "$scratch/coverage-monthly.csv" > "$scratch/coverage-report.json"
```
