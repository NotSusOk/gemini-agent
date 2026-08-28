"""Cấu hình mẫu — copy thành config.py và điền key của bạn.
KHÔNG bao giờ đẩy config.py (chứa key thật) lên GitHub!"""
GEMINI_KEY = "your-gemini-api-key-here"
API_BASE = "https://generativelanguage.googleapis.com/v1beta/openai/"

# Chuỗi failover: model xịn trước, model dự phòng sau (mỗi model quota riêng).
MODELS = [
    "gemini-3.6-flash",
    "gemini-3.5-flash",
    "gemini-3-flash-preview",
    "gemini-3.5-flash-lite",
]
