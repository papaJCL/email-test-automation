import pytest
from pages.compose_page import ComposePage
from pages.inbox_page import InboxPage


@pytest.fixture
def compose_page():
    """Creates a fresh compose page object for each test."""
    return ComposePage()


@pytest.fixture
def inbox_page():
    """Creates a fresh inbox page object for each test."""
    return InboxPage()


def compose_and_send(compose_page, to=None, cc=None, bcc=None, subject="Test Email", body="This is a test"):
    """
    Helper function that handles the full compose and send flow
    through the UI. Fills in only the fields that are provided.
    """
    compose_page.open_compose()

    if to:
        compose_page.fill_to_field(to)
    if cc:
        compose_page.fill_cc_field(cc)
    if bcc:
        compose_page.fill_bcc_field(bcc)

    compose_page.fill_subject(subject)
    compose_page.fill_body(body)
    compose_page.click_send()


def verify_email_received(inbox_page, subject="Test Email"):
    """Verifies that an email with the given subject shows up in the inbox."""
    inbox_page.navigate_to_inbox()
    assert inbox_page.is_email_present(subject) == True


def verify_email_not_received(inbox_page, subject="Test Email"):
    """Verifies that an email with the given subject does not show up in the inbox."""
    inbox_page.navigate_to_inbox()
    assert inbox_page.is_email_present(subject) == False


# Happy Paths

def test_send_to_only_ui(compose_page, inbox_page):
    """Req_159 UI: Send email with only the To field, verify it shows in inbox."""
    compose_and_send(
        compose_page,
        to=["recipient@example.com"],
        subject="To Only Test"
    )

    verify_email_received(inbox_page, "To Only Test")


def test_send_cc_only_ui(compose_page, inbox_page):
    """Req_159 UI: Send email with only the Cc field, verify it shows in inbox."""
    compose_and_send(
        compose_page,
        cc=["recipient@example.com"],
        subject="Cc Only Test"
    )

    verify_email_received(inbox_page, "Cc Only Test")


def test_send_bcc_only_ui(compose_page, inbox_page):
    """Req_159 UI: Send email with only the Bcc field, verify it shows in inbox."""
    compose_and_send(
        compose_page,
        bcc=["recipient@example.com"],
        subject="Bcc Only Test"
    )

    verify_email_received(inbox_page, "Bcc Only Test")


def test_send_to_and_cc_ui(compose_page, inbox_page):
    """Req_159 UI: Send email with To and Cc fields, verify it shows in inbox."""
    compose_and_send(
        compose_page,
        to=["recipient1@example.com"],
        cc=["recipient2@example.com"],
        subject="To and Cc Test"
    )

    verify_email_received(inbox_page, "To and Cc Test")


def test_send_to_and_bcc_ui(compose_page, inbox_page):
    """Req_159 UI: Send email with To and Bcc fields, verify it shows in inbox."""
    compose_and_send(
        compose_page,
        to=["recipient1@example.com"],
        bcc=["recipient2@example.com"],
        subject="To and Bcc Test"
    )

    verify_email_received(inbox_page, "To and Bcc Test")


def test_send_cc_and_bcc_ui(compose_page, inbox_page):
    """Req_159 UI: Send email with Cc and Bcc fields, verify it shows in inbox."""
    compose_and_send(
        compose_page,
        cc=["recipient1@example.com"],
        bcc=["recipient2@example.com"],
        subject="Cc and Bcc Test"
    )

    verify_email_received(inbox_page, "Cc and Bcc Test")


def test_send_to_cc_and_bcc_ui(compose_page, inbox_page):
    """Req_159 UI: Send email with all three fields, verify it shows in inbox."""
    compose_and_send(
        compose_page,
        to=["recipient1@example.com"],
        cc=["recipient2@example.com"],
        bcc=["recipient3@example.com"],
        subject="All Fields Test"
    )

    verify_email_received(inbox_page, "All Fields Test")


# Negative Paths

def test_send_no_recipients_ui(compose_page, inbox_page):
    """Req_159 UI: Send email with no recipients, verify error is shown."""
    compose_and_send(
        compose_page,
        subject="No Recipients Test"
    )

    # Verify an error message is displayed to the user
    error = compose_page.get_error_message()
    assert error is not None


def test_send_invalid_email_format_ui(compose_page, inbox_page):
    """Req_159 UI: Send email to invalid format, verify error is shown."""
    compose_and_send(
        compose_page,
        to=["notanemail"],
        subject="Invalid Format Test"
    )

    # Note: In a real system the UI would display a validation
    # error when the user enters an invalid email format.
    error = compose_page.get_error_message()
    assert error is not None


def test_send_unauthorized_sender_ui(compose_page, inbox_page):
    """Req_159 UI: Unauthorized user attempts to send, verify error is shown."""
    # Note: In a real system an unauthorized user would not
    # be able to access the compose page at all, or would see
    # an error when attempting to send. This test documents
    # that the UI should handle this scenario.
    compose_and_send(
        compose_page,
        to=["recipient@example.com"],
        subject="Unauthorized Test"
    )

    error = compose_page.get_error_message()
    assert error is not None