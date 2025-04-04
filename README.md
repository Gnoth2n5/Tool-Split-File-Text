# Tool Tách Chương Truyện

![Giao diện Tool](https://via.placeholder.com/600x400.png?text=Giao+diện+Tool+Tách+Chương)  

**Tool Tách Chương Truyện** là một ứng dụng desktop được viết bằng Python, sử dụng giao diện `customtkinter`, 
giúp tách các chương từ file truyện dạng `.txt` (đặc biệt là truyện convert tiếng Trung) thành các file riêng biệt. 
Công cụ này hỗ trợ xử lý encoding tự động và giữ nguyên định dạng gốc của nội dung.

## Tính năng
- Tách chương dựa trên pattern regex (mặc định: `Chương\s+\d+:`).
- Lưu phần giới thiệu (nếu có) thành file `intro.txt`.
- Tạo file riêng cho từng chương (ví dụ: `chapter_000.txt`).
- Giao diện thân thiện, hiện đại với `customtkinter`.
- Hỗ trợ xử lý file lớn và encoding phức tạp (UTF-8 hoặc tự động phát hiện).
- Có thể tùy chỉnh pattern tách chương.

## Yêu cầu hệ thống
- **Hệ điều hành**: Windows, macOS, Linux.
- **Python**: 3.1 trở lên.
- **Thư viện**:
  - `customtkinter`
  - `chardet`
