import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from tkhtmlview import HTMLLabel
import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageTk

class PiLiteBrowser:
    def __init__(self, root):
        self.root = root
        self.root.title("PiLite Browser")
        self.root.geometry("1024x600")
        self.setup_ui()
        self.history = []
        
        # Dark Mode
        self.dark_mode = True
        self.toggle_theme()

    def setup_ui(self):
        # Barra superior
        self.top_frame = ttk.Frame(self.root)
        self.top_frame.pack(side=tk.TOP, fill=tk.X)

        # Botões
        self.back_btn = ttk.Button(self.top_frame, text="←", command=self.go_back, width=3)
        self.back_btn.pack(side=tk.LEFT)

        self.refresh_btn = ttk.Button(self.top_frame, text="↻", command=self.refresh_page, width=3)
        self.refresh_btn.pack(side=tk.LEFT)

        # Barra de URL
        self.url_entry = ttk.Entry(self.top_frame, width=50)
        self.url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.url_entry.bind("<Return>", self.load_page)

        # Botão de tema
        self.theme_btn = ttk.Button(self.top_frame, text="🌙", command=self.toggle_theme, width=3)
        self.theme_btn.pack(side=tk.RIGHT)

        # Abas
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        self.create_new_tab("https://lite.duckduckgo.com")

    def create_new_tab(self, url):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Nova aba")
        
        # Área de conteúdo
        html_label = HTMLLabel(frame)
        html_label.pack(fill=tk.BOTH, expand=True)
        
        # Barra de rolagem
        scrollbar = ttk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.notebook.select(frame)
        self.load_page(url=url, html_label=html_label)
        return frame

    def load_page(self, event=None, url=None):
        current_tab = self.notebook.nametowidget(self.notebook.select())
        html_label = current_tab.winfo_children()[0]
        
        url = url or self.url_entry.get()
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        
        try:
            response = requests.get(url, timeout=5)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove elementos pesados
            for element in soup(["script", "iframe", "style", "img"]):
                element.decompose()
            
            # Atualiza interface
            html_label.set_html(str(soup))
            self.url_entry.delete(0, tk.END)
            self.url_entry.insert(0, url)
            self.root.title(f"PiLite - {url}")
            self.history.append(url)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível carregar:\n{str(e)}")

    def go_back(self):
        if len(self.history) > 1:
            self.history.pop()
            self.load_page(url=self.history[-1])

    def refresh_page(self):
        self.load_page(url=self.url_entry.get())

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        bg = "#2e2e2e" if self.dark_mode else "#ffffff"
        fg = "#ffffff" if self.dark_mode else "#000000"
        
        style = ttk.Style()
        style.configure(".", background=bg, foreground=fg)
        self.root.config(bg=bg)
        self.theme_btn.config(text="☀️" if self.dark_mode else "🌙")

if __name__ == "__main__":
    root = tk.Tk()
    app = PiLiteBrowser(root)
    root.mainloop()