## اسکیل‌های عامل | Agent skills

### زبان مستندات | Documentation language

همهٔ توضیحات و دستورهای این فایل را به هر دو زبان فارسی و انگلیسی بنویس. متن فارسی را ابتدا بیاور و هر دو نسخه را هنگام ویرایش هماهنگ نگه دار.

Write every explanation and instruction in this file in both Persian and English. Put the Persian text first and keep both versions in sync when editing.

### زبان و چیدمان گفتگو | Chat language and layout

همهٔ پیام‌هایی را که در گفتگوهای این پروژه برای کاربر می‌فرستی، از جمله پیام‌های پیشرفت، سؤال‌ها و پاسخ نهایی، به فارسی بنویس. اولین واژهٔ قابل‌مشاهدهٔ هر پیام فارسی باشد. متن فارسی را راست‌به‌چپ و راست‌چین نمایش بده و در صورت پشتیبانی رابط، از تنظیم جهت و تراز آن استفاده کن.

Write every user-facing message in this project's chats in Persian, including progress updates, questions, and final replies. Start each message with a Persian word. Display Persian text right-to-left and align it to the right, using the interface's direction and alignment settings where supported.

### پیگیری تسک‌ها | Issue tracker

مشخصات و تسک‌ها را در فایل‌های محلی Markdown در `.scratch/` ثبت کن. [روش پیگیری تسک‌ها](docs/agents/issue-tracker.md)

Track specs and issues in local Markdown under `.scratch/`. See [issue tracker conventions](docs/agents/issue-tracker.md).

### برچسب‌های دسته‌بندی تسک‌ها | Triage labels

از پنج نقش پیش‌فرض برای دسته‌بندی تسک‌ها استفاده کن. [راهنمای برچسب‌ها](docs/agents/triage-labels.md)

Use the five default roles. See [triage labels](docs/agents/triage-labels.md).

### مستندات دامنه | Domain docs

واژه‌نامه را در ریشهٔ پروژه قرار بده و تصمیم‌های معماری را در `docs/adr/` ثبت کن. [راهنمای مستندات دامنه](docs/agents/domain.md)

Use one root glossary and keep architecture decisions in `docs/adr/`. See [domain guidance](docs/agents/domain.md).

### ثبت و انتشار مراحل | Stage commits and publishing

کار هر مرحله را پس از بررسی در یک کامیت جداگانه ثبت کن. در متن کامیت تغییرات، دلیل، روش راستی‌آزمایی و محدودیت باقی‌مانده را توضیح بده. مرحلهٔ بررسی‌شده را در مخزن اختصاصی پروژه در حساب `mym1359` منتشر کن. برای انتشار از کد، گزارش‌ها و داده‌های تجمیعی استفاده کن. ریزداده‌ها و منابع خصوصی را بیرون از مخزن نگه دار.

After verifying each project stage, record it in a separate commit. Explain what changed, why, how it was verified, and any remaining limitations in the commit body. Push each verified stage to this project's dedicated repository under `mym1359`. Publish code, reports, and aggregate data. Keep loan-level inputs and private source material outside the repository.
