from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.analyzer import FinancialAnalyzer
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Turkish Financial Sentiment API",
    description="Türkçe finansal haber başlıklarını bullish/bearish/neutral olarak sınıflandırır.",
    version="1.0"
)

# Model başlarken yüklensin
logger.info("Model yükleniyor...")
analyzer = FinancialAnalyzer()
logger.info("Model hazır.")


# İstek ve cevap şablonları
class HaberIstegi(BaseModel):
    metin: str


class TopluIstek(BaseModel):
    metinler: list[str]


class AnalizCevabi(BaseModel):
    metin: str
    etiket: str
    guven: float
    karar_kaynagi: str
    hisseler: list[str]
    model_etiketi: str
    kural_etiketi: str | None


# Endpoint'ler
@app.get("/")
def ana_sayfa():
    return {
        "mesaj": "Turkish Financial Sentiment API çalışıyor",
        "versiyon": "1.0",
        "endpoints": ["/analiz", "/toplu-analiz", "/saglik"]
    }


@app.get("/saglik")
def saglik():
    return {"durum": "aktif"}


@app.post("/analiz", response_model=AnalizCevabi)
def analiz(istek: HaberIstegi):
    if not istek.metin.strip():
        raise HTTPException(status_code=400, detail="Metin boş olamaz")

    logger.info(f"Analiz isteği: {istek.metin[:60]}")
    sonuc = analyzer.analiz_et(istek.metin)
    return sonuc


@app.post("/toplu-analiz")
def toplu_analiz(istek: TopluIstek):
    if not istek.metinler:
        raise HTTPException(status_code=400, detail="Metin listesi boş olamaz")
    if len(istek.metinler) > 50:
        raise HTTPException(status_code=400, detail="En fazla 50 metin gönderilebilir")

    logger.info(f"Toplu analiz isteği: {len(istek.metinler)} metin")
    sonuclar = analyzer.toplu_analiz(istek.metinler)
    return sonuclar