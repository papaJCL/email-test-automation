class Email:
    """
    Represents an email object used to compose and send emails
    through the email application system.
    
    Attributes:
        sender (str): The email address of the person sending the email
        to (list): List of recipient email addresses in the To field
        cc (list): List of recipient email addresses in the Cc field
        bcc (list): List of recipient email addresses in the Bcc field
        subject (str): The subject line of the email
        body (str): The body content of the email

    Note: A dictionary approach could also work here
    """
    
    def __init__(self, sender, to=None, cc=None, bcc=None, subject="", body=""):
        self.sender = sender
        self.to = to or []
        self.cc = cc or []
        self.bcc = bcc or []
        self.subject = subject
        self.body = body

    def to_dict(self):
        return {
            "from": self.sender,
            "to": self.to,
            "cc": self.cc,
            "bcc": self.bcc,
            "subject": self.subject,
            "body": self.body
        }