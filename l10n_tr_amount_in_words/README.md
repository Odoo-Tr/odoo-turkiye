# Türkiye - Faturada Yazıyla Tutar

Fatura çıktısında toplam tutarın altına Türk faturalarında alışılmış **"Yalnız: ..."** satırını ekler:

> **Yalnız:** Bin İki Yüz Otuz Dört Türk Lirası Elli Altı Kuruş

## Özellikler

- **Doğru Türkçe yazım:** "bir bin" yerine "bin", "bir yüz" yerine "yüz" yazılır. Büyük harfe çevirmede Türkçe kurallar uygulanır, ör. "İki".
- **Para birimine göre birim adı:**

  | Para birimi | Birim | Alt birim |
  |---|---|---|
  | TRY | Türk Lirası | Kuruş |
  | USD | ABD Doları | Sent |
  | EUR | Avro | Sent |
  | GBP | İngiliz Sterlini | Peni |
  | CHF | İsviçre Frangı | Rappen |

  Diğer para birimlerinde Odoo'daki para birimi tanımları kullanılır.
- **Ayarlardan kapatılabilir:** **Ayarlar → Currencies → Faturada yazıyla tutar**.

## Uyumluluk

| Odoo | Dal |
|---|---|
| 18.0 | [`18.0`](https://github.com/Odoo-Tr/odoo-turkiye/tree/18.0) |
| 19.0 | [`19.0`](https://github.com/Odoo-Tr/odoo-turkiye/tree/19.0) |
| 20.0 | [`20.0`](https://github.com/Odoo-Tr/odoo-turkiye/tree/20.0) |

Sorular ve öneriler için: [odoo-tr.com](https://odoo-tr.com)
