import requests
import os
from dotenv import load_dotenv
import time

load_dotenv()


class NewsCollector:

    def __init__(self):
        self.api_key = os.getenv("NEWS_API_KEY")
        self.base_url = "https://newsapi.org/v2/everything"

    def haber_cek(self, arama_terimi: str, sayfa_boyutu: int = 20) -> list[dict]:
        params = {
            "q": arama_terimi,
            "language": "tr",
            "pageSize": sayfa_boyutu,
            "sortBy": "publishedAt",
            "apiKey": self.api_key
        }

        try:
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()["articles"]
        except Exception as e:
            print(f"Hata: {e}")
            return []

    def toplu_cek(self, terimler: list[str], bekleme: float = 1.0) -> list[dict]:
        tum_haberler = []
        for terim in terimler:
            haberler = self.haber_cek(terim)
            tum_haberler.extend(haberler)
            time.sleep(bekleme)

        # Tekrar edenleri at
        gorülen = set()
        benzersiz = []
        for haber in tum_haberler:
            baslik = haber.get("title", "")
            if baslik and baslik not in gorülen and baslik != "[Removed]":
                gorülen.add(baslik)
                benzersiz.append(haber)

        return benzersiz


if __name__ == "__main__":
    collector = NewsCollector()

    terimler = ["borsa hisse", "BIST yatırım", "Türkiye ekonomi faiz"]
    haberler = collector.toplu_cek(terimler)

    print(f"Toplam benzersiz haber: {len(haberler)}")
    for h in haberler[:3]:
        print(f"- {h['title']}")