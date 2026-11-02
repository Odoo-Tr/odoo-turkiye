# KKTC - Muhasebe

Odoo'da Kuzey Kıbrıs Türk Cumhuriyeti hiç yoktu; KKTC'deki şirketler başka bir ülke seçip KDV oranlarını kendileri tanımlamak zorundaydı. Bu modül ülkeyi, altı ilçeyi, hesap planını ve KKTC KDV oranlarını ekler.

## Özellikler

- **Ülke:** Kuzey Kıbrıs Türk Cumhuriyeti; bayrağı, Türk lirası ve +90 telefon koduyla.
- **İlçeler:** Lefkoşa, Gazimağusa, Girne, Güzelyurt, İskele, Lefke.
- **KKTC Tek Düzen Hesap Planı:** Gelir ve Vergi Dairesi'nin yayımladığı [KKTC Tek Düzen Hesap Planı](https://www.vergi.gov.ct.tr/sites/default/files/KKTC%20TEKD%C3%9CZEN%20HESAP%20PLANI.doc) Türkiye'dekiyle aynı hesap kodlarını kullanır (100 Kasa, 120 Alıcılar, 191 İndirilecek KDV, 320 Satıcılar, 360 Ödenecek Vergi ve Fonlar, 391 Hesaplanan KDV, 600 Yurtiçi Satışlar...). Hesaplar Odoo'nun Türkiye hesap planından gelir.
- **KDV:** Satış ve alış için %0, %5, %10, **%16 (genel oran)** ve %20. Satış KDV'si 391'e, alış KDV'si 191'e yazılır. Türkiye'nin KDV vergileri (%1, %10, %20 ve tevkifatlar) yüklenmez, yanlışlıkla seçilemez.

| Oran | Kapsam ([2025 Yılı KDV Oranları Tüzüğü](https://vergi.gov.ct.tr/sites/default/files/2025%20Katma%20De%C4%9Fer%20Vergisi%20Oranlar%C4%B1%20T%C3%BCz%C3%BC%C4%9F%C3%BC.pdf)) |
|---|---|
| %0 | Cetvel I |
| %5 | Cetvel II |
| %10 | Cetvel III |
| %16 | Cetvel IV: diğer cetvellerde olmayan tüm mal ve hizmetler |
| %20 | Cetvel V |

## Kurulum

1. Modülü kurun.
2. Şirketin ülkesini **Kuzey Kıbrıs Türk Cumhuriyeti** yapın.
3. **Ayarlar → Faturalama** (ya da Muhasebe) altında **Mali Yerelleştirme** olarak **KKTC Tek Düzen Hesap Planı**'nı seçip kaydedin.

Hesap planı yalnız şirkette muhasebe kaydı yokken değiştirilebilir.

## Bilmeniz gerekenler

- **Ülke kodu:** KKTC'nin uluslararası (ISO 3166) ülke kodu yoktur. Modül, devlet sitelerinin `.ct.tr` uzantısına uyarak `CT` kodunu kullanır. Yalnız ISO kodlarını kabul eden dış servisler (bazı ödeme sağlayıcıları gibi) ülkeyi tanımayabilir.
- **Oranlar:** 2025 tüzüğüne göredir; değişirse vergiler Odoo'da düzenlenebilir.
- **Henüz olmayanlar:** KKTC e-Fatura entegrasyonu ve KKTC'ye özgü beyanname raporları bu modülde yoktur.

## Uyumluluk

| Odoo | Dal |
|---|---|
| 17.0 | [`17.0`](https://github.com/Odoo-Tr/odoo-turkiye/tree/17.0) |
| 18.0 | [`18.0`](https://github.com/Odoo-Tr/odoo-turkiye/tree/18.0) |
| 19.0 | [`19.0`](https://github.com/Odoo-Tr/odoo-turkiye/tree/19.0) |
| 20.0 | [`20.0`](https://github.com/Odoo-Tr/odoo-turkiye/tree/20.0) |

Bayrak görseli: [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Flag_of_the_Turkish_Republic_of_Northern_Cyprus.svg) (kamu malı).

Sorular ve öneriler için: [odoo-tr.com](https://odoo-tr.com)
