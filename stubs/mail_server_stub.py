class MailServerStub:
    """
    Simulates the inbound and outbound mail servers from the
    email application system. Instead of actually sending or
    receiving emails over a network, this stub stores everything
    in memory so our tests can verify the correct behavior.
    """

    def __init__(self):
        self.outbox = []
        self.inbox = []

    def send_email(self, email):
        """
        Simulates sending an email through the outbound mail server.
        Stores the email in the outbox instead of actually sending it.
        Returns True if the email has at least one recipient, False otherwise.
        """
        if email.to == [] and email.cc == [] and email.bcc == []:
            return False
        else:
            self.outbox.append(email)
            return True

    def receive_email(self, email):
        """
        Simulates an email arriving on the inbound mail server.
        Stores the email in the inbox for the backend to process.
        """
        self.inbox.append(email)

    def get_outbox(self):
        """Returns all emails that were sent through the outbound server."""
        return self.outbox

    def get_inbox(self):
        """Returns all emails that arrived on the inbound server."""
        return self.inbox

    def clear(self):
        """
        Resets all data. Useful for running between tests
        so each test starts with a clean state.
        """
        self.outbox = []
        self.inbox = []