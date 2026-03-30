import re
from typing import Dict, List, Tuple, Any

# ============================================================
# STOCK / COMPANY NAME MAP
# ============================================================

STOCK_NAMES: Dict[str, List[str]] = {
    "THYAO": ["Türk Hava Yolları", "THY", "THYAO"],
    "GARAN": ["Garanti", "Garanti Bankası", "GARAN", "Garanti BBVA"],
    "AKBNK": ["Akbank", "AKBNK"],
    "EREGL": ["Ereğli", "Erdemir", "EREGL"],
    "BIMAS": ["BİM", "BIMAS", "Bim"],
    "KCHOL": ["Koç Holding", "Koç", "KCHOL"],
    "SISE": ["Şişecam", "SISE", "Sisecam"],
    "TUPRS": ["Tüpraş", "TUPRS", "Tupras"],
    "YKBNK": ["Yapı Kredi", "YKBNK", "Yapi Kredi"],
    "ASELS": ["Aselsan", "ASELS"],
    "EKGYO": ["Emlak Konut", "EKGYO"],
    "FROTO": ["Ford Otosan", "FROTO"],
    "TOASO": ["Tofaş", "TOASO", "Tofas"],
    "PGSUS": ["Pegasus", "PGSUS"],
    "SAHOL": ["Sabancı Holding", "Sabancı", "SAHOL", "Sabanci Holding", "Sabanci"],
}

# ============================================================
# AMBIGUOUS SINGLE TOKENS
# Bunlar tek başına güvenilir yön sinyali değildir.
# İstersen debug veya ek kural yazarken kullanırsın.
# ============================================================

AMBIGUOUS_KEYWORDS = [
    "satış", "yüksek", "güçlü", "kar", "kâr",
    "pozitif", "negatif", "risk", "başarı", "lider",
    "artış", "düşüş"
]

# ============================================================
# STRONG PATTERNS
# ============================================================

STRONG_BULLISH_PATTERNS = [
    r"\bsert yükseldi\b",
    r"\btavan yaptı\b",
    r"\brekor kırdı\b",
    r"\brekor tazeledi\b",
    r"\byeni zirvesini gördü\b",
    r"\bzirve yeniledi\b",
    r"\byılın en yüksek kapanışını (gerçekleştirdi|yaptı)\b",
    r"\ben yüksek kapanışını (gerçekleştirdi|yaptı)\b",
    r"\bgüçlü bilanço açıkladı\b",
    r"\bpozitif bilanço açıkladı\b",
    r"\bgüçlü büyüme rakamları açıkladı\b",
    r"\bkarını artırdı\b",
    r"\bkârını artırdı\b",
    r"\bkarını ikiye katladı\b",
    r"\bkârını ikiye katladı\b",
    r"\bbeklentilerin üzerinde kar açıkladı\b",
    r"\bbeklentilerin üzerinde k[âa]r açıkladı\b",
    r"\bnet karını yükseltti\b",
    r"\bnet k[âa]rını yükseltti\b",
    r"\bihracat gelirlerini büyüttü\b",
    r"\bsatış gelirlerini artırdı\b",
    r"\bcirosunu artırdı\b",
    r"\bkapasitesini artırdı\b",
    r"\büretim kapasitesini artırdı\b",
    r"\byatırımını büyüttü\b",
    r"\byeni sipariş aldı\b",
    r"\bihale kazandı\b",
    r"\byeni sözleşme imzaladı\b",
    r"\bgeri alım programı başlattı\b",
    r"\bpay geri alımı yaptı\b",
    r"\btemettü dağıtacağını açıkladı\b",
    r"\bdeğer kazandı\b",
    r"\byükselişe geçti\b",
    r"\bpozitif ayrıştı\b",
    r"\byolcu sayısında rekor kırdı\b",
    r"\byolcu gelirlerinde rekor açıkladı\b",
]

STRONG_BEARISH_PATTERNS = [
    r"\bsert düştü\b",
    r"\btaban yaptı\b",
    r"\byılın en düşük kapanışını (gerçekleştirdi|yaptı)\b",
    r"\ben düşük kapanışını (gerçekleştirdi|yaptı)\b",
    r"\bhisse satışı\b",
    r"\bpay satışı\b",
    r"\bblok satış\b",
    r"\bdev hisse satışı\b",
    r"\bhisselerini sattı\b",
    r"\bpaylarını sattı\b",
    r"\bikincil halka arz\b",
    r"\bzarar açıkladı\b",
    r"\bnet zarar açıkladı\b",
    r"\boperasyonel zarara geçti\b",
    r"\bbeklentilerin altında kaldı\b",
    r"\bdeğer kaybetti\b",
    r"\bsert satışlarla geriledi\b",
    r"\bsatış baskısı\b",
    r"\bçöküşe geçti\b",
    r"\berime yaşadı\b",
    r"\büretimi durdurdu\b",
    r"\büretime ara verdi\b",
    r"\bfabrika üretimine ara verdi\b",
    r"\bsiparişlerinde düşüş yaşadı\b",
    r"\bcirosu geriledi\b",
    r"\bgelirleri daraldı\b",
    r"\bnot indirimi\b",
    r"\bceza aldı\b",
    r"\bsoruşturma başlatıldı\b",
    r"\bkonkordato\b",
    r"\biflas\b",
    r"\bsavaş baskısı\b",
    r"\bjeopolitik riskler arttı\b",
    r"\bdip seviyeye geriledi\b",
    r"\bçöküş\b",
    r"\bkayıp verdi\b",
]

STRONG_NEUTRAL_PATTERNS = [
    r"\bdüşük hacim(le)?\b",
    r"\byüksek hacim(le)?\b",
    r"\bfaiz kararını açıkladı\b",
    r"\bgenel kurul tarihini duyurdu\b",
    r"\byönetim kurulu kararını açıkladı\b",
    r"\bbağımsız denetim raporunu yayınladı\b",
    r"\byıllık faaliyet raporunu yayınladı\b",
    r"\baylık bültenini yayınladı\b",
    r"\byatırımcı toplantısı düzenleyecek\b",
    r"\btoplantı yaptı\b",
    r"\bkapasite kullanım oranını açıkladı\b",
    r"\bçeyrek sonuçlarını açıkladı\b",
    r"\bfinansal sonuçlarını paylaştı\b",
    r"\bişlem saatlerini güncelledi\b",
    r"\bgenel kurul\b",
    r"\bbildirim yaptı\b",
    r"\bbaşvuru yaptı\b",
    r"\bizahname yayımlandı\b",
    r"\bhalka arz oluyor\b",
    r"\bhisse fiyatları belli oldu\b",
    r"\byatay seyretti\b",
    r"\bgüne yatay başladı\b",
    r"\bdeğişmedi\b",
    r"\bhaftalık performansı ne oldu\b",
    r"\ben çok kazandıran ve kaybettiren hisseler belli oldu\b",
    r"\bhangi yatırım aracı ne kadar kazandırdı\b",
    r"\bhaftalık kayıp yüzde\b",  # tartışmalı; istersen bearish'e taşıyabilirsin
]

# ============================================================
# MEDIUM PATTERNS
# Tek başına karar vermez; sadece destek puanı sağlar.
# ============================================================

MEDIUM_BULLISH_PATTERNS = [
    r"\barttı\b",
    r"\byükseldi\b",
    r"\bkazandı\b",
    r"\btoparlandı\b",
    r"\bgüçlendi\b",
    r"\bbüyüdü\b",
    r"\bralli yaptı\b",
    r"\bivme kazandı\b",
    r"\bpozitif ayrıştı\b",
    r"\bkar açıkladı\b",
    r"\bk[âa]r açıkladı\b",
]

MEDIUM_BEARISH_PATTERNS = [
    r"\bdüştü\b",
    r"\bgeriledi\b",
    r"\bazaldı\b",
    r"\bkaybetti\b",
    r"\bzayıfladı\b",
    r"\bdaraldı\b",
    r"\byavaşladı\b",
    r"\bnegatif ayrıştı\b",
    r"\bkayıp verdi\b",
    r"\bbaskı\b",
    r"\brisk\b",
]

MEDIUM_NEUTRAL_PATTERNS = [
    r"\baçıkladı\b",
    r"\bduyurdu\b",
    r"\bkarar\b",
    r"\brapor\b",
    r"\bprogram\b",
    r"\btarih\b",
    r"\bgüncelledi\b",
    r"\bbülten\b",
    r"\bpaylaştı\b",
]

# ============================================================
# CONTEXT RULES
# ============================================================

SATIS_BULLISH_CONTEXT = [
    r"\bsatış gelirleri\b",
    r"\bnet satışlar\b",
    r"\bsatış hacmi\b",
    r"\bsatış adetleri\b",
    r"\bciro\b",
]

SATIS_BEARISH_CONTEXT = [
    r"\bhisse satışı\b",
    r"\bpay satışı\b",
    r"\bblok satış\b",
    r"\bhisselerini sattı\b",
    r"\bpaylarını sattı\b",
    r"\bdev hisse satışı\b",
]

YUKSEK_BULLISH_CONTEXT = [
    r"\byılın en yüksek kapanışı\b",
    r"\ben yüksek kapanış\b",
    r"\byeni zirve\b",
    r"\brekor seviye\b",
]

YUKSEK_NEUTRAL_CONTEXT = [
    r"\byüksek hacim\b",
]

DUSUK_NEUTRAL_CONTEXT = [
    r"\bdüşük hacim\b",
]

KAR_BULLISH_CONTEXT = [
    r"\bkarını artırdı\b",
    r"\bkârını artırdı\b",
    r"\bkarını ikiye katladı\b",
    r"\bkârını ikiye katladı\b",
    r"\bbeklentilerin üzerinde kar\b",
    r"\bbeklentilerin üzerinde k[âa]r\b",
    r"\bnet kar açıkladı\b",
    r"\bnet k[âa]r açıkladı\b",
]

KAR_NEUTRAL_CONTEXT = [
    r"\bk[âa]r dağıtımı\b",
    r"\bk[âa]r dağıttı\b",
    r"\bk[âa]r payı\b",
    r"\bkar dağıtımı\b",
    r"\bkar dağıttı\b",
    r"\bkar payı\b",
]

QUESTION_OR_LIST_NEUTRAL_PATTERNS = [
    r"\bişte\b",
    r"\bdetaylar belli oldu\b",
    r"\bne oldu\b",
    r"\bne kadar kazandırdı\b",
    r"\ben çok kazandıran\b",
    r"\ben çok kaybettiren\b",
]

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def normalize_text(text: str) -> str:
    text = text.casefold()
    text = text.replace("’", "'").replace("`", "'").replace("“", '"').replace("”", '"')
    text = re.sub(r"\s+", " ", text).strip()
    return text

def score_patterns(text: str, patterns: List[str], weight: int) -> Tuple[int, List[str]]:
    score = 0
    matched = []
    for pat in patterns:
        if re.search(pat, text, flags=re.IGNORECASE):
            score += weight
            matched.append(pat)
    return score, matched

def detect_stocks(text: str, stock_names: Dict[str, List[str]] = STOCK_NAMES) -> List[str]:
    t = normalize_text(text)
    found = []
    for ticker, aliases in stock_names.items():
        for alias in aliases:
            alias_norm = normalize_text(alias)
            if alias_norm and re.search(rf"(?<!\w){re.escape(alias_norm)}(?!\w)", t, flags=re.IGNORECASE):
                found.append(ticker)
                break
    return sorted(set(found))

# ============================================================
# MAIN CLASSIFIER
# ============================================================

def classify_headline(text: str) -> Dict[str, Any]:
    t = normalize_text(text)

    scores = {"bullish": 0, "bearish": 0, "neutral": 0}
    matched_patterns = {"bullish": [], "bearish": [], "neutral": []}

    # ---------- Strong patterns ----------
    s, m = score_patterns(t, STRONG_BULLISH_PATTERNS, 4)
    scores["bullish"] += s
    matched_patterns["bullish"] += m

    s, m = score_patterns(t, STRONG_BEARISH_PATTERNS, 4)
    scores["bearish"] += s
    matched_patterns["bearish"] += m

    s, m = score_patterns(t, STRONG_NEUTRAL_PATTERNS, 4)
    scores["neutral"] += s
    matched_patterns["neutral"] += m

    # ---------- Medium patterns ----------
    s, m = score_patterns(t, MEDIUM_BULLISH_PATTERNS, 2)
    scores["bullish"] += s
    matched_patterns["bullish"] += m

    s, m = score_patterns(t, MEDIUM_BEARISH_PATTERNS, 2)
    scores["bearish"] += s
    matched_patterns["bearish"] += m

    s, m = score_patterns(t, MEDIUM_NEUTRAL_PATTERNS, 1)
    scores["neutral"] += s
    matched_patterns["neutral"] += m

    # ========================================================
    # CONTEXT RULES
    # ========================================================

    # 1) SATIŞ bağlamı
    if re.search(r"\b(hisse satışı|pay satışı|blok satış|hisselerini sattı|paylarını sattı|dev hisse satışı)\b", t):
        scores["bearish"] += 6
        matched_patterns["bearish"].append("CTX:hisse/pay/blok satışı -> bearish")

    if re.search(r"\b(satış gelirleri|net satışlar|satış hacmi|satış adetleri|ciro)\b", t) and \
       re.search(r"\b(arttı|yükseldi|büyüdü|güçlendi|rekor|artış)\b", t):
        scores["bullish"] += 5
        matched_patterns["bullish"].append("CTX:satış gelirleri/ciro + arttı/yükseldi -> bullish")

    # 2) HACİM bağlamı
    if re.search(r"\b(yüksek hacim|düşük hacim)\b", t):
        scores["neutral"] += 6
        matched_patterns["neutral"].append("CTX:yüksek/düşük hacim -> neutral")

    # 3) ZİRVE / DİP bağlamı
    if re.search(r"\b(yılın en yüksek kapanışı|en yüksek kapanış|yeni zirve|rekor seviye)\b", t):
        scores["bullish"] += 5
        matched_patterns["bullish"].append("CTX:yüksek kapanış/zirve/rekor seviye -> bullish")

    if re.search(r"\b(yılın en düşük kapanışı|dip seviye|dip seviyeye)\b", t):
        scores["bearish"] += 5
        matched_patterns["bearish"].append("CTX:düşük kapanış/dip seviye -> bearish")

    # 4) KAR bağlamı
    if re.search(r"\b(karını artırdı|kârını artırdı|karını ikiye katladı|kârını ikiye katladı|beklentilerin üzerinde kar|beklentilerin üzerinde k[âa]r|net kar açıkladı|net k[âa]r açıkladı)\b", t):
        scores["bullish"] += 5
        matched_patterns["bullish"].append("CTX:güçlü kar bağlamı -> bullish")

    if re.search(r"\b(kar dağıtımı|kâr dağıtımı|kar dağıttı|kâr dağıttı|kar payı|kâr payı)\b", t):
        scores["neutral"] += 3
        matched_patterns["neutral"].append("CTX:kar dağıtımı/pay -> neutral")

    # 5) SORU / LİSTE / DERLEME tipi başlıklar genelde neutral
    if re.search(r"\b(işte|detaylar belli oldu|ne oldu|ne kadar kazandırdı|en çok kazandıran|en çok kaybettiren)\b", t):
        scores["neutral"] += 3
        matched_patterns["neutral"].append("CTX:soru/liste/derleme formatı -> neutral")

    # 6) Duyuru fiilleri bull/bear sinyali varsa baskın olmamalı
    if scores["bullish"] > 0 or scores["bearish"] > 0:
        scores["neutral"] = max(0, scores["neutral"] - 2)
        matched_patterns["neutral"].append("CTX:bull/bear var, neutral duyuru puanı hafif düşürüldü")

    # 7) Çok güçlü bearish finansal olaylar
    if re.search(r"\b(savaş baskısı|jeopolitik risk|not indirimi|ceza aldı|soruşturma başlatıldı|konkordato|iflas)\b", t):
        scores["bearish"] += 4
        matched_patterns["bearish"].append("CTX:makro/olumsuz olay -> bearish")

    # 8) Bazı net bullish eventler
    if re.search(r"\b(geri alım programı başlattı|pay geri alımı yaptı|ihale kazandı|yeni sipariş aldı|yeni sözleşme imzaladı)\b", t):
        scores["bullish"] += 4
        matched_patterns["bullish"].append("CTX:geri alım/ihale/sipariş/sözleşme -> bullish")

    # ========================================================
    # TIE-BREAK / FINAL DECISION
    # ========================================================

    # Özel öncelik: hisse satışı, taban yaptı, zarar açıkladı gibi çok güçlü bearish olaylar
    if re.search(r"\b(dev hisse satışı|hisse satışı|pay satışı|blok satış|hisselerini sattı|taban yaptı|zarar açıkladı|net zarar açıkladı)\b", t):
        if scores["bearish"] >= scores["bullish"]:
            label = "bearish"
            confidence = _calc_confidence(scores, label)
            return {
                "label": label,
                "confidence": confidence,
                "scores": scores,
                "matched_patterns": matched_patterns,
                "stocks": detect_stocks(text),
                "text": text,
            }

    # Özel öncelik: rekor kırdı, tavan yaptı, güçlü bilanço, yılın en yüksek kapanışı
    if re.search(r"\b(rekor kırdı|tavan yaptı|güçlü bilanço açıkladı|yılın en yüksek kapanışını (gerçekleştirdi|yaptı)|yeni zirvesini gördü)\b", t):
        if scores["bullish"] >= scores["bearish"]:
            label = "bullish"
            confidence = _calc_confidence(scores, label)
            return {
                "label": label,
                "confidence": confidence,
                "scores": scores,
                "matched_patterns": matched_patterns,
                "stocks": detect_stocks(text),
                "text": text,
            }

    # Güçlü fark varsa o sınıfı seç
    if scores["bearish"] >= scores["bullish"] + 3 and scores["bearish"] >= scores["neutral"]:
        label = "bearish"
    elif scores["bullish"] >= scores["bearish"] + 3 and scores["bullish"] >= scores["neutral"]:
        label = "bullish"
    else:
        # Skorlar yakınsa neutral'a düş
        sorted_items = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        if len(sorted_items) >= 2 and (sorted_items[0][1] - sorted_items[1][1] <= 2):
            label = "neutral"
        else:
            label = max(scores, key=scores.get)

    confidence = _calc_confidence(scores, label)

    return {
        "label": label,
        "confidence": confidence,
        "scores": scores,
        "matched_patterns": matched_patterns,
        "stocks": detect_stocks(text),
        "text": text,
    }

def _calc_confidence(scores: Dict[str, int], label: str) -> float:
    values = sorted(scores.values(), reverse=True)
    top = values[0]
    second = values[1] if len(values) > 1 else 0
    if top <= 0:
        return 0.34
    margin = top - second

    # Basit heuristik confidence
    # Çok agresif 1.00 vermemesi için sınırlandı.
    conf = 0.50 + min(0.45, margin * 0.08)
    return round(conf, 2)

# ============================================================
# OPTIONAL: KEYWORD-ONLY FALLBACK
# İstersen bu listeleri de kullanabilirsin ama önerilen sistem regex+context.
# ============================================================

BULLISH_KEYWORDS = [
    "yükseldi", "arttı", "kazandı", "rekor", "güçlendi",
    "tavan", "büyüdü", "toparlandı", "ivme", "çıkış",
    "rallisi", "pozitif", "büyüme", "değer kazandı",
    "ihracat artışı", "bilanço güçlü", "zirve", "yüksek kapanış"
]

BEARISH_KEYWORDS = [
    "düştü", "azaldı", "kaybetti", "geriledi", "zayıfladı",
    "taban", "zarar", "çöktü", "negatif", "kayıp",
    "baskı", "kriz", "endişe", "sert satış", "değer kaybetti",
    "çöküş", "erime", "daraldı", "yavaşladı", "olumsuz", "risk",
    "hisse satışı", "pay satışı", "blok satış"
]

NEUTRAL_KEYWORDS = [
    "açıkladı", "duyurdu", "toplantı", "genel kurul",
    "rapor", "bülten", "güncelledi", "tarih", "program",
    "başvuru", "bildirim", "karar", "değişmedi", "yatay",
    "düşük hacim", "yüksek hacim", "faiz kararı", "faaliyet raporu"
]

# ============================================================
# DEMO
# ============================================================

if __name__ == "__main__":
    samples = [
        "Koç'tan savaş tedbiri: TÜPRAŞ'ta dev hisse satışı",
        "Koç Holding'den dikkat çeken hareket: Tüpraş hisselerini sattı!",
        "Koç Holding'den 7.5 milyar liralık Tüpraş hisse satışı",
        "THYAO hisseleri rekor kırdı",
        "Akbank güçlü bilanço açıkladı",
        "Şişecam yılın en yüksek kapanışını gerçekleştirdi",
        "EREGL hisseleri taban yaptı",
        "BIST100 endeksi güne düşük hacimle başladı",
        "Merkez Bankası faiz kararını açıkladı",
        "Altın, borsa, euro ve dolar: Yatırımcıya en çok ne kazandırdı?",
    ]

    for s in samples:
        result = classify_headline(s)
        print("-" * 80)
        print("TEXT      :", result["text"])
        print("STOCKS    :", result["stocks"])
        print("LABEL     :", result["label"])
        print("CONF      :", result["confidence"])
        print("SCORES    :", result["scores"])
        print("MATCHED   :", result["matched_patterns"])