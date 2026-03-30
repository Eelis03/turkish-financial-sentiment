from transformers import pipeline
from src.keywords import BULLISH_KEYWORDS, BEARISH_KEYWORDS
from src.stock_matcher import hisse_bul


class FinancialAnalyzer:

    def __init__(self, model_adi: str = "Eelis/turkish-financial-bert-v2"):
        self.model = pipeline("text-classification", model=model_adi)

    def _anahtar_kelime_skoru(self, metin: str) -> str | None:
        """
        Metinde bullish/bearish anahtar kelime var mı kontrol et.
        Model kararını desteklemek için kullanılır.
        """
        metin_lower = metin.lower()
        bullish_skor = sum(1 for k in BULLISH_KEYWORDS if k in metin_lower)
        bearish_skor = sum(1 for k in BEARISH_KEYWORDS if k in metin_lower)

        if bullish_skor > bearish_skor:
            return "bullish"
        elif bearish_skor > bullish_skor:
            return "bearish"
        return None

    def analiz_et(self, metin: str) -> dict:
        """
        Metni analiz et — model + anahtar kelime hibrit.
        """
        # Model tahmini
        tahmin = self.model(metin)[0]
        model_etiketi = tahmin["label"]
        model_guveni = round(tahmin["score"], 2)

        # Anahtar kelime kontrolü
        keyword_etiketi = self._anahtar_kelime_skoru(metin)

        # Hibrit karar
        # Model güveni düşükse anahtar kelimeye bak
        if model_guveni < 0.75 and keyword_etiketi:
            final_etiket = keyword_etiketi
            kaynak = "keyword"
        else:
            final_etiket = model_etiketi
            kaynak = "model"

        # Hisse tespiti
        hisseler = hisse_bul(metin)

        return {
            "metin": metin,
            "etiket": final_etiket,
            "guven": model_guveni,
            "karar_kaynagi": kaynak,
            "hisseler": hisseler,
            "model_etiketi": model_etiketi,
            "keyword_etiketi": keyword_etiketi,
        }

    def toplu_analiz(self, metinler: list[str]) -> list[dict]:
        return [self.analiz_et(m) for m in metinler]


if __name__ == "__main__":
    analyzer = FinancialAnalyzer()

    metinler = [
        "Türk Hava Yolları büyük zarar açıkladı",
        "Garanti Bankası ve Akbank hisseleri yükseldi",
        "Borsa İstanbul güne yatay başladı",
        "Tüpraş rekor kar açıkladı",
        "THYAO hisseleri sert düştü",
    ]

    for metin in metinler:
        sonuc = analyzer.analiz_et(metin)
        emoji = "🟢" if sonuc["etiket"] == "bullish" else "🔴" if sonuc["etiket"] == "bearish" else "⚪"
        print(f"{emoji} [{sonuc['etiket'].upper()}] ({sonuc['guven']}) — {sonuc['karar_kaynagi']}")
        print(f"   Hisseler: {sonuc['hisseler']}")
        print(f"   {metin}\n")