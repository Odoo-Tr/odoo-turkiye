# Türkiye - Bankalar

Türkiye'de faaliyet gösteren 67 bankayı EFT kodları ve BIC (SWIFT) kodlarıyla Odoo'ya ekler. Bir kişiye ya da şirkete Türk IBAN'ı girildiğinde banka kendiliğinden seçilir.

> TR62 **0001 0**012 3456 7890 1234 56 → IBAN'ın 5–9. haneleri banka kodudur: 00010 → T.C. Ziraat Bankası A.Ş.

## Neler eklenir?

| Banka türü | Sayı |
|---|---|
| Mevduat bankaları | 35 |
| Kalkınma ve yatırım bankaları | 21 |
| Katılım bankaları | 10 |
| TMSF bankası | 1 |

- Her bankanın adı BDDK listesindeki resmî unvanıdır; EFT kodu banka kartında **EFT Kodu** alanında görünür ve banka listesinde aranabilir.
- Adil Katılım Bankası'nın yayımlanmış bir EFT kodu bulunamadığı için yalnız adı ve BIC'i eklenir.
- Altı bankanın BIC kodu boş bırakıldı (Fups Bank, Türk Ticaret Bankası, İller Bankası, Q Yatırım Bankası, Tera Yatırım Bankası, Ziraat Katılım Bankası): güvenilir bir kaynakta doğrulanamadı. Hepsi Bank'ın listelerde görünen BIC'i eski unvanına (Rabobank) ait olduğu için o da eklenmedi.

## Nasıl çalışır?

1. Kişinin **Muhasebe → Banka Hesapları** bölümüne Türk IBAN'ını girin.
2. Banka seçilmemişse IBAN'daki koddan bulunup seçilir; banka elle seçildiyse değiştirilmez.

Odoo 20'de ayrı bir banka listesi yoktur; banka adı ve BIC doğrudan hesabın üzerine yazılır.

## Kaynaklar

- Banka listesi ve unvanlar: BDDK (Bankacılık Düzenleme ve Denetleme Kurumu) banka listesi.
- EFT ve BIC kodları: Türkiye Bankalar Birliği banka bilgileri ile TCMB FAST katılımcı listesi, birbirleriyle karşılaştırılarak.
- IBAN yapısı: TCMB, Uluslararası Banka Hesap Numarası (IBAN) Tebliği.

Bankalar birleşip kapandıkça liste değişir; eksik ya da eski bir kayıt görürseniz bize bildirin.

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
