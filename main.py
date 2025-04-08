import tkinter as tk 
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
import pytesseract
import os

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class ImageToTextApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Image To Text')
        self.root.geometry('600x700')
        self.image_path = None

        tk.Label(root, text='Image To Text', font=('Helvetica', 18, 'bold')).pack(pady=10)

        tk.Button(root, text='Select Image', command=self.load_image).pack(pady=10)

        self.image_label = tk.Label(root)
        self.image_label.pack(pady=10)

        self.text_area = tk.Text(root, height=15, wrap=tk.WORD)
        self.text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text='Converter', command=self.convert_image_to_text).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text='Reset', command=self.reset).pack(side=tk.LEFT, padx=5)

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[('Image Files', '*.png *.jpg *.jpeg *.bmp')])
        if file_path:
            self.image_path = file_path
            img = Image.open(file_path)
            img.thumbnail((400, 400))
            self.tk_image = ImageTk.PhotoImage(img)
            self.image_label.config(image=self.tk_image)

    def convert_image_to_text(self):
        if self.image_path:
            try: 
                text = pytesseract.image_to_string(Image.open(self.image_path))
                self.text_area.delete('1.0', tk.END)
                self.text_area.insert(tk.END, text)
            except Exception as e:
                messagebox.showerror('Erro', f'Converting image error: {e}')
        else: 
            messagebox.showwarning('Alert', 'No image selected.')
    
    def reset(self):
        self.image_path = None
        self.image_label.config(image='')
        self.text_area.delete('1.o', tk.END)

if __name__ == '__main__':
    root = tk.Tk()
    app = ImageToTextApp(root)
    root.mainloop()