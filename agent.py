"""Agent core — vòng lặp agent: model ↔ tools ↔ trả lời."""
import json
from openai import OpenAI
from config import GEMINI_KEY, GEMINI_BASE, DEEPSEEK_KEY, DEEPSEEK_BASE, MODELS
from memory import nho, nho_gi, memory_text
from lich_hoc import them_lop, them_buoi, doi_buoi, them_ngoai_le, xoa_ngoai_le, lich_text

# ── 1. Khai báo tools (dạng JSON Schema — model đọc để biết gọi gì) ──
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "tinh_toan",
            "description": "Tính kết quả biểu thức toán học đơn giản (+, -, *, /, **)",
            "parameters": {
                "type": "object",
                "properties": {
                    "bieu_thuc": {"type": "string", "description": "VD: 3*4+5"}
                },
                "required": ["bieu_thuc"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "doc_file",
            "description": "Đọc nội dung một file text trên máy",
            "parameters": {
                "type": "object",
                "properties": {
                    "duong_dan": {"type": "string", "description": "Đường dẫn file, VD: /Users/admin/agent_demo.py"}
                },
                "required": ["duong_dan"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "nho",
            "description": "Ghi nhớ một thông tin về người dùng (VD: tên, sở thích, ngày sinh)",
            "parameters": {
                "type": "object",
                "properties": {
                    "key": {"type": "string", "description": "Tên thông tin, VD: ten_user"},
                    "value": {"type": "string", "description": "Giá trị, VD: Đạt"}
                },
                "required": ["key", "value"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "nho_gi",
            "description": "Xem lại thông tin đã ghi nhớ trước đó",
            "parameters": {
                "type": "object",
                "properties": {
                    "key": {"type": "string", "description": "Tên thông tin cần xem, VD: ten_user"}
                },
                "required": ["key"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "chay_lenh",
            "description": "Chạy lệnh terminal trên máy (macOS). Dùng khi cần xem file, chạy script, kiểm tra hệ thống... VD: ls, pwd, python3 script.py, df -h",
            "parameters": {
                "type": "object",
                "properties": {
                    "lenh": {"type": "string", "description": "Lệnh cần chạy trong terminal"}
                },
                "required": ["lenh"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "them_lop",
            "description": "Thêm lớp học mới vào lịch",
            "parameters": {
                "type": "object",
                "properties": {
                    "ten_lop": {"type": "string", "description": "Tên lớp, VD: Toán 10A"}
                },
                "required": ["ten_lop"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "them_buoi",
            "description": "Thêm buổi học vào lịch của 1 lớp",
            "parameters": {
                "type": "object",
                "properties": {
                    "ten_lop": {"type": "string", "description": "Tên lớp"},
                    "ngay": {"type": "string", "description": "Ngày trong tuần, VD: thứ 2"},
                    "gio": {"type": "string", "description": "Giờ học, VD: 19:00"},
                    "mon": {"type": "string", "description": "Môn học (tùy chọn)"}
                },
                "required": ["ten_lop", "ngay", "gio"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "doi_buoi",
            "description": "Đổi lịch 1 buổi học đột xuất (đổi ngày/giờ)",
            "parameters": {
                "type": "object",
                "properties": {
                    "ten_lop": {"type": "string", "description": "Tên lớp"},
                    "ngay_cu": {"type": "string", "description": "Ngày hiện tại của buổi cần đổi, VD: thứ 2"},
                    "ngay_moi": {"type": "string", "description": "Ngày mới (tùy chọn)"},
                    "gio_moi": {"type": "string", "description": "Giờ mới (tùy chọn)"}
                },
                "required": ["ten_lop", "ngay_cu"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "xem_lich",
            "description": "Xem toàn bộ lịch học hiện tại",
            "parameters": {"type": "object", "properties": {}}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "them_ngoai_le",
            "description": "Ghi ngoại lệ cho 1 NGÀY CỤ THỂ (nghỉ hôm đó hoặc đổi giờ hôm đó) — KHÔNG ảnh hưởng lịch tuần. Dùng khi giáo viên báo nghỉ/đổi giờ đột xuất đúng 1 ngày.",
            "parameters": {
                "type": "object",
                "properties": {
                    "ten_lop": {"type": "string", "description": "Tên lớp"},
                    "ngay_thang": {"type": "string", "description": "Ngày cụ thể dạng DD/MM/YYYY, VD: 31/08/2026"},
                    "loai": {"type": "string", "enum": ["nghi", "doi_gio"], "description": "nghi = nghỉ hôm đó, doi_gio = đổi giờ hôm đó"},
                    "gio_moi": {"type": "string", "description": "Giờ mới nếu loai=doi_gio (VD: 20:00)"}
                },
                "required": ["ten_lop", "ngay_thang", "loai"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "xoa_ngoai_le",
            "description": "Bỏ ngoại lệ đã ghi cho 1 ngày cụ thể",
            "parameters": {
                "type": "object",
                "properties": {
                    "ten_lop": {"type": "string", "description": "Tên lớp"},
                    "ngay_thang": {"type": "string", "description": "Ngày dạng DD/MM/YYYY"}
                },
                "required": ["ten_lop", "ngay_thang"]
            }
        }
    },
]

# ── 2. Hàm chạy tool thật — đây là nơi agent "hành động" ──
def chay_tool(name: str, args: dict) -> str:
    if name == "tinh_toan":
        bieu_thuc = args["bieu_thuc"]
        try:
            # eval tính toán — chỉ dùng cho demo, đừng eval code không tin cậy!
            return str(eval(bieu_thuc))
        except Exception as e:
            return f"Lỗi tính toán: {e}"
    elif name == "doc_file":
        try:
            with open(args["duong_dan"], "r", encoding="utf-8") as f:
                return f.read()[:2000]  # giới hạn 2000 ký tự
        except Exception as e:
            return f"Lỗi đọc file: {e}"
    elif name == "nho":
        return nho(args["key"], args["value"])
    elif name == "nho_gi":
        return nho_gi(args["key"])
    elif name == "chay_lenh":
        import subprocess
        try:
            # shell=True cho phép chạy lệnh phức tạp (có pipe, &&, v.v.)
            # timeout=30: chặn lệnh chạy treo vô hạn
            ket_qua = subprocess.run(
                args["lenh"], shell=True,
                capture_output=True, text=True, timeout=30,
            )
            out = (ket_qua.stdout + ket_qua.stderr).strip()
            return out[:2000] if out else "(lệnh chạy xong, không có output)"
        except subprocess.TimeoutExpired:
            return "Lỗi: lệnh chạy quá 30 giây, đã bị huỷ"
        except Exception as e:
            return f"Lỗi chạy lệnh: {e}"
    elif name == "them_lop":
        return them_lop(args["ten_lop"])
    elif name == "them_buoi":
        return them_buoi(args["ten_lop"], args["ngay"], args.get("gio", ""), args.get("mon", ""))
    elif name == "doi_buoi":
        return doi_buoi(args["ten_lop"], args["ngay_cu"], args.get("ngay_moi", ""), args.get("gio_moi", ""))
    elif name == "xem_lich":
        return lich_text()
    elif name == "them_ngoai_le":
        return them_ngoai_le(args["ten_lop"], args["ngay_thang"], args.get("loai", "nghi"), args.get("gio_moi", ""))
    elif name == "xoa_ngoai_le":
        return xoa_ngoai_le(args["ten_lop"], args["ngay_thang"])
    return f"Tool '{name}' không tồn tại"

# ── 3. Vòng lặp agent — trái tim của toàn bộ hệ thống ──
# 2 clients: DeepSeek (trả phí, không giới hạn) + Gemini (free, giới hạn 20/ngày/model)
clients = {
    "deepseek": OpenAI(base_url=DEEPSEEK_BASE, api_key=DEEPSEEK_KEY),
    "gemini": OpenAI(base_url=GEMINI_BASE, api_key=GEMINI_KEY),
}

def chay_agent(noi_dung_user: str, max_vong: int = 5) -> str:
    # messages là "cuộc trò chuyện" — đầy đủ mọi thứ model cần biết
    messages = [
        # System prompt: định nghĩa "tính cách" + nhét trí nhớ đã có vào
        {"role": "system", "content": (
            "Bạn là trợ lý AI thân thiện tên Gemi. Trả lời ngắn gọn, tự nhiên. "
            "NGÔN NGỮ TRẢ LỜI: ưu tiên theo trí nhớ (nếu có ghi ngon_ngu thì dùng ngôn ngữ đó), "
            "không có thì mặc định tiếng Việt. "
            "Trí nhớ của bạn về người dùng:\n" + memory_text()
        )},
        {"role": "user", "content": noi_dung_user}
    ]

    for i in range(max_vong):
        # Bước A: hỏi model — trả lời hoặc gọi tool?
        # Failover: lỗi model này (quota/hết tiền) → thử model kế tiếp trong MODELS
        resp = None
        for model, nguon in MODELS:
            try:
                resp = clients[nguon].chat.completions.create(
                    model=model,
                    messages=messages,
                    tools=TOOLS,
                )
                break  # gọi thành công, dùng model này
            except Exception as e:
                is_quota = "429" in str(e) or "quota" in str(e).lower() or "RESOURCE_EXHAUSTED" in str(e) or "insufficient" in str(e).lower()
                print(f"  ⚠️ Model {model} ({nguon}) lỗi: {str(e)[:80]}")
                if not is_quota:
                    # Lỗi khác (không phải quota) — đừng đổi model, báo luôn
                    raise e
        if resp is None:
            return "⚠️ Tất cả model đều hết quota hôm nay — mai thử lại hoặc thêm key!"
        msg = resp.choices[0].message

        # Bước B: model muốn gọi tool?
        if msg.tool_calls:
            # Thêm tin nhắn assistant có tool_calls vào lịch sử (bắt buộc với API)
            messages.append(msg)
            for call in msg.tool_calls:
                print(f"  🔧 Gọi tool: {call.function.name}({call.function.arguments})")
                ket_qua = chay_tool(call.function.name, json.loads(call.function.arguments))
                print(f"  ✅ Kết quả: {ket_qua[:80]}")
                # Trả kết quả về cho model dưới role="tool"
                messages.append({
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": ket_qua,
                })
            # Lặp tiếp — model nhận kết quả và quyết định tiếp
        else:
            # Model trả lời xong — không gọi tool nữa
            return msg.content

    return "⚠️ Hết số vòng lặp tối đa — agent không hoàn thành."

# ── Chạy thử ──
if __name__ == "__main__":
    while True:
        cau_hoi = input("\n🧠 Bạn: ")
        if cau_hoi.lower() in ("exit", "thoat"):
            break
        print("🤖 Agent: ", end="", flush=True)
        print(chay_agent(cau_hoi))
