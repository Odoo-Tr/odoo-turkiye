# Türkiye - Mali Tablolar

Mizanı, ayrıntılı bilançoyu ve ayrıntılı gelir tablosunu Tek Düzen Hesap Planı sıralamasıyla PDF ve Excel olarak verir. Odoo Community'de mali rapor yoktur; bu modül mali müşavirin ve beyannamenin istediği üç tabloyu ekler.

> 30.04.2025 bilançosu: **I. Dönen Varlıklar** altında A. Hazır Değerler → 1. Kasa, C. Ticari Alacaklar → 1. Alıcılar; **257 Birikmiş Amortismanlar (-)** gibi indirim kalemleri parantez içinde. Aktif ve pasif toplamı aynı.

## Nasıl çalışır?

1. **Faturalama → Raporlama → Türkiye Mali Tabloları** menüsünü açın.
2. **Mizan**, **Bilanço** ya da **Gelir Tablosu**'nu seçin.
3. Tarihleri girip **PDF Yazdır** ya da **Excel'e Aktar** düğmesine basın.

| Tablo | İçerik |
|---|---|
| Mizan | Her ana hesap (100, 120, 320...) için devir, dönem ve toplam borç/alacak, borç bakiyesi ve alacak bakiyesi. İsterseniz alt hesaplarla (102001 gibi). |
| Bilanço | I-V bölümleri, A, B, C... grupları ve numaralı satırlar. Önceki yılın aynı günüyle karşılaştırmalı. |
| Gelir tablosu | A. Brüt Satışlar'dan Dönem Net Kârı veya Zararı'na tüm ara toplamlar. Geçen yılın aynı dönemiyle karşılaştırmalı. |

- **Hesapların yeri:** Hesap kodunun ilk üç hanesine bakılır (102001 → 102 Bankalar). Satır adları ve sırası Tek Düzen Hesap Planı'ndandır.
- **Kapanış fişi kesilmemişse:** Yılın sonucu bilançoda **59 Dönem Net Kârı (Zararı)** grubunda, önceki yılların kapanmamış sonucu **57 / 58** grubunda ayrı satırda gösterilir. Böylece bilanço her zaman tutar.
- **Mizanda devir:** Bilanço hesaplarının devri ilk kayıttan başlar. Gelir tablosu hesaplarının (6 ve 7) devri ise mali yıl başından başlar. Önceki yılların kapanmamış sonucu mizanın sonunda tek satırda devir olarak yer alır.
- **Kapanış fişleri:** 690 ya da 692 hesabına satırı olan fişler gelir tablosuna alınmaz. Yıl kapandıktan sonra da gelir tablosu doğru çıkar.
- **7/A ve 7/B:** Yansıtması yapılmamış maliyet hesaplarının bakiyesi gelir tablosunda ayrı satırda görünür:
  - 71-74 satışların maliyetine eklenir.
  - 75-77 ve 79 faaliyet giderlerine eklenir.
  - 78 finansman giderlerine eklenir.
- **Taslak kayıtlar:** Varsayılan olarak yalnız onaylanmış kayıtlar alınır. **Taslak kayıtları dahil et** işaretlenirse taslaklar da girer.

## Bilmeniz gerekenler

- Hesap planınız Tek Düzen Hesap Planı'na uymalıdır; Odoo'nun Türkiye hesap planı uyar. Kodu üç rakamla başlamayan hesaplar, nazım hesaplar (9) ve formda yeri olmayan hesaplar (ör. 690, 697, 698) tablonun altında ayrıca listelenir. Bakiyeleri sıfır değilse aktif-pasif farkı uyarı olarak gösterilir.
- Gelir tablosundaki harflendirme (A-K) KAP'ta yayımlanan ayrıntılı gelir tablolarındaki düzene göredir. Kaynaklar arasında harflendirme farklılık gösterebiliyor. Tebliğin Resmî Gazete'deki ek tablolarıyla tek tek karşılaştırmadım.
- Ters bakiyeli hesaplar (ör. borç bakiyeli 320 Satıcılar) olduğu yerde eksi olarak görünür; karşı tarafa aktarılmaz.
- Tutarlar şirketin para birimindedir. Rapor tek şirket içindir; şube ya da konsolidasyon yapmaz.
- Beyanname öncesi tabloları mali müşavirinize kontrol ettirin.

## Kaynak

- Muhasebe Sistemi Uygulama Genel Tebliği (Sıra No: 1), 26.12.1992 tarihli ve 21447 mükerrer sayılı Resmî Gazete.
- Hesap adları: İSMMMO, Tekdüzen Hesap Çerçevesi ve Hesap Planı.

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
