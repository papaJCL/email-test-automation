from utils.email_schema import Email
from stubs.mail_server_stub import MailServerStub
from stubs.database_stub import DatabaseStub


def send_email_and_verify(mail_server, database, sender, to=None, cc=None, bcc=None, subject="", body=""):
    """
    Helper function that handles the full send email flow.
    Creates the email, sends it through the mail server,
    saves it to the database, and verifies everything worked.
    Used by all Req_159 backend test cases.
    """
    email = Email(sender=sender, to=to, cc=cc, bcc=bcc, subject=subject, body=body)

    result = mail_server.send_email(email)

    if result == True:
        database.save_sent_email(email)
        database.save_received_email(email)

    return result


def mark_as_spam(database, address):
    """
    Helper function that marks an email address as spam
    in the database. Used as setup for Req_42 spam tests.
    """
    database.add_to_spam_list(address)


def unmark_as_spam(database, address):
    """
    Helper function that removes an email address from the
    spam list in the database. Used for the unmark edge case.
    """
    database.remove_from_spam_list(address)


def receive_and_route_email(mail_server, database, sender, to=None, cc=None, bcc=None, subject="", body=""):
    """
    Helper function that simulates an incoming email and
    routes it based on the spam list. If the sender is on
    the spam list, the email goes to spam. Otherwise it
    goes to the inbox. Returns 'spam' or 'inbox' so the
    test can verify the routing.
    """
    email = Email(sender=sender, to=to, cc=cc, bcc=bcc, subject=subject, body=body)

    mail_server.receive_email(email)

    if database.is_spam(sender) == True:
        return "spam"
    else:
        database.save_received_email(email)
        return "inbox"