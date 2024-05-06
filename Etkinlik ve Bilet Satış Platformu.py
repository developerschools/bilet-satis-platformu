import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QListWidget, QComboBox, QDateTimeEdit, QCalendarWidget
from PyQt5.QtGui import QPixmap, QImage, QPalette, QBrush
from datetime import datetime

class Etkinlik:
    def __init__(self, ad, tarih, saat, mekan):
        self.ad = ad  # Etkinlik adı
        self.tarih = tarih  # Etkinlik tarihi
        self.saat = saat  # Etkinlik saati
        self.mekan = mekan  # Etkinlik mekanı
        self.biletler = []  # Etkinlik için satılan biletlerin listesi

    def bilet_sat(self, bilet):
        self.biletler.append(bilet)  # Etkinlik için bilet satışı ekleniyor

class Bilet:
    def __init__(self, numara, etkinlik):
        self.numara = numara  # Bilet numarası
        self.etkinlik = etkinlik  # Biletin satıldığı etkinlik

class Kullanıcı:
    def __init__(self, ad, soyad):
        self.ad = ad  # Kullanıcı adı
        self.soyad = soyad  # Kullanıcı soyadı
        self.biletler = []  # Kullanıcının satın aldığı biletlerin listesi

    def bilet_al(self, bilet):
        self.biletler.append(bilet)  # Kullanıcının bilet satın alması

class Arayuz(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Etkinlik ve Bilet Satış Platformu")
        self.etkinlikler = []  # Etkinliklerin listesi
        self.initUI()

        # SQLite bağlantısını oluştur
        self.conn = sqlite3.connect('veritabani.db')
        self.create_tables()

    def initUI(self):
        self.result_label = QLabel()  # Sonuçları göstermek için etiket
        self.result_label.setStyleSheet("color: green; font-weight: bold;")  # Sonuç etiketinin görünümü

        etkinlik_ekle_groupbox = self.create_etkinlik_ekle_groupbox()  # Etkinlik ekleme arayüzü
        bilet_sat_groupbox = self.create_bilet_sat_groupbox()  # Bilet satışı arayüzü
        bilet_al_groupbox = self.create_bilet_al_groupbox()  # Bilet alma arayüzü

        main_layout = QVBoxLayout()  # Ana düzen
        main_layout.addWidget(etkinlik_ekle_groupbox)  # Etkinlik ekleme arayüzünü ana düzene ekleme

        h_layout = QHBoxLayout()  # Yatay düzen
        h_layout.addWidget(bilet_sat_groupbox)  # Bilet satışı arayüzünü yatay düzene ekleme
        h_layout.addWidget(bilet_al_groupbox)  # Bilet alma arayüzünü yatay düzene ekleme

        main_layout.addLayout(h_layout)  # Yatay düzeni ana düzene ekleme
        main_layout.addWidget(self.result_label)  # Sonuç etiketini ana düzene ekleme

        self.setLayout(main_layout)  # Ana düzeni ayarlama

        # Arka plan resmi
        pixmap = self.load_image_from_url("https://www.stilfon.com/wp-content/uploads/2022/02/B171.jpg")  # Arka plan resmi URL'si
        if pixmap:
            palette = self.palette()
            palette.setBrush(QPalette.Window, QBrush(pixmap))
            self.setPalette(palette)

    def create_etkinlik_ekle_groupbox(self):
        groupbox = QWidget()  # Grup kutusu oluşturma
        layout = QVBoxLayout()  # Dikey düzen oluşturma
        groupbox.setLayout(layout)  # Grup kutusuna düzeni ayarlama

        ad_label = QLabel("Etkinlik Adı:")  # Etkinlik adı etiketi
        self.ad_entry = QLineEdit()  # Etkinlik adı giriş alanı
        layout.addWidget(ad_label)  # Etkinlik adı etiketini düzene ekleme
        layout.addWidget(self.ad_entry)  # Etkinlik adı giriş alanını düzene ekleme

        tarih_label = QLabel("Tarih:")  # Tarih etiketi
        self.tarih_edit = QCalendarWidget()  # Takvim düzenleyici
        layout.addWidget(tarih_label)  # Tarih etiketini düzene ekleme
        layout.addWidget(self.tarih_edit)  # Takvim düzenleyiciyi düzene ekleme

        saat_label = QLabel("Saat:")  # Saat etiketi
        self.saat_edit = QDateTimeEdit()  # Saat düzenleyici
        self.saat_edit.setDateTime(datetime.now())  # Varsayılan olarak şu anki saati ayarlama
        self.saat_edit.setDisplayFormat("HH:mm")  # Saat formatını ayarlama
        layout.addWidget(saat_label)  # Saat etiketini düzene ekleme
        layout.addWidget(self.saat_edit)  # Saat düzenleyiciyi düzene ekleme

        mekan_label = QLabel("Mekan:")  # Mekan etiketi
        self.mekan_entry = QLineEdit()  # Mekan giriş alanı
        layout.addWidget(mekan_label)  # Mekan etiketini düzene ekleme
        layout.addWidget(self.mekan_entry)  # Mekan giriş alanını düzene ekleme

        etkinlik_ekle_button = QPushButton("Etkinlik Ekle")  # Etkinlik ekleme düğmesi
        etkinlik_ekle_button.clicked.connect(self.etkinlik_ekle)  # Düğmeye tıklandığında çağrılacak işlevi bağlama
        layout.addWidget(etkinlik_ekle_button)  # Etkinlik ekleme düğmesini düzene ekleme

        return groupbox  # Grup kutusunu döndürme

    def create_bilet_sat_groupbox(self):
        groupbox = QWidget()  # Grup kutusu oluşturma
        layout = QVBoxLayout()  # Dikey düzen oluşturma
        groupbox.setLayout(layout)  # Grup kutusuna düzeni ayarlama

        etkinlik_label = QLabel("Etkinlik:")  # Etkinlik etiketi
        self.etkinlik_combobox = QComboBox()  # Etkinlik kombobox'ı
        layout.addWidget(etkinlik_label)  # Etkinlik etiketini düzene ekleme
        layout.addWidget(self.etkinlik_combobox)  # Etkinlik kombobox'ını düzene ekleme

        bilet_numara_label = QLabel("Bilet Numarası:")  # Bilet numarası etiketi
        self.bilet_numara_entry = QLineEdit()  # Bilet numarası giriş alanı
        layout.addWidget(bilet_numara_label)  # Bilet numarası etiketini düzene ekleme
        layout.addWidget(self.bilet_numara_entry)  # Bilet numarası giriş alanını düzene ekleme

        bilet_sat_button = QPushButton("Bilet Sat")  # Bilet satışı düğmesi
        bilet_sat_button.clicked.connect(self.bilet_sat)  # Düğmeye tıklandığında çağrılacak işlevi bağlama
        layout.addWidget(bilet_sat_button)  # Bilet satışı düğmesini düzene ekleme

        return groupbox  # Grup kutusunu döndürme

    def create_bilet_al_groupbox(self):
        groupbox = QWidget()  # Grup kutusu oluşturma
        layout = QVBoxLayout()  # Dikey düzen oluşturma
        groupbox.setLayout(layout)  # Grup kutusuna düzeni ayarlama

        kullanici_label = QLabel("Kullanıcı Adı:")  # Kullanıcı adı etiketi
        self.kullanici_entry = QLineEdit()  # Kullanıcı adı giriş alanı
        layout.addWidget(kullanici_label)  # Kullanıcı adı etiketini düzene ekleme
        layout.addWidget(self.kullanici_entry)  # Kullanıcı adı giriş alanını düzene ekleme

        soyad_label = QLabel("Kullanıcı Soyadı:")  # Kullanıcı soyadı etiketi
        self.soyad_entry = QLineEdit()  # Kullanıcı soyadı giriş alanı
        layout.addWidget(soyad_label)  # Kullanıcı soyadı etiketini düzene ekleme
        layout.addWidget(self.soyad_entry)  # Kullanıcı soyadı giriş alanını düzene ekleme

        bilet_al_button = QPushButton("Bilet Al")  # Bilet alma düğmesi
        bilet_al_button.clicked.connect(self.bilet_al)  # Düğmeye tıklandığında çağrılacak işlevi bağlama
        layout.addWidget(bilet_al_button)  # Bilet alma düğmesini düzene ekleme

        return groupbox  # Grup kutusunu döndürme

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS etkinlikler
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                           ad TEXT,
                           tarih DATE,
                           saat TEXT,
                           mekan TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS biletler
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                           numara TEXT,
                           etkinlik_id INTEGER,
                           FOREIGN KEY (etkinlik_id) REFERENCES etkinlikler(id))''')
        self.conn.commit()

    def etkinlik_ekle(self):
        ad = self.ad_entry.text()  # Etkinlik adını alın
        tarih = self.tarih_edit.selectedDate().toPyDate()  # Tarih bilgisini alın
        saat = self.saat_edit.time().toPyTime().strftime("%H:%M")  # Saat bilgisini string olarak alın ve biçimlendirin
        mekan = self.mekan_entry.text()  # Mekan bilgisini alın

        if ad.strip() == "" or mekan.strip() == "":  # Etkinlik adı veya mekan bilgisi boşsa
            self.result_label.setText("Lütfen etkinlik adı ve mekan bilgilerini girin.")  # Kullanıcıya bir mesaj göster
            return

        etkinlik = Etkinlik(ad, tarih, saat, mekan)  # Yeni bir etkinlik oluşturun
        self.etkinlikler.append(etkinlik)  # Etkinlik listesine etkinliği ekleyin
        self.populate_etkinlik_combobox()  # Etkinliklerin bulunduğu comboBox'ı güncelleyin

        # Etkinliği veritabanına ekleyin
        cursor = self.conn.cursor()
        cursor.execute('''INSERT INTO etkinlikler (ad, tarih, saat, mekan)
                          VALUES (?, ?, ?, ?)''', (ad, tarih, saat, mekan))
        self.conn.commit()

        self.result_label.setText("Etkinlik başarıyla eklendi.")  # Kullanıcıya bir başarı mesajı göster

    def bilet_sat(self):
        etkinlik_index = self.etkinlik_combobox.currentIndex()  # Seçilen etkinliğin indeksini alın
        bilet_numara = self.bilet_numara_entry.text()  # Bilet numarasını alın

        if etkinlik_index == -1:  # Eğer etkinlik seçilmediyse
            self.result_label.setText("Lütfen bir etkinlik seçin.")  # Kullanıcıya bir mesaj göster
            return

        etkinlik = self.etkinlikler[etkinlik_index]  # Seçilen etkinliği alın
        bilet = Bilet(bilet_numara, etkinlik)  # Yeni bir bilet oluşturun
        etkinlik.bilet_sat(bilet)  # Etkinlik sınıfında tanımlı bilet_sat fonksiyonunu çağırarak bilet satışını gerçekleştirin

        # Bileti veritabanına ekleyin
        cursor = self.conn.cursor()
        cursor.execute('''INSERT INTO biletler (numara, etkinlik_id)
                          VALUES (?, ?)''', (bilet_numara, etkinlik_index + 1))
        self.conn.commit()

        self.result_label.setText("Bilet başarıyla satıldı.")  # Kullanıcıya bir başarı mesajı göster

    def bilet_al(self):
        kullanici_ad = self.kullanici_entry.text()  # Kullanıcı adını alın
        kullanici_soyad = self.soyad_entry.text()  # Kullanıcı soyadını alın

        if kullanici_ad.strip() == "" or kullanici_soyad.strip() == "":  # Eğer kullanıcı adı veya soyadı boşsa
            self.result_label.setText("Lütfen kullanıcı adı ve soyadı girin.")  # Kullanıcıya bir mesaj göster
            return

        kullanici = Kullanıcı(kullanici_ad, kullanici_soyad)  # Yeni bir kullanıcı oluşturun
        self.result_label.setText(f"{kullanici_ad} {kullanici_soyad} kullanıcısı başarıyla oluşturuldu.")  # Kullanıcıya bir başarı mesajı göster

    def populate_etkinlik_combobox(self):
        self.etkinlik_combobox.clear()  # ComboBox'ı temizleyin
        for etkinlik in self.etkinlikler:  # Tüm etkinlikler için
            self.etkinlik_combobox.addItem(etkinlik.ad)  # ComboBox'a etkinlik adını ekleyin

    def load_image_from_url(self, url):
        try:
            import requests
            response = requests.get(url)
            image = QImage()
            image.loadFromData(response.content)
            pixmap = QPixmap(image)
            return pixmap
        except Exception as e:
            print(f"Error loading image from URL: {e}")
            return None

if __name__ == '__main__':
    app = QApplication(sys.argv)  # Uygulama oluştur
    ex = Arayuz()  # Arayüzü oluştur
    ex.show()  # Arayüzü göster
    sys.exit(app.exec_())  # Uygulamayı çalıştır ve çıkış kodunu al
