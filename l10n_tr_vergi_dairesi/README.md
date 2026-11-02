# Türkiye - Vergi Daireleri

Türkiye'deki 1.046 vergi dairesi ve malmüdürlüğünü iline göre Odoo'ya ekler. Kişi ve şirket formuna, serbest metin yerine listeden seçilen bir **Vergi Dairesi** alanı gelir.

> İli İstanbul olan bir müşteride liste İstanbul'un vergi daireleriyle sınırlanır: Kadıköy Vergi Dairesi Müdürlüğü, Beyoğlu Vergi Dairesi Müdürlüğü…

## Nasıl çalışır?

1. Ülkesi Türkiye olan bir kişinin formunda, vergi numarasının altındaki **Vergi Dairesi** alanından seçim yapın.
2. Kişinin ili girilmişse liste o ille sınırlanır.
3. Şirketinizin vergi dairesini **Ayarlar → Şirketler**'de aynı alana girin.

- Odoo kişiyi adresiyle birlikte gösterdiğinde vergi dairesi adın altına eklenir.
- Liste **Kişiler → Yapılandırma → Yerelleştirme → Vergi Daireleri**'nden görüntülenip düzenlenebilir.
- Ülkesi Türkiye olmayan kişilerde alan gizlenir.

## Nilvera e-Fatura ve Odoo 20

Odoo 18 ve 19'da Nilvera e-Fatura'nın genişletilmiş modülü (`l10n_tr_nilvera_einvoice_extended`) kuruluysa vergi daireleri onunla zaten gelir; bu modül onunla birlikte kurulamaz. Odoo 20'de vergi daireleri Odoo'nun kendi Türkiye yerelleştirmesinde (`l10n_tr`) hazır geldiği için bu modül 15.0–19.0 içindir. Model ve alan adları Odoo 20'dekilerle aynıdır (`l10n_tr.tax.office`, `l10n_tr_tax_office_id`).

## Kaynak ve lisans

Vergi dairesi listesi (`l10n_tr.tax.office.csv`) ile modelin ve kişi adında gösterimin yapısı, Odoo S.A.'nın Odoo 20 Türkiye yerelleştirmesinden (`l10n_tr`, LGPL-3) alınıp eski sürümlere uyarlanmıştır. Liste zamanla değişebilir; güncel durum için Gelir İdaresi Başkanlığı'nı esas alın.

## Uyumluluk

| Odoo | Dal |
|---|---|
| 15.0 | [`15.0`](https://github.com/Odoo-Tr/odoo-turkiye/tree/15.0) |
| 16.0 | [`16.0`](https://github.com/Odoo-Tr/odoo-turkiye/tree/16.0) |
| 17.0 | [`17.0`](https://github.com/Odoo-Tr/odoo-turkiye/tree/17.0) |
| 18.0 | [`18.0`](https://github.com/Odoo-Tr/odoo-turkiye/tree/18.0) |
| 19.0 | [`19.0`](https://github.com/Odoo-Tr/odoo-turkiye/tree/19.0) |

Sorular ve öneriler için: [odoo-tr.com](https://odoo-tr.com)
