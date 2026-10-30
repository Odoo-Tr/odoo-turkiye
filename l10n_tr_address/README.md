# Türkiye - İl ve İlçe Adresleri

Odoo 81 ili tanır ama ilçeleri tanımaz; şehir alanı serbest metin olduğu için aynı ilçe "Kadıköy", "KADIKOY", "Kadıköy/İst." diye farklı farklı yazılır. Bu modül **81 ilin 973 ilçesini** ekler ve ilçeyi, seçilen ile göre süzülen bir listeye çevirir.

> Caferağa Mah. Moda Cad. No: 12
> 34710 **Kadıköy/İstanbul**
> Türkiye

## Özellikler

- **973 ilçe:** Odoo'daki 81 ile bağlı olarak gelir. 51 ildeki "Merkez" ilçeleri de dahildir.
- **İle göre süzülen liste:** Kişi kartında il seçilince yalnız o ilin ilçeleri listelenir. İlçe seçilince il kendiliğinden dolar, il değiştirilince başka ile ait ilçe temizlenir.
- **Türk adres düzeni:** Belgelerde adres "posta kodu İlçe/İl" biçiminde yazılır.
- **Mevcut kişiler eşleştirilir:** Kurulumda şehir alanı dolu kişiler ilçeleriyle eşleştirilir. "Karşıyaka", "KARSIYAKA" ve "Sarıyer / İstanbul" gibi yazımlar tanınır. "Merkez" gibi birden çok ilde olan adlar yalnız il belliyse eşleştirilir.
- **Sonradan içe aktarılan kişiler için:** Kişi listesinde kayıtları seçip **İşlemler → İlçeleri eşleştir**.

İlçeler **Kişiler → Yapılandırma → Yerelleştirme → Şehirler** menüsünden görülebilir. Listeye kişi kartından yeni ilçe eklenemez; yeni bir ilçe gerekirse bu menüden eklenir.

## Kurulumda değişen ayarlar

Türkiye ülke kaydında üç ayar değişir. Modül kaldırılınca Odoo'nun varsayılanlarına döner.

| Ayar | Değer |
|---|---|
| Şehirleri listeden seçtir | Açık |
| İl zorunlu (web sitesi ve portal adres formları) | Açık |
| Adres biçimi | `posta kodu İlçe/İl` |

## Uyumluluk

| Odoo | Dal |
|---|---|
| 18.0 | [`18.0`](https://github.com/Odoo-Tr/odoo-turkiye/tree/18.0) |
| 19.0 | [`19.0`](https://github.com/Odoo-Tr/odoo-turkiye/tree/19.0) |
| 20.0 | [`20.0`](https://github.com/Odoo-Tr/odoo-turkiye/tree/20.0) (web sitesi ve portal adres formunda da ilçe listesi) |

## Veri kaynağı

İlçe listesi [TurkiyeAPI](https://github.com/ubeydeozdmr/turkiye-api) 2025 veri setinden alındı (MIT, Copyright (c) 2022-2026 Ubeyde Emir Özdemir) ve iki bağımsız listeyle ([turkey-neighbourhoods](https://github.com/muratgozel/turkey-neighbourhoods), [il-ilce-json](https://github.com/snrylmz/il-ilce-json)) karşılaştırıldı; üçü de il il aynı 973 ilçeyi verir.

Sorular ve öneriler için: [odoo-tr.com](https://odoo-tr.com)
