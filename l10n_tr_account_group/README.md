# Türkiye - Hesap Grupları (Odoo 15)

Odoo 15'in Türkiye hesap planında (`l10n_tr`) hesap grupları yoktur; hesap planı düz bir liste olarak görünür. Bu modül Tek Düzen Hesap Planı'nın 8 ana grubunu ve 56 alt grubunu ekler; hesaplar koduna göre gruplarına kendiliğinden yerleşir.

> 100 Kasa → **10 HAZIR DEĞERLER** → **1 DÖNEN VARLIKLAR**

## Nasıl çalışır?

1. Modülü kurun. Türkiye hesap planını kullanan şirketlere gruplar hemen eklenir; şirkette zaten aynı kodlu bir grup varsa atlanır.
2. Türkiye hesap planı sonradan yüklenen şirketler grupları planla birlikte alır.
3. Hesapların grup bilgisi kodlarına göre kendiliğinden dolar; hesap planı listesi gruplara göre gruplanabilir.

Odoo 16 ve sonrasında bu gruplar Odoo'nun kendi Türkiye planında bulunduğu için modül yalnız 15.0 içindir.

## Kaynak ve lisans

Grup listesi Odoo S.A.'nın Odoo 17 Türkiye yerelleştirmesindeki `account.group-tr.csv` dosyasından alınmıştır (LGPL-3). Orada adı boş olan iki grup (54 Kâr Yedekleri, 9 Nazım Hesaplar) adlandırıldı ve 76. gruptaki yazım hatası düzeltildi.

## Uyumluluk

| Odoo | Dal |
|---|---|
| 15.0 | [`15.0`](https://github.com/Odoo-Tr/odoo-turkiye/tree/15.0) |

Sorular ve öneriler için: [odoo-tr.com](https://odoo-tr.com)
