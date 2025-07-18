import tkinter as tk
from tkinter import ttk, messagebox
import requests
from bs4 import BeautifulSoup

class MiniBrowser:
    def __init__(self, root):
        self.root = root
        self.root.title("Pi Zero Browser")
        self.root.geometry("800x480")
        
        # Barra de URL
        self.url_bar = ttk.Entry(width=80)
        self.url_bar.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        self.url_bar.bind("<Return>", self.load_page)
        
        # Abas
        self.notebook = ttk.Notebook()
        self.notebook.pack(expand=True, fill=tk.BOTH)
        
        # Botões
        btn_frame = ttk.Frame()
        btn_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        ttk.Button(btn_frame, text="←", command=self.go_back).pack(side=tk.LEFT)
        ttk.Button(btn_frame, text="↻", command=self.refresh).pack(side=tk.LEFT)
        ttk.Button(btn_frame, text="+", command=self.new_tab).pack(side=tk.LEFT)
        
        # Primeira aba
        self.new_tab()
    
    def new_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Nova Aba")
        
        text = tk.Text(frame, wrap=tk.WORD)
        text.pack(expand=True, fill=tk.BOTH)
        
        self.notebook.select(frame)
        return text
    
    def load_page(self, event=None):
        url = self.url_bar.get()
        if not url.startswith(("http://", "https://")):
            url = "http://" + url
        
        try:
            # Modo econômico: só baixa texto
            response = requests.get(url, timeout=5)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove scripts/anúncios
            for script in soup(["script", "iframe", "style"]):
                script.decompose()
                
            text = self.notebook.nametowidget(self.notebook.select()).children["!text"]
            text.delete(1.0, tk.END)
            text.insert(tk.END, soup.get_text())
            
            self.root.title(f"Pi Browser - {url}")
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível carregar:\n{str(e)}")
    
    def go_back(self):
        # Implementação simplificada
        messagebox.showinfo("Info", "Funcionalidade de voltar não implementada (use o histórico do terminal)")
    
    def refresh(self):
        self.load_page()

if __name__ == "__main__":
    root = tk.Tk()
    MiniBrowser(root)
    root.mainloop()
