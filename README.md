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