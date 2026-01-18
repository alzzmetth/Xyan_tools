# Xyan_tools
XYANZ adalah alat profesional untuk mengekstrak kode HTML, CSS, dan JavaScript dari website secara langsung melalui terminal. Dibangun dengan Python dan menggunakan BeautifulSoup untuk parsing yang akurat.

✨ Fitur Utama

· 🔥 Ekstraksi Lengkap: HTML, CSS, dan JavaScript dari website manapun
· 🎨 Syntax Highlighting: Warna berbeda untuk setiap jenis kode (HTML/CSS/JS)
· 📊 Statistik Detail: Analisis komprehensif elemen webpage
· ⚡ Real-time Preview: Tampilkan hasil langsung di terminal
· 🎯 Interface Merah: Desain terminal dengan dominasi warna merah
· 🔗 Support Eksternal: Ekstrak CSS dan JavaScript dari file eksternal
· 📈 Progress Indicator: Animasi loading dengan visual menarik

📋 Prasyarat

· Python 3.6 atau lebih tinggi
· pip (Python package manager)

🚀 Instalasi Cepat

Metode 1: Clone Repository

```bash
git clone https://github.com/username/xyanz-extractor.git
cd xyanz-extractor
pip install -r requirements.txt
python xyanz.py
```

Metode 2: Manual Installation

```bash
# Clone atau download file xyanz.py
# Install dependencies
pip install colorama requests beautifulsoup4

# Jalankan alat
python xyanz.py
```

📖 Cara Penggunaan

1. Menjalankan XYANZ

```bash
python xyanz.py
```

2. Input Domain

```
══════════════════════════════════════════════════════════════
                    MASUKKAN DOMAIN
══════════════════════════════════════════════════════════════

📌 Format: domain.com atau https://domain.com
❌ Ketik 'keluar' untuk berhenti
──────────────────────────────────────────────────────────────
➤ example.com
```

3. Proses Ekstraksi

· Sistem akan menampilkan animasi loading merah
· Mengambil halaman website
· Mengekstrak semua kode (HTML, CSS, JavaScript)
· Menampilkan statistik

4. Menu Interaktif

```
PILIH KODE UNTUK DITAMPILKAN:
1. HTML
2. CSS
3. JavaScript
4. Tampilkan Semua
5. Website Baru
6. Keluar

➤ Pilihan (1-6):
```

🔧 Fitur Teknis

📊 Statistik yang Diperoleh

· Jumlah tag meta, link, dan gambar
· Total script (inline dan eksternal)
· Ukuran setiap jenis kode (karakter)
· Judul halaman
· Waktu ekstraksi

🎨 Syntax Highlighting

· HTML: Tag merah, atribut cyan, nilai hijau
· CSS: Selector kuning, properti cyan, nilai hijau
· JavaScript: Keyword magenta, string hijau, angka kuning

🌐 Support Website

· Website dengan HTTPS/HTTP
· Halaman dengan multiple CSS/JS eksternal
· Website dengan framework JavaScript
· Halaman responsif/mobile-friendly

📝 Contoh Output

Statistik

```
📊 STATISTIK EKSTRAKSI
─────────────────────────
• Judul Halaman: Example Domain
• Tag Meta: 3
• Link: 15
• Gambar: 8
• Script: 5
• Ukuran HTML: 12,345 karakter
• Ukuran CSS: 4,567 karakter
• Ukuran JS: 8,901 karakter
```

Preview Kode

```
══════════════════════════════════════════════════════════════
 🚀 HTML 
══════════════════════════════════════════════════════════════
  1 │ <!DOCTYPE html>
  2 │ <html lang="en">
  3 │ <head>
  4 │     <meta charset="UTF-8">
  5 │     <meta name="viewport" content="width=device-width, initial-scale=1.0">
  6 │     <title>Example Domain</title>
  7 │     <style>
  8 │         body { background: #f0f0f0; }
  9 │     </style>
 10 │ </head>
```

🛠️ Dependencies

Package Version Description
colorama =0.4.4 Cross-platform colored terminal text
requests =2.25.1 HTTP library for Python
beautifulsoup4 =4.9.3 HTML parsing library

🔍 Teknik Ekstraksi

1. HTML Parsing

· Menggunakan BeautifulSoup untuk parsing akurat
· Menjaga struktur indentasi asli
· Memisahkan inline dan external resources

2. CSS Extraction

· Tag <style> inline
· Atribut style pada elemen
· File CSS eksternal
· Import statements

3. JavaScript Extraction

· Tag <script> inline
· File JS eksternal
· Event handlers
· Dynamic script injection detection

⚠️ Catatan Penting

Legal Considerations

· Gunakan alat ini hanya untuk website yang Anda miliki
· Patuhi robots.txt dan terms of service
· Hormati hak cipta dan lisensi kode

Technical Limitations

· Tidak bisa mengekstrak kode yang di-generate oleh JavaScript
· Membutuhkan koneksi internet untuk website eksternal
· Mungkin terdeteksi sebagai bot oleh beberapa website

🚀 Advanced Usage

Command Line Arguments

```bash
# Ekstrak langsung tanpa menu interaktif
python xyanz.py --url https://example.com --output html

# Tampilkan hanya CSS
python xyanz.py --url https://example.com --css-only

# Save output to file
python xyanz.py --url https://example.com --save output.txt
```

Integration dengan Tools Lain

```python
from xyanz import XyanzExtractor

extractor = XyanzExtractor()
result = extractor.extract_code("https://example.com")
# Gunakan result['html'], result['css'], result['js']
```

🐛 Troubleshooting

Common Issues

1. Connection Error
   ```
   Solution: Periksa koneksi internet dan firewall
   ```
2. SSL Certificate Error
   ```
   Solution: Tambahkan verify=False pada requests.get()
   ```
3. Website Blocked
   ```
   Solution: Ubah User-Agent atau tambahkan delay
   ```
4. Memory Error (Large Websites)
   ```
   Solution: Gunakan --chunk-size untuk websites besar
   ```

Debug Mode

```bash
python xyanz.py --debug --url https://example.com
```

📈 Roadmap

· v1.1: Support untuk SPA (Single Page Applications)
· v1.2: Export ke berbagai format (JSON, Markdown)
· v1.3: Batch processing untuk multiple URLs
· v1.4: API untuk integrasi dengan tools lain
· v1.5: GUI interface dengan Tkinter

🤝 Kontribusi

Kontribusi dipersilakan! Ikuti langkah berikut:

1. Fork repository
2. Buat branch fitur (git checkout -b feature/AmazingFeature)
3. Commit perubahan (git commit -m 'Add some AmazingFeature')
4. Push ke branch (git push origin feature/AmazingFeature)
5. Buat Pull Request

📄 Lisensi

Distributed under the MIT License. See LICENSE for more information.

📞 Kontak

Developer Team - team@xyanz.dev

Project Link: https://github.com/username/xyanz-extractor

🙏 Acknowledgments

· BeautifulSoup - Untuk HTML parsing
· Requests - Untuk HTTP requests
· Colorama - Untuk terminal colors
· Komunitas Python Indonesia

---

<div align="center">

Made with ❤️ by XYANZ Team

⭐ Star di GitHub • 
🐛 Report Bug • 
💡 Request Feature

</div>

🎯 Quick Start Example

```bash
# Clone repository
git clone https://github.com/username/xyanz-extractor.git

# Navigate to directory
cd xyanz-extractor

# Install dependencies
pip install -r requirements.txt

# Run with example
python xyanz.py

# Enter: example.com
# Choose: 4 (Tampilkan Semua)
```

🔄 Update

Untuk mendapatkan versi terbaru:

```bash
cd xyanz-extractor
git pull origin main
pip install --upgrade -r requirements.txt
```

---

Note: Alat ini dikembangkan untuk membantu developer dalam analisis website. Gunakan dengan bijak dan bertanggung jawab.
