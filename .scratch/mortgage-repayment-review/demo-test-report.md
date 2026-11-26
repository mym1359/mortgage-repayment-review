# گزارش آزمون دموی آفلاین | Offline demo test report

نسخهٔ آزموده‌شده `6aab465` است. آزمون‌ها روی یک پروندهٔ ساختگی انجام شدند.

Tested revision `6aab465` with the single synthetic case.

| بررسی / Check | نتیجه / Result |
| --- | --- |
| قبل از برگشت / Before reversal | در ۱۱ ژوئن، نسخهٔ دوم توافق و قسط ژوئن معتبرند و ارجاعی بابت برگشت پرداخت وجود ندارد. / On June 11, agreement v2 applies, the June installment is confirmed, and there is no reversal referral. |
| بعد از برگشت / After reversal | در ۱۳ ژوئن، نسخهٔ دوم توافق معتبر است، قسط مه آخرین قسط تأییدشده است و برگشت ۱۲ ژوئن ارجاع انسانی را بر اساس قاعدهٔ `REV-1 v1.0` فعال می‌کند. / On June 13, agreement v2 still applies, May is the last confirmed installment, and the June 12 reversal triggers human review under `REV-1 v1.0`. |
| شواهد / Evidence | پیوندهای توافق، پرداخت و برگشت به رویدادهای درست اشاره می‌کنند. رویداد برگشت در نمای قبل از برگشت دیده نمی‌شود. / Agreement, payment, and reversal links target the correct entries. The earlier view excludes the reversal. |
| تصمیم کارشناس / Reviewer decision | یادداشت خالی رد شد. ثبت اصلاحیه تصمیم اول را حفظ کرد. پیش‌نویس‌ها، تصمیم‌ها و اصلاحیه‌ها به تاریخ بازبینی خود تعلق دارند. / Blank notes were rejected. A revision preserved the original decision. Drafts, decisions, and revisions stayed with their respective review dates. |
| ذخیره و بازیابی / Storage and restoration | رابط پس از راه‌اندازی دوباره با همان داده‌های ذخیره‌شده سابقه را بازیابی کرد. با حافظهٔ مسدود، رابط به‌درستی اعلام کرد که تصمیم فقط در همان زبانه نگه‌داری می‌شود. / The interface restored history when initialized with the same stored values. With storage blocked, it correctly reported that the decision would be kept in the current tab only. |

هر سه آزمون قواعد با `node --test demo/review.test.js` و هر نه آزمون پژوهشی با `python -m unittest discover -s research` موفق بودند. مسیر رابط در محیط شبیه‌سازی‌شدهٔ DOM با فایل‌های واقعی دمو و بدون درخواست شبکه بررسی شد. اتصال پیش‌نمایش به مرورگر به‌دلیل پایان مهلت راه‌اندازی برقرار نشد. ظاهر رابط و رفتار ذخیره‌سازی در اجرای مستقیم فایل در مرورگر همچنان نیاز به آزمون دارند.

All three rule tests passed with `node --test demo/review.test.js`, and all nine research tests passed with `python -m unittest discover -s research`. The interface workflow was tested in a DOM simulation using the actual demo files and no network requests. The preview relay timed out, so visual rendering and storage behavior when opening the file directly in a browser remain unverified.
