from transformers import pipeline
from src.keywords import classify_headline


class FinancialAnalyzer:

    def __init__(self, model_adi: str = "Eelis/turkish-financial-bert-v2"):
        self.model = pipeline("text-classification", model=model_adi)

    def analiz_et(self, metin: str) -> dict:
        # Model tahmini
        tahmin = self.model(metin)[0]
        model_etiketi = tahmin["label"]
        model_guveni = round(tahmin["score"], 2)

        # Kural bazlı sistem
        kural_sonuc = classify_headline(metin)
        kural_etiketi = kural_sonuc["label"]
        kural_guveni = kural_sonuc["confidence"]

        # Hibrit karar
        # Model güveni yüksekse modele güven
        # Düşükse kural sistemine bak
        if model_guveni >= 0.85:
            final_etiket = model_etiketi
            kaynak = "model"
        elif kural_guveni >= 0.70:
            final_etiket = kural_etiketi
            kaynak = "kural"
        else:
            # İkisi de emin değilse neutral
            final_etiket = "neutral"
            kaynak = "fallback"

        return {
            "metin": metin,
            "etiket": final_etiket,
            "guven": model_guveni,
            "karar_kaynagi": kaynak,
            "hisseler": kural_sonuc["stocks"],
            "model_etiketi": model_etiketi,
            "kural_etiketi": kural_etiketi,
        }

    def toplu_analiz(self, metinler: list[str]) -> list[dict]:
        return [self.analiz_et(m) for m in metinler]


if __name__ == "__main__":
    analyzer = FinancialAnalyzer()

    metinler = [
        "Koç'tan savaş tedbiri: TÜPRAŞ'ta dev hisse satışı",
        "THYAO hisseleri rekor kırdı",
        "Akbank güçlü bilanço açıkladı",
        "Merkez Bankası faiz kararını açıkladı",
        "BIST100 endeksi güne düşük hacimle başladı",
        "Garanti Bankası karını artırdı",
        "EREGL hisseleri taban yaptı",
    ]

    for metin in metinler:
        sonuc = analyzer.analiz_et(metin)
        emoji = "🟢" if sonuc["etiket"] == "bullish" else "🔴" if sonuc["etiket"] == "bearish" else "⚪"
        print(f"{emoji} [{sonuc['etiket'].upper()}] model:{sonuc['model_etiketi']} kural:{sonuc['kural_etiketi']} kaynak:{sonuc['karar_kaynagi']}")
        print(f"   Hisseler: {sonuc['hisseler']}")
        print(f"   {metin}\n")