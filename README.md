Repo : https://github.com/qowiys/naiki-sportswear
Web : muhammad-qowiy-naikisportswear.pbp.cs.ui.ac.id

Tugas 2

1. - Buat projek django dengan menjalankan command 'django-admin startproject naiki_sportswear' di terminal
   - Buat app main di level root dengan command 'python manage.py startapp main
   - Tambahkan 'main' di INSTALLED_APPS pada file setting.py
   - Buat model product yang diinginkan di models.py
   - Buat view dan template untuk menampilkan nama dan kelas
   - Migrasi database dengan command 'python manage.py makemigrations' dan 'python manage.py migrate'
   - Push ke pws dan juga git

2. 
[Client Browser] --HTTP GET / --> [Web Server (nginx/gunicorn/uwsgi)]
      |
      v
[Django WSGI entry] -> settings.py loaded (DATABASE, INSTALLED_APPS, TEMPLATES ...)
      |
      v
[URL Resolver] (naiki_sportswear/urls.py)  --matches--> include('main.urls')
      |
      v
[main/urls.py]  --matches path '' --> calls views.index
      |
      v
[views.index(request)] 
    - may call main.models.Product.objects.filter(...)
    - prepares context data
    - calls render(request, 'main/index.html', context)
      |
      v
[Template Engine] (loads main/templates/main/index.html)
      |
      v
[HTTP Response] (HTML)  <-- returned to Client Browser

- urls.py (project & app)

Peran: memetakan path URL ke fungsi/class view. Project urls.py biasanya meng-include urls dari app.

- views.py

Peran: menerima HttpRequest, menjalankan logika (mengambil data lewat model, memproses), dan mereturn HttpResponse atau render(template, context).

- models.py

Peran: definisi struktur data (ORM). View memanggil Model.objects.* untuk baca/tulis ke database.

- HTML (template)

Peran: representasi tampilan. Template menerima context dari view untuk di-render jadi HTML.

3. settings.py mengontrol perilaku seluruh aplikasi Django — lingkungan, keamanan, middleware, DB, file statis, dll. contoh :
    - Mengatur INSTALLED_APPS: daftar app yang terdaftar (penting agar models/migrations/templatetags berfungsi)
    - DATABASES: koneksi DB (sqlite/postgres/mysql). Menentukan engine, nama DB, credensial
    - MIDDLEWARE: urutan middleware yang memproses request/response (security, sessions, auth)
    - TEMPLATES: konfigurasi engine template, lokasi direktori template, context processors
    - STATIC & MEDIA: direktori dan URL untuk file statis dan media upload
    - AUTHENTICATION: pengaturan user model, login redirect, password validators
    - DEBUG & ALLOWED_HOSTS: mode debug lokal vs produksi; host yang diizinkan
    - SECRET_KEY: kunci rahasia (HARUS disimpan aman, jangan push ke Git)
    - LOGGING: pengaturan logging
    - STATIC_ROOT / MEDIA_ROOT: lokasi collectstatic, upload files di server

4. Migrasi = sinkronisasi antara kode model Python dengan struktur tabel di database, dicatat step-by-step agar aman dan konsisten. Penjelasan step-by-step :
    - Definisikan model di models.py.
    - Jalankan python manage.py makemigrations → Django membuat file migrasi (Python script) berisi instruksi perubahan database.
    - Jalankan python manage.py migrate → Django menerjemahkan instruksi migrasi jadi SQL (CREATE TABLE, ALTER TABLE, dll.) lalu menjalankannya di database.
    - Django menyimpan catatan migrasi yang sudah dijalankan di tabel khusus (django_migrations) agar tidak dijalankan ulang.

5. Menurut saya sebegai orang yang baru pertama kali belajar pengembangan perangkat lunak, django mudah dimengerti dan tampilannya tidak terlalu membingungkan

6. Sejauh ini belum ada feedback karena asisten dosen sudah membuat petunjuk-petunjuk tutorial 1 mudah dimengerti

Tugas 3

1. Data delivery di sini berarti mekanisme mengirim dan menyinkronkan data antar komponen (API → front-end, service → service, pihak ketiga seperti kurir, dsb). Tanpa mekanisme delivery yang jelas, fitur seperti notifikasi order, sinkron stok, atau webhook ke kurir akan rentan terlambat, tidak konsisten, atau gampang gagal.

2. JSON lebih baik dibanding XML untuk kebutuhan modern karena lebih ringkas, cepat diparsing, mudah dibaca, dan terintegrasi langsung dengan JavaScript maupun bahasa pemrograman lain. JSON juga lebih populer daripada XML karena ukuran datanya lebih kecil, performa lebih baik, dan ekosistem API (REST/GraphQL) sudah menjadikannya standar de facto, sementara XML cenderung lebih berat dan verbose.

3. is_valid() melakukan beberapa hal penting ketika form dikirim:
- Binding & parsing: memeriksa data yang dibind ke form (request.POST/request.FILES).
- Field-level validation: menjalankan clean_<field>() dan validator bawaan (max_length, required, dsb.).
- Form-level validation: menjalankan clean() di form untuk aturan yang melibatkan beberapa field.
- Menyediakan cleaned_data: kalau valid → data yang “bersih” (terkonversi ke tipe Python) tersedia di form.cleaned_data.
- Mengisi form.errors: kalau tidak valid, form.errors berisi pesan validasi untuk ditampilkan ke user.

is_valid() penting karena :
- Mencegah data invalid/berbahaya masuk ke model/database.
- Menyediakan alur untuk menampilkan error yang ramah ke user.
- Menyediakan data yang sudah dikonversi (mis. string → datetime, string → int) sehingga aman untuk disimpan.

4. CSRF (Cross-Site Request Forgery) terjadi ketika browser pengguna melakukan request yang tampak sah ke situs A, namun request itu dipicu oleh halaman jahat di situs B dan browser tetap mengirim cookie sesi sehingga tindakan dilakukan atas nama pengguna.

Peran csrf_token:
- Django menyisipkan token unik di form ({% csrf_token %}) dan memeriksa token itu saat menerima POST.
- Token memastikan request berasal dari origin yang valid (halaman yang diberikan token), bukan dari situs lain.
- Jika tidak menambahkan csrf_token:
- Middleware Django akan menolak request POST (jika CSRF protection aktif) → error 403.
- Jika CSRF protection dimatikan (@csrf_exempt) atau cookie disalahkonfigurasi → situs menjadi rentan. Penyerang bisa membuat form/javasript di situs lain yang mengirim POST ke endpointmu; browser korban akan menyertakan cookie autentik sehingga aksi berjalan (contoh: transfer uang, ubah alamat, hapus data).

Contoh eksploitasi sederhana:
- Korban login ke bank.example.com.
- Penyerang membuat halaman evil.com yang berisi <form action="https://bank.example.com/transfer" method="POST">... auto submit ...</form>.
- Jika bank.example.com tidak memverifikasi CSRF, form dari evil.com akan membuat bank melakukan transfer memakai cookie sesi korban.

5. - Merancang data & API → tentukan struktur data (mis. product dengan nama, harga, kategori) dan gunakan JSON agar ringan dan mudah diintegrasikan.
   - Membuat model & migration → definisikan model di Django lalu jalankan makemigrations dan migrate agar database siap.
   - Menggunakan form + is_valid() → form Django memastikan input valid dan aman sebelum disimpan ke database.
   - Menambahkan {% csrf_token %} → mencegah serangan CSRF saat pengguna mengirim form.
   - Uji coba end-to-end → jalankan alur lengkap (buat produk → tampil di halaman utama → validasi → tampil detail) untuk memastikan semua berjalan sesuai rencana.

6. Sejauh ini belum ada feedback karena asisten dosen sudah membuat petunjuk-petunjuk tutorial 2 mudah dimengerti

Screenshot Postman : https://drive.google.com/drive/folders/1yB9Gha4R16czTbWZ1H9L8eeoViuKQXVZ?usp=sharing