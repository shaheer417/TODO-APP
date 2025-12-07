"""
Email Notification Agent for sending task alerts.

This agent handles sending email notifications for high priority tasks,
overdue tasks, and upcoming tasks (within 1 hour).
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from typing import Optional, List
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from todo_app.models.task import Task, Priority, Status


class EmailAgent:
    """
    Sub-Agent responsible for email notifications.

    Sends email alerts for:
    - High priority tasks
    - Overdue tasks
    - Upcoming tasks (within 1 hour of due date)
    """

    def __init__(self):
        """Initialize EmailAgent with email configuration."""
        self.recipient_email = os.getenv("RECIPIENT_EMAIL", "niazi2822@gmail.com")
        self.sender_email = os.getenv("EMAIL_SENDER", "todo.app.notifications@gmail.com")
        self.sender_password = os.getenv("EMAIL_PASSWORD", "")
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587

    def should_notify_skill(self, task: Task) -> tuple[bool, str]:
        """
        Determine if a task should trigger an email notification.

        Args:
            task: Task to check

        Returns:
            Tuple of (should_notify: bool, reason: str)
        """
        if task.status == Status.COMPLETED:
            return False, ""

        # Check if task is overdue
        if task.is_overdue():
            return True, "overdue"

        # Check if task is high priority
        if task.priority == Priority.HIGH:
            return True, "high_priority"

        # Check if task is due within 1 hour
        if task.due_date:
            time_until_due = task.due_date - datetime.now()
            if timedelta(0) < time_until_due <= timedelta(hours=1):
                return True, "upcoming"

        return False, ""

    def create_email_body_skill(self, task: Task, reason: str) -> str:
        """
        Create formatted email body for task notification.

        Args:
            task: Task to create email for
            reason: Notification reason (overdue, high_priority, upcoming)

        Returns:
            HTML formatted email body
        """
        reason_messages = {
            "overdue": "⚠️ OVERDUE TASK ALERT",
            "high_priority": "🔥 HIGH PRIORITY TASK",
            "upcoming": "⏰ TASK DUE SOON (Within 1 Hour)"
        }

        alert_type = reason_messages.get(reason, "TASK NOTIFICATION")

        # Create HTML email
        html = f"""
        <html>
            <body style="font-family: Arial, sans-serif; padding: 20px; background-color: #f5f5f5;">
                <div style="max-width: 600px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                    <h2 style="color: #333; border-bottom: 3px solid #666; padding-bottom: 10px;">
                        {alert_type}
                    </h2>

                    <div style="margin-top: 20px;">
                        <h3 style="color: #555; margin-bottom: 15px;">📝 Task Details</h3>

                        <table style="width: 100%; border-collapse: collapse;">
                            <tr>
                                <td style="padding: 10px; background-color: #f9f9f9; font-weight: bold; width: 150px;">Task ID:</td>
                                <td style="padding: 10px;">{task.id}</td>
                            </tr>
                            <tr>
                                <td style="padding: 10px; background-color: #f9f9f9; font-weight: bold;">Title:</td>
                                <td style="padding: 10px;"><strong>{task.title}</strong></td>
                            </tr>
                            <tr>
                                <td style="padding: 10px; background-color: #f9f9f9; font-weight: bold;">Priority:</td>
                                <td style="padding: 10px;">
                                    <span style="background-color: {'#ff4444' if task.priority == Priority.HIGH else '#ffbb33' if task.priority == Priority.MEDIUM else '#00C851'};
                                                 color: white;
                                                 padding: 5px 15px;
                                                 border-radius: 5px;
                                                 font-weight: bold;">
                                        {task.priority.value.upper()}
                                    </span>
                                </td>
                            </tr>
                            <tr>
                                <td style="padding: 10px; background-color: #f9f9f9; font-weight: bold;">Description:</td>
                                <td style="padding: 10px;">{task.description or 'No description'}</td>
                            </tr>
                            <tr>
                                <td style="padding: 10px; background-color: #f9f9f9; font-weight: bold;">Due Date:</td>
                                <td style="padding: 10px;">
                                    {task.due_date.strftime('%Y-%m-%d %H:%M') if task.due_date else 'No due date'}
                                </td>
                            </tr>
                            <tr>
                                <td style="padding: 10px; background-color: #f9f9f9; font-weight: bold;">Tags:</td>
                                <td style="padding: 10px;">{', '.join(task.tags) if task.tags else 'No tags'}</td>
                            </tr>
                            <tr>
                                <td style="padding: 10px; background-color: #f9f9f9; font-weight: bold;">Created:</td>
                                <td style="padding: 10px;">{task.created_at.strftime('%Y-%m-%d %H:%M')}</td>
                            </tr>
                        </table>
                    </div>

                    <div style="margin-top: 30px; padding: 15px; background-color: #f0f0f0; border-left: 4px solid #666; border-radius: 5px;">
                        <p style="margin: 0; color: #555;">
                            <strong>Action Required:</strong> Please review and complete this task as soon as possible.
                        </p>
                    </div>

                    <div style="margin-top: 30px; text-align: center; color: #999; font-size: 12px;">
                        <p>🚀 This is an automated notification from TODO MASTER</p>
                        <p>Your Ultimate Productivity Companion</p>
                    </div>
                </div>
            </body>
        </html>
        """

        return html

    def send_notification_skill(self, task: Task, reason: str) -> bool:
        """
        Send email notification for a task.

        Args:
            task: Task to send notification for
            reason: Notification reason

        Returns:
            True if email sent successfully, False otherwise
        """
        try:
            # Check if email credentials are configured
            if not self.sender_password:
                print("Warning: Email password not configured. Skipping email notification.")
                print(f"Task '{task.title}' requires notification ({reason})")
                return False

            # Create message
            message = MIMEMultipart("alternative")
            message["Subject"] = f"TODO Master Alert: {task.title}"
            message["From"] = self.sender_email
            message["To"] = self.recipient_email

            # Create email body
            html_body = self.create_email_body_skill(task, reason)
            html_part = MIMEText(html_body, "html")
            message.attach(html_part)

            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(message)

            print(f"✅ Email notification sent for task: {task.title} (Reason: {reason})")
            return True

        except Exception as e:
            print(f"❌ Failed to send email notification: {str(e)}")
            return False

    def check_and_notify_task_skill(self, task: Task) -> bool:
        """
        Check if task needs notification and send if necessary.

        Args:
            task: Task to check and notify

        Returns:
            True if notification was sent, False otherwise
        """
        should_notify, reason = self.should_notify_skill(task)
        if should_notify:
            return self.send_notification_skill(task, reason)
        return False

    def check_and_notify_tasks_skill(self, tasks: List[Task]) -> int:
        """
        Check multiple tasks and send notifications as needed.

        Args:
            tasks: List of tasks to check

        Returns:
            Number of notifications sent
        """
        notifications_sent = 0
        for task in tasks:
            if self.check_and_notify_task_skill(task):
                notifications_sent += 1
        return notifications_sent
