# Yol haritası

*Son güncelleme: 2 Kasım 2026*

Odoo Türkiye'nin açık kaynak Türkiye modüllerinde neyin yayında olduğu, sırada ne olduğu ve neyi neden yapmadığımız.

## Yayında

Community sürümünde kurulabilir. Her modülün çalıştığı Odoo sürümleri yanında yazılı.

- **[TCMB Döviz Kurları](https://github.com/Odoo-Tr/odoo-turkiye/tree/19.0/l10n_tr_tcmb_rates)** (`l10n_tr_tcmb_rates`): Döviz kurlarını her gün TCMB gösterge kurları bülteninden otomatik günceller. Odoo 15–20.
- **[Faturada Yazıyla Tutar](https://github.com/Odoo-Tr/odoo-turkiye/tree/19.0/l10n_tr_amount_in_words)** (`l10n_tr_amount_in_words`): Fatura çıktısına "Yalnız: ... Türk Lirası ... Kuruş" satırını ekler. Odoo 15–20.
- **[İl ve İlçe Adresleri](https://github.com/Odoo-Tr/odoo-turkiye/tree/19.0/l10n_tr_address)** (`l10n_tr_address`): 81 ilin 973 ilçesi; il seçilince yalnız o ilin ilçeleri listelenir, adresler "İlçe/İl" biçiminde yazılır. Odoo 15–20.
- **[Gelir Vergisi Stopajı](https://github.com/Odoo-Tr/odoo-turkiye/tree/19.0/l10n_tr_stopaj)** (`l10n_tr_stopaj`): Serbest meslek ve kira ödemelerinde %20 stopaj, doğru hesaplarla; muhtasar için aylık stopaj listesi. Odoo 17–20.
- **[KKTC Muhasebe](https://github.com/Odoo-Tr/odoo-turkiye/tree/19.0/l10n_kktc)** (`l10n_kktc`): Kuzey Kıbrıs Türk Cumhuriyeti: ülke, altı ilçe, KKTC Tek Düzen Hesap Planı ve %0/%5/%10/%16/%20 KDV. Odoo 17–20.
- **[Kur Farkı Faturası](https://github.com/Odoo-Tr/odoo-turkiye/tree/19.0/l10n_tr_kur_farki)** (`l10n_tr_kur_farki`): Dövizli faturanın tahsilat ya da ödemesinde oluşan kur farkı için KDV'si iç yüzdeyle hesaplanmış fatura, tek tıkla. Odoo 16–20.
- **[Kur Değerlemesi](https://github.com/Odoo-Tr/odoo-turkiye/tree/19.0/l10n_tr_kur_degerleme)** (`l10n_tr_kur_degerleme`): Dönem sonunda dövizli alacak, borç ve banka hesaplarını değerleme günü kuruyla değerler; fark 646/656'ya (VUK 280). Odoo 15–20.
- **[Resmi Tatiller](https://github.com/Odoo-Tr/odoo-turkiye/tree/19.0/l10n_tr_resmi_tatil)** (`l10n_tr_resmi_tatil`): Ulusal bayramlar, genel tatiller ve 2025–2030 dini bayramları, arife ve 28 Ekim yarım günleriyle İzin'e yüklenir. Odoo 15–20.
- **[Yıllık İzin](https://github.com/Odoo-Tr/odoo-turkiye/tree/19.0/l10n_tr_yillik_izin)** (`l10n_tr_yillik_izin`): İş Kanunu md. 53'e göre kıdemden 14/20/26 gün yıllık izin; her hizmet yılı dolunca otomatik tahsis. Odoo 15–20.
- **[Türk Bankaları](https://github.com/Odoo-Tr/odoo-turkiye/tree/19.0/l10n_tr_banka)** (`l10n_tr_banka`): 67 banka, EFT ve BIC kodlarıyla; Türk IBAN'ı girilince banka kendiliğinden seçilir. Odoo 15–20.
- **[Vergi Daireleri](https://github.com/Odoo-Tr/odoo-turkiye/tree/19.0/l10n_tr_vergi_dairesi)** (`l10n_tr_vergi_dairesi`): 1.046 vergi dairesi; kişi ve şirkette ile göre süzülen Vergi Dairesi alanı. Odoo 15–19 (Odoo 20'de Odoo'nun kendisinde var).
- **[Hesap Grupları (Odoo 15)](https://github.com/Odoo-Tr/odoo-turkiye/tree/15.0/l10n_tr_account_group)** (`l10n_tr_account_group`): Odoo 15'in Türkiye hesap planında olmayan Tek Düzen Hesap Planı grupları. Yalnız Odoo 15.

## Sırada

Bu sırayla geliştirilecek.

1. **Mizan, bilanço ve gelir tablosu** · Orta: Tek Düzen Hesap Planı'na göre finansal raporlar, Community için.

## Planlanıyor

Kapsamı büyük; tasarım aşamasında.

- **e-Fatura ve e-Arşiv (Community)** · Büyük: Odoo 20 ile Nilvera entegrasyonu yalnız Enterprise'da kaldı. Community için e-Fatura ve e-Arşiv gönderimi.
- **Çek ve senet portföyü** · Büyük: Çek ve senet girişi, ciro, tahsil ve portföy takibi.

## Değerlendiriliyor

İhtiyaç ve firma API'lerine erişim netleşince sıraya alınacak.

- **KKTC e-Fatura**: Gelir ve Vergi Dairesi'nin e-Fatura web servisi. Test için KKTC'de kayıtlı bir firmanın test hesabı ve e-imzası gerekiyor.
- **Banka ekstresi içe aktarma**: Türk bankalarının Excel ve CSV ekstreleri.
- **Fatura ve irsaliye çıktısı**: Türkiye'de alışılmış belge düzeni.
- **Ödeme: PayTR, Param**: iyzico Odoo 19'da zaten var.
- **SMS: Netgsm, İleti Merkezi**: Odoo'nun SMS bildirimleri için Türk sağlayıcılar.
- **Kargo: Yurtiçi, Aras, MNG, PTT**: Gönderi oluşturma, etiket ve takip.
- **Pazaryerleri: Trendyol, Hepsiburada, n11**: Ürün, stok ve sipariş eşitleme.

## Kapsam dışı

Şu an yapılmayacak olanlar ve nedenleri.

- **KDV tevkifatı**: Odoo'nun Türkiye yerelleştirmesinde zaten var.
- **VKN/TCKN doğrulama**: Odoo 15–20'de Odoo'nun kendisinde var.
- **Ba-Bs formları**: Eylül 2024 döneminden itibaren kaldırıldı (VUK Genel Tebliği Sıra No. 565).
- **Bordro**: Community'de bordro altyapısı yok; mevzuat yükü çok ağır.
- **e-Defter**: GİB'in özel teknik gereksinimlerine tabi; bu proje kapsamında değil.
- **Yazar kasa (ÖKC)**: Cihaz üreticisine bağlı entegrasyon gerektirir.

## Öneri ve katkı

- **Yeni modül önerisi:** [odoo-tr.com forumu, Yeni Özellikler & İstekler](https://odoo-tr.com/t/yeni-ozellikler-istekler)
- **Hata ve öneri:** [GitHub issue](https://github.com/Odoo-Tr/odoo-turkiye/issues)
- **Katkı:** Pull request'ler açıktır. Mevzuata dayanan değişikliklerde kaynak (GİB, Resmî Gazete) belirtin.

Sıra ve kapsam ihtiyaçlara göre değişebilir.
