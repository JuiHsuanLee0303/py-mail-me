"""
py-mail-me is a simple Python package for sending email notifications after task completion.
"""

import os
import smtplib
import logging
import asyncio
import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from functools import wraps
from typing import Optional, Union, List, Dict, Any, Callable
from pathlib import Path
import tempfile
from datetime import datetime
import ssl
import atexit
from tenacity import retry, stop_after_attempt, wait_exponential

from .exceptions import EmailConfigError, EmailAuthError, EmailSendError
from .templates import EmailTemplate, SUCCESS_TEMPLATE, ERROR_TEMPLATE

# Configure logger
logger = logging.getLogger(__name__)

# Global set to track temporary files
_temp_files = set()

def cleanup_temp_files():
    """Clean up temporary files at program exit"""
    for file_path in _temp_files:
        try:
            if os.path.exists(file_path):
                os.unlink(file_path)
        except Exception as e:
            logger.debug(f"Failed to delete temp file {file_path}: {e}")

# Register cleanup function
atexit.register(cleanup_temp_files)

class EmailNotifier:
    def __init__(
        self,
        email: Union[str, List[str]],
        subject: str = "Task Completed",
        attach_logs: bool = False,
        host: Optional[str] = None,
        port: Optional[int] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        use_tls: bool = True,
        max_retries: int = 3,
        template: Optional[EmailTemplate] = None,
        async_mode: bool = False
    ):
        """
        Initialize EmailNotifier.
        
        Args:
            email: Recipient email address(es)
            subject: Email subject
            attach_logs: Whether to attach execution logs
            host: SMTP server host
            port: SMTP server port
            username: SMTP username
            password: SMTP password
            use_tls: Whether to use TLS
            max_retries: Maximum number of retry attempts
            template: Custom email template
            async_mode: Whether to send emails asynchronously
        """
        self.email = [email] if isinstance(email, str) else email
        self.subject = subject
        self.attach_logs = attach_logs
        self.host = host or os.getenv("EMAIL_HOST", "smtp.gmail.com")
        self.port = port or int(os.getenv("EMAIL_PORT", "587"))
        self.username = username or os.getenv("EMAIL_USER")
        self.password = password or os.getenv("EMAIL_PASSWORD")
        self.use_tls = use_tls
        self.max_retries = max_retries
        self.template = template or SUCCESS_TEMPLATE
        self.async_mode = async_mode
        
        if not all([self.username, self.password]):
            raise EmailConfigError("Email credentials not provided")
            
        self.log_file = None
        self.log_handler = None
        if self.attach_logs:
            self._setup_logging()
        
        logger.debug(f"Initialized EmailNotifier for {self.email}")
    
    def _setup_logging(self):
        """Set up logging with a temporary file"""
        try:
            # Create a temporary file and track it
            self.log_file = tempfile.NamedTemporaryFile(
                mode='w',
                delete=False,
                prefix='task_log_',
                suffix='.txt'
            )
            _temp_files.add(self.log_file.name)
            
            # Create and configure the handler
            self.log_handler = logging.FileHandler(self.log_file.name)
            self.log_handler.setFormatter(
                logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            )
        except Exception as e:
            logger.error(f"Failed to set up logging: {e}")
            if self.log_file:
                try:
                    self.log_file.close()
                    os.unlink(self.log_file.name)
                    _temp_files.discard(self.log_file.name)
                except:
                    pass
            raise
            
    def __enter__(self):
        if self.attach_logs:
            self.start_logging()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if self.attach_logs:
                self.stop_logging()
            
            if self.async_mode:
                asyncio.create_task(self.send_notification_async(error=exc_val if exc_type else None))
            else:
                self.send_notification(error=exc_val if exc_type else None)
        finally:
            self._cleanup()

    async def __aenter__(self):
        if self.attach_logs:
            self.start_logging()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        try:
            if self.attach_logs:
                self.stop_logging()
            
            if self.async_mode:
                await self.send_notification_async(error=exc_val if exc_type else None)
            else:
                self.send_notification(error=exc_val if exc_type else None)
        finally:
            await self._cleanup_async()
                
    def start_logging(self):
        """Start capturing logs"""
        if self.log_handler:
            logging.getLogger().addHandler(self.log_handler)
            logger.debug("Started log capture")
        
    def stop_logging(self):
        """Stop capturing logs"""
        if self.log_handler:
            try:
                logging.getLogger().removeHandler(self.log_handler)
                self.log_handler.close()
                logger.debug("Stopped log capture")
            except Exception as e:
                logger.error(f"Error stopping log capture: {e}")

    def _cleanup(self):
        """Clean up resources"""
        if self.log_handler:
            try:
                self.log_handler.close()
            except:
                pass
            self.log_handler = None
        
        if self.log_file:
            try:
                self.log_file.close()
            except:
                pass
            self.log_file = None

    async def _cleanup_async(self):
        """Clean up resources asynchronously"""
        self._cleanup()
        await asyncio.sleep(0)  # Give event loop a chance to handle file operations

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry_error_callback=lambda retry_state: retry_state.outcome.result()
    )
    async def send_notification_async(self, error: Optional[Exception] = None):
        """Send email notification asynchronously"""
        try:
            msg = await self._prepare_email(error)
            
            # Use aiosmtplib for async SMTP operations
            smtp = aiosmtplib.SMTP(
                hostname=self.host,
                port=self.port,
                start_tls=self.use_tls
            )
            
            await smtp.connect()
            await smtp.login(self.username, self.password)
            await smtp.send_message(msg)
            await smtp.quit()
            
            logger.info(f"Async email sent successfully to {self.email}")
            
        except aiosmtplib.SMTPAuthenticationError as e:
            logger.error(f"SMTP authentication failed: {e}")
            raise EmailAuthError(f"SMTP authentication failed: {e}")
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            raise EmailSendError(f"Failed to send email: {e}")
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry_error_callback=lambda retry_state: retry_state.outcome.result()
    )
    def send_notification(self, error: Optional[Exception] = None):
        """Send email notification synchronously"""
        try:
            msg = asyncio.run(self._prepare_email(error))
            self._send_email(msg)
            logger.info(f"Email sent successfully to {self.email}")
            
        except smtplib.SMTPAuthenticationError as e:
            logger.error(f"SMTP authentication failed: {e}")
            raise EmailAuthError(f"SMTP authentication failed: {e}")
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            raise EmailSendError(f"Failed to send email: {e}")
    
    async def _prepare_email(self, error: Optional[Exception] = None) -> MIMEMultipart:
        """Prepare email message with template"""
        msg = MIMEMultipart('alternative')
        msg['From'] = self.username
        msg['To'] = ', '.join(self.email)
        msg['Subject'] = self.subject
        
        # Get log content if available
        log_content = ""
        if self.attach_logs and self.log_file:
            with open(self.log_file.name, 'r') as f:
                log_content = f.read()
        
        # Render template
        content = self.template.render(
            title=self.subject,
            message="Task completed successfully!" if not error else "Task failed!",
            details=log_content,
            error=error,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        
        # Attach both HTML and text versions
        msg.attach(MIMEText(content['text'], 'plain'))
        msg.attach(MIMEText(content['html'], 'html'))
        
        # Attach log file if enabled
        if self.attach_logs and self.log_file:
            with open(self.log_file.name, 'rb') as f:
                log_attachment = MIMEApplication(f.read(), _subtype='txt')
                log_attachment.add_header(
                    'Content-Disposition',
                    'attachment',
                    filename=f'task_log_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
                )
                msg.attach(log_attachment)
        
        return msg
    
    def _send_email(self, msg: MIMEMultipart):
        """Send email using SMTP"""
        context = ssl.create_default_context() if self.use_tls else None
        
        with smtplib.SMTP(self.host, self.port) as server:
            if self.use_tls:
                server.starttls(context=context)
            server.login(self.username, self.password)
            server.send_message(msg)

def py_mail_me(
    email: Union[str, List[str]],
    subject: str = "Task Completed",
    attach_logs: bool = False,
    host: Optional[str] = None,
    port: Optional[int] = None,
    username: Optional[str] = None,
    password: Optional[str] = None,
    use_tls: bool = True,
    max_retries: int = 3,
    template: Optional[EmailTemplate] = None,
    async_mode: bool = False
):
    """Decorator for sending email notifications after task completion"""
    def decorator(func: Callable):
        if asyncio.iscoroutinefunction(func):
            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                async with EmailNotifier(
                    email=email,
                    subject=subject,
                    attach_logs=attach_logs,
                    host=host,
                    port=port,
                    username=username,
                    password=password,
                    use_tls=use_tls,
                    max_retries=max_retries,
                    template=template,
                    async_mode=True
                ):
                    return await func(*args, **kwargs)
            return async_wrapper
        else:
            @wraps(func)
            def sync_wrapper(*args, **kwargs):
                with EmailNotifier(
                    email=email,
                    subject=subject,
                    attach_logs=attach_logs,
                    host=host,
                    port=port,
                    username=username,
                    password=password,
                    use_tls=use_tls,
                    max_retries=max_retries,
                    template=template,
                    async_mode=async_mode
                ):
                    return func(*args, **kwargs)
            return sync_wrapper
        
    return decorator 