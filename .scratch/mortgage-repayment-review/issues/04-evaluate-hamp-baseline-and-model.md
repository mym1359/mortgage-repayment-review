# 04. ارزیابی خط پایه و مدل زمان‌گسسته | Evaluate the HAMP baseline and discrete-time model

Status: ready-for-agent

Blocked by: 03

## هدف | What to build

پس از تأیید پوشش در تسک ۰۳، خط پایهٔ ماه ششم را با مدل زمان‌گسسته‌ای مقایسه کنید که از روند پرداخت و وضعیت گزارش استفاده می‌کند. نتیجه باید عملکرد و محدودیت‌های مقایسه را برای بازبینی مستقل روشن کند.

Once ticket 03 establishes coverage, compare the month-six baseline with a discrete-time model that uses payment history and reporting status. Report performance and comparison limits for independent review.

## معیارهای پذیرش | Acceptance criteria

- [ ] خط پایه، روش مقایسه و معیارها از جمله امتیاز بریر پیش از بازکردن مجموعهٔ آزمون تثبیت شوند. / Fix the baseline, comparison method, and metrics, including the Brier score, before opening the test partition.
- [ ] انتخاب ویژگی و تنظیم مدل فقط در آموزش و اعتبارسنجی انجام شود. آزمون نهایی تا تثبیت روش قفل بماند. / Select features and tune the model with training and validation only. Keep the final test locked until the method is fixed.
- [ ] خطا، کالیبراسیون و عدم‌قطعیت هر دو روش را با دستور بازتولید و محدودیت‌های ارزیابی گزارش کنید. آمار منتشرشده تجمیعی باشد. / Report error, calibration, and uncertainty for both approaches, along with reproduction instructions and evaluation limits. Publish aggregate statistics.

[مشخصات پروژه / Project spec](../spec.md)
