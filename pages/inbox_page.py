class InboxPage:
    """
    Page Object for the inbox screen.
    Handles all interactions related to viewing
    and managing received emails.
    """

    def navigate_to_inbox(self):
        # Click the inbox folder in the sidebar to navigate to inbox
        pass

    def get_email_list(self):
        # Locate and return all email elements displayed in the inbox
        pass

    def get_email_count(self):
        # Return the number of emails currently showing in the inbox
        pass

    def open_email(self, subject):
        # Find an email by subject line and click to open it
        pass

    def get_email_sender(self):
        # Return the sender address of the currently open email
        pass

    def get_email_recipients(self):
        # Return the To, Cc, Bcc recipients of the currently open email
        pass

    def mark_as_spam(self, subject):
        # Find an email by subject, select it, and click the mark as spam button
        pass

    def is_email_present(self, subject):
        # Check if an email with the given subject exists in inbox
        # Returns True or False
        pass