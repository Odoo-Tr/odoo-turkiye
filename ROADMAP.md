# Yol haritası

*Son güncelleme: 30 Ekim 2026*

Odoo Türkiye'nin açık kaynak Türkiye modüllerinde neyin yayında olduğu, sırada ne olduğu ve neyi neden yapmadığımız.

## Yayında

Odoo 19 ve 20'de çalışır, Community sürümünde kurulabilir.

- **[TCMB Döviz Kurları](https://github.com/Odoo-Tr/odoo-turkiye/tree/19.0/l10n_tr_tcmb_rates)** (`l10n_tr_tcmb_rates`): Döviz kurlarını her gün TCMB gösterge kurları bülteninden otomatik günceller.
- **[Faturada Yazıyla Tutar](https://github.com/Odoo-Tr/odoo-turkiye/tree/19.0/l10n_tr_amount_in_words)** (`l10n_tr_amount_in_words`): Fatura çıktısına "Yalnız: ... Türk Lirası ... Kuruş" satırını ekler.
- **[İl ve İlçe Adresleri](https://github.com/Odoo-Tr/odoo-turkiye/tree/19.0/l10n_tr_address)** (`l10n_tr_address`): 81 ilin 973 ilçesi; il seçilince yalnız o ilin ilçeleri listelenir, adresler "İlçe/İl" biçiminde yazılır.

## Sırada

Bu sırayla geliştirilecek.

1. **Gelir vergisi stopajı** · Küçük: Serbest meslek ve kira stopajı vergileri, serbest meslek makbuzu çıktısı.
2. **Kur farkı faturası** · Orta: Tahsilatta oluşan kur farkı için faturanın oluşturulması.
3. **Mizan, bilanço ve gelir tablosu** · Orta: Tek Düzen Hesap Planı'na göre finansal raporlar, Community için.

## Planlanıyor

Kapsamı büyük; tasarım aşamasında.

- **e-Fatura ve e-Arşiv (Community)** · Büyük: Odoo 20 ile Nilvera entegrasyonu yalnız Enterprise'da kaldı. Community için e-Fatura ve e-Arşiv gönderimi.
- **Çek ve senet portföyü** · Büyük: Çek ve senet girişi, ciro, tahsil ve portföy takibi.

## Değerlendiriliyor

İhtiyaç ve firma API'lerine erişim netleşince sıraya alınacak.

- **Banka ekstresi içe aktarma**: Türk bankalarının Excel ve CSV ekstreleri.
- **Fatura ve irsaliye çıktısı**: Türkiye'de alışılmış belge düzeni.
- **Ödeme: PayTR, Param**: iyzico Odoo 19'da zaten var.
- **SMS: Netgsm, İleti Merkezi**: Odoo'nun SMS bildirimleri için Türk sağlayıcılar.
- **Kargo: Yurtiçi, Aras, MNG, PTT**: Gönderi oluşturma, etiket ve takip.
- **Pazaryerleri: Trendyol, Hepsiburada, n11**: Ürün, stok ve sipariş eşitleme.

## Kapsam dışı

Şu an yapılmayacak olanlar ve nedenleri.

- **KDV tevkifatı**: Odoo'nun Türkiye yerelleştirmesinde zaten var.
- **Ba-Bs formları**: Eylül 2024 döneminden itibaren kaldırıldı (VUK Genel Tebliği Sıra No. 565).
- **Bordro**: Community'de bordro altyapısı yok; mevzuat yükü çok ağır.
- **e-Defter**: GİB'in özel teknik gereksinimlerine tabi; bu proje kapsamında değil.
- **Yazar kasa (ÖKC)**: Cihaz üreticisine bağlı entegrasyon gerektirir.

## Öneri ve katkı

- **Yeni modül önerisi:** [odoo-tr.com forumu, Yeni Özellikler & İstekler](https://odoo-tr.com/t/yeni-ozellikler-istekler)
- **Hata ve öneri:** [GitHub issue](https://github.com/Odoo-Tr/odoo-turkiye/issues)
- **Katkı:** Pull request'ler açıktır. Mevzuata dayanan değişikliklerde kaynak (GİB, Resmî Gazete) belirtin.

Sıra ve kapsam ihtiyaçlara göre değişebilir.
