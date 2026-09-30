import random
import tkinter as tk

# ---------------------------------------------------------
# OYUN DEĞİŞKENLERİ VE KELİME LİSTESİ
# ---------------------------------------------------------
KELIMELER = [
    "PYTHON",
    "YAZILIM",
    "KLAVYE",
    "BİLGİSAYAR",
    "KODLAMA",
    "İNTERNET",
    "EKRAN",
]

secilen_kelime = ""
tahmin_edilenler = []
yanlis_sayisi = 0
MAX_YANLIS = 6

# ---------------------------------------------------------
# OYUN MANTIĞI VE ÇİZİM FONKSİYONLARI
# ---------------------------------------------------------


def oyunu_baslat():
    global secilen_kelime, tahmin_edilenler, yanlis_sayisi
    secilen_kelime = random.choice(KELIMELER)
    tahmin_edilenler = []
    yanlis_sayisi = 0

    # Çizim alanını temizle ve darağacını çiz
    tuval.delete("all")
    daragaci_ciz()

    # Ekran yazılarını güncelle
    kelime_gorunumu_guncelle()
    durum_etiketi.config(
        text=f"Kalan Yanlış Hakkı: {MAX_YANLIS - yanlis_sayisi}", fg="black"
    )

    # Butonları tekrar aktif hale getir
    for btn in harf_butonlari.values():
        btn.config(state="normal", bg="#f0f0f0")


def daragaci_ciz():
    # Zemin ve direkler
    tuval.create_line(20, 180, 100, 180, width=3)  # Taban
    tuval.create_line(60, 180, 60, 20, width=3)  # Dikey direk
    tuval.create_line(60, 20, 130, 20, width=3)  # Üst direk
    tuval.create_line(130, 20, 130, 40, width=2)  # İp


def adam_ciz(asama):
    if asama == 1:
        # Kafa
        tuval.create_oval(115, 40, 145, 70, width=2)
    elif asama == 2:
        # Gövde
        tuval.create_line(130, 70, 130, 120, width=2)
    elif asama == 3:
        # Sol Kol
        tuval.create_line(130, 85, 110, 105, width=2)
    elif asama == 4:
        # Sağ Kol
        tuval.create_line(130, 85, 150, 105, width=2)
    elif asama == 5:
        # Sol Bacak
        tuval.create_line(130, 120, 110, 150, width=2)
    elif asama == 6:
        # Sağ Bacak
        tuval.create_line(130, 120, 150, 150, width=2)


def kelime_gorunumu_guncelle():
    gorunum = ""
    for harf in secilen_kelime:
        if harf in tahmin_edilenler:
            gorunum += harf + " "
        else:
            gorunum += "_ "
    kelime_etiketi.config(text=gorunum.strip())


def harf_tahmin_et(harf):
    global yanlis_sayisi

    # Tıklanan butonu pasif yap
    harf_butonlari[harf].config(state="disabled")

    if harf in secilen_kelime:
        tahmin_edilenler.append(harf)
        harf_butonlari[harf].config(bg="#a3e4d7")  # Doğruysa yeşilimsi yap
        kelime_gorunumu_guncelle()

        # Kazanma kontrolü
        kazandi = all(h in tahmin_edilenler for h in secilen_kelime)
        if kazandi:
            durum_etiketi.config(
                text="Tebrikler, Kazandınız! 🎉", fg="green"
            )
            butonlari_dondur()
    else:
        yanlis_sayisi += 1
        harf_butonlari[harf].config(bg="#f9e79f")  # Yanlışsa sarımsı yap
        adam_ciz(yanlis_sayisi)
        durum_etiketi.config(
            text=f"Kalan Yanlış Hakkı: {MAX_YANLIS - yanlis_sayisi}", fg="black"
        )

        # Kaybetme kontrolü
        if yanlis_sayisi == MAX_YANLIS:
            durum_etiketi.config(
                text=f"Kaybettiniz! Kelime: {secilen_kelime}", fg="red"
            )
            kelime_etiketi.config(text=" ".join(list(secilen_kelime)))
            butonlari_dondur()


def butonlari_dondur():
    for btn in harf_butonlari.values():
        btn.config(state="disabled")


# ---------------------------------------------------------
# ARAYÜZ (GUI) TASARIMI
# ---------------------------------------------------------
pencere = tk.Tk()
pencere.title("Adam Asmaca Oyunu")
pencere.geometry("450x520")
pencere.resizable(False, False)

# 1. Çizim Alanı (Canvas)
tuval = tk.Canvas(pencere, width=200, height=200, bg="white")
tuval.pack(pady=10)

# 2. Gizli Kelime Alanı
kelime_etiketi = tk.Label(pencere, text="", font=("Courier", 20, "bold"))
kelime_etiketi.pack(pady=10)

# 3. Durum Bilgisi
durum_etiketi = tk.Label(pencere, text="", font=("Arial", 11, "bold"))
durum_etiketi.pack(pady=5)

# 4. Sanal Klavye / Harf Butonları
klavye_cercevesi = tk.Frame(pencere)
klavye_cercevesi.pack(pady=10)

HARFLER = [
    "A",
    "B",
    "C",
    "Ç",
    "D",
    "E",
    "F",
    "G",
    "Ğ",
    "H",
    "I",
    "İ",
    "J",
    "K",
    "L",
    "M",
    "N",
    "O",
    "Ö",
    "P",
    "R",
    "S",
    "Ş",
    "T",
    "U",
    "Ü",
    "V",
    "Y",
    "Z",
]

harf_butonlari = {}
satir = 0
sutun = 0

for harf in HARFLER:
    # lambda h=harf yapısı her butonun kendi harfini fonksiyona göndermesini sağlar
    btn = tk.Button(
        klavye_cercevesi,
        text=harf,
        width=3,
        height=1,
        font=("Arial", 9, "bold"),
        command=lambda h=harf: harf_tahmin_et(h),
    )
    btn.grid(row=satir, column=sutun, padx=2, pady=2)
    harf_butonlari[harf] = btn

    sutun += 1
    if sutun > 7:  # Her satırda 8 buton olsun
        sutun = 0
        satir += 1

# 5. Yeniden Başlat Butonu
yeni_oyun_btn = tk.Button(
    pencere,
    text="Yeni Oyun",
    font=("Arial", 10, "bold"),
    bg="#85c1e9",
    command=oyunu_baslat,
)
yeni_oyun_btn.pack(pady=5)

# Oyunu ilk kez başlat
oyunu_baslat()

# Pencereyi çalıştır
pencere.mainloop()
