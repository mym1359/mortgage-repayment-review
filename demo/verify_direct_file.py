"""Verify the ACS-002 offline workflow by opening the demo directly in Chromium."""

from pathlib import Path
from tempfile import TemporaryDirectory

from playwright.sync_api import expect, sync_playwright


DEMO_URL = Path(__file__).with_name("index.html").resolve().as_uri()
DECISION = "Resolve conflict · Confirm version 2"
INITIAL_NOTE = "DOC-01 confirms AGR-04 as the applicable agreement."
REVISION_NOTE = "DOC-01 was received June 16. PAY-04 was posted June 5."


def review_date(page, day):
    page.locator("fieldset label").filter(has_text=f"Jun {day}, 2025").click()
    expect(page.locator("#evidence-caption")).to_contain_text(f"Recorded through Jun {day}, 2025")


def open_case(context):
    page = context.pages[0]
    page.goto(DEMO_URL)
    expect(page).to_have_url(DEMO_URL)
    page.get_by_label("Review case").select_option("ACS-002")
    expect(page.locator("#case-id")).to_have_text("Case ACS-002")
    return page


def pending(page):
    expect(page.locator("#agreement-value")).to_have_text("Agreement unresolved")
    expect(page.locator("#payment-value")).to_have_text("May 1, 2025")
    expect(page.locator("#payment-detail")).to_contain_text("June installment pending")
    expect(page.locator("#decision-history li")).to_have_count(0)


def confirmed(page):
    expect(page.locator("#agreement-value")).to_have_text("Version 2")
    expect(page.locator("#payment-value")).to_have_text("Jun 1, 2025")
    expect(page.locator("#payment-detail")).to_have_text("$1,350.00 · Posted Jun 5, 2025")


def save(page, note):
    page.get_by_label("Decision", exact=True).select_option(label=DECISION)
    page.get_by_label("Review notes").fill(note)
    page.get_by_role("button", name="Save decision").click()
    expect(page.get_by_role("status")).to_have_text("Decision saved in this browser.")


def verify_history(page):
    entries = page.locator("#decision-history li")
    expect(entries).to_have_count(2)
    expect(entries.first.locator("strong")).to_have_text("Revision 1 · " + DECISION)
    expect(entries.first.locator("p")).to_have_text(REVISION_NOTE)
    expect(entries.last.locator("strong")).to_have_text(DECISION)
    expect(entries.last.locator("p")).to_have_text(INITIAL_NOTE)
    for entry in entries.all():
        expect(entry.get_by_role("link", name="Evidence DOC-01")).to_have_attribute("href", "#DOC-01")


def main():
    with TemporaryDirectory() as profile, sync_playwright() as playwright:
        context = playwright.chromium.launch_persistent_context(profile)
        try:
            page = open_case(context)
            print("Direct Chromium URL:", page.url, flush=True)
            version = context.new_cdp_session(page).send("Browser.getVersion")["product"]
            print("Chromium version:", version, flush=True)
            review_date(page, 13)
            pending(page)
            expect(page.locator("#DOC-01")).to_have_count(0)

            review_date(page, 17)
            pending(page)
            page.get_by_role("link", name="View confirmation").click()
            expect(page).to_have_url(DEMO_URL + "#DOC-01")
            expect(page.locator("#DOC-01")).to_contain_text("Confirms AGR-04")
            pending(page)
            save(page, INITIAL_NOTE)
            confirmed(page)
            save(page, REVISION_NOTE)
            verify_history(page)
            page.close()
        finally:
            context.close()

        context = playwright.chromium.launch_persistent_context(profile)
        try:
            page = open_case(context)
            review_date(page, 17)
            confirmed(page)
            verify_history(page)
            review_date(page, 13)
            pending(page)
            expect(page.locator("#DOC-01")).to_have_count(0)
            print("Decision and revision survived reopening the same file in the same profile.")
            print("Of June 13 and June 17, only June 17 confirms the June installment after saving.")
        finally:
            context.close()


if __name__ == "__main__":
    main()
