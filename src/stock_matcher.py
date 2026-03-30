from src.keywords import STOCK_NAMES


def hisse_bul(metin: str) -> list[str]:
    """
    Metinde geçen hisse kodlarını döndürür.
    Örnek: "Türk Hava Yolları zarar açıkladı" → ["THYAO"]
    """
    bulunan = []
    metin_lower = metin.lower()

    for kod, isimler in STOCK_NAMES.items():
        for isim in isimler:
            if isim.lower() in metin_lower:
                if kod not in bulunan:
                    bulunan.append(kod)
                break

    return bulunan


if __name__ == "__main__":
    test_metinler = [
        "Türk Hava Yolları büyük zarar açıkladı",
        "Garanti Bankası ve Akbank hisseleri yükseldi",
        "Borsa İstanbul güne yatay başladı",
        "Tüpraş ve Ereğli sert satışlarla geriledi",
    ]

    for metin in test_metinler:
        hisseler = hisse_bul(metin)
        print(f"Metin: {metin}")
        print(f"Bulunan hisseler: {hisseler}\n")