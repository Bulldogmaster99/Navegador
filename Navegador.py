import gi
gi.require_version("Gtk", "3.0")
gi.require_version("WebKit2", "4.0")
from gi.repository import Gtk, WebKit2

# Código do seu navegador aqui

class PiZeroBrowser(Gtk.Window):
    def __init__(self):
        super().__init__(title="PiZero Browser")
        self.set_default_size(800, 480)  # Resolução ideal para Pi Zero
        
        # Configurações para economizar recursos
        self.settings = WebKit2.Settings()
        self.settings.set_enable_javascript(True)  # Desative se não precisar de JS
        self.settings.set_enable_media_stream(False)  # Desativa vídeo/áudio
        self.settings.set_enable_smooth_scrolling(False)
        
        self.webview = WebKit2.WebView(settings=self.settings)
        self.webview.load_uri("https://lite.duckduckgo.com")  # Página inicial leve
        
        # Barra de URL
        self.url_bar = Gtk.Entry()
        self.url_bar.connect("activate", self.load_url)
        
        # Botões (Voltar/Recarregar)
        self.back_btn = Gtk.Button(label="←")
        self.back_btn.connect("clicked", self.go_back)
        self.reload_btn = Gtk.Button(label="↻")
        self.reload_btn.connect("clicked", self.reload_page)
        
        # Layout
        header = Gtk.Box(spacing=5)
        header.pack_start(self.back_btn, False, False, 0)
        header.pack_start(self.url_bar, True, True, 0)
        header.pack_start(self.reload_btn, False, False, 0)
        
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        vbox.pack_start(header, False, False, 0)
        vbox.pack_start(self.webview, True, True, 0)
        
        self.add(vbox)
    
    def load_url(self, widget):
        url = self.url_bar.get_text()
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        self.webview.load_uri(url)
        self.url_bar.set_text(url)
    
    def go_back(self, widget):
        self.webview.go_back()
    
    def reload_page(self, widget):
        self.webview.reload()

def main():
    win = PiZeroBrowser()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()

if __name__ == "__main__":
    main()
