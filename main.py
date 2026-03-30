from src.collector import NewsCollector
from src.analyzer import FinancialAnalyzer

def main():
    collector = NewsCollector()
    analyzer = FinancialAnalyzer()

    print("Haberler çekiliyor...\n")
    terimler = ["borsa hisse", "BIST yatırım", "Türkiye ekonomi faiz"]
    haberler = collector.toplu_cek(terimler)
    print(f"{len(haberler)} haber çekildi.\n")

    print("Analiz yapılıyor...\n")
    sonuclar = {"bullish": [], "bearish": [], "neutral": []}

    for haber in haberler:
        baslik = haber.get("title", "")
        if not baslik:
            continue

        sonuc = analyzer.analiz_et(baslik)

        # Sadece hisse içeren haberleri göster
        if sonuc["hisseler"]:
            sonuclar[sonuc["etiket"]].append(sonuc)

    # Özet
    print("=" * 60)
    print("HISSE BAZLI ANALİZ SONUÇLARI")
    print("=" * 60)

    for etiket, liste in sonuclar.items():
        emoji = "🟢" if etiket == "bullish" else "🔴" if etiket == "bearish" else "⚪"
        print(f"\n{emoji} {etiket.upper()} ({len(liste)} haber)")
        for s in liste:
            print(f"  [{', '.join(s['hisseler'])}] {s['metin']}")

    print("\n" + "=" * 60)
    print(f"Toplam analiz: {sum(len(v) for v in sonuclar.values())} hisse içeren haber")

if __name__ == "__main__":
    main()