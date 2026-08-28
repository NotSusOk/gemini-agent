"""Trí nhớ đơn giản — lưu JSON vào file, giống như "não bộ" của agent."""
import json
import os

MEMORY_FILE = os.path.join(os.path.dirname(__file__), "memory.json")

# ── 1. Đọc trí nhớ từ file ──
def doc_memory() -> dict:
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

# ── 2. Ghi trí nhớ xuống file ──
def ghi_memory(data: dict):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ── 3. Nhớ một thông tin mới (key → value) ──
def nho(key: str, value: str):
    data = doc_memory()
    data[key] = value
    ghi_memory(data)
    return f"Đã nhớ: {key} = {value}"

# ── 4. Lấy thông tin đã nhớ ──
def nho_gi(key: str) -> str:
    data = doc_memory()
    return data.get(key, "Không có thông tin này.")

# ── 5. Liệt kê toàn bộ trí nhớ dạng văn bản (để đưa vào prompt) ──
def memory_text() -> str:
    data = doc_memory()
    if not data:
        return "(chưa có gì trong trí nhớ)"
    return "\n".join(f"- {k}: {v}" for k, v in data.items())

# ── Test nhanh ──
if __name__ == "__main__":
    nho("ten_user", "Đạt")
    print("Trí nhớ hiện tại:")
    print(memory_text())
    print("\nHỏi lại:", nho_gi("ten_user"))
