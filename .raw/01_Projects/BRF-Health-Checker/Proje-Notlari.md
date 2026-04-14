# BRF Health Checker

**Durum:** ✅ Çalışıyor (manuel restart gerekebilir)  
**Lokasyon:** `/home/tughan/clawd/projects/brf-health-checker/`  
**Port:** 8765  
**Stack:** FastAPI + pdfplumber + GPT-4o-mini

---

## Amaç

İsveç'teki BRF (Bostadsrättsförening / Housing Association) ekonomik sağlığını analiz eden tool. ~90.000 BRF satışı/yıl, rakip yok.

---

## Özellikler

- PDF yıllık rapor analizi (pdfplumber → metin çıkarma)
- GPT-4o-mini ile skorlama
- Health score: 0-100
- Liquidity, debt ratio, maintenance plan analysis

---

## Test Sonuçları (Gerçek BRF'ler)

| BRF | Skor | Notlar |
|-----|------|--------|
| Kungsängen | 55/100 | Orta risk |
| Väduren | 60/100 | Kabul edilebilir |
| Fågelbärsträdet | 75/100 | İyi durum |

---

## Bilinen Sorunlar

- **Liquidity hesaplama bug'u** — Tuğhan "acil değil" dedi
- **Systemd service eksik** — Reboot sonrası manuel restart gerekli

---

## Gelecek Planı

- pdfplumber → markitdown geçişi (beklemede)
- Systemd service kurulumu
- Monetizasyon: €5/kullanım veya €10/ay

---

**Başlangıç:** 19 Şubat 2026
