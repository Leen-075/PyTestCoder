# app/utils/security.py
import html

def sanitize_content(content: str) -> str:
    """
    清理可能包含XSS的内容
    Args:
        content: 需要清理的内容
    Returns:
        清理后的内容
    """
    return html.escape(content)