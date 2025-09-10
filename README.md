Repo : https://github.com/qowiys/naiki-sportswear
Web : muhammad-qowiy-naikisportswear.pbp.cs.ui.ac.id

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