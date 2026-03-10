class SpamPage:
    """
    Page Object for the spam folder screen.
    Handles all interactions related to viewing
    and managing spam emails.
    """

    def navigate_to_spam(self):
        # Click the spam folder in the sidebar to navigate to spam
        pass

    def get_email_list(self):
        # Locate and return all email elements displayed in the spam folder
        pass

    def get_email_count(self):
        # Return the number of emails currently showing in the spam folder
        pass

    def is_email_present(self, subject):
        # Check if an email with the given subject exists in spam
        # Returns True/False
        pass

    def unmark_as_spam(self, subject):
        # Find an email by subject, select it, and click the unmark spam button
        pass