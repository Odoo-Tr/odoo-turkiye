"""Tutarları Türkçe yazıya çevirir: 1234.56 TRY -> "Bin İki Yüz Otuz Dört Türk Lirası Elli Altı Kuruş"."""

ONES = ["", "bir", "iki", "üç", "dört", "beş", "altı", "yedi", "sekiz", "dokuz"]
TENS = ["", "on", "yirmi", "otuz", "kırk", "elli", "altmış", "yetmiş", "seksen", "doksan"]
SCALES = ["", "bin", "milyon", "milyar", "trilyon", "katrilyon"]

# Para birimi kodu -> (ana birim, alt birim)
CURRENCY_WORDS = {
    "TRY": ("Türk Lirası", "Kuruş"),
    "USD": ("ABD Doları", "Sent"),
    "EUR": ("Avro", "Sent"),
    "GBP": ("İngiliz Sterlini", "Peni"),
    "CHF": ("İsviçre Frangı", "Rappen"),
}


def _tr_capitalize(word):
    first = {"i": "İ", "ı": "I"}.get(word[0], word[0].upper())
    return first + word[1:]


def _three_digits(number):
    hundreds, rest = divmod(number, 100)
    tens, ones = divmod(rest, 10)
    words = []
    if hundreds:
        if hundreds > 1:
            words.append(ONES[hundreds])
        words.append("yüz")
    if tens:
        words.append(TENS[tens])
    if ones:
        words.append(ONES[ones])
    return words


def integer_to_words(number):
    """Pozitif tam sayıyı Türkçe kelime listesine çevirir (küçük harf)."""
    if number == 0:
        return ["sıfır"]
    words = []
    scale = 0
    while number:
        number, group = divmod(number, 1000)
        if group:
            group_words = _three_digits(group)
            if scale == 1 and group == 1:
                group_words = []  # "bir bin" değil "bin"
            if SCALES[scale]:
                group_words.append(SCALES[scale])
            words = group_words + words
        scale += 1
    return words


def amount_to_words(amount, currency_code="TRY", unit_label=None, subunit_label=None, decimals=2):
    """Tutarı "Bin İki Yüz Otuz Dört Türk Lirası Elli Altı Kuruş" biçiminde döndürür."""
    amount = round(abs(amount), decimals)
    whole = int(amount)
    fraction = round((amount - whole) * 10**decimals) if decimals else 0
    if fraction >= 10**decimals:  # yuvarlama taşması
        whole, fraction = whole + 1, 0
    unit, subunit = CURRENCY_WORDS.get(currency_code, (unit_label or currency_code, subunit_label or ""))
    text = " ".join(_tr_capitalize(word) for word in integer_to_words(whole)) + " " + unit
    if fraction and subunit:
        text += " " + " ".join(_tr_capitalize(word) for word in integer_to_words(fraction)) + " " + subunit
    return text
