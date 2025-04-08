import tkinter as tk 
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import pytesseract
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
import re
from langdetect import detect

# T5 model in Portuguese by UNICAMP
MODEL_NAME = "unicamp-dl/ptt5-base-portuguese-vocab"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
corrector = pipeline("text2text-generation", model=model, tokenizer=tokenizer)

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def clean_ocr_text(text):
    text = text.replace('0 ', 'O ')
    text = re.sub(r'0(\w)', r'O\1', text)
    text = text.replace('“', '"').replace('”', '"')
    text = text.replace('‘', "'").replace('’', "'")
    return text

def detect_language(text):
    try:
        return detect(text)
    except:
        return 'unknown'

def ai_format_text(text):
    lines = text.splitlines()
    corrected_lines = []

    for line in lines:
        if line.strip():
            prompt = f"reformule: {line.strip()}"
            result = corrector(prompt, max_length=512, clean_up_tokenization_spaces=True)
            generated_text = result[0]['generated_text'].strip().replace("reformule: ", "")
            corrected_lines.append(generated_text)
        else:
            corrected_lines.append('')
    return '\n'.join(corrected_lines)

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

        tk.Button(button_frame, text='Convert', command=self.convert_image_to_text).pack(side=tk.LEFT, padx=10)
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
                text = clean_ocr_text(text)
                formatted_text = ai_format_text(text)
                self.text_area.delete('1.0', tk.END)
                self.text_area.insert(tk.END, formatted_text)
            except Exception as e:
                messagebox.showerror('Error', f'Error converting image: {e}')
        else:
            messagebox.showwarning('Warning', 'No image selected.')

    def reset(self):
        self.image_path = None
        self.image_label.config(image='')
        self.text_area.delete('1.0', tk.END)

if __name__ == '__main__':
    root = tk.Tk()
    app = ImageToTextApp(root)
    root.mainloop()
