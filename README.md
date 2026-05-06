# kpl-ticketing-system

# Event Ticketing & Booking System

Proyek ini adalah implementasi sistem pemesanan tiket acara menggunakan **Clean Architecture** dan **Domain-Driven Design (DDD)** sebagai bagian dari mata kuliah Konstruksi Perangkat Lunak di Institut Teknologi Sepuluh Nopember (ITS) [cite: 1].

## 1. Prerequisite

Sebelum menjalankan proyek ini, pastikan Anda telah menginstal perangkat lunak berikut:
* **Python 3.12+**
* **uv**: Pengelola dependensi dan environment Python yang sangat cepat.
* **PostgreSQL**: Database relasional yang wajib digunakan sesuai spesifikasi proyek [cite: 1].
* **Visual Studio Code**: Editor teks yang direkomendasikan dengan ekstensi:
    * Python (Microsoft)
    * Ruff (Astral Software) untuk linting dan formatting.

## 2. How to Run This Project

Ikuti langkah-langkah berikut untuk setup awal:

1.  **Sinkronisasi Dependensi**:
    Gunakan `uv` untuk menginstal semua library yang diperlukan dan membuat virtual environment secara otomatis:
    ```bash
    uv sync
    ```

2.  **Aktivasi Virtual Environment**:
    * Windows: `.venv\Scripts\activate`
    * macOS/Linux: `source .venv/bin/activate`

3.  **Menjalankan Aplikasi (FastAPI)**:
    Gunakan perintah berikut untuk menjalankan server development:
    ```bash
    uv run uvicorn src.main:app --reload
    ```

4.  **Menjalankan Unit Test**:
    Untuk memverifikasi logika domain (Target Week 9-10) [cite: 1]:
    ```bash
    uv run pytest
    ```

---

## 3. Business Rules (BR)

Daftar aturan bisnis berikut diekstrak langsung dari *User Stories* dan *Acceptance Criteria* dalam dokumen studi kasus [cite: 1]:

### Event Management
* **BR1**: Event tidak dapat dibuat jika tanggal berakhir lebih awal dari tanggal mulai [cite: 1].
* **BR2**: Kapasitas maksimum event harus lebih besar dari nol [cite: 1].
* **BR3**: Event yang baru dibuat harus berstatus `Draft` [cite: 1].
* **BR4**: Event hanya dapat dipublikasikan jika memiliki setidaknya satu kategori tiket aktif [cite: 1].
* **BR5**: Event hanya dapat dipublikasikan jika total kuota tiket tidak melebihi kapasitas maksimum event [cite: 1].
* **BR6**: Event dengan status `Draft` dapat diubah menjadi `Published` [cite: 1].
* **BR7**: Event dengan status `Cancelled` tidak dapat dipublikasikan [cite: 1].
* **BR8**: Event dengan status `Published` dapat dibatalkan [cite: 1].
* **BR9**: Event dengan status `Completed` tidak dapat dibatalkan [cite: 1].
* **BR10**: Saat event dibatalkan, semua kategori tiket tidak dapat lagi dibeli [cite: 1].
* **BR11**: Saat event dibatalkan, pemesanan yang sudah dibayar harus ditandai sebagai `Refund Required` [cite: 1].

### Ticket Category
* **BR12**: Harga tiket tidak boleh kurang dari nol [cite: 1].
* **BR13**: Kuota tiket harus lebih besar dari nol [cite: 1].
* **BR14**: Periode penjualan tiket harus berakhir sebelum atau pada tanggal mulai event [cite: 1].
* **BR15**: Total kuota semua kategori tiket tidak boleh melebihi kapasitas maksimum event [cite: 1].
* **BR16**: Kategori tiket dapat dinonaktifkan jika event belum selesai [cite: 1].
* **BR17**: Pelanggan tidak dapat membeli tiket dari kategori yang tidak aktif [cite: 1].

### Booking & Payment
* **BR18**: Pemesanan hanya dapat dibuat untuk event dengan status `Published` [cite: 1].
* **BR19**: Pemesanan hanya dapat dibuat untuk kategori tiket yang aktif [cite: 1].
* **BR20**: Pemesanan hanya dapat dibuat dalam periode penjualan tiket [cite: 1].
* **BR21**: Jumlah tiket dalam pemesanan harus lebih besar dari nol [cite: 1].
* **BR22**: Jumlah tiket tidak boleh melebihi sisa kuota tiket [cite: 1].
* **BR23**: Pelanggan tidak boleh memiliki lebih dari satu pemesanan aktif untuk event yang sama [cite: 1].
* **BR24**: Pemesanan yang baru dibuat harus berstatus `PendingPayment` [cite: 1].
* **BR25**: Pemesanan harus memiliki batas waktu pembayaran (payment deadline) [cite: 1].
* **BR26**: Harga total tidak boleh negatif [cite: 1].
* **BR27**: Pemesanan hanya dapat dibayar jika statusnya `PendingPayment` [cite: 1].
* **BR28**: Pemesanan tidak dapat dibayar jika batas waktu pembayaran telah lewat [cite: 1].
* **BR29**: Jumlah pembayaran harus sama dengan harga total pemesanan [cite: 1].
* **BR30**: Pemesanan dengan status `PendingPayment` berubah menjadi `Expired` setelah batas waktu pembayaran lewat [cite: 1].
* **BR31**: Pemesanan dengan status `Paid` tidak dapat ditandai sebagai kedaluwarsa [cite: 1].
* **BR32**: Saat pemesanan kedaluwarsa, kuota tiket yang sebelumnya dipesan harus dilepaskan kembali [cite: 1].

### Ticket & Check-in
* **BR33**: Check-in hanya dapat dilakukan untuk event yang sesuai dengan tiket [cite: 1].
* **BR34**: Tiket harus berstatus `Active` untuk dapat check-in [cite: 1].
* **BR35**: Tiket yang sudah check-in tidak dapat digunakan lagi [cite: 1].
* **BR36**: Check-in hanya dapat dilakukan pada hari H event atau dalam jendela waktu check-in yang diizinkan [cite: 1].
* **BR37**: Status tiket tidak boleh berubah jika check-in gagal [cite: 1].

### Refund Management
* **BR38**: Refund hanya dapat diajukan untuk pemesanan dengan status `Paid` [cite: 1].
* **BR39**: Refund tidak dapat diajukan jika ada tiket dari pemesanan tersebut yang sudah check-in [cite: 1].
* **BR40**: Refund hanya dapat diajukan sebelum batas waktu refund [cite: 1].
* **BR41**: Refund hanya dapat disetujui jika statusnya `Requested` [cite: 1].
* **BR42**: Saat refund disetujui, tiket terkait berubah menjadi `Cancelled` [cite: 1].
* **BR43**: Saat refund disetujui, pemesanan terkait berubah menjadi `Refunded` [cite: 1].
* **BR44**: Refund hanya dapat ditolak jika statusnya `Requested` [cite: 1].
* **BR45**: Alasan penolakan wajib diberikan saat menolak refund [cite: 1].
* **BR46**: Saat refund ditolak, pemesanan terkait tetap berstatus `Paid` [cite: 1].
* **BR47**: Refund hanya dapat ditandai sebagai `PaidOut` jika statusnya `Approved` [cite: 1].
* **BR48**: Referensi pembayaran wajib dicatat saat refund dibayarkan (PaidOut) [cite: 1].
* **BR49**: Refund yang sudah `PaidOut` tidak dapat disetujui, ditolak, atau dibatalkan lagi [cite: 1].

---

## 4. Initial Domain Model Draft

Model domain ini dirancang berdasarkan prinsip DDD Taktis untuk menjaga konsistensi aturan bisnis (Invariants) [cite: 1].

### Aggregate Root: Event
* **Entities**: `TicketCategory`
* **Value Objects**: `DateRange`, `Money`
* **Responsibility**: Menjaga integritas jadwal event dan kuota tiket global.

### Aggregate Root: Booking
* **Value Objects**: `Money`
* **Responsibility**: Mengelola siklus reservasi tiket dari pembuatan hingga pembayaran atau kedaluwarsa.

### Aggregate Root: Ticket
* **Value Objects**: `TicketCode`
* **Responsibility**: Digunakan oleh Gate Officer untuk validasi dan proses check-in.

### Aggregate Root: Refund
* **Responsibility**: Mengelola alur pengajuan, persetujuan, dan pembayaran pengembalian dana.

---

## 5. Ubiquitous Language Glossary

Istilah-istilah standar yang digunakan dalam proyek ini [cite: 1]:

| Term | Meaning |
| :--- | :--- |
| Event | Aktivitas yang diselenggarakan oleh Event Organizer. |
| Event Organizer | Pengguna yang membuat dan mengelola event. |
| Customer | Pengguna yang memesan dan membeli tiket. |
| Gate Officer | Pengguna yang memvalidasi tiket saat check-in. |
| Ticket Category | Tipe tiket (misal: Regular, VIP, Early Bird). |
| Quota | Jumlah maksimum tiket yang tersedia per kategori. |
| Booking | Reservasi sementara sebelum pembayaran selesai. |
| Pending Payment | Status pemesanan yang menunggu pembayaran. |
| Paid | Status pemesanan yang sudah lunas. |
| Expired | Status pemesanan yang melewati batas waktu bayar. |
| Ticket | Bukti kehadiran yang dibuat setelah pemesanan dibayar. |
| Ticket Code | Kode unik untuk identifikasi dan validasi tiket. |
| Check-in | Proses validasi tiket saat peserta masuk lokasi. |
| Refund | Proses pengembalian uang kepada pelanggan. |
| Money | Value object yang merepresentasikan jumlah dan mata uang. |
| Sales Period | Periode waktu kategori tiket dapat dibeli. |
| Payment Deadline | Batas waktu penyelesaian pembayaran pemesanan. |