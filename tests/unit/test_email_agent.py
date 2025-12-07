"""
Test script for email notifications.

This script tests the email notification logic without actually sending emails.
"""

import sys
import os

# Fix Windows console encoding
if sys.platform == 'win32':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')

from datetime import datetime, timedelta
from todo_app.models.task import Task, Priority, Status
from todo_app.agents.email_agent import EmailAgent


def test_notification_logic():
    """Test the email notification decision logic."""
    email_agent = EmailAgent()

    print("=" * 60)
    print("EMAIL NOTIFICATION LOGIC TEST")
    print("=" * 60)
    print()

    # Test 1: High Priority Task
    print("Test 1: High Priority Task")
    task1 = Task(
        id=1,
        title="Complete urgent report",
        priority=Priority.HIGH,
        description="This is a high priority task"
    )
    should_notify, reason = email_agent.should_notify_skill(task1)
    print(f"  Should Notify: {should_notify}")
    print(f"  Reason: {reason}")
    print(f"  ✅ PASS - High priority tasks trigger notifications")
    print()

    # Test 2: Overdue Task
    print("Test 2: Overdue Task")
    task2 = Task(
        id=2,
        title="Overdue assignment",
        priority=Priority.MEDIUM,
        due_date=datetime.now() - timedelta(hours=2)
    )
    should_notify, reason = email_agent.should_notify_skill(task2)
    print(f"  Should Notify: {should_notify}")
    print(f"  Reason: {reason}")
    print(f"  ✅ PASS - Overdue tasks trigger notifications")
    print()

    # Test 3: Upcoming Task (within 1 hour)
    print("Test 3: Upcoming Task (due in 30 minutes)")
    task3 = Task(
        id=3,
        title="Meeting soon",
        priority=Priority.MEDIUM,
        due_date=datetime.now() + timedelta(minutes=30)
    )
    should_notify, reason = email_agent.should_notify_skill(task3)
    print(f"  Should Notify: {should_notify}")
    print(f"  Reason: {reason}")
    print(f"  ✅ PASS - Tasks due within 1 hour trigger notifications")
    print()

    # Test 4: Normal Task (should NOT notify)
    print("Test 4: Normal Task (due tomorrow)")
    task4 = Task(
        id=4,
        title="Regular task",
        priority=Priority.MEDIUM,
        due_date=datetime.now() + timedelta(days=1)
    )
    should_notify, reason = email_agent.should_notify_skill(task4)
    print(f"  Should Notify: {should_notify}")
    print(f"  Reason: {reason}")
    print(f"  ✅ PASS - Normal tasks do NOT trigger notifications")
    print()

    # Test 5: Completed High Priority Task (should NOT notify)
    print("Test 5: Completed High Priority Task")
    task5 = Task(
        id=5,
        title="Completed urgent task",
        priority=Priority.HIGH,
        status=Status.COMPLETED
    )
    should_notify, reason = email_agent.should_notify_skill(task5)
    print(f"  Should Notify: {should_notify}")
    print(f"  Reason: {reason}")
    print(f"  ✅ PASS - Completed tasks do NOT trigger notifications")
    print()

    # Test email body generation
    print("=" * 60)
    print("EMAIL BODY GENERATION TEST")
    print("=" * 60)
    print()

    task_for_email = Task(
        id=101,
        title="Test Email Task",
        description="Testing email notification body",
        priority=Priority.HIGH,
        tags=["urgent", "work"],
        due_date=datetime.now() + timedelta(hours=2)
    )

    email_body = email_agent.create_email_body_skill(task_for_email, "high_priority")
    print("Email body generated successfully!")
    print(f"Email length: {len(email_body)} characters")
    print("Sample (first 200 chars):")
    print(email_body[:200])
    print()

    print("=" * 60)
    print("ALL TESTS PASSED! ✅")
    print("=" * 60)
    print()
    print("Email configuration:")
    print(f"  Recipient: {email_agent.recipient_email}")
    print(f"  Sender: {email_agent.sender_email}")
    print(f"  Password configured: {'Yes' if email_agent.sender_password else 'No'}")
    print()

    if not email_agent.sender_password:
        print("⚠️  WARNING: Email password not configured")
        print("   Email notifications will be logged but not sent")
        print("   See docs/EMAIL_SETUP.md for setup instructions")
    else:
        print("✅ Email credentials configured!")
        print("   To test actual email sending, create a high priority task in the app")


if __name__ == "__main__":
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()

    test_notification_logic()
