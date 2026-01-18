import requests
from bs4 import BeautifulSoup
import urllib.parse
import re
import time
from urllib.parse import urljoin, urlparse
import sys
import os
from colorama import init, Fore, Back, Style

# Initialize colorama
init(autoreset=True)

class XyanzExtractor:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def show_banner(self):
        """Menampilkan banner XYANZ berwarna merah menyala"""
        print(Fore.RED + Style.BRIGHT)
        print(Fore.RED + """\n
  ██╗  ██╗██╗   ██╗ █████╗ ███╗   ██╗███████╗
  ╚██╗██╔╝╚██╗ ██╔╝██╔══██╗████╗  ██║╚══███╔╝
   ╚███╔╝  ╚████╔╝ ███████║██╔██╗ ██║  ███╔╝ 
   ██╔██╗   ╚██╔╝  ██╔══██║██║╚██╗██║ ███╔╝  
  ██╔╝ ██╗   ██║   ██║  ██║██║ ╚████║███████╗
  ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝
        """)   

    
    def show_loading(self, message):
        """Animasi loading merah"""
        print(Fore.RED + Style.BRIGHT + "🔥 " + message + " " + Style.RESET_ALL, end="")
        
        animation = ["▉", "▊", "▋", "▌", "▍", "▎", "▏", "▎", "▍", "▌", "▋", "▊", "▉"]
        for i in range(len(animation)):
            sys.stdout.write("\r" + Fore.RED + Style.BRIGHT + "🔥 " + message + " " + animation[i % len(animation)] + " " + Style.RESET_ALL)
            sys.stdout.flush()
            time.sleep(0.1)
        print()
    
    def clear_screen(self):
        """Membersihkan layar"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def get_input(self):
        """Mendapatkan input domain"""
        
        print("masukan domain : ")
        print(Fore.RED + "─" * 60 + Style.RESET_ALL)
        
        while True:
            domain = input(Fore.RED + "➤ " + Style.RESET_ALL).strip()
            if domain.lower() in ['keluar', 'exit', 'quit']:
                return None
            if domain:
                return domain
            print(Fore.RED + "⚠ Domain tidak boleh kosong!" + Style.RESET_ALL)
    
    def normalize_url(self, domain):
        """Menormalisasi URL"""
        if not domain.startswith(('http://', 'https://')):
            return 'https://' + domain
        return domain
    
    def fetch_page(self, url):
        """Mengambil halaman web"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(Fore.RED + f"✖ Gagal mengambil halaman: {str(e)[:50]}..." + Style.RESET_ALL)
            return None
    
    def extract_code(self, html, url):
        """Mengekstrak semua kode dari HTML"""
        soup = BeautifulSoup(html, 'html.parser')
        
        # HTML
        full_html = soup.prettify()
        
        # CSS
        css_code = ""
        css_blocks = []
        
        # CSS inline dari tag style
        for style in soup.find_all('style'):
            if style.string:
                css_blocks.append(style.string.strip())
        
        # CSS dari atribut style
        for tag in soup.find_all(style=True):
            css_blocks.append(f"/* Inline: {tag.name} */\n{tag['style']}")
        
        # CSS eksternal
        for link in soup.find_all('link', rel='stylesheet'):
            css_url = link.get('href')
            if css_url:
                full_css_url = urljoin(url, css_url)
                try:
                    css_response = self.session.get(full_css_url, timeout=5)
                    if css_response.status_code == 200:
                        css_blocks.append(f"/* External: {full_css_url} */\n{css_response.text}")
                except:
                    pass
        
        if css_blocks:
            css_code = "\n" + "═"*50 + "\n".join(css_blocks)
        
        # JavaScript
        js_code = ""
        js_blocks = []
        
        # JS inline
        for script in soup.find_all('script'):
            if script.string and script.string.strip():
                js_blocks.append(script.string.strip())
        
        # JS eksternal
        for script in soup.find_all('script', src=True):
            js_url = script.get('src')
            if js_url:
                full_js_url = urljoin(url, js_url)
                try:
                    js_response = self.session.get(full_js_url, timeout=5)
                    if js_response.status_code == 200:
                        js_blocks.append(f"/* External: {full_js_url} */\n{js_response.text}")
                except:
                    pass
        
        if js_blocks:
            js_code = "\n" + "═"*50 + "\n".join(js_blocks)
        
        # Metadata
        title = soup.title.string if soup.title else "Tidak ada judul"
        meta_tags = len(soup.find_all('meta'))
        links = len(soup.find_all('a'))
        images = len(soup.find_all('img'))
        scripts = len(soup.find_all('script'))
        
        return {
            'title': title,
            'html': full_html,
            'css': css_code,
            'js': js_code,
            'stats': {
                'meta': meta_tags,
                'links': links,
                'images': images,
                'scripts': scripts,
                'html_size': len(full_html),
                'css_size': len(css_code),
                'js_size': len(js_code)
            }
        }
    
    def display_stats(self, stats):
        """Menampilkan statistik dengan desain merah"""
        print(Fore.RED + Style.BRIGHT + "\n" + "📊 STATISTIK EKSTRAKSI")
        print(Fore.RED + "─" * 40 + Style.RESET_ALL)
        
        stats_text = f"""
        {Fore.RED}• Judul Halaman: {Fore.WHITE}{stats.get('title', 'N/A')}
        {Fore.RED}• Tag Meta: {Fore.WHITE}{stats['stats']['meta']}
        {Fore.RED}• Link: {Fore.WHITE}{stats['stats']['links']}
        {Fore.RED}• Gambar: {Fore.WHITE}{stats['stats']['images']}
        {Fore.RED}• Script: {Fore.WHITE}{stats['stats']['scripts']}
        {Fore.RED}• Ukuran HTML: {Fore.WHITE}{stats['stats']['html_size']:,} karakter
        {Fore.RED}• Ukuran CSS: {Fore.WHITE}{stats['stats']['css_size']:,} karakter
        {Fore.RED}• Ukuran JS: {Fore.WHITE}{stats['stats']['js_size']:,} karakter
        """
        print(stats_text)
    
    def display_code(self, code_type, content, max_lines=30):
        """Menampilkan kode dengan warna merah"""
        print(Fore.RED + Style.BRIGHT + "\n" + "═" * 70)
        print(f" 🚀 {code_type.upper()} ")
        print("═" * 70 + Style.RESET_ALL)
        
        if not content:
            print(Fore.RED + "✖ Tidak ada kode " + code_type + " ditemukan" + Style.RESET_ALL)
            return
        
        lines = content.split('\n')
        
        # Tampilkan preview 30 baris pertama
        for i, line in enumerate(lines[:max_lines]):
            line_num = i + 1
            # Highlight syntax sederhana
            if code_type == 'html':
                colored_line = self.highlight_html(line)
            elif code_type == 'css':
                colored_line = self.highlight_css(line)
            elif code_type == 'javascript':
                colored_line = self.highlight_js(line)
            else:
                colored_line = Fore.WHITE + line
            
            print(f"{Fore.RED}{line_num:3} │ {colored_line}{Style.RESET_ALL}")
        
        if len(lines) > max_lines:
            print(Fore.RED + f"\n📄 Menampilkan {max_lines} dari {len(lines)} baris..." + Style.RESET_ALL)
        
        # Opsi untuk melihat lebih banyak
        if len(lines) > max_lines:
            print(Fore.RED + "\n" + "─" * 40)
            show_more = input(Fore.RED + "👁 Tampilkan semua kode? (y/n): " + Style.RESET_ALL).lower()
            if show_more == 'y':
                print(Fore.RED + "═" * 70)
                print(f" 📋 {code_type.upper()} LENGKAP ")
                print("═" * 70 + Style.RESET_ALL)
                for i, line in enumerate(lines):
                    line_num = i + 1
                    if code_type == 'html':
                        colored_line = self.highlight_html(line)
                    elif code_type == 'css':
                        colored_line = self.highlight_css(line)
                    elif code_type == 'javascript':
                        colored_line = self.highlight_js(line)
                    else:
                        colored_line = Fore.WHITE + line
                    
                    print(f"{Fore.RED}{line_num:4} │ {colored_line}{Style.RESET_ALL}")
    
    def highlight_html(self, line):
        """Highlight syntax HTML"""
        if not line.strip():
            return Fore.WHITE + line
        
        # Tag HTML
        line = re.sub(r'&lt;(/?)(\w+)&gt;', 
                     Fore.RED + r'&lt;\1' + Fore.YELLOW + r'\2' + Fore.RED + r'&gt;' + Fore.WHITE, 
                     line)
        
        # Attributes
        line = re.sub(r'(\w+)=["\'][^"\']*["\']', 
                     Fore.CYAN + r'\1' + Fore.WHITE + r'="' + Fore.GREEN + r'\g<0>' + Fore.WHITE + r'"', 
                     line)
        
        # Comments
        if '<!--' in line and '-->' in line:
            line = Fore.GREEN + line + Style.RESET_ALL
        
        return Fore.WHITE + line
    
    def highlight_css(self, line):
        """Highlight syntax CSS"""
        if not line.strip():
            return Fore.WHITE + line
        
        # Selectors
        line = re.sub(r'([^{}]+){', 
                     Fore.YELLOW + r'\1' + Fore.WHITE + r'{', 
                     line)
        
        # Properties
        line = re.sub(r'(\s*)([a-z-]+)(\s*:\s*)', 
                     Fore.CYAN + r'\1\2' + Fore.WHITE + r'\3', 
                     line)
        
        # Values
        line = re.sub(r':\s*([^;]+);', 
                     Fore.WHITE + r': ' + Fore.GREEN + r'\1' + Fore.WHITE + r';', 
                     line)
        
        # Comments
        if '/*' in line and '*/' in line:
            line = Fore.GREEN + line
        
        return Fore.WHITE + line
    
    def highlight_js(self, line):
        """Highlight syntax JavaScript"""
        if not line.strip():
            return Fore.WHITE + line
        
        # Keywords
        keywords = ['function', 'var', 'let', 'const', 'if', 'else', 'for', 'while', 
                   'return', 'true', 'false', 'null', 'undefined', 'new', 'this']
        
        for keyword in keywords:
            line = re.sub(r'\b' + keyword + r'\b', 
                         Fore.MAGENTA + keyword + Fore.WHITE, 
                         line)
        
        # Strings
        line = re.sub(r'["\'][^"\']*["\']', 
                     Fore.GREEN + r'\g<0>' + Fore.WHITE, 
                     line)
        
        # Numbers
        line = re.sub(r'\b\d+\b', 
                     Fore.YELLOW + r'\g<0>' + Fore.WHITE, 
                     line)
        
        # Comments
        if '//' in line:
            parts = line.split('//', 1)
            line = Fore.WHITE + parts[0] + Fore.GREEN + '//' + parts[1]
        
        return Fore.WHITE + line
    
    def run(self):
        """Menjalankan ekstraktor"""
        self.clear_screen()
        self.show_banner()
        
        while True:
            domain = self.get_input()
            if not domain:
                print(Fore.RED + "\n👋 Selesai!" + Style.RESET_ALL)
                break
            
            url = self.normalize_url(domain)
            
            print(Fore.RED + Style.BRIGHT + f"\n🎯 Target: {url}" + Style.RESET_ALL)
            
            # Proses ekstraksi
            self.show_loading("Mengakses website")
            
            html = self.fetch_page(url)
            if not html:
                print(Fore.RED + "✖ Gagal mengambil data dari website" + Style.RESET_ALL)
                continue
            
            self.show_loading("Mengekstrak kode HTML")
            time.sleep(0.3)
            
            self.show_loading("Mengekstrak kode CSS")
            time.sleep(0.3)
            
            self.show_loading("Mengekstrak kode JavaScript")
            time.sleep(0.3)
            
            print(Fore.RED + Style.BRIGHT + "\n✅ EKSTRAKSI BERHASIL!" + Style.RESET_ALL)
            
            # Ekstrak kode
            result = self.extract_code(html, url)
            
            # Tampilkan statistik
            self.display_stats(result)
            
            # Tampilkan kode
            print(Fore.RED + "\n" + "═" * 70)
            print(" 📋 PREVIEW KODE ")
            print("═" * 70 + Style.RESET_ALL)
            
            # Menu pilihan
            while True:
                print(Fore.RED + "\nPILIH KODE UNTUK DITAMPILKAN:")
                print(Fore.RED + "1. HTML")
                print(Fore.RED + "2. CSS")
                print(Fore.RED + "3. JavaScript")
                print(Fore.RED + "4. Tampilkan Semua")
                print(Fore.RED + "5. Website Baru")
                print(Fore.RED + "6. Keluar")
                
                choice = input(Fore.RED + "\n➤ Pilihan (1-6): " + Style.RESET_ALL).strip()
                
                if choice == '1':
                    self.display_code('html', result['html'])
                elif choice == '2':
                    self.display_code('css', result['css'])
                elif choice == '3':
                    self.display_code('javascript', result['js'])
                elif choice == '4':
                    self.display_code('html', result['html'])
                    input(Fore.RED + "\n↵ Enter untuk lanjut ke CSS..." + Style.RESET_ALL)
                    self.display_code('css', result['css'])
                    input(Fore.RED + "\n↵ Enter untuk lanjut ke JavaScript..." + Style.RESET_ALL)
                    self.display_code('javascript', result['js'])
                elif choice == '5':
                    self.clear_screen()
                    self.show_banner()
                    break
                elif choice == '6':
                    print(Fore.RED + "\n👋 Selesai!" + Style.RESET_ALL)
                    return
                else:
                    print(Fore.RED + "⚠ Pilihan tidak valid!" + Style.RESET_ALL)
                
                input(Fore.RED + "\n↵ Enter untuk kembali ke menu..." + Style.RESET_ALL)

def check_dependencies():
    """Memeriksa dan menginstal dependensi"""
    try:
        from colorama import init
        init()
    except ImportError:
        print("Menginstal Colorama...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "colorama"])
    
    try:
        import requests
    except ImportError:
        print("Menginstal Requests...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        print("Menginstal BeautifulSoup4...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "beautifulsoup4"])

def main():
    """Fungsi utama"""
    # Periksa dependensi
    check_dependencies()
    
    # Jalankan extractor
    extractor = XyanzExtractor()
    extractor.run()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(Fore.RED + "\n\n✖ Dihentikan oleh pengguna" + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"\n⚠ Error: {e}" + Style.RESET_ALL)
