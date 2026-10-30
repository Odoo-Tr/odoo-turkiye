# Türkiye - Kur Farkı Faturası

Dövizli bir fatura farklı kurdan tahsil edildiğinde ya da ödendiğinde oluşan kur farkı KDV'ye tabidir ve lehine oluşan tarafça faturalanır. Odoo kur farkını 646 Kambiyo Karları / 656 Kambiyo Zararları hesabına yazar ama fatura kesmez. Bu modül kur farkı faturasını tek tıkla oluşturur.

> 6.000 USD'lik fatura 41,20'den kesildi, 42,55'ten tahsil edildi: 8.100,00 TL kur farkı = **6.750,00 matrah + 1.350,00 KDV (%20)**.

## Nasıl çalışır?

1. Dövizli faturanın tahsilatını ya da ödemesini her zamanki gibi kaydedin.
2. Faturada henüz faturalanmamış kur farkı varsa üstte bir bilgi bandı çıkar: tutar ve kimin lehine olduğu.
3. **Kur Farkı Faturası** düğmesine basın, taslağı kontrol edip onaylayın.

| Durum | Oluşan belge |
|---|---|
| Lehinize (daha fazla tahsil ettiniz ya da daha az ödediniz) | Sizin keseceğiniz **satış faturası** |
| Karşı tarafın lehine | Karşı tarafın göndereceği faturayı kaydetmek için **alış faturası** taslağı; onların fatura numarasını Referans'a girin |

- **KDV iç yüzdeyle hesaplanır:** Kur farkı KDV dahil kabul edilir; oran asıl faturadaki orandır. Birden çok oranlı faturalarda kur farkı oranlara göre bölünür.
- **Tarih:** Tahsilat ya da ödeme tarihi.
- **Muhasebe:** Kur farkı tutarı asıl tahsilat ya da ödemeyle zaten alındığı veya ödendiği için, onaylanan kur farkı faturası otomatik bir mahsup kaydıyla kur farkı hesabına kapatılır ve "Ödendi" görünür. Sonuçta 646'da (ya da 656'da) matrah kalır, KDV 391'e (ya da 191'e) geçer.
- **Kısmi ödemeler:** Her ödemenin kur farkı bir kez faturalanır; sonraki ödemeler için ayrıca kur farkı faturası oluşturulabilir.
- **Toplu oluşturma:** Fatura listesinde kayıtları seçip **İşlemler → Kur farkı faturası oluştur**.
- **Geri alma:** Kur farkı faturası taslağa çekilirse mahsup kaydı ters kayıtla iptal edilir. İptal edilen kur farkı faturasının tutarı yeniden faturalanabilir.

## Bilmeniz gerekenler

- **Tevkifatlı faturalar** ve yüzde dışı vergiler otomatik işlenmez; düğme nedenini söyler, bu faturaları elle oluşturun.
- **Yalnız gerçekleşen kur farkı:** Yıl sonu ya da geçici vergi dönemi değerlemesinden doğan kur farkı için KDV hesaplanmaz ve fatura düzenlenmez; modül yalnız tahsilat ve ödemelerde oluşan farkı faturalar.
- e-Fatura gönderimi bu modülün konusu değildir; oluşan fatura e-Fatura entegrasyonunuz varsa onunla gönderilir.

## Uyumluluk

| Odoo | Dal |
|---|---|
| 18.0 | [`18.0`](https://github.com/Odoo-Tr/odoo-turkiye/tree/18.0) |
| 19.0 | [`19.0`](https://github.com/Odoo-Tr/odoo-turkiye/tree/19.0) |
| 20.0 | [`20.0`](https://github.com/Odoo-Tr/odoo-turkiye/tree/20.0) |

Sorular ve öneriler için: [odoo-tr.com](https://odoo-tr.com)
