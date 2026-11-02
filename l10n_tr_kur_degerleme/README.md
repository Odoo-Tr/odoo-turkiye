# Türkiye - Kur Değerlemesi

Dönem sonunda açık dövizli alacak, borç ve döviz banka hesaplarını değerleme günündeki kurla yeniden değerler, farkı 646 Kambiyo Karları / 656 Kambiyo Zararları hesabına yazar. Geçici vergi dönemlerinde ve yıl sonunda VUK 280. madde gereği yapılan değerleme içindir.

> 10.000 USD'lik açık alacak 41,20'den kayıtlı, değerleme günü kuru 42,10: **9.000,00 TL kambiyo karı** (120 borç, 646 alacak).

## Nasıl çalışır?

1. **Muhasebe → Muhasebe → Kur Değerlemesi**'ni açın.
2. Değerleme tarihini (varsayılan: geçen ayın son günü) ve yevmiye defterini seçin.
3. Neyin değerleneceğini işaretleyin: **Alacaklar ve borçlar**, **Banka ve kasa hesapları**.
4. **Değerle**'ye basın. Onaylanmış bir yevmiye kaydı oluşur.

- **Alacak ve borçlar:** Değerleme tarihinde açık olan dövizli kalemler, cari hesap, iş ortağı ve para birimi bazında toplanır. Tarihten sonra yapılan tahsilat ve ödemeler hesaba katılmaz; kalem o gün açık olduğu tutarla değerlenir.
- **Banka ve kasa:** Para birimi şirket para biriminden farklı olan banka ve kasa defterlerinin hesapları, tarihteki döviz bakiyesiyle değerlenir.
- **Kur:** Odoo'da o tarih için geçerli olan şirket kuru kullanılır. [TCMB Döviz Kurları](../l10n_tr_tcmb_rates) modülüyle kurları TCMB'den çekebilirsiniz.
- **KDV:** Değerleme farkı faturalanmaz ve KDV hesaplanmaz. Tahsilat ya da ödemede gerçekleşen kur farkı içinse [Kur Farkı Faturası](../l10n_tr_kur_farki) modülüne bakın.
- **Ters kayıt (isteğe bağlı):** **Ertesi gün ters kaydet** işaretlenirse ertesi gün aynı tutarda ters kayıt atılır; açık kalemler fatura kurlarına döner, tahsilattaki kur farkı Odoo'nun kendi kaydıyla oluşur. Ters kayıt kanuni bir zorunluluk değil, yaygın bir uygulamadır.

## Bilmeniz gerekenler

- VUK 280'e göre döviz alacak ve borçlar ile döviz mevduatı TCMB döviz alış kuruyla, kasadaki efektif ise efektif alış kuruyla değerlenir. Modül her kalem için şirketin Odoo'daki kurunu kullanır; kasadaki efektif için farklı kur gerekiyorsa o kaydı elle düzeltin.
- Hangi günün bülteninin kullanılacağını ve dönem sonu kayıtlarınızı mali müşavirinizle teyit edin.
- Yalnız türü alacak ya da borç olan hesaplardaki dövizli kalemler ve döviz banka/kasa defterleri değerlenir. Başka türdeki dövizli hesaplar (örneğin dövize endeksli sözleşmeler) dahil edilmez.

## Kaynak

213 sayılı Vergi Usul Kanunu, madde 280 ve Vergi Usul Kanunu Genel Tebliği (Sıra No: 590).

## Uyumluluk

| Odoo | Dal |
|---|---|
| 15.0 | [`15.0`](https://github.com/Odoo-Tr/odoo-turkiye/tree/15.0) |
| 16.0 | [`16.0`](https://github.com/Odoo-Tr/odoo-turkiye/tree/16.0) |
| 17.0 | [`17.0`](https://github.com/Odoo-Tr/odoo-turkiye/tree/17.0) |
| 18.0 | [`18.0`](https://github.com/Odoo-Tr/odoo-turkiye/tree/18.0) |
| 19.0 | [`19.0`](https://github.com/Odoo-Tr/odoo-turkiye/tree/19.0) |
| 20.0 | [`20.0`](https://github.com/Odoo-Tr/odoo-turkiye/tree/20.0) |

Sorular ve öneriler için: [odoo-tr.com](https://odoo-tr.com)
