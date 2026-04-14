# Trading Projeleri Geçmişi

## 1. BTC Momentum Tracker (Şubat 2026)

### Deneme 1: 2-Saatlik Marketler (İptal Edildi)

**Tarih:** 12 Şubat 2026, 22:45-23:00  
**İstek:** "Sabaha kadar hiç bir şey sormadan bu işi hallet"

**Sorun:** Polymarket API erişimi yok  
**Çözüm (başlangıç):** Simülasyon (lag + noise modelleme)  
**Kullanıcı tepkisi:** "Tamamını iptal et bu senin yapabileceğin bir iş gibi durmuyor"

**Ders:**
- ❌ Simülasyon sunma, gerçek entegrasyon isteniyorsa
- ❌ "Sabaha kadar" sözü verme, kritik dependency eksikse
- ✅ Sınırlamaları baştan söyle
- ✅ Alternatif zaman çizelgesi sun veya erken iptal et

### Deneme 2: 15-Dakika Lag Detection (Başarılı)

**Tarih:** 12 Şubat 2026, 23:03-23:15  
**Kullanıcı:** "İmkanlarını kullan, pes ediyorsun!"

**Bulunan Çözüm:**
- ✅ Polymarket 15-min BTC markets: `/crypto/15M`
- ✅ URL pattern: `/event/btc-updown-15m-{timestamp}`
- ✅ Browser scraping çalışıyor
- ✅ Binance WebSocket entegrasyonu
- ✅ Lag detection algoritması

**Strateji:**
> "15 min bitcoin marketlerindeki düşük fiyatlandırmaları alıp yükselmesini denesem?"

- BTC pump ederken UP @ 48¢ al
- Market tepki verince 75¢ sat
- Kâr: +56% per trade

---

## 2. Simmer Copytrading

**Durum:** ✅ Aktif  
**API:** Simmer API (sk_live_...)  
**Bakiye:** $10,000 SIM (virtual)  
**Limit:** Max $100/trade, $500/günlük

---

## 3. Stock News Edge Tracker

**Durum:** ✅ Üretimde  
**Discord:** #trade kanalı  
**Kaynaklar:** X/Twitter (Bird CLI) + RSS  
**Eşik:** Edge skor ≥ 6/10 → alarm

---

## Trading Strateji Evrimi

1. **Başlangıç:** Whale copy (uzun vadeli pozisyonlar)
2. **Pivot:** Kısa vadeli sadece (max 1-2 gün) — kullanıcı tercihi
3. **Yeni:** BTC momentum scalping (2-saat, lag exploitasyonu)

**Beklenen ROI:**
- 2-saat: $15-25/gün
- 15-dakika: $20-40/gün (sonra)

**Hedef:** $50 → $500-800 (1 ay)

---

**Ders:** API yoksa browser scraping, simülasyon son çare değil ilk çare değil.
