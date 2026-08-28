"""Quản lý lịch học — lưu JSON, giống memory.py nhưng cho lịch học."""
import json
import os
from datetime import datetime

LICH_FILE = os.path.join(os.path.dirname(__file__), "lich_hoc.json")

def doc_lich() -> dict:
    if os.path.exists(LICH_FILE):
        try:
            with open(LICH_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def ghi_lich(data: dict):
    with open(LICH_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def them_lop(ten_lop: str) -> str:
    data = doc_lich()
    if ten_lop not in data:
        data[ten_lop] = []  # danh sách buổi học
        ghi_lich(data)
    return f"Đã thêm lớp '{ten_lop}'"

def them_buoi(ten_lop: str, ngay: str, gio: str, mon: str = "") -> str:
    """Thêm 1 buổi học: ten_lop, ngay (VD: thứ 4), gio (VD: 19:00), mon (VD: Toán)."""
    data = doc_lich()
    if ten_lop not in data:
        data[ten_lop] = []
    buoi = {"ngay": ngay, "gio": gio, "mon": mon, "them_luc": datetime.now().strftime("%Y-%m-%d %H:%M")}
    data[ten_lop].append(buoi)
    ghi_lich(data)
    return f"Đã thêm buổi {mon} lớp '{ten_lop}' lúc {ngay} {gio}"

def doi_buoi(ten_lop: str, ngay_cu: str, ngay_moi: str = "", gio_moi: str = "") -> str:
    """Đổi lịch 1 buổi: tìm buổi theo ngay_cu trong lớp, đổi sang ngay_moi/gio_moi."""
    data = doc_lich()
    if ten_lop not in data:
        return f"Không tìm thấy lớp '{ten_lop}'"
    for buoi in data[ten_lop]:
        if buoi["ngay"] == ngay_cu:
            if ngay_moi:
                buoi["ngay"] = ngay_moi
            if gio_moi:
                buoi["gio"] = gio_moi
            ghi_lich(data)
            return f"Đã đổi lịch lớp '{ten_lop}': {ngay_cu} → {buoi['ngay']} {buoi['gio']}"
    return f"Không tìm thấy buổi học ngày {ngay_cu} trong lớp '{ten_lop}'"

def xoa_buoi(ten_lop: str, ngay: str) -> str:
    data = doc_lich()
    if ten_lop not in data:
        return f"Không tìm thấy lớp '{ten_lop}'"
    for buoi in data[ten_lop]:
        if buoi["ngay"] == ngay:
            data[ten_lop].remove(buoi)
            ghi_lich(data)
            return f"Đã xoá buổi {buoi['mon']} lớp '{ten_lop}' ngày {ngay}"
    return f"Không tìm thấy buổi ngày {ngay}"

# ── Ngoại lệ: đổi/nghỉ ĐÚNG NGÀY CỤ THỂ, không ảnh hưởng lịch tuần ──
def them_ngoai_le(ten_lop: str, ngay_thang: str, loai: str = "nghi", gio_moi: str = "") -> str:
    """Ngoại lệ 1 ngày: ngay_thang (VD: 31/08/2026), loai = nghi | doi_gio, gio_moi nếu doi_gio."""
    data = doc_lich()
    if "ngoai_le" not in data:
        data["ngoai_le"] = {}
    if ten_lop not in data["ngoai_le"]:
        data["ngoai_le"][ten_lop] = {}
    if loai == "nghi":
        data["ngoai_le"][ten_lop][ngay_thang] = {"loai": "nghi"}
        ghi_lich(data)
        return f"Đã ghi: lớp '{ten_lop}' NGHỈ ngày {ngay_thang} (chỉ hôm đó, lịch tuần giữ nguyên)"
    elif loai == "doi_gio":
        data["ngoai_le"][ten_lop][ngay_thang] = {"loai": "doi_gio", "gio_moi": gio_moi}
        ghi_lich(data)
        return f"Đã ghi: lớp '{ten_lop}' ngày {ngay_thang} đổi giờ sang {gio_moi} (chỉ hôm đó)"
    return "Loại ngoại lệ không hợp lệ (nghi | doi_gio)"

def xoa_ngoai_le(ten_lop: str, ngay_thang: str) -> str:
    data = doc_lich()
    if data.get("ngoai_le", {}).get(ten_lop, {}).get(ngay_thang):
        del data["ngoai_le"][ten_lop][ngay_thang]
        ghi_lich(data)
        return f"Đã bỏ ngoại lệ lớp '{ten_lop}' ngày {ngay_thang}"
    return f"Không có ngoại lệ nào ngày {ngay_thang}"

def lich_text() -> str:
    """Toàn bộ lịch dạng văn bản cho model/người xem."""
    data = doc_lich()
    if not data:
        return "(chưa có lịch học nào)"
    lines = []
    for lop, buois in data.items():
        if lop == "ngoai_le":
            continue
        lines.append(f"Lớp {lop}:")
        for b in buois:
            mon = f" ({b['mon']})" if b.get("mon") else ""
            lines.append(f"  - {b['ngay']} {b['gio']}{mon}")
    # Ngoại lệ
    if data.get("ngoai_le"):
        lines.append("Ngoại lệ (chỉ áp dụng đúng hôm đó):")
        for lop, items in data["ngoai_le"].items():
            for ngay, info in items.items():
                if info["loai"] == "nghi":
                    lines.append(f"  - {lop} ngày {ngay}: NGHỈ")
                else:
                    lines.append(f"  - {lop} ngày {ngay}: đổi giờ → {info.get('gio_moi','')}")
    return "\n".join(lines)

if __name__ == "__main__":
    them_lop("Toán 10A")
    them_buoi("Toán 10A", "thứ 2", "19:00", "Toán")
    them_buoi("Toán 10A", "thứ 5", "19:00", "Toán")
    print(lich_text())
    print("---")
    print(doi_buoi("Toán 10A", "thứ 2", ngay_moi="thứ 3", gio_moi="20:00"))
    print(lich_text())
