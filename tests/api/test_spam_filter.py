import pytest
from stubs.mail_server_stub import MailServerStub
from stubs.database_stub import DatabaseStub
from utils.email_helpers import mark_as_spam, unmark_as_spam, receive_and_route_email


@pytest.fixture
def mail_server():
    """Creates a fresh mail server stub for each test."""
    return MailServerStub()


@pytest.fixture
def database():
    """Creates a fresh database stub for each test."""
    return DatabaseStub()


# Happy Paths

def test_mark_email_as_spam(mail_server, database):
    """Req_42: User marks an email address as spam, verify it is in the spam list."""
    mark_as_spam(database, "spammer@example.com")

    assert database.is_spam("spammer@example.com") == True
    assert len(database.get_spam_list()) == 1


def test_flagged_address_routes_to_spam(mail_server, database):
    """Req_42: New email from a flagged address automatically routes to spam."""
    mark_as_spam(database, "spammer@example.com")

    result = receive_and_route_email(
        mail_server=mail_server,
        database=database,
        sender="spammer@example.com",
        to=["user@example.com"],
        subject="Buy stuff",
        body="This is spam"
    )

    assert result == "spam"


# Edge Cases

def test_unmark_spam_routes_to_inbox(mail_server, database):
    """Req_42: User unmarks an address, new emails go back to inbox."""
    mark_as_spam(database, "friend@example.com")
    unmark_as_spam(database, "friend@example.com")

    assert database.is_spam("friend@example.com") == False

    result = receive_and_route_email(
        mail_server=mail_server,
        database=database,
        sender="friend@example.com",
        to=["user@example.com"],
        subject="Hey",
        body="Not spam anymore"
    )

    assert result == "inbox"


def test_flagged_address_in_cc(mail_server, database):
    """Req_42: Flagged address shows up in Cc, verify how system handles it."""
    mark_as_spam(database, "spammer@example.com")

    # Note: Our current routing checks the sender field only.
    # In a real system we may also want to check if a spam
    # address appears in the Cc field. This test documents
    # that behavior for future discussion.
    result = receive_and_route_email(
        mail_server=mail_server,
        database=database,
        sender="legit@example.com",
        to=["user@example.com"],
        cc=["spammer@example.com"],
        subject="Group thread",
        body="This has a spammer in cc"
    )

    assert result == "inbox"


def test_empty_spam_list_routes_to_inbox(mail_server, database):
    """Req_42: Spam list is empty, all emails route to inbox normally."""
    assert len(database.get_spam_list()) == 0

    result = receive_and_route_email(
        mail_server=mail_server,
        database=database,
        sender="anyone@example.com",
        to=["user@example.com"],
        subject="Hello",
        body="Normal email"
    )

    assert result == "inbox"


def test_multiple_addresses_marked_as_spam(mail_server, database):
    """Req_42: Multiple addresses marked as spam, all filter correctly."""
    mark_as_spam(database, "spammer1@example.com")
    mark_as_spam(database, "spammer2@example.com")
    mark_as_spam(database, "spammer3@example.com")

    assert len(database.get_spam_list()) == 3

    result1 = receive_and_route_email(
        mail_server=mail_server,
        database=database,
        sender="spammer1@example.com",
        to=["user@example.com"],
        subject="Spam 1",
        body="Spam email 1"
    )

    result2 = receive_and_route_email(
        mail_server=mail_server,
        database=database,
        sender="spammer2@example.com",
        to=["user@example.com"],
        subject="Spam 2",
        body="Spam email 2"
    )

    result3 = receive_and_route_email(
        mail_server=mail_server,
        database=database,
        sender="spammer3@example.com",
        to=["user@example.com"],
        subject="Spam 3",
        body="Spam email 3"
    )

    assert result1 == "spam"
    assert result2 == "spam"
    assert result3 == "spam"