import tkinter as tk 
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import pytesseract
import os
import re

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class ImageToTextApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Image To Text')
        self.root.geometry('700x800')
        self.root.configure(bg='#f0f4f8')

        self.image_path = None

        style = ttk.Style()
        style.configure('TButton', font=('Segoe UI', 10), padding=6)
        style.configure('TLabel', font=('Segoe UI', 12), background='#f0f4f8')

        ttk.Label(root, text='🖼️ Image To Text', font=('Segoe UI', 18, 'bold')).pack(pady=20)

        tk.Button(root, text='Select Image', bg='#FFF000', fg='#000000', font=('Segoe UI', 10), command=self.load_image).pack(pady=10)

        self.image_label = ttk.Label(root)
        self.image_label.pack(pady=10)

        self.text_area = tk.Text(root, height=15, font=('Consolas', 11), wrap=tk.WORD, relief=tk.GROOVE, borderwidth=2)
        self.text_area.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        button_frame = ttk.Frame(root)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text='Converter', command=self.convert_image_to_text).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text='Reset', command=self.reset).pack(side=tk.LEFT, padx=10)

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[('Image Files', '*.png *.jpg *.jpeg *.bmp')])
        if file_path:
            self.image_path = file_path
            img = Image.open(file_path)
            img.thumbnail((500, 500))
            self.tk_image = ImageTk.PhotoImage(img)
            self.image_label.config(image=self.tk_image)

    def convert_image_to_text(self):
        if self.image_path:
            try: 
                text = pytesseract.image_to_string(Image.open(self.image_path))
                formatted_text = self.format_text(text)
                self.text_area.delete('1.0', tk.END)
                self.text_area.insert(tk.END, formatted_text)
            except Exception as e:
                messagebox.showerror('Erro', f'Converting image error: {e}')
        else: 
            messagebox.showwarning('Alert', 'No image selected.')
    
    def reset(self):
        self.image_path = None
        self.image_label.config(image='')
        self.text_area.delete('1.0', tk.END)

    def format_text(self, raw_text):
        text = re.sub('r[ ]{2,}', ' ', raw_text)
        text = re.sub(r'\n{2,}', '\n', text)

        text = re.sub(r"(\w+)-\n(\w+)", r"\1\2", text)

        text = '\n'.join(line.capitalize() for line in text.splitlines())

        return text.strip()

if __name__ == '__main__':
    root = tk.Tk()
    app = ImageToTextApp(root)
    root.mainloop()