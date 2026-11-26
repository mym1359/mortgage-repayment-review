# وضعیت پژوهش هامپ و دادهٔ مورد نیاز | HAMP research status and outstanding data

## وضعیت | Status

| بخش / Work | نتیجه / Status |
|---|---|
| بازسازی نرخ‌های تاریخی / Historical rate reconstruction | تکمیل و بازتولید شد. اختلاف ۲۹ مورد از ۳۰ نرخ حداکثر ۰٫۲۰ واحد درصد بود. Completed and reproduced. Twenty-nine of 30 estimates were within 0.20 percentage points. |
| تقویم و پوشش گروه‌ها / Calendar and cohort coverage | تکمیل و بازتولید شد. ۹۶٬۳۷۰ اصلاح از آموزش کنار گذاشته شد و پوشش ۱۰۲ گروه ماهانه بررسی شد. Completed and reproduced. The revised boundary holds out 96,370 modifications and the table covers 102 effective-month cohorts. |
| ارزیابی مدل در سطح وام / Loan-level model evaluation | در انتظار شاهد معتبر برای زمان دسترسی به گزارش ماه ششم و نسخهٔ برچسب پیامد. Awaiting authoritative evidence of month-six report and outcome-label availability. |

بررسی منابع عمومی، نمونه‌ای قابل استفاده برای احراز هر دو زمان در یک اصلاح پیدا نکرد. آرشیوهای تکمیلی ماه فعالیت را ثبت می‌کنند و نسخه‌های بایگانی‌شده شاهد وجود مقادیر در تاریخ بایگانی‌اند. برای اجرای ارزیابی باید سابقهٔ زمان‌دار یا نسخه‌های قابل تطبیق هر دو نوع شاهد در اختیار باشد. آزمون‌های ساختگی، منطق کنترل را تأیید کردند.

The public-source review did not identify a sample establishing both availability times for the same modification. The supplemental archives identify the activity month, and captured releases prove that a particular version existed by its capture date. Evaluation requires a timestamped history or compatible vintages establishing both facts. Synthetic tests verified the evaluation checks.

[بازسازی تاریخی / Historical reconstruction](hamp-historical-reconstruction.md) · [جدول پوشش ماهانه / Monthly coverage](hamp-monthly-evaluation-coverage.md) · [اعتبارسنج فراداده / Metadata checks](hamp-evaluation-readiness.md)

## بررسی تکمیلی فایل‌های ۲۰۱۱ | Additional check of the 2011 files

دو فایل از نسخهٔ سپتامبر ۲۰۱۱ با ثبت‌های بایگانی اکتبر ۲۰۱۱ بازیابی شدند. چکیدهٔ هر دو با نمایهٔ بایگانی برابر بود. فایل منطقهٔ ۸ شامل ۴٬۴۲۷ ردیف داده و ۱۰۴ ستون بود. فایل منطقهٔ ۹۹ همان ۱۰۴ ستون را داشت و ردیف داده‌ای نداشت. در طرح این دو فایل، تاریخ اقدام و وضعیت ارسال وجود داشت. ماه فعالیت، تاریخ پردازش `DD493` و زمان دسترسی به نسخهٔ برچسب در آن‌ها یافت نشد. نتیجه به همین دو فایل محدود است.

Two September 2011 files were recovered from October 2011 captures. Both payload digests matched the archive index. Region 8 contained 4,427 data rows and 104 columns. Region 99 contained the same 104 columns and no data rows. Their headers included action date and submission status. They did not contain an activity-month field, the `DD493` processing date, or label-version availability. This finding is limited to the two inspected files.

| فایل / File | چکیدهٔ بایگانی / Archived payload SHA-1 in Base32 |
|---|---|
| `HMP_Public_User_Mod_Data_8_20110916.csv` | `OOSWX4FJSRDBUWXP4NSMF56QTLXX5R3K` |
| `HMP_Public_User_Mod_Data_99_20110916.csv` | `4XZLSGIQYTVV64HQASYW22E27G3Q3FGW` |

[آرشیو منطقهٔ ۸ / Region 8 capture](https://web.archive.org/web/20111029000338id_/http://www.treasury.gov/initiatives/financial-stability/results/Documents/HMP_Public_User_Mod_Data_8_20110916.csv) · [آرشیو منطقهٔ ۹۹ / Region 99 capture](https://web.archive.org/web/20111029000112id_/http://www.treasury.gov/initiatives/financial-stability/results/Documents/HMP_Public_User_Mod_Data_99_20110916.csv) · [راهنمای نسخه‌های تکمیلی / Supplemental release guide](https://home.treasury.gov/system/files/136/HAMP%20Performance%20Supplemental%20Data%20File%20User%20Guide%20v1.0.pdf)

## بررسی نخستین نمونهٔ مجاز | First authorized sample

درخواست اول دربارهٔ موجودی نسخه‌ها و فرهنگ داده است. اگر نمونهٔ مجاز در دسترس باشد، این موارد برای یک یا چند اصلاح، کاربرد منبع را مشخص می‌کنند.

The initial inquiry asks for a release inventory and a data dictionary. If an authorized sample is available, the following fields can establish whether the source supports the evaluation for one or more modifications.

| شاهد / Evidence | اقلام مورد نیاز / Required items |
|---|---|
| هویت و دامنه / Identity and coverage | شناسهٔ مستعار پایدارِ وام و اصلاح، گروه برنامه، تاریخ اثر و بازهٔ پوشش موجود. Stable pseudonymous loan and modification IDs, program tier, effective date, and source coverage period. |
| گزارش و وضعیت ماه ششم / Month-six report and status | ماه فعالیت، زمان رویداد، زمان اولین دسترسی یا زمان تأییدشدهٔ انتشار همان نسخه، شناسهٔ نسخه و زمان‌های اصلاح. برای وضعیت فعال و خروجی پرداخت از همین قاعدهٔ زمانی استفاده شود. Activity month, event time, first availability or verified release time of the same version, version ID, and revision dates. Apply the same timing requirement to active status and payment inputs. |
| شواهد پیامد / Outcome evidence | تاریخ وقوع و دسترسی به برچسب خروج یا تسویه. برای پروندهٔ بدون رخداد یا با پیگیری ناقص، آخرین زمان مشاهده و زمان دسترسی به آن. Exit or payoff event and label availability. For event-free or censored cases, last observation time and when that evidence became available. |
| تعریف زمان و منشأ / Time semantics and provenance | فرهنگ داده، منطقهٔ زمانی، تعریف «دریافت»، «پردازش» و «دسترسی»، و مستنداتی که رکوردهای اصلاحی را به نسخهٔ قبلی وصل می‌کنند. Data dictionary, time zones, definitions of receipt, processing, and availability, and documentation linking corrections to prior versions. |

پیش از تبدیل نمونه به ورودی اعتبارسنج، باید زمان گزارش و زمان برچسب با منبع اصلی تطبیق داده شوند. نمونهٔ اولیه فقط امکان استفاده از منبع را می‌سنجد. برای ادعای عملکرد مدل، به پوشش معتبر گروه‌های آموزش، اعتبارسنجی و آزمون و اجرای ارزیابی نیاز داریم. دادهٔ نمونهٔ واقعی و مدارک دسترسی خارج از مخزن نگهداری می‌شوند.

Verify feature and outcome times against source evidence before converting the sample to validator inputs. The initial sample tests source feasibility. Model performance claims require valid coverage across training, validation, and test and a completed evaluation. Keep real sample data and access records outside the repository.

## پیش‌نویس استعلام | Draft inquiry

مسیر اولیه، نشانی رسمی پرسش‌های دادهٔ هامپ است. این متن برای استعلام موجودی و تعریف اقلام آماده شده است.

The initial contact is Treasury's published MHA data inquiries address. This draft asks about the available records and field definitions.

[نشانی رسمی پرسش‌های مربوط به دادهٔ هامپ / Official MHA data inquiries listing](https://home.treasury.gov/data/troubled-assets-relief-program/reports/mha-public-file)

**گیرنده / To** — `MHA_Data_Questions@treasury.gov`

**موضوع / Subject** — Availability of historical HAMP monthly releases and timing documentation

> Hello,
>
> I am conducting reproducible research on repayment after permanent Tier 1 HAMP modifications. I am looking for historical records or release documentation covering the 2009–2017 modification cohorts and their follow-up through 2018.
>
> Does Treasury maintain an inventory or archive of original monthly releases, or documentation that links the activity month to the first receipt, processing, acceptance, or release timestamp of each Official Monthly Report and later correction? Is there equivalent timing documentation for disqualifications, payoffs, and completed follow-up? In particular, I would like to know whether original and corrected versions can be distinguished using stable pseudonymous identifiers.
>
> Public links or a data dictionary would be sufficient to start. If relevant records require restricted access, could you direct me to the appropriate custodian and authorized process for evaluating a small de-identified sample? The inquiry does not request borrower names, addresses, or account numbers.
>
> Thank you.

**ترجمهٔ پیشنهادی برای بازبینی / Persian review translation**

> در حال انجام پژوهشی بازتولیدپذیر دربارهٔ بازپرداخت پس از اصلاحات دائمی گروه اول هامپ هستم. به‌دنبال موجودی نسخه‌های ماهانهٔ اصلی برای اصلاحات سال‌های ۲۰۰۹ تا ۲۰۱۷ و پیگیری آن‌ها تا پایان ۲۰۱۸ هستم.
>
> آیا آرشیو یا مستنداتی وجود دارد که ماه فعالیت را به زمان اولین دریافت، پردازش، پذیرش یا انتشار گزارش ماهانه و اصلاح‌های بعدی وصل کند؟ آیا برای خروج، تسویه و پایان پیگیری هم مستندات معادل وجود دارد؟ همچنین می‌خواهم بدانم آیا نسخهٔ اصلی و اصلاح‌شده با شناسه‌های مستعار پایدار قابل تشخیص‌اند.
>
> برای شروع، پیوندهای عمومی یا فرهنگ داده کافی است. اگر دسترسی محدود است، لطفاً متولی و مسیر مجاز بررسی نمونهٔ کوچکِ بدون مشخصات شناسایی را معرفی کنید. این استعلام نام، نشانی یا شمارهٔ حساب وام‌گیرندگان را درخواست نمی‌کند.
>
> سپاس.
