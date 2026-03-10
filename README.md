# Email Application Test Automation

## The Problem

We've got an email application system with a UI, a backend that handles all the processing, a database, and inbound/outbound mail servers. The goal is to write automated tests against two requirements:

Req_159: Emails should be sent to any valid email address using the To, Cc, and/or Bcc fields

Req_42: Any email address the user flags as spam should automatically get routed to the spam folder going forward

## My Approach

This project uses Python with a Page Object Model structure. The actual application doesn't exist so all interactions with the UI, servers, and database are stubbed out. The focus here is on the test design, the code structure, and showing how this would work against a real system.

POM was chosen because it keeps the test logic separate from the page interactions. If the UI changes, you update the page object, not every single test. It makes everything easier to maintain and scale.

## My Test Cases

### Req_159: Sending Emails

**Happy Paths** (tests that verify the system works correctly under normal expected conditions):

1. Send email to To only
2. Send email to Cc only
3. Send email to Bcc only
4. Send email to To + Cc
5. Send email to To + Bcc
6. Send email to Cc + Bcc
7. Send email to To + Cc + Bcc

**Negative Paths** (tests that verify the system handles errors and bad input correctly):

1. Send email with no recipients
2. Send email to an invalid email format
3. Send email to a nonexistent address
4. Send email from an unauthorized sender

### Req_42: Spam Filtering

**Happy Paths:**

1. User manually marks an email as spam, verify it moves to the spam folder
2. New email arrives from a flagged address, verify it automatically routes to spam

**Edge Cases** (tests that verify the system handles unusual or boundary scenarios correctly):

1. User unmarks an address, new emails from that sender go back to inbox
2. Flagged address shows up in Cc, verify how the system handles it
3. Spam list is empty, all emails route to inbox normally
4. Multiple addresses marked as spam, all filter correctly

## My Assumptions

1. The way I read Req_42, "identified as spam by the user" means the user manually flags an email address as spam. The automatic part is what happens after that, any future emails from that address get routed to the spam folder without the user doing anything.

2. Spam filtering only checks the sender address. If a flagged address shows up in the Cc or Bcc fields but isn't the sender, the email still goes to the inbox. This is a design decision that could go either way and would be worth discussing with the team.

3. Our email schema only covers the basic fields: from, to, cc, bcc, subject, and body. A real email system would also handle things like attachments, timestamps, read receipts, and priority flags. These were left out to keep the scope focused on the two requirements.

4. Email format validation, sender authentication, and address existence checks would all be handled by the real backend and mail servers. Our stubs don't implement this logic but the tests document where that validation should happen.

5. Page objects are pseudocoded since there's no real application to automate against. The structure and method signatures are real, the implementations would be filled in once connected to an actual UI.

6. Each test runs with a completely clean state. No data carries over between tests.

## Features Not Implemented

1. Email format validation. There's no logic that checks if an email address is actually valid (like has an @ symbol, proper domain, etc.). In a real system the backend or mail server would handle this.

2. Sender authentication. Nothing is checking if the person sending the email is actually authorized to send. A real system would verify credentials before letting you send anything.

3. Address existence verification. The outbound mail server doesn't check if the recipient address actually exists. A real server would bounce back an error for addresses that don't exist.

4. Attachment support. Emails in this project only have text fields. No ability to attach files, images, etc.

5. Timestamps. Emails don't have a sent or received time. A real system would track when every email was sent and received.

6. Read receipts and priority flags. These are standard email features that weren't in scope for the two requirements.

7. Full UI automation. The page objects have the correct structure and methods but the actual browser interactions aren't implemented since there's no real application to connect to.

8. Sent folder. There's no sent folder page object or UI tests for verifying sent emails from the sender's perspective.

9. Real database and server connections. Everything runs in memory using stubs. In a real implementation these would connect to actual databases and mail servers.
