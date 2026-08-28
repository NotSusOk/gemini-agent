"""Cấu hình mẫu — copy thành config.py và điền key của bạn.
KHÔNG bao giờ đẩy config.py (chứa key thật) lên GitHub!"""
GEMINI_KEY = "your-gemini-api-key-here"
GEMINI_BASE = "https://generativelanguage.googleapis.com/v1beta/openai/"

DEEPSEEK_KEY = "your-deepseek-api-key-here"
DEEPSEEK_BASE = "https://api.deepseek.com/v1"

# Chuỗi failover: (model, nguồn). DeepSeek chính (không giới hạn), Gemini dự phòng (free).
MODELS = [
    ("deepseek-v4-flash", "deepseek"),
    ("gemini-3.6-flash", "gemini"),
    ("gemini-3.5-flash", "gemini"),
    ("gemini-3-flash-preview", "gemini"),
]
