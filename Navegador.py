import tkinter as tk
from tkinter import scrolledtext, messagebox
from urllib.request import urlopen
from urllib.error import URLError

class MiniBrowser:
    def __init__(self, root):
        self.root = root
        self.root.title("PiZero Browser")
        self.root.geometry("800x480")
        self.dark_mode = False
        
        # Interface
        self.create_widgets()
        
    def create_widgets(self):
        # Barra superior
        top_frame = tk.Frame(self.root)
        top_frame.pack(fill=tk.X)
        
        # Botões
        tk.Button(top_frame, text="←", command=self.go_back).pack(side=tk.LEFT)
        tk.Button(top_frame, text="↻", command=self.refresh).pack(side=tk.LEFT)
        
        # Barra de URL
        self.url_entry = tk.Entry(top_frame, width=50)
        self.url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.url_entry.bind("<Return>", self.load_page)
        
        # Botão de tema
        self.theme_btn = tk.Button(top_frame, text="🌙", command=self.toggle_theme)
        self.theme_btn.pack(side=tk.RIGHT)
        
        # Área de conteúdo
        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD)
        self.text_area.pack(fill=tk.BOTH, expand=True)
        
        # Carrega página inicial
        self.load_page(url="https://example.com")

    def load_page(self, event=None, url=None):
        url = url or self.url_entry.get()
        if not url.startswith(("http://", "https://")):
            url = "http://" + url
        
        try:
            with urlopen(url, timeout=5) as response:
                content = response.read().decode('utf-8', errors='ignore')
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, content[:5000])  # Limita a 5000 caracteres
                self.url_entry.delete(0, tk.END)
                self.url_entry.insert(0, url)
                
        except URLError as e:
            messagebox.showerror("Erro", f"Não foi possível carregar:\n{str(e)}")

    def go_back(self):
        pass  # Implementação simplificada

    def refresh(self):
        self.load_page()

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        bg = "#333333" if self.dark_mode else "#ffffff"
        fg = "#ffffff" if self.dark_mode else "#000000"
        
        self.root.config(bg=bg)
        self.text_area.config(bg=bg, fg=fg)
        self.theme_btn.config(text="☀️" if self.dark_mode else "🌙")

if __name__ == "__main__":
    root = tk.Tk()
    app = MiniBrowser(root)
    root.mainloop()
