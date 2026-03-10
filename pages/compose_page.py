class ComposePage:
    """
    Page Object for the email compose screen.
    Handles all interactions related to writing
    and sending a new email.
    """

    def open_compose(self):
        # Click the compose/new email button to open the compose window
        pass

    def fill_to_field(self, addresses):
        # Locate the To input field and enter the email addresses
        pass

    def fill_cc_field(self, addresses):
        # Locate the Cc input field and enter the email addresses
        pass

    def fill_bcc_field(self, addresses):
        # Locate the Bcc input field and enter the email addresses
        pass

    def fill_subject(self, subject):
        # Locate the subject input field and enter the subject text
        pass

    def fill_body(self, body):
        # Locate the body text area and enter the email body
        pass

    def click_send(self):
        # Click the send button to send email
        pass

    def get_error_message(self):
        # Locate and return any error message displayed after send attempt
        pass