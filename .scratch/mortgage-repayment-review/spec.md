# مشخصات سامانهٔ بازبینی بازپرداخت وام مسکن آمریکا | U.S. mortgage repayment review specification

Status: ready-for-agent

## بیان مسئله | Problem Statement

کارشناس بانک منطقه‌ای یا تعاونی اعتبار آمریکا برای بازبینی وام اصلاح‌شده باید بتواند نسخهٔ معتبر توافق، آخرین قسط کاملِ اعمال‌شده و علت ارجاع احتمالی پرونده را با شواهد توضیح دهد. کد فعلی پروژه ابزار پژوهش تاریخی است. از همین پژوهش می‌توان آموخت که دادهٔ ناقص، نسخهٔ متأخر و تاریخ سررسید در مقایسه با تاریخ ثبت پرداخت چه اثری بر نتیجه می‌گذارند.

A reviewer at a U.S. regional bank or credit union needs evidence of the applicable modification agreement, the last full applied installment, and the reason for any referral. The current codebase supports historical research. That research exposes the consequences of missing reports, later revisions, and the difference between an installment due date and a payment posting date.

پژوهش تجمیعی بازتولید شده است. هنوز برای هیچ پرونده‌ای در منابع عمومی بررسی‌شده، زمان دسترسی به گزارش خودِ ماه ششم و زمان دسترسی به برچسب پیامد هم‌زمان اثبات نشده‌اند. این شکاف مانع ارزیابی مدل در سطح وام است.

The aggregate research is reproducible. The audited public sources did not establish both availability of the actual month-six report and availability of the outcome label for the same case. This gap blocks loan-level model evaluation.

## راه‌حل | Solution

مرحلهٔ قابل اجرا، آماده‌سازی و اعتبارسنجی نمونهٔ زمان‌دارِ مجاز است. پژوهشگر باید برای هر ورودی، ماه فعالیت، نسخه و زمان دسترسی را به شاهد منبع وصل کند. خروجی این مرحله گزارش تجمیعی با شمارش ورودی‌ها، خطاها، موارد فاقد شاهد و تصمیم مستند دربارهٔ امکان ارزیابی است. گزارش موجود و شواهد منبع برای بازبینی مستقل حفظ می‌شوند.

The actionable slice is to prepare and validate an authorized timestamped sample. The researcher traces activity month, version, and availability for each input back to source evidence. The output is an aggregate report with input counts, violations, cases missing evidence, and a documented decision on whether evaluation can proceed. Preserve the existing research reports and source evidence for independent reproduction.

پس از تأیید داده، ارزیابی تاریخی در سطح وام طبق پروتکل زمان‌دار انجام می‌شود. دموی آفلاین بازبینی انسانی با دادهٔ ساختگی، برگشت پرداخت در `ACS-001` و تعارض نسخه‌های امضاشدهٔ توافق در `ACS-002` را پوشش می‌دهد. کارشناس وضعیت پرونده را در تاریخ بازبینی می‌بیند و با استناد به شواهد تصمیم می‌گیرد.

After source approval, evaluate the historical loan-level outcome under the time-aware protocol. The offline human-review demo uses synthetic data to cover a payment reversal in `ACS-001` and conflicting signed agreements in `ACS-002`. The reviewer sees the case as of the selected review date and uses the evidence to make a decision.

## داستان‌های کاربر | User Stories

1. به‌عنوان پژوهشگر، می‌خواهم منشأ، نسخه، تاریخ دریافت و اثرانگشت هر منبع را داشته باشم تا دادهٔ استفاده‌شده قابل شناسایی باشد.

   As a researcher, I want each source's provenance, version, retrieval date, and digest so that the input can be identified.
2. به‌عنوان متولی داده، می‌خواهم شناسهٔ مستعار وام و اصلاح جدا باشند تا اتصال نسخه‌ها دقیق و انتقال داده محدود بماند.

   As a data custodian, I want separate pseudonymous loan and modification IDs so that records join accurately with limited data transfer.
3. به‌عنوان پژوهشگر، می‌خواهم ماه فعالیت به همان نسخهٔ گزارش وصل باشد تا ورودی ماه ششم را مشخص کنم.

   As a researcher, I want the activity month linked to the same report version so that I can identify the month-six input.
4. به‌عنوان پژوهشگر، می‌خواهم زمان رخداد و زمان اولین دسترسی به نسخه را جدا داشته باشم تا دادهٔ دیررس را تشخیص دهم.

   As a researcher, I want separate event and first-availability times so that I can identify late data.
5. به‌عنوان پژوهشگر، می‌خواهم نسخهٔ اصلاحی به نسخهٔ قبلی وصل باشد تا بتوانم مقدار قابل مشاهده در برش را بازسازی کنم.

   As a researcher, I want corrected versions linked to their predecessors so that I can reconstruct what was visible at cutoff.
6. به‌عنوان پژوهشگر، می‌خواهم فعال بودن اصلاح در پایان ماه ششم با شاهد همان زمان احراز شود تا جامعهٔ ارزیابی درست باشد.

   As a researcher, I want active status at month six substantiated with contemporaneous evidence so that the evaluation cohort is valid.
7. به‌عنوان پژوهشگر، می‌خواهم تاریخ سررسید آخرین قسط کامل اعمال‌شده از تاریخ واریز و دورهٔ فعالیت متمایز باشد تا هر تاریخ را درست تفسیر کنم.

   As a researcher, I want the last applied full installment's due date distinguished from posting date and activity period so that I can interpret each date correctly.
8. به‌عنوان پژوهشگر، می‌خواهم ردیف مفقود، گزارش‌نشده، تکراری و متعارض جداگانه شمارش شوند تا فقدان گزارش را با رفتار پرداخت اشتباه نگیرم.

   As a researcher, I want missing, unreported, duplicate, and conflicting rows counted separately so that absence of a report is interpreted correctly.
9. به‌عنوان پژوهشگر، می‌خواهم حداقل یک نمونهٔ مجاز تا منبع اصلی قابل ردیابی باشد تا پیش از پردازش گروه‌های کامل، قابلیت استفادهٔ منبع را بسنجیم.

   As a researcher, I want at least one authorized sample traceable to its source so that I can judge feasibility before processing full cohorts.
10. به‌عنوان پژوهشگر، می‌خواهم خروج `Disqualified` و زمان دسترسی به برچسب آن مشخص باشد تا پیامد را در پنجرهٔ درست بسنجم.

    As a researcher, I want the `Disqualified` event and its label-availability time so that I can measure the outcome within the correct window.
11. به‌عنوان پژوهشگر، می‌خواهم تسویه، سانسور و مشاهدهٔ کامل بدون رخداد جدا بمانند تا نرخ پیامد بر مبنای پیگیری معتبر باشد.

    As a researcher, I want payoff, censoring, and complete event-free follow-up kept distinct so that outcome rates reflect valid follow-up.
12. به‌عنوان بازبین داده، می‌خواهم یک وام در بیش از یک بخش نباشد تا وابستگی اصلاح‌های همان وام ارزیابی را مخدوش نکند.

    As a data reviewer, I want each loan confined to one partition so that related modifications cannot contaminate the evaluation.
13. به‌عنوان بازبین داده، می‌خواهم زمان دسترسی آخرین برچسب هر بخش پیش از اولین برش بخش بعد باشد تا ارزیابی ترتیب زمانی را رعایت کند.

    As a data reviewer, I want every partition's final label-availability time to precede the next partition's first cutoff so that evaluation respects chronology.
14. به‌عنوان پژوهشگر، می‌خواهم موارد بلااستفاده و دلیل هر دسته در گزارش باشند تا بدانم کمبود شواهد کجاست.

    As a researcher, I want excluded cases counted by reason so that evidence gaps can be located.
15. به‌عنوان پژوهشگر، می‌خواهم پوشش به تفکیک ماه اثر و بخش زمانی گزارش شود تا دربارهٔ آمادگی کل داده تصمیم بگیرم.

    As a researcher, I want coverage by effective month and partition so that I can decide whether the full dataset is ready.
16. به‌عنوان بازبین مستقل، می‌خواهم نتایج تجمیعی قبلی و اختلاف حل‌نشدهٔ گزارش خزانه‌داری حفظ شوند تا بتوانم ادعا را بازتولید کنم.

    As an independent reviewer, I want the prior aggregate results and unresolved Treasury discrepancy preserved so that I can reproduce the claim.
17. به‌عنوان پژوهشگر، می‌خواهم پس از احراز داده، خط پایه و روش مقایسه پیش از آزمون مشخص شوند تا برآورد عملکرد قابل تفسیر باشد.

    As a researcher, I want the baseline and comparison method fixed before testing once data are qualified so that performance estimates remain interpretable.
18. به‌عنوان پژوهشگر، می‌خواهم نتایج کالیبراسیون، خطا و عدم‌قطعیت گزارش شوند تا ارزیابی بر یک عدد متکی نباشد.

    As a researcher, I want calibration, error, and uncertainty reported so that evaluation does not rest on a single score.
19. به‌عنوان مالک پروژه، می‌خواهم فقط کد، مستندات و آمار تجمیعی منتشر شوند تا ریزداده و مکاتبات خصوصی بیرون از مخزن بمانند.

    As a project owner, I want publication limited to code, documentation, and aggregate evidence so that raw data and private correspondence stay outside the repository.
20. به‌عنوان کارشناس در دمو، می‌خواهم نسخهٔ معتبر توافق و شواهد تأیید آن را در تاریخ بررسی ببینم تا علت انتخاب نسخه روشن باشد.

    As a reviewer in the demo, I want the applicable agreement and its supporting evidence as of the review date so that I can explain the version selected.
21. به‌عنوان کارشناس در دمو، می‌خواهم آخرین قسط کاملِ اعمال‌شده و برگشت‌های پرداخت را ببینم تا پرداخت برگشتی را در نتیجهٔ پرونده لحاظ کنم.

    As a reviewer in the demo, I want to see the last full applied installment and payment reversals so that I can account for reversals in the case result.
22. به‌عنوان کارشناس در دمو، می‌خواهم تعارض توافق یا برگشت پرداخت همراه با دلیل و نسخهٔ قاعده ارجاع شود تا بررسی قابل پیگیری باشد.

    As a reviewer in the demo, I want agreement conflicts and payment reversals flagged for review with a reason and rule version so that the review is traceable.
23. به‌عنوان کارشناس در دمو، می‌خواهم نتیجهٔ بررسی و اصلاحیه ثبت شود تا سابقهٔ تصمیم‌گیری و تغییرات قابل بازبینی بماند.

    As a reviewer in the demo, I want the decision and any correction recorded so that the review history can be audited.

24. به‌عنوان کارشناس، می‌خواهم نمای ۱۳ ژوئن پروندهٔ `ACS-002` هر دو نسخهٔ متعارض را نشان دهد تا بدانم چرا آخرین قسط تأییدشده مربوط به مه است.

    As a reviewer, I want the June 13 view of `ACS-002` to show both competing versions so that I can see why May remains the last confirmed installment.
25. به‌عنوان کارشناس، می‌خواهم در نمای ۱۷ ژوئن سند `DOC-01` را از خط زمانی باز کنم تا پیش از انتخاب نسخهٔ دوم، مدرک امضاشده را بررسی کنم.

    As a reviewer, I want to open `DOC-01` from the timeline in the June 17 view so that I can examine the signed evidence before choosing version 2.
26. به‌عنوان کارشناس، می‌خواهم پرونده تا زمان ثبت تصمیم مستند در وضعیت بررسی بماند تا دریافت سند به‌تنهایی قسط ژوئن را تأیید نکند.

    As a reviewer, I want the case to remain pending until I save a documented decision so that receipt of evidence alone cannot confirm the June installment.
27. به‌عنوان کارشناس، می‌خواهم پس از تأیید نسخهٔ دوم، آخرین قسط تأییدشده همراه با سررسید، مبلغ و تاریخ ثبت پرداخت به‌روز شود تا بتوانم نتیجه را با دفتر پرداخت تطبیق دهم.

    As a reviewer, I want the last confirmed installment to update with its due date, amount, and posting date after I confirm version 2 so that I can reconcile the result with the payment ledger.
28. به‌عنوان کارشناس، می‌خواهم اصلاحیه در کنار تصمیم اولیه و با پیوند به سند ثبت شود تا سابقهٔ بررسی حفظ شود.

    As a reviewer, I want the revision recorded alongside the original decision with a link to the evidence so that I can audit the review history.
29. به‌عنوان کارشناس، می‌خواهم پس از بازکردن دوبارهٔ همان نسخهٔ محلی دمو در همان پروفایل مرورگر، هر دو ثبت را ببینم تا سابقهٔ بررسی را بازیابی کنم.

    As a reviewer, I want to see both entries after reopening the same local copy of the demo in the same browser profile so that I can recover the review history.
30. به‌عنوان کارشناس، می‌خواهم تصمیم ۱۷ ژوئن بر نمای ۱۳ ژوئن اثر نگذارد تا بتوانم آنچه در تاریخ قبلی قابل احراز بود بازبینی کنم.

    As a reviewer, I want the June 17 decision to leave the June 13 view intact so that I can review what could be established on the earlier date.

## تصمیم‌های پیاده‌سازی | Implementation Decisions

- **مرحلهٔ فعلی.** ورود نمونهٔ مجاز را به ورودی‌های اعتبارسنجی فرادادهٔ موجود وصل کنید. بررسی منشأ و وضعیت فعال در نمونه پیش از تبدیل به آن ورودی‌ها انجام می‌شود. عبور از کنترل سازگاری فراداده به‌تنهایی اصالت یا کامل بودن منبع را ثابت نمی‌کند.
- **هویت و زمان.** شناسه‌ها برای اتصال و تفکیک‌اند. برش در ابتدای ماه هفتم و انحصاری برای ویژگی است. هر نسخهٔ ویژگی به‌همراه آفست زمانی صریح ثبت می‌شود و زمان رویداد و دسترسی‌اش باید پیش از برش باشند. تاریخ سررسید، تاریخ وقوع یا ثبت پرداخت تلقی نمی‌شود.
- **جامعه و پیامد.** اصلاحات دائمی گروه اول هامپ که بر مبنای شاهد موجود در برش فعال‌اند وارد جامعه می‌شوند. پیامد، خروج مستند `Disqualified` از ابتدای ماه هفتم تا پیش از ابتدای ماه سیزدهم است. تسویه رویداد رقیب است. خروج دیگر یا پیگیری ناقص سانسور می‌شود. تبدیل به «بدون رخداد» تنها با شاهد پیگیری تا پایان پنجره مجاز است.
- **تفکیک.** ژوئیهٔ ۲۰۰۹ تا ژوئن ۲۰۱۲ برای آموزش، نیمهٔ دوم ۲۰۱۲ حذف تقویمی، ۲۰۱۳ برای اعتبارسنجی، ۲۰۱۴ فاصله و ۲۰۱۵ تا ۲۰۱۷ برای آزمون در نظر گرفته می‌شوند. اولین برش اعتبارسنجی ۱ ژوئیهٔ ۲۰۱۳ است. آخرین زمان دسترسی به برچسب‌های بخش قبلی باید پیش از اولین برش بخش بعد باشد. اگر شواهد تأخیر نشان دهند، دامنهٔ آموزش دوباره محدود می‌شود.
- **ردیابی و انتشار.** مدارک منبع، ریزداده و مکاتبات بیرون از مخزن می‌مانند. هر مرحلهٔ بررسی‌شده با شرح تغییر، شواهد و محدودیت‌ها در یک کامیت ثبت می‌شود. خروجی عمومی شامل دادهٔ تجمیعی و مشخصات بازتولید است.
- **ارزیابی مشروط.** پس از احراز منبع و تأیید پوشش، ابتدا خط پایهٔ سادهٔ ماه ششم و سپس روش زمان‌گسسته با روند پرداخت و وضعیت گزارش بررسی می‌شود. انتخاب ویژگی و تنظیم مدل در آموزش و اعتبارسنجی انجام می‌شود و آزمون نهایی قفل می‌ماند. معیارهای پیشنهادی طرح، از جمله امتیاز بریر، پیش از باز کردن آزمون تثبیت می‌شوند. آستانهٔ بهبود یا نتیجهٔ مدل هنوز تعیین یا مشاهده نشده است.
- **دموی بازبینی.** نتیجهٔ پرونده از نسخه‌های توافق، رویدادهای دفتر پرداخت و شواهد موجود تا تاریخ بازبینی به دست می‌آید. در `ACS-002`، نسخه‌های دوم و سوم تاریخ اجرای یکسان و مبلغ‌های متفاوت دارند. سند `DOC-01` که ۱۶ ژوئن دریافت شد، `AGR-04` (نسخهٔ دوم) را معتبر می‌داند و `AGR-05` (نسخهٔ سوم) را پس می‌گیرد. ثبت تأیید نسخهٔ دوم همراه با یادداشت، قسط ۱ ژوئن به مبلغ ۱٬۳۵۰ دلار را در نمای ۱۷ ژوئن تأیید می‌کند.
- **سابقهٔ تصمیم.** ثبت دوباره، اصلاحیه‌ای به سابقه اضافه می‌کند. هر ثبت به پرونده و تاریخ بازبینی تعلق دارد و تصمیم حل تعارض، مرجع سند را حفظ می‌کند. بازیابی پس از بازکردن دوباره به ذخیره‌سازی مرورگر وابسته است. در صورت در دسترس نبودن آن، رابط اعلام می‌کند که ثبت فقط در همان زبانه می‌ماند.

- **Current slice.** Feed an authorized sample into the existing metadata validation interface. Verify source provenance and active status before conversion. Passing metadata consistency alone does not establish origin or completeness.
- **Identity and time.** IDs support joins and partitioning. The feature cutoff is the exclusive start of month seven. Record explicit offsets, and require feature event and availability times before cutoff. A due date is distinct from the time a payment occurred or posted.
- **Cohort and outcome.** Include permanent Tier 1 HAMP modifications supported as active at cutoff. The endpoint is documented `Disqualified` from the start of month seven up to the exclusive start of month thirteen. Payoff competes with it. Other exits and incomplete follow-up are censored. Event-free status requires evidence through the full window.
- **Partitioning.** Train on July 2009–June 2012, hold out the second half of 2012, validate on 2013, leave a 2014 gap, and test on 2015–2017. The first validation cutoff is July 1, 2013. Earlier labels must be available before the next partition's first cutoff. Move the training boundary earlier if actual availability requires it.
- **Traceability and publication.** Keep source records, microdata, and correspondence outside the repository. Record each verified stage in a commit with what changed, the evidence, and remaining limitations. Publish aggregate results and reproduction instructions.
- **Conditional evaluation.** Once provenance and coverage are established, compare a simple month-six baseline with a discrete-time model using payment and reporting history. Select features and tune with training and validation only and keep the test locked. Finalize proposed metrics, including the Brier score, before opening the test. No improvement threshold or evaluation result has been approved or observed.
- **Review demo.** Versioned agreements, payment ledger events, and evidence available by the review date determine the case findings. In `ACS-002`, versions 2 and 3 share an effective date and have different amounts. `DOC-01`, received June 16, establishes `AGR-04` (version 2) as applicable and withdraws `AGR-05` (version 3). Saving the version 2 confirmation with a note confirms the $1,350 June 1 installment in the June 17 view.
- **Decision history.** Saving again appends a revision. Each entry is scoped to its case and review date, and a conflict resolution keeps the evidence reference. Restoration after reopening depends on browser storage. When it is unavailable, the interface reports that the entry stays in the current tab.

## تصمیم‌های آزمون | Testing Decisions

- سطح اصلی آزمون مسیر پژوهش از ورودی نمونه و شواهد آن تا وضعیت خروج و گزارش تجمیعی است. از ورودی اعتبارسنج موجود استفاده کنید و جزئیات داخلی SQL و ترتیب فراخوانی‌ها را در آزمون تثبیت نکنید. آزمون‌های ساختگی موجودِ مرز زمانی، تکرار شناسه و زمان برچسب، سابقهٔ این روش هستند.
- پذیرش قطعهٔ فعلی نیازمند نتیجهٔ قابل توضیح برای ورودی معتبر، ورودی نامعتبر و شاهد ناقص است. ورودی یا برچسب دیررس، نشت شناسه میان بخش‌ها، منفی زودرس، یا نسخهٔ فاقد تأیید منبع باید در گزارش به‌روشنی مشخص شود. در خروجی عمومی شناسهٔ پرونده نمایش داده نمی‌شود.
- اجرای مجدد بازسازی عمومی باید همان ۳۰ سلول و جدول ۱۰۲ گروه ماهانه را تولید کند. اختلاف ماه دوازدهم گروه دوم در سال ۲۰۱۷ باید در گزارش قابل مشاهده بماند. راستی‌آزمایی دادهٔ عمومی و آزمون ساختگی، معیارهای پذیرش مستقل دارند.
- آزمون پذیرش دمو از رابط مرورگر انجام می‌شود. در `ACS-002` نماهای ۱۳ و ۱۷ ژوئن را پیش از ثبت مقایسه کنید، `DOC-01` را باز کنید، تصمیم و اصلاحیه را ثبت کنید و پس از بستن مرورگر و بازکردن دوباره از همان مسیر، سابقه را بررسی کنید. در مقایسهٔ این دو نما، قسط ژوئن فقط در نمای ۱۷ ژوئن و پس از ثبت تصمیم باید تأیید شود. برای پذیرش اجرای آفلاین، دمو را مستقیماً از مسیر فایل محلی باز کنید. آزمون‌های موجود قواعد، منطق تاریخ شواهد و برگشت پرداخت را از طریق رابط ارزیابی پرونده می‌سنجند.

- Test the research slice at its external boundary, from sample and evidence intake to exit status and aggregate report. Use the existing validator interface and avoid pinning SQL internals or call order. Existing synthetic tests of time boundaries, identity separation, and label timing are the precedent.
- Acceptance of the current slice requires an explainable result for valid input, invalid input, and insufficient evidence. The report identifies late inputs or labels, identity overlap, premature negatives, and unverified source versions. Published output contains no case identifiers.
- Re-running public reconstruction should yield the same 30 cells and 102 monthly cohorts. The unresolved Tier 2 month-twelve difference for 2017 remains visible. Public-data verification and synthetic controls have independent acceptance checks.
- Run demo acceptance through the browser UI. In `ACS-002`, compare June 13 and June 17 before saving, open `DOC-01`, save a decision and a revision, then close the browser and reopen the same path to check the history. Of these two views, only June 17 should confirm the June installment, and only after saving the decision. Offline acceptance requires opening the demo directly from its local file path. The existing rule suite exercises evidence dates and payment reversals through the case evaluation interface.

## خارج از دامنه | Out of Scope

آموزش یا آزمون مدل با ریزدادهٔ فاقد شواهد زمانی، تصمیم اعتباری یا اقدام وصول خودکار، تماس با وام‌گیرنده، ورود دادهٔ مشتری به مخزن، استقرار عملیاتی، پایلوت با شریک و ادعا دربارهٔ بهبود وصول یا انطباق مقرراتی خارج از دامنهٔ کار فعلی‌اند. سناریوهای اعتراض و رویداد تکراری در این مرحلهٔ دمو پوشش داده نمی‌شوند.

Model development or testing with unverified timing, automated credit or collection actions, borrower contact, customer data in the repository, production deployment, a partner pilot, and claims of improved recovery or regulatory compliance are outside the current scope. Dispute and repeated-event scenarios are outside this demo slice.

## یادداشت‌های تکمیلی | Further Notes

برچسب آمادگی این سند برای کارهای مشخص‌شدهٔ آماده‌سازی و راستی‌آزمایی است. ارزیابی مدل به دریافت شاهد بیرونی وابسته است. تا زمان تدوین این سند، نمونهٔ مناسب برای اثبات زمان دسترسی دریافت نشده بود. اگر منبع تنها بخشی از زمان‌ها را تأیید کند، نتیجهٔ نمونه باید با همان دامنه گزارش شود.

The readiness label covers the specified preparation and verification work. Model evaluation depends on external source evidence. At drafting, no suitable timestamped sample had been received. If a source verifies only some timestamps, report the sample result with that limited scope.

در کامیت `296882d`، نتیجهٔ هر ۱۶ آزمون خودکار موفق بود. در آزمون Chromium از طریق `localhost`، تصمیم و اصلاحیه پس از بستن و بازکردن دوباره در همان پروفایل باقی ماندند و قسط ژوئن فقط در نمای ۱۷ ژوئن پس از ثبت تصمیم تأیید شد. سیاست محیط اجرای مستقیم `file://` را مسدود کرد. بررسی ماندگاری از مسیر مستقیم فایل همچنان در انتظار اجراست.

At commit `296882d`, all 16 automated tests passed. In Chromium over `localhost`, the decision and revision persisted after closing and reopening with the same profile, and June was confirmed only in the June 17 view after saving. The environment blocked direct `file://` navigation. Persistence when opening the file directly still needs verification.

[گزارش وضعیت پژوهش / Research status](../../docs/research/hamp-research-status.md) · [پروتکل زمان‌دار / Time-aware protocol](../../docs/research/hamp-asof-protocol.md) · [جدول پوشش / Coverage](../../docs/research/hamp-monthly-evaluation-coverage.md) · [اعتبارسنج فراداده / Metadata checks](../../docs/research/hamp-evaluation-readiness.md) · [بازسازی تاریخی / Historical reconstruction](../../docs/research/hamp-historical-reconstruction.md)
