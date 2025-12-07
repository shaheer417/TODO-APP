# Email Notifications - Complete Guide

## Table of Contents
1. [Overview](#overview)
2. [Features](#features)
3. [Setup Instructions](#setup-instructions)
4. [Skills Documentation](#skills-documentation)
5. [Usage](#usage)
6. [Testing](#testing)
7. [Troubleshooting](#troubleshooting)

---

## Overview

TODO Master automatically sends email notifications to **niazi2822@gmail.com** for urgent tasks including high priority tasks, overdue tasks, and tasks due within 1 hour.

### When Notifications Are Sent

The app automatically sends email alerts for:

1. **High Priority Tasks** - Any task marked as HIGH priority
2. **Overdue Tasks** - Tasks that have passed their due date
3. **Upcoming Tasks** - Tasks due within 1 hour

### Email Features

Each notification includes:
- Beautiful HTML-formatted email
- Color-coded alert type (Overdue, High Priority, or Upcoming)
- Complete task details (ID, title, priority, description, tags, due date)
- Professional branding with TODO MASTER logo

---

## Features

### Email Notification Agent (`todo_app/agents/email_agent.py`)

A dedicated EmailAgent sub-agent that handles all email notification logic with the following skills:

#### Skills List

| Skill | Purpose | Parameters | Returns |
|-------|---------|------------|---------|
| `should_notify_skill()` | Check if notification needed | Task | (bool, reason) |
| `create_email_body_skill()` | Generate HTML email | Task, reason | HTML string |
| `send_notification_skill()` | Send email via SMTP | Task, reason | bool |
| `check_and_notify_task_skill()` | Check & send for one task | Task | bool |
| `check_and_notify_tasks_skill()` | Check & send for many tasks | List[Task] | int count |

### Integration Points

Email notifications are checked automatically at:

1. **When adding a new task** - Immediately checks if notification needed
2. **When viewing all tasks** - Scans all tasks and sends alerts for urgent ones

---

## Setup Instructions

### Step 1: Install Dependencies

Install the required Python package:

```bash
pip install python-dotenv
```

Or install all dependencies:

```bash
pip install -r requirements.txt
```

### Step 2: Create Gmail App Password

**Important:** You need to use a Gmail App Password, NOT your regular Gmail password.

1. Go to your Google Account: https://myaccount.google.com/security
2. Enable **2-Step Verification** if not already enabled
3. Go to App Passwords: https://myaccount.google.com/apppasswords
4. Select **Mail** as the app
5. Select your device
6. Click **Generate**
7. Copy the 16-character password (e.g., `abcd efgh ijkl mnop`)

### Step 3: Configure Environment Variables

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit the `.env` file with your credentials:
   ```
   EMAIL_SENDER=your-email@gmail.com
   EMAIL_PASSWORD=abcdefghijklmnop
   RECIPIENT_EMAIL=niazi2822@gmail.com
   ```

   Replace:
   - `your-email@gmail.com` with your Gmail address
   - `abcdefghijklmnop` with your App Password (remove spaces)
   - Keep `RECIPIENT_EMAIL` as `niazi2822@gmail.com`

### Step 4: Test the Setup

Run the TODO app and create a high priority task:

```bash
python -m todo_app.main
```

Then:
1. Select option `2` (Add New Task)
2. Enter any task title
3. Enter any description
4. For priority, enter: `high`
5. Complete the rest of the fields

You should see: `✅ Email notification sent for task: [task name]`

Check **niazi2822@gmail.com** for the email notification!

---

## Skills Documentation

### 1. `should_notify_skill(task: Task) -> tuple[bool, str]`

**Purpose**: Determine if a task should trigger an email notification.

**Notification Criteria**:
- **Overdue**: Task is past due date and status is PENDING
- **High Priority**: Task priority is HIGH and status is PENDING
- **Upcoming**: Task is due within 1 hour and status is PENDING

**Example**:
```python
email_agent = EmailAgent()
task = Task(id=1, title="Urgent", priority=Priority.HIGH)
should_notify, reason = email_agent.should_notify_skill(task)
# Returns: (True, "high_priority")
```

### 2. `create_email_body_skill(task: Task, reason: str) -> str`

**Purpose**: Create formatted HTML email body for task notification.

**Parameters**:
- `task` (Task): Task to create email for
- `reason` (str): Notification reason ("overdue", "high_priority", "upcoming")

**Returns**: HTML formatted email body with:
- Color-coded alert type header
- Formatted task details table
- Priority badge with color coding
- Professional branding

### 3. `send_notification_skill(task: Task, reason: str) -> bool`

**Purpose**: Send email notification via Gmail SMTP.

**Email Details**:
- **Subject**: "TODO Master Alert: {task.title}"
- **From**: Configured sender email (EMAIL_SENDER)
- **To**: niazi2822@gmail.com (RECIPIENT_EMAIL)
- **Format**: HTML with inline CSS
- **Server**: smtp.gmail.com:587 (TLS)

**Returns**: True if successful, False otherwise

### 4. `check_and_notify_task_skill(task: Task) -> bool`

**Purpose**: Convenience method to check and send notification for a single task.

**Workflow**:
1. Calls `should_notify_skill()` to check criteria
2. If needed, calls `send_notification_skill()` to send
3. Returns result

### 5. `check_and_notify_tasks_skill(tasks: List[Task]) -> int`

**Purpose**: Check multiple tasks and send notifications as needed.

**Returns**: Number of notifications sent

**Example**:
```python
email_agent = EmailAgent()
tasks = task_manager.get_all_tasks_skill()
count = email_agent.check_and_notify_tasks_skill(tasks)
print(f"{count} notifications sent")
```

---

## Usage

### In the Application

The email agent is automatically integrated:

```python
# In main.py - initialized with other agents
self.email_agent = EmailAgent()

# When adding a task
self.email_agent.check_and_notify_task_skill(task)

# When viewing all tasks
notifications_sent = self.email_agent.check_and_notify_tasks_skill(tasks)
```

### Manual Testing

Test notification logic without sending emails:

```bash
# Run with pytest
python -m pytest tests/unit/test_email_agent.py -v

# Or run directly
python tests/unit/test_email_agent.py
```

This validates:
- High priority task detection
- Overdue task detection
- Upcoming task detection (within 1 hour)
- Normal task filtering (no notification)
- Completed task filtering (no notification)
- Email body generation
- Configuration status

---

## Testing

### Run the Test Suite

```bash
# Run with pytest (recommended)
python -m pytest tests/unit/test_email_agent.py -v

# Or run directly
python tests/unit/test_email_agent.py
```

**Expected Output**:
```
============================================================
EMAIL NOTIFICATION LOGIC TEST
============================================================

Test 1: High Priority Task
  Should Notify: True
  Reason: high_priority
  ✅ PASS - High priority tasks trigger notifications

[... more tests ...]

============================================================
ALL TESTS PASSED! ✅
============================================================
```

### Test Scenarios

- ✅ High priority task → Notification sent
- ✅ Task due in 30 min → Notification sent
- ✅ Overdue task → Notification sent
- ✅ Normal task → No notification
- ✅ Completed high priority → No notification

---

## Troubleshooting

### "Email password not configured" Warning

**Solution**:
1. Make sure you created a `.env` file (not `.env.example`)
2. Check that `EMAIL_PASSWORD` is filled in correctly
3. Restart the app after editing `.env`

### Email Not Sending

**Common issues**:

1. **Wrong App Password Format**
   - Remove all spaces from the App Password
   - Should be 16 characters: `abcdefghijklmnop`

2. **2-Step Verification Not Enabled**
   - You must enable 2-Step Verification before creating App Passwords
   - Go to: https://myaccount.google.com/security

3. **Gmail Security Settings**
   - Check if Google blocked the sign-in attempt
   - Verify App Password was created correctly

4. **Incorrect Email Address**
   - Verify `EMAIL_SENDER` matches your Gmail account exactly

### Testing Without Email Setup

The app works perfectly without email setup! You'll just see console messages instead of actual emails:

```
Warning: Email password not configured. Skipping email notification.
Task 'Urgent Task' requires notification (high_priority)
```

---

## Configuration

### Environment Variables

```bash
# Gmail account to send notifications FROM
EMAIL_SENDER=your-email@gmail.com

# Gmail App Password (not your regular password!)
EMAIL_PASSWORD=abcdefghijklmnop

# Recipient email (where notifications will be sent)
RECIPIENT_EMAIL=niazi2822@gmail.com
```

### SMTP Settings

- **Server**: smtp.gmail.com
- **Port**: 587
- **Security**: TLS encryption
- **Authentication**: Gmail App Password

---

## Security

- Your `.env` file is listed in `.gitignore` and will NOT be committed to Git
- Never share your App Password with anyone
- Emails are sent via Gmail's secure SMTP server (TLS encryption)
- The recipient email (niazi2822@gmail.com) is configured via environment variables

---

## Files Created

### Core Files
1. `todo_app/agents/email_agent.py` - Email notification agent with skills
2. `.env.example` - Template for email configuration
3. `test_email_notifications.py` - Test suite

### Updated Files
1. `todo_app/main.py` - Integrated email agent
2. `requirements.txt` - Added python-dotenv
3. `.gitignore` - Added .env
4. `README.md` - Added email documentation

---

## Advanced Configuration

### Changing Notification Time Window

Edit `todo_app/agents/email_agent.py`:

```python
# Change from 1 hour to 2 hours
if timedelta(0) < time_until_due <= timedelta(hours=2):  # Changed
    return True, "upcoming"
```

### Customizing Email Template

Edit the `create_email_body_skill()` method in `email_agent.py` to customize the HTML email template.

---

## Support

If you encounter any issues:
1. Check this documentation
2. Verify your `.env` file is configured correctly
3. Make sure you're using a Gmail App Password (not regular password)
4. Run `python -m pytest tests/unit/test_email_agent.py -v` to test
5. Check your internet connection

---

**Last Updated**: December 7, 2025
**Version**: 1.0.0
**Developer**: Claude (Anthropic)
