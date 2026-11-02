# Türkiye - Resmi Tatiller

Türkiye'nin ulusal bayramlarını, genel tatillerini ve dini bayramlarını Odoo İzin'e resmi tatil olarak yükler. İzin süreleri hesaplanırken bu günler çalışma günü sayılmaz.

> 2026: Ramazan Bayramı 19 Mart 13:00 – 22 Mart, Kurban Bayramı 26 Mayıs 13:00 – 30 Mayıs.

## Neler yüklenir?

| Tatil | Süre |
|---|---|
| Yılbaşı (1 Ocak), 23 Nisan, 1 Mayıs, 19 Mayıs, 15 Temmuz, 30 Ağustos | Tam gün |
| Cumhuriyet Bayramı | 28 Ekim 13:00'ten itibaren yarım gün, 29 Ekim tam gün |
| Ramazan Bayramı | Arife 13:00'ten itibaren 3,5 gün |
| Kurban Bayramı | Arife 13:00'ten itibaren 4,5 gün |

Dini bayram tarihleri 2025–2030 yılları için hazırdır:

| Yıl | Ramazan Bayramı arifesi | Kurban Bayramı arifesi |
|---|---|---|
| 2025 | 29 Mart | 5 Haziran |
| 2026 | 19 Mart | 26 Mayıs |
| 2027 | 8 Mart | 15 Mayıs |
| 2028 | 25 Şubat | 4 Mayıs |
| 2029 | 13 Şubat | 23 Nisan |
| 2030 | 3 Şubat | 12 Nisan |

## Nasıl çalışır?

1. Modülü kurduğunuzda ülkesi Türkiye olan şirketler için içinde bulunulan yıldan 2030'a kadar tatiller yüklenir.
2. Başka yıl ya da şirket için **İzin → Yapılandırma → Türkiye Resmi Tatilleri** sihirbazını açın, yılları ve şirketleri seçip **Tatilleri Yükle**'ye basın.
3. Aynı saatlere denk gelen bir resmi tatil zaten varsa o kayıt atlanır; sihirbazı tekrar çalıştırmak kopya oluşturmaz.

- Saatler Türkiye saatine (Europe/Istanbul) göredir.
- Bir dini bayram ulusal bir bayramla çakışırsa (2027'de Kurban Bayramı ile 19 Mayıs, 2029'da Kurban Bayramı ile 23 Nisan) Odoo üst üste binen tatile izin vermediği için ikisi tek kayıtta birleştirilir.
- Odoo 20'de Odoo'nun kendi Türkiye tatil listesi yerine bu modülün listesi kullanılır; Odoo'nun listesinde arife yarım günleri yoktur.

## Kaynaklar

- Sabit tarihler ve yarım günler: 2429 sayılı Ulusal Bayram ve Genel Tatiller Hakkında Kanun ([mevzuat.gov.tr](https://www.mevzuat.gov.tr/mevzuat?MevzuatNo=2429&MevzuatTur=1&MevzuatTertip=5)).
- Dini bayram tarihleri: Diyanet İşleri Başkanlığı dini günler takvimi. Diyanet ileri yılların tarihlerini hesapla ilan eder; yıl yaklaşınca resmî takvimle karşılaştırın.
- Cumhurbaşkanlığı kararıyla verilen ek idari izinler (köprü günleri) kamu kurumları içindir ve yüklenmez.

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
