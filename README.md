# py-mail-me

**py-mail-me** is a simple Python package that automatically sends email notifications after task completion (such as data processing, model training, web scraping, etc.), with attached logs or execution outputs. It's perfect for long-running programs, scheduled tasks, CI/CD pipelines, and automation scripts.

---

## Features

- **Automatic email notifications upon task completion**
- **Support for log file and output attachments**
- **Quick integration via decorators or context managers**
- **Customizable email recipients, subjects, and content**
- **Integration with Python's logging module**

---

## Installation

1. Install directly by `pip install` (**not available now**)

   ```bash
   pip install py-mail-me
   ```

2. Or install the latest version from GitHub:

   ```bash
   pip install git+https://github.com/juihsuanlee0303/py-mail-me.git
   ```

---

## Quick Start

### Using the Decorator

```python
from py_mail_me import py_mail_me

@py_mail_me(
    email="you@example.com",
    subject="Task Completion Notification",
    attach_logs=True,
    password="your-app-password"
)
def long_running_task():
    print("Processing...")
    # Task logic here
```

### Using the Context Manager

```python
from py_mail_me import EmailNotifier

with EmailNotifier(
    email="you@example.com",
    subject="Data Processing Complete",
    attach_logs=True,
    password="your password"
):
    # Main work here
    print("Processing...")
```

---

## Configuration

Set up email credentials using environment variables or a `.env` file:

```bash
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
```

Or pass configuration parameters directly in the code.

---

## Parameters

### EmailNotifier and py_mail_me Parameters

| Parameter   | Type             | Required | Default          | Description                                |
| ----------- | ---------------- | -------- | ---------------- | ------------------------------------------ |
| email       | str or List[str] | Yes      | -                | Email address(es) to receive notifications |
| subject     | str              | No       | "Task Completed" | Email subject line                         |
| attach_logs | bool             | No       | False            | Whether to attach execution logs           |
| host        | str              | No       | "smtp.gmail.com" | SMTP server host                           |
| port        | int              | No       | 587              | SMTP server port                           |
| username    | str              | No       | EMAIL_USER       | SMTP username (defaults to env var)        |
| password    | str              | No       | EMAIL_PASSWORD   | SMTP password (defaults to env var)        |

### Environment Variables

| Variable       | Required | Default          | Description                             |
| -------------- | -------- | ---------------- | --------------------------------------- |
| EMAIL_HOST     | No       | "smtp.gmail.com" | SMTP server host                        |
| EMAIL_PORT     | No       | 587              | SMTP server port                        |
| EMAIL_USER     | Yes\*    | -                | SMTP username (required if not in code) |
| EMAIL_PASSWORD | Yes\*    | -                | SMTP password (required if not in code) |

\* Either environment variables or direct parameters must be provided for authentication.

### Gmail Setup

If using Gmail:

1. Enable 2-Step Verification in your Google Account
2. Generate an App Password:
   - Go to Google Account Settings
   - Security > 2-Step Verification > App passwords
   - Select "Mail" and your device
   - Use the generated password in EMAIL_PASSWORD

---

## Examples

The `examples` directory contains several practical use cases:

### 1. Machine Learning Training Notification (decorator_example.py)

Using a decorator to send notifications after model training:

```python
@py_mail_me(
    email="your-email@gmail.com",
    subject="Model Training Complete",
    attach_logs=True,
    password="your-app-password"
)
def train_model():
    logger.info("Starting model training...")
    # Training process...
    logger.info("Training complete!")
```

### 2. Web Scraping Task (context_manager_example.py)

Using a context manager to send notifications to multiple recipients after web scraping:

```python
with EmailNotifier(
    email=["admin@example.com", "team@example.com"],
    subject="Web Scraping Complete",
    attach_logs=True,
    password="your password"
):
    logger.info("Starting web scraping task...")
    # Scraping process...
    logger.info("Scraping complete")
```

### 3. Error Handling (error_handling_example.py)

Demonstrating automatic error notifications:

```python
with EmailNotifier(
    email="admin@example.com",
    subject="Data Processing Status",
    attach_logs=True,
    password="your password"
):
    try:
        result = process_data(invalid_data)
    except Exception as e:
        logger.error(f"Processing failed: {str(e)}")
        raise  # EmailNotifier will catch and send error notification
```

Complete example code can be found in the `examples` directory.

---

## Use Cases

- Data processing workflows (ETL, data cleaning)
- Machine learning training tasks
- Web scraping and report generation
- Daily/weekly scheduled tasks
- Automated testing or deployment notifications
- Remote notifications for CLI tools

---

## Roadmap

- [x] Basic email notification functionality
- [x] Log file and output attachments
- [ ] Error catching and notification
- [ ] Support for multiple notification channels (Telegram, Slack, LINE Notify)
- [ ] Web UI for notification history management
- [ ] Automatic Python logging module integration

---

## Contributing

Contributions are welcome! Feel free to submit PRs or open issues to discuss new features or improvements.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/my-feature`)
5. Submit a Pull Request

---

## License

MIT License

---

## Contact

For questions or suggestions, please contact:

- GitHub: [juihsuanlee0303](https://github.com/juihsuanlee0303)
- Email: juihsuanlee0303@gmail.com
