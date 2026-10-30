# Türkiye - TCMB Döviz Kurları

Odoo'daki döviz kurlarını her gün **TCMB gösterge kurları** bülteninden (`today.xml`) otomatik günceller. **Community** sürümünde çalışır.

## Özellikler

- **Kur türü seçimi:** Döviz alış, döviz satış, efektif alış ya da efektif satış. Seçilen tür bir para birimi için yayınlanmamışsa döviz alış kullanılır.
- **Ertesi gün kuralı (varsayılan açık):** TCMB kurları her iş günü 15.30'da açıklanır ve uygulamada bir sonraki gün için kullanılır. Bu ayar açıkken D gününün bülteni D+1 tarihli kur olarak kaydedilir. Hafta sonu ve tatillerde son açıklanan kur geçerli kalır.
- **Birim farkları:** JPY gibi 100 birim üzerinden yayınlanan kurlar 1 birime çevrilir.
- **TL dışı şirket para birimi:** Şirketin para birimi TL değilse (ör. USD), kurlar TCMB üzerinden çapraz hesaplanır.
- **Çoklu şirket:** Her şirket için ayrı ayar ve ayrı kur kaydı.
- **Otomatik ve elle güncelleme:** Zamanlanmış görev 3 saatte bir çalışır. Ayarlardaki **Kurları şimdi güncelle** düğmesiyle elle de güncellenebilir.

## Kullanım

1. Modülü kurun.
2. **Faturalama / Muhasebe → Yapılandırma → Ayarlar → Currencies** bölümünde **TCMB döviz kurları**'nı açın.
3. Kur türünü seçin ve **Kurları şimdi güncelle**'ye basın.

Yalnız **etkin** para birimlerinin kuru güncellenir.

## Uyumluluk

| Odoo | Dal |
|---|---|
| 19.0 | [`19.0`](https://github.com/Odoo-Tr/odoo-turkiye/tree/19.0) |
| 20.0 | [`20.0`](https://github.com/Odoo-Tr/odoo-turkiye/tree/20.0) |

## Not

Kurlar TCMB'nin herkese açık bülteninden alınır. Hangi kurun kullanılacağı (alış/satış, işlem günü/önceki gün) işleminizin türüne göre değişebilir; mevzuat açısından mali müşavirinize danışın.

Sorular ve öneriler için: [odoo-tr.com](https://odoo-tr.com)
