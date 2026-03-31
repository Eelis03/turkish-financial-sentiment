import gradio as gr
from src.collector import NewsCollector
from src.analyzer import FinancialAnalyzer
from collections import defaultdict

collector = NewsCollector()
analyzer = FinancialAnalyzer()

ARAMA_TERIMLERI = [
    "borsa hisse yatırım",
    "BIST hisse senedi",
    "Türkiye ekonomi faiz",
    "şirket kar zarar",
    "temettü hisse"
]

def haberleri_cek_ve_analiz_et():
    haberler = collector.toplu_cek(ARAMA_TERIMLERI)

    bullish_satirlar = []
    bearish_satirlar = []
    neutral_satirlar = []

    # Hisse bazlı sayaç
    hisse_skorlari = defaultdict(lambda: {"bullish": 0, "bearish": 0, "neutral": 0})

    for haber in haberler:
        baslik = haber.get("title", "")
        if not baslik or baslik == "[Removed]":
            continue

        sonuc = analyzer.analiz_et(baslik)
        tarih = haber.get("publishedAt", "")[:10]
        kaynak = haber.get("source", {}).get("name", "")
        hisseler = sonuc["hisseler"]
        hisse_str = ", ".join(hisseler) if hisseler else "—"
        guven = f"{sonuc['guven']:.0%}"

        # Hisse skorlarını güncelle
        for hisse in hisseler:
            hisse_skorlari[hisse][sonuc["etiket"]] += 1

        satir = f"**{baslik}**\n📅 {tarih} | 📰 {kaynak} | 📊 {hisse_str} | 🎯 {guven}"

        if sonuc["etiket"] == "bullish":
            bullish_satirlar.append(satir)
        elif sonuc["etiket"] == "bearish":
            bearish_satirlar.append(satir)
        else:
            neutral_satirlar.append(satir)

    # Hisse bazlı özet tablo
    hisse_tablo = "## 📈 Hisse Bazlı Sentiment\n\n"
    hisse_tablo += "| Hisse | 🟢 Bullish | 🔴 Bearish | ⚪ Neutral | Genel |\n"
    hisse_tablo += "|-------|-----------|-----------|-----------|-------|\n"

    for hisse, skorlar in sorted(hisse_skorlari.items()):
        b = skorlar["bullish"]
        be = skorlar["bearish"]
        n = skorlar["neutral"]
        if b > be:
            genel = "🟢 Bullish"
        elif be > b:
            genel = "🔴 Bearish"
        else:
            genel = "⚪ Neutral"
        hisse_tablo += f"| **{hisse}** | {b} | {be} | {n} | {genel} |\n"

    if not hisse_skorlari:
        hisse_tablo += "| — | — | — | — | — |\n"

    def formatla(satirlar, emoji, etiket):
        if not satirlar:
            return f"*{etiket} haber bulunamadı.*"
        return "\n\n---\n\n".join(f"{emoji} {s}" for s in satirlar)

    bullish_text = formatla(bullish_satirlar, "🟢", "Bullish")
    bearish_text = formatla(bearish_satirlar, "🔴", "Bearish")
    neutral_text = formatla(neutral_satirlar, "⚪", "Neutral")

    ozet = f"""
## 📊 Analiz Özeti
| | Sayı |
|---|---|
| 🟢 Bullish | {len(bullish_satirlar)} |
| 🔴 Bearish | {len(bearish_satirlar)} |
| ⚪ Neutral | {len(neutral_satirlar)} |
| 📰 Toplam | {len(bullish_satirlar) + len(bearish_satirlar) + len(neutral_satirlar)} |

{hisse_tablo}
"""

    return ozet, bullish_text, bearish_text, neutral_text


with gr.Blocks(title="Türkçe Finansal Sentiment Analizi", theme=gr.themes.Soft()) as demo:

    gr.Markdown("""
    # 🇹🇷 Türkçe Finansal Sentiment Analizi
    Türkçe finansal haberleri gerçek zamanlı olarak **bullish**, **bearish** veya **neutral** olarak sınıflandırır.
    """)

    cek_btn = gr.Button("🔄 Haberleri Çek ve Analiz Et", variant="primary", size="lg")

    ozet_kutu = gr.Markdown()

    with gr.Row():
        with gr.Column():
            gr.Markdown("## 🟢 Bullish Haberler")
            bullish_kutu = gr.Markdown()

        with gr.Column():
            gr.Markdown("## 🔴 Bearish Haberler")
            bearish_kutu = gr.Markdown()

    gr.Markdown("## ⚪ Neutral Haberler")
    neutral_kutu = gr.Markdown()

    cek_btn.click(
        fn=haberleri_cek_ve_analiz_et,
        outputs=[ozet_kutu, bullish_kutu, bearish_kutu, neutral_kutu]
    )

if __name__ == "__main__":
    demo.launch()