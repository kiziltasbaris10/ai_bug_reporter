import re

def analyze_log_advanced(log: str) -> dict:
    log_lower = log.lower()

    if "timeout" in log_lower:
        return {
            "category": "Timeout Error",
            "reason": "Detected 'timeout' in log",
            "suggestion": "Check internet connection or server response time."
        }
    elif "connection refused" in log_lower:
        return {
            "category": "Connection Error",
            "reason": "Detected 'connection refused' in log",
            "suggestion": "Ensure the server is running and accepting connections."
        }
    elif re.search(r"null\s+pointer", log_lower):
        return {
            "category": "Null Pointer Exception",
            "reason": "Detected 'null pointer' in log",
            "suggestion": "Check for uninitialized variables in your code."
        }
    elif "500" in log_lower:
        return {
            "category": "Server Error (500)",
            "reason": "Detected HTTP 500 status",
            "suggestion": "Check server logs for internal error."
        }
    elif "404" in log_lower:
        return {
            "category": "Not Found Error (404)",
            "reason": "Detected HTTP 404 status",
            "suggestion": "Verify the requested resource exists."
        }
    else:
        return {
            "category": "Unknown",
            "reason": "No known error pattern matched",
            "suggestion": "Please check logs manually."
        }
