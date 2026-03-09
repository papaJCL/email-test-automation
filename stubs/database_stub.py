class DatabaseStub:
    """
    Simulates the personal database from the email application system.
    Stores sent emails, received emails, and the spam list in memory
    instead of connecting to a real database.

    This stub is used so our tests can verify database behavior
    without needing a live database connection.
    """

    def __init__(self):
        self.sent_emails = []
        self.received_emails = []
        self.spam_list = []

    def save_sent_email(self, email):
        """Saves an email to the sent emails table."""
        self.sent_emails.append(email)

    def save_received_email(self, email):
        """Saves an email to the received emails table."""
        self.received_emails.append(email)

    def get_sent_emails(self):
        """Returns all sent emails."""
        return self.sent_emails

    def get_received_emails(self):
        """Returns all received emails."""
        return self.received_emails

    def add_to_spam_list(self, address):
        """Adds an email address to the spam list."""
        if address not in self.spam_list:
            self.spam_list.append(address)

    def remove_from_spam_list(self, address):
        """Removes an email address from the spam list."""
        if address in self.spam_list:
            self.spam_list.remove(address)

    def is_spam(self, address):
        """Checks if an email address is on the spam list."""
        return address in self.spam_list

    def get_spam_list(self):
        """Returns all addresses on the spam list."""
        return self.spam_list

    def clear(self):
        """
        Resets all data. Useful for running between tests
        so each test starts with a clean state.
        """
        self.sent_emails = []
        self.received_emails = []
        self.spam_list = []