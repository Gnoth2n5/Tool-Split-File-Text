import re
import os
from pathlib import Path
import customtkinter as ctk
from tkinter import filedialog, messagebox

class ChapterSplitterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tool Tách Chương")
        self.root.geometry("600x400")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Biến lưu trữ
        self.input_file = ""
        self.output_dir = ""
        self.pattern = r"Chương\s+\d+:"

        # Tạo giao diện
        self.create_widgets()

    def create_widgets(self):
        title_label = ctk.CTkLabel(self.root, text="Tool Tách Chương Truyện", font=("Arial", 20, "bold"))
        title_label.pack(pady=20)

        frame = ctk.CTkFrame(self.root)
        frame.pack(pady=10, padx=20, fill="both", expand=True)

        self.input_label = ctk.CTkLabel(frame, text="Chọn file txt: Chưa chọn")
        self.input_label.pack(pady=5)
        input_btn = ctk.CTkButton(frame, text="Chọn File", command=self.select_input_file)
        input_btn.pack(pady=5)

        self.output_label = ctk.CTkLabel(frame, text="Thư mục đầu ra: Chưa chọn")
        self.output_label.pack(pady=5)
        output_btn = ctk.CTkButton(frame, text="Chọn Thư Mục", command=self.select_output_dir)
        output_btn.pack(pady=5)

        pattern_label = ctk.CTkLabel(frame, text="Pattern tách chương:")
        pattern_label.pack(pady=5)
        self.pattern_entry = ctk.CTkEntry(frame, width=300)
        self.pattern_entry.insert(0, "Chương\s+\d+:")
        self.pattern_entry.pack(pady=5)

        run_btn = ctk.CTkButton(frame, text="Tách Chương", command=self.split_chapters, fg_color="#28a745", hover_color="#218838")
        run_btn.pack(pady=20)

        self.status_label = ctk.CTkLabel(self.root, text="")
        self.status_label.pack(pady=10)

    def select_input_file(self):
        self.input_file = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if self.input_file:
            self.input_label.configure(text=f"Chọn file txt: {os.path.basename(self.input_file)}")

    def select_output_dir(self):
        self.output_dir = filedialog.askdirectory()
        if self.output_dir:
            self.output_label.configure(text=f"Thư mục đầu ra: {self.output_dir}")
        else:
            self.output_dir = "output"

    def split_chapters(self):
        if not self.input_file:
            messagebox.showerror("Lỗi", "Vui lòng chọn file txt!")
            return
        if not self.output_dir:
            self.output_dir = "output"

        self.pattern = self.pattern_entry.get() or r"Chương\s+\d+:"
        try:
            Path(self.output_dir).mkdir(parents=True, exist_ok=True)

            # Đọc file
            try:
                with open(self.input_file, 'r', encoding='utf-8') as file:
                    content = file.read()
            except UnicodeDecodeError:
                import chardet
                with open(self.input_file, 'rb') as file:
                    raw = file.read()
                    encoding = chardet.detect(raw)['encoding']
                with open(self.input_file, 'r', encoding=encoding) as file:
                    content = file.read()

            # Tách nội dung thành các phần dựa trên pattern
            parts = re.split(f"({self.pattern}.*?)(?=\n|$)", content, flags=re.MULTILINE)
            chapters = []
            intro_content = ""

            for i in range(len(parts)):
                part = parts[i].strip()
                if part:
                    if re.match(self.pattern, part):
                        # Đây là tiêu đề chương
                        chapter_title = part
                        # Lấy nội dung chương từ phần tiếp theo
                        if i + 1 < len(parts):
                            chapter_content = parts[i + 1].strip()
                            chapters.append({"title": chapter_title, "content": chapter_content})
                    elif not chapters:  # Phần trước chương 1 là phần giới thiệu
                        intro_content = part

            # Lưu phần giới thiệu (nếu có)
            if intro_content:
                self.save_intro(intro_content)

            # Lưu các chương
            for idx, chapter in enumerate(chapters):
                self.save_chapter(chapter, idx)

            self.status_label.configure(text=f"Đã tách thành công {len(chapters)} chương!")
            messagebox.showinfo("Thành công", f"Đã tách {len(chapters)} chương vào {self.output_dir}")

        except Exception as e:
            self.status_label.configure(text=f"Lỗi: {str(e)}")
            messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {str(e)}")

    def save_intro(self, intro_content):
        filepath = os.path.join(self.output_dir, "intro.txt")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(intro_content)

    def save_chapter(self, chapter, chapter_number):
        filename = f"chapter_{str(chapter_number).zfill(3)}.txt"
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(chapter["title"] + "\n\n")
            f.write(chapter["content"])

if __name__ == "__main__":
    root = ctk.CTk()
    app = ChapterSplitterApp(root)
    root.mainloop()