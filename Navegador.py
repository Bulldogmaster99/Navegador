import sys
import os
import tempfile
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QPushButton, QTabWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, QTimer

class TemporaryBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pi Zero 2W Browser")
        self.setGeometry(100, 100, 800, 600)
        
        # Dicionário para armazenar arquivos temporários por aba
        self.temp_files = {}
        
        # Configuração da interface
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        
        # Barra de endereço
        self.address_bar = QLineEdit()
        self.address_bar.setPlaceholderText("Digite a URL (ex: https://example.com)")
        self.go_button = QPushButton("Ir")
        self.go_button.clicked.connect(self.load_url)
        
        # Widget de abas
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        
        # Adicionar primeira aba
        self.add_new_tab()
        
        # Layout
        url_layout = QVBoxLayout()
        url_layout.addWidget(self.address_bar)
        url_layout.addWidget(self.go_button)
        self.layout.addLayout(url_layout)
        self.layout.addWidget(self.tabs)
        
    def add_new_tab(self, url=None):
        """Adiciona uma nova aba ao navegador"""
        web_view = QWebEngineView()
        
        if url:
            web_view.load(QUrl(url))
        else:
            web_view.setHtml("<h1>Nova Aba</h1><p>Digite uma URL e clique em Ir</p>")
        
        # Configurar para capturar HTML quando a página carregar
        web_view.loadFinished.connect(lambda ok, view=web_view: self.page_loaded(ok, view))
        
        index = self.tabs.addTab(web_view, "Nova Aba")
        self.tabs.setCurrentIndex(index)
        
        # Inicializar entrada para esta aba no dicionário
        self.temp_files[index] = None
        
    def load_url(self):
        """Carrega a URL digitada na barra de endereços"""
        url = self.address_bar.text()
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        
        current_webview = self.tabs.currentWidget()
        if current_webview:
            current_webview.load(QUrl(url))
    
    def page_loaded(self, ok, web_view):
        """Executado quando a página termina de carregar"""
        if ok:
            # Obter o HTML da página
            web_view.page().toHtml(self.save_html_file)
            
            # Atualizar título da aba
            title = web_view.title()
            if len(title) > 15:
                title = title[:15] + "..."
            index = self.tabs.indexOf(web_view)
            self.tabs.setTabText(index, title)
    
    def save_html_file(self, html_content):
        """Salva o HTML em um arquivo temporário e o abre"""
        index = self.tabs.currentIndex()
        current_webview = self.tabs.currentWidget()
        
        # Se já existir um arquivo temporário para esta aba, remova-o
        if self.temp_files.get(index):
            try:
                os.unlink(self.temp_files[index])
            except:
                pass
        
        # Criar novo arquivo temporário
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
            f.write(html_content)
            temp_file_path = f.name
        
        # Salvar referência ao arquivo temporário
        self.temp_files[index] = temp_file_path
        
        # Carregar o arquivo localmente
        current_webview.load(QUrl.fromLocalFile(temp_file_path))
    
    def close_tab(self, index):
        """Fecha a aba e remove o arquivo temporário associado"""
        if index in self.temp_files and self.temp_files[index]:
            try:
                os.unlink(self.temp_files[index])
            except:
                pass
            del self.temp_files[index]
        
        widget = self.tabs.widget(index)
        if widget:
            widget.deleteLater()
        
        self.tabs.removeTab(index)
        
        # Se não houver mais abas, adicione uma nova
        if self.tabs.count() == 0:
            self.add_new_tab()
    
    def closeEvent(self, event):
        """Limpando todos os arquivos temporários ao fechar a janela"""
        for index, file_path in self.temp_files.items():
            if file_path:
                try:
                    os.unlink(file_path)
                except:
                    pass
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Configurar para melhor desempenho no Pi Zero 2W
    os.environ['QTWEBENGINE_CHROMIUM_FLAGS'] = '--single-process --disable-gpu'
    
    browser = TemporaryBrowser()
    browser.show()
    sys.exit(app.exec_())
