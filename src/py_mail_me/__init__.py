"""
py-mail-me is a simple Python package for sending email notifications after task completion.
"""

import os
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from functools import wraps
from typing import Optional, Union, List
from pathlib import Path
import tempfile
from datetime import datetime

class EmailNotifier:
    def __init__(
        self,
        email: Union[str, List[str]],
        subject: str = "Task Completed",
        attach_logs: bool = False,
        host: Optional[str] = None,
        port: Optional[int] = None,
        username: Optional[str] = None,
        password: Optional[str] = None
    ):
        self.email = [email] if isinstance(email, str) else email
        self.subject = subject
        self.attach_logs = attach_logs
        self.host = host or os.getenv("EMAIL_HOST", "smtp.gmail.com")
        self.port = port or int(os.getenv("EMAIL_PORT", "587"))
        self.username = username or os.getenv("EMAIL_USER")
        self.password = password or os.getenv("EMAIL_PASSWORD")
        
        if not all([self.username, self.password]):
            raise ValueError("Email credentials not provided")
            
        self.log_file = None
        if self.attach_logs:
            self.log_file = tempfile.NamedTemporaryFile(
                mode='w',
                delete=False,
                prefix='task_log_',
                suffix='.txt'
            )
            
    def __enter__(self):
        if self.attach_logs:
            self.start_logging()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.attach_logs:
            self.stop_logging()
        self.send_notification(error=exc_val if exc_type else None)
        if self.log_file:
            try:
                os.unlink(self.log_file.name)
            except:
                pass
                
    def start_logging(self):
        """Start capturing logs"""
        self.log_handler = logging.FileHandler(self.log_file.name)
        self.log_handler.setFormatter(
            logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        )
        logging.getLogger().addHandler(self.log_handler)
        
    def stop_logging(self):
        """Stop capturing logs"""
        if hasattr(self, 'log_handler'):
            logging.getLogger().removeHandler(self.log_handler)
            self.log_handler.close()
            
    def send_notification(self, error=None):
        """Send email notification"""
        msg = MIMEMultipart()
        msg['From'] = self.username
        msg['To'] = ', '.join(self.email)
        msg['Subject'] = self.subject
        
        # Email content
        content = "Task completed successfully!" if not error else f"Task failed: {str(error)}"
        msg.attach(MIMEText(content, 'plain'))
        
        # Attach logs if enabled
        if self.attach_logs and self.log_file:
            with open(self.log_file.name, 'rb') as f:
                log_attachment = MIMEApplication(f.read(), _subtype='txt')
                log_attachment.add_header(
                    'Content-Disposition',
                    'attachment',
                    filename=f'task_log_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
                )
                msg.attach(log_attachment)
                
        # Send email
        with smtplib.SMTP(self.host, self.port) as server:
            server.starttls()
            server.login(self.username, self.password)
            server.send_message(msg)

def py_mail_me(
    email: Union[str, List[str]],
    subject: str = "Task Completed",
    attach_logs: bool = False,
    host: Optional[str] = None,
    port: Optional[int] = None,
    username: Optional[str] = None,
    password: Optional[str] = None
):
    """Decorator for sending email notifications after task completion"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with EmailNotifier(
                email=email,
                subject=subject,
                attach_logs=attach_logs,
                host=host,
                port=port,
                username=username,
                password=password
            ):
                return func(*args, **kwargs)
        return wrapper
    return decorator 