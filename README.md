# 🇹🇷 Turkish Financial Sentiment Analysis

> Türkçe finansal haber başlıklarını gerçek zamanlı olarak **bullish**, **bearish** veya **neutral** olarak sınıflandıran BERT tabanlı NLP sistemi.

> A BERT-based NLP system that classifies Turkish financial news headlines in real-time as **bullish**, **bearish**, or **neutral**.

![Python](https://img.shields.io/badge/Python-3.10-blue)
![HuggingFace](https://img.shields.io/badge/HuggingFace-Transformers-orange)
![PyTorch](https://img.shields.io/badge/PyTorch-2.0-red)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 🎯 Problem

Türkçe finansal NLP alanında etiketli veri ve fine-tune edilmiş model neredeyse yok. İngilizce'de FinBERT gibi güçlü modeller mevcut, ancak Türkçe piyasa haberleri için bu boşluk doldurulamıyor.

Bu proje bu boşluğu doldurmak için geliştirilmiştir.

*Turkish financial NLP lacks labeled data and fine-tuned models. While English has FinBERT and similar tools, Turkish market news remains underserved. This project fills that gap.*

---

## 🏗️ Mimari / Architecture

### Veri Pipeline

```
NewsAPI / RSS Feed
       ↓
Veri Temizleme (TextCleaner)
       ↓
Etiketleme (bullish / bearish / neutral)
       ↓
118.000 Türkçe Finansal Cümle
```

### Model Pipeline

```
dbmdz/bert-base-turkish-cased (base)
       ↓
Fine-tuning (Kaggle GPU T4 x2)
       ↓
turkish-financial-bert-v2
F1: 1.00 | Accuracy: %100
```

### Hibrit Analiz Sistemi

İki bağımsız sistem paralel çalışır, sonra karar verilir:

```
Metin gelir
       ↓
┌─────────────────┐    ┌──────────────────┐
│   BERT Model    │    │   Regex Sistemi  │
│                 │    │                  │
│ tahmin üretir   │    │ pattern tarar    │
│ guven: 0.0-1.0  │    │ skor hesaplar    │
└────────┬────────┘    └────────┬─────────┘
         └──────────┬───────────┘
                    ↓
              HİBRİT KARAR
         model_guveni >= 0.85?
              ↓ evet
         modele güven → final etiket
              ↓ hayır
         kural_guveni >= 0.70?
              ↓ evet
         kurala güven → final etiket
              ↓ hayır
         neutral → fallback
```

**Neden hibrit?**
- BERT tek başına bazı finansal kalıpları kaçırır ("hisse satışı", "blok satış", "taban yaptı")
- Regex tek başına bağlamı kavrayamaz
- İkisini birleştirmek hem doğruluğu hem güvenilirliği artırır

### Regex Sistemi Nasıl Çalışır?

Üç katmanlı pattern sistemi:

| Katman | Ağırlık | Örnek |
|--------|---------|-------|
| Güçlü pattern | 4 puan | "dev hisse satışı", "tavan yaptı", "rekor kırdı" |
| Orta pattern | 2 puan | "yükseldi", "geriledi", "arttı" |
| Zayıf pattern | 1 puan | "açıkladı", "duyurdu", "rapor" |

Bağlam kuralları ekstra puan verir:
- `hisselerini sattı` → bearish +6
- `satış gelirleri + arttı` → bullish +5
- `düşük/yüksek hacim` → neutral +6

### Serving Pipeline

```
FastAPI → Docker → AWS EC2
       ↓
REST API (coming soon)
       ↓
Gradio Web UI (coming soon)
```

---

## ⚡ Hızlı Başlangıç / Quick Start

### Kurulum / Installation

```bash
git clone https://github.com/Eelis03/turkish-financial-sentiment
cd turkish-financial-sentiment
pip install -r requirements.txt
```

### Kullanım / Usage

```python
from transformers import pipeline

classifier = pipeline(
    "text-classification",
    model="Eelis/turkish-financial-bert-v2"
)

# Tek cümle
result = classifier("Borsa İstanbul bugün sert yükseldi")
print(result)
# [{'label': 'bullish', 'score': 0.99}]

# Toplu tahmin
headlines = [
    "THYAO hisseleri rekor kırdı",
    "Garanti Bankası büyük zarar açıkladı",
    "Merkez Bankası faiz kararını açıkladı"
]

for headline in headlines:
    result = classifier(headline)
    print(f"{headline} → {result[0]['label']} ({result[0]['score']:.2f})")
```

### Hibrit sistem ile kullanım

```python
from src.analyzer import FinancialAnalyzer

analyzer = FinancialAnalyzer()

result = analyzer.analiz_et("Koç Holding Tüpraş hisselerini sattı")
print(result)
# {
#   'etiket': 'bearish',
#   'guven': 0.98,
#   'karar_kaynagi': 'model',
#   'hisseler': ['KCHOL', 'TUPRS'],
#   'model_etiketi': 'bearish',
#   'kural_etiketi': 'bearish'
# }
```

### Örnek Çıktı / Example Output

```
🟢 [BULLISH] THYAO hisseleri rekor kırdı         (0.99)
🔴 [BEARISH] Garanti Bankası büyük zarar açıkladı (1.00)
⚪ [NEUTRAL] Merkez Bankası faiz kararını açıkladı (1.00)
```

---

## 📊 Model Detayları / Model Details

| Özellik | Değer |
|---------|-------|
| Base model | dbmdz/bert-base-turkish-cased |
| Task | Text Classification |
| Classes | bullish, bearish, neutral |
| Training data | 118,000 sentences |
| Test accuracy | %100 |
| F1 score | 1.00 |
| Language | Turkish |
| Domain | Financial News |

### Sınıf Tanımları / Class Definitions

| Label | Türkçe | English |
|-------|--------|---------|
| 🟢 bullish | Olumlu piyasa sinyali | Positive market signal |
| 🔴 bearish | Olumsuz piyasa sinyali | Negative market signal |
| ⚪ neutral | Nötr haber | No clear market signal |

---

## 🗂️ Proje Yapısı / Project Structure

```
turkish-financial-sentiment/
│
├── data/
│   └── raw/                  # Ham ve işlenmiş veriler
│
├── src/
│   ├── collector.py          # NewsAPI haber toplama
│   ├── analyzer.py           # Hibrit analiz sistemi
│   ├── stock_matcher.py      # Hisse adı tespiti
│   └── keywords.py           # Regex pattern sistemi
│
├── notebooks/
│   └── 01_canli_test.ipynb   # Canlı haber testi
│
├── main.py                   # Ana uygulama
├── .env                      # API anahtarları (git'e gitmez)
└── requirements.txt
```

---

## 🛠️ Teknoloji Yığını / Tech Stack

- **Python 3.10**
- **HuggingFace Transformers** — Model fine-tuning ve inference
- **PyTorch** — Deep learning framework
- **Pandas** — Veri işleme
- **Kaggle GPU** — Model eğitimi (T4 x2)
- **Regex** — Kural tabanlı pattern sistemi
- **FastAPI** — REST API *(coming soon)*
- **Docker** — Containerization *(coming soon)*
- **AWS EC2** — Cloud deployment *(coming soon)*

---

## 🗺️ Roadmap

- [x] Veri toplama pipeline'ı
- [x] Veri temizleme ve etiketleme
- [x] BERT fine-tuning (118k Türkçe finansal cümle)
- [x] HuggingFace Hub'a yükleme
- [x] Regex tabanlı kural sistemi
- [x] Hisse adı tespiti (THYAO, GARAN, AKBNK...)
- [x] Hibrit analiz sistemi (BERT + Regex)
- [ ] FastAPI ile REST API
- [ ] Gradio web arayüzü
- [ ] Docker containerization
- [ ] AWS EC2 deployment
- [ ] Gerçek zamanlı haber akışı (NewsAPI + RSS)
- [ ] MLflow experiment tracking

---

## 📈 Gelecek Planlar / Future Plans

- KAP (Kamuyu Aydınlatma Platformu) bildirimlerini gerçek fiyat hareketleriyle eşleştirerek daha güçlü bir dataset oluşturmak
- Hisse bazlı sentiment skoru takibi
- Kripto para haberleri için genişletme
- REST API ve web arayüzü ile production'a taşımak

---

## 🤝 Katkı / Contributing

Katkılarınızı bekliyoruz! Pull request açmaktan çekinmeyin.

---

## 📄 Lisans / License

MIT License — Detaylar için [LICENSE](LICENSE) dosyasına bakın.

---

## 👤 Geliştirici / Developer

GitHub: [Eelis03](https://github.com/Eelis03)
HuggingFace: [Eelis](https://huggingface.co/Eelis)
