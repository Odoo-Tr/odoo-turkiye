# Odoo Türkiye Modülleri

Türkiye'deki şirketlerin ihtiyaçları için açık kaynak Odoo modülleri. [Odoo Türkiye](https://odoo-tr.com) topluluğu tarafından geliştirilir. Hepsi **Community** sürümünde çalışır.

| Modül | Ne yapar |
|---|---|
| [`l10n_tr_tcmb_rates`](l10n_tr_tcmb_rates) | Döviz kurlarını her gün TCMB gösterge kurları bülteninden otomatik günceller |
| [`l10n_tr_amount_in_words`](l10n_tr_amount_in_words) | Fatura çıktısına "Yalnız: ... Türk Lirası ... Kuruş" satırını ekler |
| [`l10n_tr_address`](l10n_tr_address) | 81 ilin 973 ilçesi; il seçilince yalnız o ilin ilçeleri listelenir, adresler "İlçe/İl" biçiminde yazılır |

Sırada neler var: [yol haritası](ROADMAP.md) · [odoo-tr.com/p/3-yol-haritasi](https://odoo-tr.com/p/3-yol-haritasi)

## Sürümler

Her Odoo sürümü ayrı bir daldadır:

| Odoo | Dal |
|---|---|
| 19.0 | [`19.0`](https://github.com/Odoo-Tr/odoo-turkiye/tree/19.0) |
| 20.0 | [`20.0`](https://github.com/Odoo-Tr/odoo-turkiye/tree/20.0) |

## Kurulum

```bash
git clone -b 19.0 https://github.com/Odoo-Tr/odoo-turkiye.git
```

1. Klasörü Odoo'nun `addons_path` ayarına ekleyin.
2. Odoo'yu yeniden başlatın.
3. **Uygulamalar** menüsünde **Uygulama Listesini Güncelle**'ye basın.
4. Modülü arayıp kurun.

Docker kullanıyorsanız klasörü `/mnt/extra-addons` yoluna bağlayın.

## Destek

- **Hata ve öneri:** [Issue açın](https://github.com/Odoo-Tr/odoo-turkiye/issues).
- **Sorular:** [odoo-tr.com](https://odoo-tr.com) forumu.

## Lisans

[LGPL-3.0](LICENSE)
