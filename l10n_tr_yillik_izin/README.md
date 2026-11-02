# Türkiye - Yıllık İzin

4857 sayılı İş Kanunu'nun 53. maddesine göre yıllık ücretli izin hakkını kıdemden hesaplar ve her hizmet yılı dolduğunda izin tahsisini Odoo İzin'e kendiliğinden ekler.

> 1 Mart 2019'da işe giren 48 yaşındaki çalışan, 1 Mart 2026'da 7. hizmet yılını doldurur: **20 gün** yıllık izin.

## Hak edilen süre

| Kıdem | Yıllık izin |
|---|---|
| 1 yıldan 5 yıla kadar (5 dahil) | 14 gün |
| 5 yıldan fazla, 15 yıldan az | 20 gün |
| 15 yıl ve daha fazla | 26 gün |

- 18 ve daha küçük yaştaki ya da 50 ve daha büyük yaştaki çalışanlara en az 20 gün verilir. Yaş, hizmet yılının dolduğu güne göre hesaplanır.
- Yer altı işlerinde çalışanların izni 4 gün artırılır.
- Bunlar kanundaki en az sürelerdir; iş sözleşmesi ya da toplu sözleşmeyle daha uzun izin verilebilir.

## Nasıl çalışır?

1. Modül kurulunca Odoo'nun **Ücretli İzin** türü "Türkiye yıllık izni" olarak işaretlenir. Başka bir izin türü kullanacaksanız **İzin → Yapılandırma → İzin Türleri**'nde işareti o türe taşıyın.
2. Çalışan formunda **Kıdem Başlangıcı**'nı girin; gerekiyorsa **Yer Altı İşi**'ni işaretleyin. Formda tamamlanan hizmet yılı ve hak edilen gün görünür.
3. Her gün çalışan zamanlanmış görev, hizmet yılını dolduran çalışanlara o yılın iznini tahsis eder ve onaylar. Beklemeden tahsis için formdaki **Tahsis Et** düğmesine basın.

- Her hizmet yılı için tek tahsis oluşturulur; görev tekrar çalışınca kopya oluşmaz.
- Yalnız içinde bulunulan hizmet yılı tahsis edilir. Önceki yıllardan kalan izinleri, kullanılan günleri bilen insan kaynakları ekibi elle girmelidir.
- İzin süresine denk gelen ulusal bayram, hafta tatili ve genel tatil günleri izinden sayılmaz (md. 56). Bunun için Odoo'nun çalışma takvimi ve resmi tatiller kullanılır; tatilleri yüklemek için [Türkiye - Resmi Tatiller](../l10n_tr_resmi_tatil) modülünü kurabilirsiniz.

## Kaynak

4857 sayılı İş Kanunu, madde 53–56 ([mevzuat.gov.tr](https://www.mevzuat.gov.tr/mevzuat?MevzuatNo=4857&MevzuatTur=1&MevzuatTertip=5)). Yer altı işleri için 4 günlük ek, 6552 sayılı Kanun'la eklenmiştir.

## Uyumluluk

| Odoo | Dal |
|---|---|
| 15.0 | [`15.0`](https://github.com/Odoo-Tr/odoo-turkiye/tree/15.0) |
| 16.0 | [`16.0`](https://github.com/Odoo-Tr/odoo-turkiye/tree/16.0) |
| 17.0 | [`17.0`](https://github.com/Odoo-Tr/odoo-turkiye/tree/17.0) |
| 18.0 | [`18.0`](https://github.com/Odoo-Tr/odoo-turkiye/tree/18.0) |
| 19.0 | [`19.0`](https://github.com/Odoo-Tr/odoo-turkiye/tree/19.0) |
| 20.0 | [`20.0`](https://github.com/Odoo-Tr/odoo-turkiye/tree/20.0) |

Odoo 20'de izin türleri "iş girişi türü" olarak birleştirildi; modül orada Türkiye'ye ait ücretli izin türünü kullanır.

Sorular ve öneriler için: [odoo-tr.com](https://odoo-tr.com)
