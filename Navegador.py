import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import requests
from bs4 import BeautifulSoup

class PiLiteBrowser:
    def __init__(self, root):
        self.root = root
        self.root.title("PiLite Basic")
        self.root.geometry("1024x600")
        self.setup_ui()
        self.history = []
        self.dark_mode = False
        self.toggle_theme()

    def setup_ui(self):
        # Barra superior
        self.top_frame = ttk.Frame(self.root)
        self.top_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        # Botões de navegação
        self.back_btn = ttk.Button(self.top_frame, text="←", width=3, command=self.go_back)
        self.back_btn.pack(side=tk.LEFT)

        self.refresh_btn = ttk.Button(self.top_frame, text="↻", width=3, command=self.refresh_page)
        self.refresh_btn.pack(side=tk.LEFT)

        # Barra de URL
        self.url_entry = ttk.Entry(self.top_frame, width=60)
        self.url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.url_entry.bind("<Return>", self.load_page)

        # Botão de tema
        self.theme_btn = ttk.Button(self.top_frame, text="🌙", width=3, command=self.toggle_theme)
        self.theme_btn.pack(side=tk.RIGHT)

        # Abas
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        self.create_new_tab()

    def create_new_tab(self, url="https://lite.duckduckgo.com"):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Nova aba")
        
        # Área de texto com rolagem
        text_area = scrolledtext.ScrolledText(
            frame,
            wrap=tk.WORD,
            font=('Arial', 10),
            padx=10,
            pady=10
        )
        text_area.pack(fill=tk.BOTH, expand=True)
        
        self.notebook.select(frame)
        self.load_page(url=url, text_area=text_area)
        return frame

    def load_page(self, event=None, url=None, text_area=None):
        if not text_area:
            current_tab = self.notebook.nametowidget(self.notebook.select())
            text_area = current_tab.winfo_children()[0]
        
        url = url or self.url_entry.get()
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        
        try:
            response = requests.get(url, timeout=5)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove elementos complexos
            for element in soup(["script", "style", "iframe", "img", "video"]):
                element.decompose()
            
            # Extrai texto limpo
            clean_text = soup.get_text(separator="\n", strip=True)
            text_area.delete(1.0, tk.END)
            text_area.insert(tk.END, clean_text)
            
            self.url_entry.delete(0, tk.END)
            self.url_entry.insert(0, url)
            self.root.title(f"PiLite - {url[:30]}...")
            self.history.append(url)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar:\n{str(e)}")

    def go_back(self):
        if len(self.history) > 1:
            self.history.pop()
            self.load_page(url=self.history[-1])

    def refresh_page(self):
        self.load_page()

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        bg = "#2e2e2e" if self.dark_mode else "#ffffff"
        fg = "#ffffff" if self.dark_mode else "#000000"
        
        self.root.config(bg=bg)
        self.theme_btn.config(text="☀️" if self.dark_mode else "🌙")
        
        # Aplica tema a todas as abas
        for tab_id in self.notebook.tabs():
            tab = self.notebook.nametowidget(tab_id)
            text_area = tab.winfo_children()[0]
            text_area.config(
                bg=bg,
                fg=fg,
                insertbackground=fg
            )

if __name__ == "__main__":
    root = tk.Tk()
    app = PiLiteBrowser(root)
    root.mainloop()