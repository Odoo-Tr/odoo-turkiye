# Türkiye - Gelir Vergisi Stopajı

Serbest meslek erbabına (avukat, mali müşavir, danışman, doktor) ya da şahıs mülk sahibine ödeme yapan şirket, ödemeden %20 gelir vergisi keser ve vergi dairesine yatırır. Bu modül o stopajı Odoo'ya doğru hesaplarla ekler ve muhtasar beyanname için aylık listesini verir.

> Avukatlık ücreti 10.000,00 + KDV 2.000,00 − stopaj 2.000,00 = **10.000,00 ödenecek**, 2.000,00 vergi dairesine.

## Neden gerekli?

Odoo'nun Türkiye modülünde (`l10n_tr`):

- serbest meslek stopajı **yoktur**,
- kira stopajı (`PR WH 20%`) vardır ama tutarı **191 İndirilecek KDV** hesabına yazar; stopaj ödenecek bir vergidir, KDV indirimi değildir.

## Özellikler

| Vergi | Kullanım | Hesap |
|---|---|---|
| Stopaj Serbest Meslek %20 | Alış: serbest meslek ücreti (GVK 94/2-b) | 360001 Ödenecek Gelir Vergisi Stopajı |
| Stopaj Kira %20 | Alış: şahıstan kira (GVK 94/5-a) | 360001 Ödenecek Gelir Vergisi Stopajı |
| Stopaj Serbest Meslek %20 | Satış: müşterinin kestiği stopaj | 193001 Peşin Ödenen Gelir Vergisi Stopajı |

- **Net fiyat seçenekleri:** Her verginin "(net fiyat)" hâli de var. Net kira ya da net ücret girilir, brüt tutarı Odoo hesaplar: 8.000 net → 10.000 brüt, 2.000 stopaj.
- **Stopaj listesi:** **Faturalama → Raporlama → Gelir Vergisi Stopajı**. Tarih, belge, iş ortağı, VKN/TCKN, stopaj türü, brüt tutar ve stopaj; aylara göre gruplanır, pivot görünümü de var. İade faturaları eksi tutarla düşer.
- **Mevcut şirketler:** Türkiye hesap planını kullanan şirketlere kurulumda hesaplar ve vergiler otomatik eklenir.

## Bilmeniz gerekenler

- **Oranlar:** Serbest meslek ve kira stopajı %20 olarak tanımlıdır. Oranlar Cumhurbaşkanı kararıyla değişebilir; vergiler sıradan Odoo vergileridir, gerekirse düzenlenebilir. Telif ödemeleri (GVK 94/2-a) farklı orana tabi olduğu için bu modülde yoktur.
- **Serbest meslek makbuzu basılmaz:** Vergiden muaf olmayan serbest meslek erbabı 2020'den bu yana e-SMM düzenlemek zorundadır (VUK Genel Tebliği Sıra No. 509). Makbuz GİB üzerinden ya da bir entegratörle düzenlenir; Odoo'daki kayıt muhasebe içindir.
- **Muhtasar kodları:** Liste beyanname için gereken tutarları verir; beyannamedeki ödeme türü kodlarını mali müşavirinizle kontrol edin.
- **Kaldırma:** Modül kaldırılınca hesap ve vergiler şirkette kalır (Odoo'nun hesap planı kayıtları gibi); yalnız stopaj listesi kaybolur.

## Uyumluluk

| Odoo | Dal |
|---|---|
| 18.0 | [`18.0`](https://github.com/Odoo-Tr/odoo-turkiye/tree/18.0) |
| 19.0 | [`19.0`](https://github.com/Odoo-Tr/odoo-turkiye/tree/19.0) |
| 20.0 | [`20.0`](https://github.com/Odoo-Tr/odoo-turkiye/tree/20.0) |

Sorular ve öneriler için: [odoo-tr.com](https://odoo-tr.com)
