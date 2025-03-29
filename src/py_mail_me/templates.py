"""
Email templates for py-mail-me package.
"""

from typing import Dict, Any, Optional
from string import Template
from .exceptions import TemplateError

DEFAULT_HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 0;
            background-color: #f8f9fa;
            color: #212529;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 30px 20px;
            background-color: #ffffff;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 1px solid #e9ecef;
        }
        .title {
            color: #2c3e50;
            font-size: 24px;
            font-weight: 600;
            margin: 0;
        }
        .content {
            padding: 20px 0;
        }
        .message {
            font-size: 16px;
            margin-bottom: 20px;
        }
        .success {
            color: #198754;
            padding: 15px;
            background-color: #d1e7dd;
            border-radius: 6px;
            margin-bottom: 20px;
        }
        .error {
            color: #842029;
            padding: 15px;
            background-color: #f8d7da;
            border-radius: 6px;
            margin-bottom: 20px;
        }
        .details {
            background-color: #f8f9fa;
            border-radius: 6px;
            padding: 15px;
            margin-bottom: 20px;
            font-family: 'SF Mono', 'Consolas', 'Monaco', monospace;
            font-size: 14px;
            overflow-x: auto;
            white-space: pre-wrap;
            word-wrap: break-word;
        }
        .footer {
            text-align: center;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #e9ecef;
            color: #6c757d;
            font-size: 14px;
        }
        @media (max-width: 600px) {
            .container {
                padding: 20px 15px;
            }
            .title {
                font-size: 20px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1 class="title">${title}</h1>
        </div>
        <div class="content">
            <div class="${status_class}">
                ${message}
            </div>
            ${details}
            ${error_info}
        </div>
        <div class="footer">
            <p>Sent by py-mail-me</p>
            <p>${timestamp}</p>
        </div>
    </div>
</body>
</html>
"""

DEFAULT_TEXT_TEMPLATE = """
${title}
${separator}

${message}

${details}
${error_info}

---
Sent by py-mail-me
${timestamp}
"""

class EmailTemplate:
    def __init__(
        self,
        html_template: Optional[str] = None,
        text_template: Optional[str] = None
    ):
        self.html_template = Template(html_template or DEFAULT_HTML_TEMPLATE)
        self.text_template = Template(text_template or DEFAULT_TEXT_TEMPLATE)
        
    def render(
        self,
        title: str,
        message: str,
        details: str = "",
        error: Optional[Exception] = None,
        **kwargs: Any
    ) -> Dict[str, str]:
        """
        Render both HTML and text versions of the email.
        
        Args:
            title: Email title
            message: Main message
            details: Additional details
            error: Exception object if any
            **kwargs: Additional template variables
            
        Returns:
            Dict containing 'html' and 'text' versions
        """
        try:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Convert newlines to <br> for HTML display
            formatted_details = details.replace('\n', '<br>') if details else ""
            formatted_error = str(error).replace('\n', '<br>') if error else ""
            
            template_vars = {
                'title': title,
                'message': message,
                'details': f'<div class="details">{formatted_details}</div>' if details else "",
                'status_class': 'error' if error else 'success',
                'error_info': f'<div class="details error">{formatted_error}</div>' if error else "",
                'timestamp': timestamp,
                **kwargs
            }
            
            # Plain text version
            text_vars = {
                **template_vars,
                'separator': '=' * len(title),
                'details': details or "",
                'error_info': f"\nError: {str(error)}" if error else ""
            }
            
            return {
                'html': self.html_template.safe_substitute(template_vars),
                'text': self.text_template.safe_substitute(text_vars)
            }
        except Exception as e:
            raise TemplateError(f"Failed to render template: {str(e)}")

# Default templates for different scenarios
SUCCESS_TEMPLATE = EmailTemplate()
ERROR_TEMPLATE = EmailTemplate() 