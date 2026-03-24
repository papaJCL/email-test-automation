import pytest
from pages.inbox_page import InboxPage
from pages.spam_page import SpamPage


@pytest.fixture
def inbox_page():
    """Creates a fresh inbox page object for each test."""
    return InboxPage()


@pytest.fixture
def spam_page():
    """Creates a fresh spam page object for each test."""
    return SpamPage()


# Happy Paths

def test_mark_email_as_spam_ui(inbox_page, spam_page):
    """Req_42 UI: User marks an email as spam, verify it moves to spam folder."""
    inbox_page.navigate_to_inbox()
    inbox_page.mark_as_spam("Suspicious Email")

    # Verify email is no longer in the inbox
    assert inbox_page.is_email_present("Suspicious Email") == False

    # Verify email is now in the spam folder
    spam_page.navigate_to_spam()
    assert spam_page.is_email_present("Suspicious Email") == True


def test_flagged_address_auto_routes_to_spam_ui(inbox_page, spam_page):
    """Req_42 UI: New email from a flagged address automatically shows in spam."""
    # First mark an email from the sender as spam
    inbox_page.navigate_to_inbox()
    inbox_page.mark_as_spam("First Email From Spammer")

    # When a new email arrives from the same sender
    # it should automatically route to spam, not the inbox
    # Note: In a real system we would wait for or simulate
    # a new incoming email from the same sender here
    assert inbox_page.is_email_present("Second Email From Spammer") == False

    spam_page.navigate_to_spam()
    assert spam_page.is_email_present("Second Email From Spammer") == True


# Edge Cases

def test_unmark_spam_returns_to_inbox_ui(inbox_page, spam_page):
    """Req_42 UI: User unmarks an address, new emails go back to inbox."""
    # Mark as spam first
    inbox_page.navigate_to_inbox()
    inbox_page.mark_as_spam("Falsely Flagged Email")

    # Now unmark it from the spam folder
    spam_page.navigate_to_spam()
    spam_page.unmark_as_spam("Falsely Flagged Email")

    # Verify the email is back in the inbox
    assert spam_page.is_email_present("Falsely Flagged Email") == False

    inbox_page.navigate_to_inbox()
    assert inbox_page.is_email_present("Falsely Flagged Email") == True


def test_flagged_address_in_cc_ui(inbox_page, spam_page):
    """Req_42 UI: Email with a flagged address in Cc stays in inbox."""
    # Mark a sender as spam
    inbox_page.navigate_to_inbox()
    inbox_page.mark_as_spam("Direct Spam Email")

    # A different email arrives where the flagged address is
    # in the Cc line, not the sender
    # Note: This should stay in the inbox since the actual
    # sender is not flagged. Only the Cc contains the spam address.
    assert inbox_page.is_email_present("Group Email With Spammer In Cc") == True

    spam_page.navigate_to_spam()
    assert spam_page.is_email_present("Group Email With Spammer In Cc") == False


def test_empty_spam_folder_ui(inbox_page, spam_page):
    """Req_42 UI: Spam folder is empty when no emails have been flagged."""
    spam_page.navigate_to_spam()

    assert spam_page.get_email_count() == 0


def test_multiple_spam_emails_ui(inbox_page, spam_page):
    """Req_42 UI: Multiple emails marked as spam all show in spam folder."""
    inbox_page.navigate_to_inbox()
    inbox_page.mark_as_spam("Spam Email 1")
    inbox_page.mark_as_spam("Spam Email 2")
    inbox_page.mark_as_spam("Spam Email 3")

    # Verify none of them are in the inbox
    assert inbox_page.is_email_present("Spam Email 1") == False
    assert inbox_page.is_email_present("Spam Email 2") == False
    assert inbox_page.is_email_present("Spam Email 3") == False

    # Verify all three are in the spam folder
    spam_page.navigate_to_spam()
    assert spam_page.is_email_present("Spam Email 1") == True
    assert spam_page.is_email_present("Spam Email 2") == True
    assert spam_page.is_email_present("Spam Email 3") == True
    assert spam_page.get_email_count() == 3