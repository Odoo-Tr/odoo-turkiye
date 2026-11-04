# Odoo Türkiye Modülleri

Türkiye'deki şirketlerin ihtiyaçları için açık kaynak Odoo modülleri. [Odoo Türkiye](https://odoo-tr.com) topluluğu tarafından geliştirilir. Hepsi **Community** sürümünde çalışır.

| Modül | Ne yapar |
|---|---|
| [`l10n_tr_tcmb_rates`](l10n_tr_tcmb_rates) | Döviz kurlarını her gün TCMB gösterge kurları bülteninden otomatik günceller |
| [`l10n_tr_amount_in_words`](l10n_tr_amount_in_words) | Fatura çıktısına "Yalnız: ... Türk Lirası ... Kuruş" satırını ekler |
| [`l10n_tr_address`](l10n_tr_address) | 81 ilin 973 ilçesi; il seçilince yalnız o ilin ilçeleri listelenir, adresler "İlçe/İl" biçiminde yazılır |
| [`l10n_tr_kur_degerleme`](l10n_tr_kur_degerleme) | Dönem sonunda dövizli alacak, borç ve banka hesaplarının kur değerlemesi (VUK 280) |
| [`l10n_tr_resmi_tatil`](l10n_tr_resmi_tatil) | Ulusal bayramlar, genel tatiller ve 2025–2030 dini bayramları; arife ve 28 Ekim yarım günleri |
| [`l10n_tr_yillik_izin`](l10n_tr_yillik_izin) | İş Kanunu md. 53'e göre kıdemden yıllık izin hakkı; her hizmet yılında otomatik tahsis |
| [`l10n_tr_banka`](l10n_tr_banka) | 67 banka, EFT ve BIC kodlarıyla; Türk IBAN'ı girilince banka kendiliğinden seçilir |
| [`l10n_tr_vergi_dairesi`](l10n_tr_vergi_dairesi) | 1.046 vergi dairesi; kişi ve şirkette listeden seçilen Vergi Dairesi alanı |
| [`l10n_tr_account_group`](l10n_tr_account_group) | Tek Düzen Hesap Planı'nın hesap grupları (Odoo 15'in Türkiye planında yok) |
| [`l10n_tr_mali_tablolar`](l10n_tr_mali_tablolar) | Tek Düzen Hesap Planı sıralamasıyla mizan, ayrıntılı bilanço ve ayrıntılı gelir tablosu; PDF ve Excel |

Sırada neler var: [yol haritası](ROADMAP.md) · [odoo-tr.com/p/3-yol-haritasi](https://odoo-tr.com/p/3-yol-haritasi)

## Sürümler

Her Odoo sürümü ayrı bir daldadır:

| Odoo | Dal |
|---|---|
| 15.0 | [`15.0`](https://github.com/Odoo-Tr/odoo-turkiye/tree/15.0) |
| 16.0 | [`16.0`](https://github.com/Odoo-Tr/odoo-turkiye/tree/16.0) |
| 17.0 | [`17.0`](https://github.com/Odoo-Tr/odoo-turkiye/tree/17.0) |
| 18.0 | [`18.0`](https://github.com/Odoo-Tr/odoo-turkiye/tree/18.0) |
| 19.0 | [`19.0`](https://github.com/Odoo-Tr/odoo-turkiye/tree/19.0) |
| 20.0 | [`20.0`](https://github.com/Odoo-Tr/odoo-turkiye/tree/20.0) |

### Hangi modül hangi sürümde

| Modül | 15 | 16 | 17 | 18 | 19 | 20 |
|---|---|---|---|---|---|---|
| `l10n_tr_tcmb_rates` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| `l10n_tr_amount_in_words` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| `l10n_tr_address` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| `l10n_tr_stopaj` | – | – | ✓ | ✓ | ✓ | ✓ |
| `l10n_kktc` | – | – | ✓ | ✓ | ✓ | ✓ |
| `l10n_tr_kur_farki` | – | ✓ | ✓ | ✓ | ✓ | ✓ |
| `l10n_tr_kur_degerleme` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| `l10n_tr_resmi_tatil` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| `l10n_tr_yillik_izin` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| `l10n_tr_banka` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| `l10n_tr_vergi_dairesi` | ✓ | ✓ | ✓ | ✓ | ✓ | – |
| `l10n_tr_account_group` | ✓ | – | – | – | – | – |
| `l10n_tr_mali_tablolar` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

## Kurulum

```bash
git clone -b 15.0 https://github.com/Odoo-Tr/odoo-turkiye.git
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
