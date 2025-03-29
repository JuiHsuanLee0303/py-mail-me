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
    <style>
        body { font-family: Arial, sans-serif; }
        .success { color: #28a745; }
        .error { color: #dc3545; }
        .content { padding: 20px; }
        pre { background: #f8f9fa; padding: 10px; }
    </style>
</head>
<body>
    <div class="content">
        <h2>${title}</h2>
        <div class="${status_class}">
            <p>${message}</p>
        </div>
        ${details}
        ${error_info}
        <hr>
        <p><small>Sent by py-mail-me</small></p>
    </div>
</body>
</html>
"""

DEFAULT_TEXT_TEMPLATE = """
${title}
${message}
${details}
${error_info}

Sent by py-mail-me
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
            template_vars = {
                'title': title,
                'message': message,
                'details': f"<pre>{details}</pre>" if details else "",
                'status_class': 'error' if error else 'success',
                'error_info': f"<pre class='error'>Error: {str(error)}</pre>" if error else "",
                **kwargs
            }
            
            # Plain text version
            text_vars = {
                **template_vars,
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