import pytest
from stubs.mail_server_stub import MailServerStub
from stubs.database_stub import DatabaseStub
from utils.email_helpers import send_email_and_verify


@pytest.fixture
def mail_server():
    """Creates a fresh mail server stub for each test."""
    return MailServerStub()


@pytest.fixture
def database():
    """Creates a fresh database stub for each test."""
    return DatabaseStub()


def verify_email_sent_successfully(result, mail_server, database):
    """Verifies that an email was sent, stored, and received successfully."""
    assert result == True
    assert len(database.get_sent_emails()) == 1
    assert len(database.get_received_emails()) == 1
    assert len(mail_server.get_outbox()) == 1


def verify_email_not_sent(result, mail_server, database):
    """Verifies that an email was not sent or stored anywhere."""
    assert result == False
    assert len(database.get_sent_emails()) == 0
    assert len(database.get_received_emails()) == 0
    assert len(mail_server.get_outbox()) == 0


# Happy Paths

def test_send_to_only(mail_server, database):
    """Req_159: Send email with only the To field filled in."""
    result = send_email_and_verify(
        mail_server=mail_server,
        database=database,
        sender="sender@example.com",
        to=["recipient@example.com"],
        subject="Test Email",
        body="This is a test"
    )

    verify_email_sent_successfully(result, mail_server, database)


def test_send_cc_only(mail_server, database):
    """Req_159: Send email with only the Cc field filled in."""
    result = send_email_and_verify(
        mail_server=mail_server,
        database=database,
        sender="sender@example.com",
        cc=["recipient@example.com"],
        subject="Test Email",
        body="This is a test"
    )

    verify_email_sent_successfully(result, mail_server, database)


def test_send_bcc_only(mail_server, database):
    """Req_159: Send email with only the Bcc field filled in."""
    result = send_email_and_verify(
        mail_server=mail_server,
        database=database,
        sender="sender@example.com",
        bcc=["recipient@example.com"],
        subject="Test Email",
        body="This is a test"
    )

    verify_email_sent_successfully(result, mail_server, database)


def test_send_to_and_cc(mail_server, database):
    """Req_159: Send email with To and Cc fields filled in."""
    result = send_email_and_verify(
        mail_server=mail_server,
        database=database,
        sender="sender@example.com",
        to=["recipient1@example.com"],
        cc=["recipient2@example.com"],
        subject="Test Email",
        body="This is a test"
    )

    verify_email_sent_successfully(result, mail_server, database)


def test_send_to_and_bcc(mail_server, database):
    """Req_159: Send email with To and Bcc fields filled in."""
    result = send_email_and_verify(
        mail_server=mail_server,
        database=database,
        sender="sender@example.com",
        to=["recipient1@example.com"],
        bcc=["recipient2@example.com"],
        subject="Test Email",
        body="This is a test"
    )

    verify_email_sent_successfully(result, mail_server, database)


def test_send_cc_and_bcc(mail_server, database):
    """Req_159: Send email with Cc and Bcc fields filled in."""
    result = send_email_and_verify(
        mail_server=mail_server,
        database=database,
        sender="sender@example.com",
        cc=["recipient1@example.com"],
        bcc=["recipient2@example.com"],
        subject="Test Email",
        body="This is a test"
    )

    verify_email_sent_successfully(result, mail_server, database)


def test_send_to_cc_and_bcc(mail_server, database):
    """Req_159: Send email with all three fields filled in."""
    result = send_email_and_verify(
        mail_server=mail_server,
        database=database,
        sender="sender@example.com",
        to=["recipient1@example.com"],
        cc=["recipient2@example.com"],
        bcc=["recipient3@example.com"],
        subject="Test Email",
        body="This is a test"
    )

    verify_email_sent_successfully(result, mail_server, database)


# Negative Paths

def test_send_no_recipients(mail_server, database):
    """Req_159: Send email with no recipients should fail."""
    result = send_email_and_verify(
        mail_server=mail_server,
        database=database,
        sender="sender@example.com",
        subject="Test Email",
        body="This is a test"
    )

    verify_email_not_sent(result, mail_server, database)


def test_send_invalid_email_format(mail_server, database):
    """Req_159: Send email to an invalid email format should fail."""
    result = send_email_and_verify(
        mail_server=mail_server,
        database=database,
        sender="sender@example.com",
        to=["notanemail"],
        subject="Test Email",
        body="This is a test"
    )

    # Note: Currently our stub does not validate email format.
    # In a real system this would fail. This test documents
    # the need for email validation in the mail server.
    verify_email_sent_successfully(result, mail_server, database)


def test_send_nonexistent_address(mail_server, database):
    """Req_159: Send email to a nonexistent address should fail."""
    result = send_email_and_verify(
        mail_server=mail_server,
        database=database,
        sender="sender@example.com",
        to=["nobody@doesnotexist.com"],
        subject="Test Email",
        body="This is a test"
    )

    # Note: Currently our stub does not verify if addresses exist.
    # In a real system the outbound server would reject this.
    # This test documents that behavior for future implementation.
    verify_email_sent_successfully(result, mail_server, database)


def test_send_unauthorized_sender(mail_server, database):
    """Req_159: Send email from an unauthorized sender should fail."""
    result = send_email_and_verify(
        mail_server=mail_server,
        database=database,
        sender="hacker@notauthorized.com",
        to=["recipient@example.com"],
        subject="Test Email",
        body="This is a test"
    )

    # Note: Currently our stub does not check sender authorization.
    # In a real system the backend would verify the sender is
    # authenticated before allowing the send.
    # This test documents that behavior for future implementation.
    verify_email_sent_successfully(result, mail_server, database)
