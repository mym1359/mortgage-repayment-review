# بررسی نخستین نمونهٔ مجاز هامپ | First authorized HAMP sample review

ابتدا در محیط خصوصی، مجوز استفاده و منشأ گزارش‌ها را بررسی کنید. برای هر اصلاح، نسخهٔ گزارش ماه ششم، وضعیت فعال تا پایان همان ماه، و رویداد پیامد یا شواهد پیگیری را با منبع اصلی تطبیق دهید. تعریف زمان دریافت، پردازش و دسترسی را از فرهنگ داده یا مستند منبع بگیرید. فیلد `verified` نتیجهٔ این بررسی است. اعتبارسنج به منبع اصلی وصل نمی‌شود.

In a private environment, confirm authorization and report provenance first. For each modification, verify the month-six report version, active status through the end of that month, and the outcome event or follow-up evidence against the original source. Use source documentation to interpret receipt, processing, and availability times. The `verified` field records that source review. The validator does not access original sources.

## ورودی خصوصی | Private input

ورودی یک آرایهٔ JSON با یک شیء برای هر اصلاح است. فایل و مستندات پشتیبان را بیرون از مخزن نگه دارید. در صورت نبودن شاهد، مقدار آن را وارد نکنید یا `null` ثبت کنید.

The input is a JSON array with one object per modification. Keep the input and supporting materials outside the repository. Leave missing evidence absent or set it to `null`.

| فیلد / Field | مقدار / Value |
| --- | --- |
| `loan_id`, `modification_id` | شناسه‌های مستعار و پایدار وام و اصلاح. / Stable pseudonymous loan and modification IDs. |
| `program_tier`, `permanent` | گروه برنامه به صورت عدد و پرچم دائمی بودن بر اساس شاهد منبع. / Numeric program tier and permanent status supported by the source. |
| `split`, `effective_month` | بخش `train`، `validation` یا `test` و ماه اثر به شکل `YYYY-MM`. / Partition and effective month in `YYYY-MM`. |
| `cutoff_at`, `horizon_end_at` | ابتدای ماه‌های هفتم و سیزدهم. / Start of months seven and thirteen. |
| `month_six_report` | شیء شاهد به همراه `activity_month` به شکل `YYYY-MM`. / Evidence object with an `activity_month` in `YYYY-MM`. |
| `month_six_report_history` | برای گزارش اصلاح‌شده، زنجیرهٔ گزارش‌های پیشین با همان `activity_month` و زمان دسترسی هر نسخه. / For a corrected report, supply the chain of predecessor evidence objects with the same `activity_month` and each version's availability time. |
| `active_status` | شیء شاهد به همراه `active`. تاریخ مشاهده باید در ماه ششم باشد. مقدار `true` باید وضعیت همان اصلاح را در برش احراز کند. / Evidence object with `active`. The observation must be dated in month six, and `true` must establish the modification's status at cutoff. |
| `outcome` | شیء شاهد به همراه `disposition` از میان `disqualified`، `paid_off`، `censored` و `no_event`. زمان رویداد برای دو مورد آخر، پایان مشاهده است. / Evidence object with `disposition` set to one of the listed values. For the last two, event time is the end of observation. |
| `features` | آرایهٔ اشیای شاهد با نام `feature` از میان `last_installment_month_gap`، `reporting_pattern` و `payment_history_change`. برای فاصلهٔ آخرین قسط، `due_date` به شکل `YYYY-MM-DD` و `posted_at` به‌عنوان زمان ثبت پرداخت را جدا وارد کنید. `event_at` این ورودی باید با زمان ثبت پرداخت یکی باشد. / Array of evidence objects with a `feature` from the listed names. For the last installment gap, supply `due_date` as `YYYY-MM-DD` and `posted_at` as the payment posting timestamp. Its `event_at` must match the posting instant. |

هر شیء شاهد شامل `source_ref` (مرجع خصوصی منبع)، `version`، `supersedes` (شناسهٔ نسخهٔ پیشین یا `null` برای نسخهٔ اولیه)، `sha256` (چکیدهٔ فایل منبع)، `retrieved_at`، `event_at`، `available_at` و `verified` است. زمان‌ها را با آفست صریح وارد کنید. برای هر ورودی یک شاهد ثبت کنید و زمان دسترسی همان نسخه را از منبع احراز کنید.

Each evidence object has `source_ref` (private source locator), `version`, `supersedes` (predecessor ID or `null` for the original version), `sha256` (source file digest), `retrieved_at`, `event_at`, `available_at`, and `verified`. Supply explicit timezone offsets. Record evidence for every input and substantiate availability for the exact version.

## اجرا و تفسیر | Run and interpret

```sh
python research/hamp_sample_review.py --sample /private/path/sample.json
```

| کد خروج / Exit code | معنی / Meaning |
| --- | --- |
| `0` | `sample_supported`: شواهد ثبت‌شده کامل‌اند و فرادادهٔ نمونه از اعتبارسنج عبور کرده است. / The recorded evidence is complete and the sample metadata passed the validator. |
| `1` | `insufficient_evidence` یا `metadata_rejected`: گزارش تجمیعی علت و شمار مغایرت‌ها را نشان می‌دهد. / Aggregate counts show evidence gaps or metadata violations. |
| `2` | `invalid_input`: دلیل با یکی از کدهای `unreadable_file`، `invalid_json`، `invalid_record` یا `invalid_timestamp` گزارش می‌شود. / The reason is reported as one of the listed codes. |

اعتبارسنج فراداده فقط اصلاح‌هایی را بررسی می‌کند که شاهد قابل استفادهٔ پیامد دارند. گزارش کمبود شواهد تمام نمونه را پوشش می‌دهد. این فرمان برای نمونهٔ اولیه وجود هر سه بخش زمانی را الزام نمی‌کند. نتیجهٔ موفق برای احراز پوشش گروه‌های کامل کفایت نمی‌کند. انتشار گزارش به شمارش‌های تجمیعی محدود می‌شود.

The metadata check covers modifications with usable outcome evidence. The evidence-gap counts cover the entire sample. The initial sample can use fewer than three partitions. Full-cohort coverage requires its own evaluation. Publish aggregate counts only.

[پروتکل زمان‌دار / Time-aware protocol](hamp-asof-protocol.md) · [اعتبارسنج فراداده / Metadata validator](hamp-evaluation-readiness.md)
