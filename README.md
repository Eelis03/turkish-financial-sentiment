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
 
```
┌─────────────────────────────────────────────────────┐
│                   VERİ PIPELINE                      │
│                                                     │
│  NewsAPI / RSS Feed                                 │
│       ↓                                             │
│  Veri Temizleme (TextCleaner)                       │
│       ↓                                             │
│  Etiketleme (bullish / bearish / neutral)           │
│       ↓                                             │
│  118.000 Türkçe Finansal Cümle                      │
└─────────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────────┐
│                  MODEL PIPELINE                      │
│                                                     │
│  dbmdz/bert-base-turkish-cased (base)               │
│       ↓                                             │
│  Fine-tuning (Kaggle GPU T4 x2)                     │
│       ↓                                             │
│  turkish-financial-bert-v2                          │
│  F1: 1.00 | Accuracy: %100                         │
└─────────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────────┐
│                 SERVING PIPELINE                     │
│                                                     │
│  FastAPI → Docker → AWS EC2                         │
│       ↓                                             │
│  REST API (coming soon)                             │
│       ↓                                             │
│  Gradio Web UI (coming soon)                        │
└─────────────────────────────────────────────────────┘
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
 
### Örnek Çıktı / Example Output
 
```
THYAO hisseleri rekor kırdı          → bullish  (0.99)
Garanti Bankası büyük zarar açıkladı → bearish  (1.00)
Merkez Bankası faiz kararını açıkladı → neutral  (1.00)
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
├── src/                      # Kaynak kodlar
│   ├── collector.py          # Haber toplama
│   ├── cleaner.py            # Veri temizleme
│   └── model.py              # Model inference
│
├── notebooks/
│   ├── 01_veri_inceleme.ipynb
│   └── 02_model_egitim.ipynb
│
├── outputs/                  # Model çıktıları
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
- **FastAPI** — REST API *(coming soon)*
- **Docker** — Containerization *(coming soon)*
- **AWS EC2** — Cloud deployment *(coming soon)*
 
---
 
## 🗺️ Roadmap
 
- [x] Veri toplama pipeline'ı
- [x] Veri temizleme ve etiketleme
- [x] BERT fine-tuning
- [x] HuggingFace Hub'a yükleme
- [ ] FastAPI ile REST API
- [ ] Gradio web arayüzü
- [ ] Docker containerization
- [ ] AWS EC2 deployment
- [ ] Gerçek zamanlı haber akışı (NewsAPI + RSS)
- [ ] MLflow experiment tracking
 
---
 
## 📈 Gelecek Planlar / Future Plans
 
- KAP (Kamuyu Aydınlatma Platformu) bildirimlerini gerçek fiyat hareketleriyle eşleştirerek daha güçlü bir dataset oluşturmak
- Hisse bazlı sentiment takibi
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