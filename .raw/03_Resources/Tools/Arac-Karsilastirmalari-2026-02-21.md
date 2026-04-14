# Araç Karşılaştırmaları ve İncelemeler

**Tarih:** 21 Şubat 2026

---

## QuantMuse (0xemmkty/QuantMuse)

**GitHub:** 1.8k ⭐, Python  
**Tanım:** AI destekli quantitative trading sistemi

### Özellikler
- **Veri Kaynakları:** Binance, Yahoo Finance, Alpha Vantage
- **AI/ML:** GPT entegrasyonu, sentiment analizi
- **Modeller:** XGBoost, Random Forest, Neural Networks
- **Stratejiler:** 8+ yerleşik quant strateji
- **Araçlar:** Backtesting motoru, FastAPI dashboard

### Karar: Kurulmadı ❌

**Neden:**
- Mevcut Simmer/paper trading setup'u daha basit ve yeterli
- Kurulum ve öğrenme maliyeti yüksek
- Şu anki ihtiyaçlardan daha karmaşık

**Ne zaman kurulur:**
- Ciddi backtesting ve multi-factor strateji geliştirme ihtiyacı olursa
- Paper trading'den production'a geçiş yapılacaksa

---

## NoteDiscovery (gamosoft/NoteDiscovery)

**GitHub:** 2.3k ⭐, JavaScript/Python  
**Tanım:** Self-hosted not alma (Notion/Evernote alternatifi)

### Özellikler
- Markdown tabanlı
- Docker ile self-hosted
- Graph view (bağlantılı notlar)
- LaTeX/Math desteği
- HTML export

### Karar: Gerek yok ❌

**Neden:**
- Zaten Obsidian skill'i kurulu ve çalışıyor
- Obsidian daha olgun ekosistem
- NotDiscovery yeni/alternatif ama avantajı yetersiz

### Karşılaştırma

| | NoteDiscovery | Obsidian |
|---|---------------|----------|
| **Kurulum** | Docker (web) | Local app |
| **Ekosistem** | Yeni/az | Olgun/çok plugin |
| **Sync** | Self-hosted free | Ücretli sync (veya git) |
| **Format** | Markdown | Markdown |
| **OpenClaw** | ❌ Skill yok | ✅ Skill var |

---

## Build with Claude (davepoon/buildwithclaude)

**Tanım:** Claude Code için plugin marketplace

### İçerik
- 117 Agent (Python, Go, DevOps, Security uzmanları)
- 175 Command (`/commit`, `/docs`, `/tdd`)
- 28 Hook (Slack, Discord, Telegram alerts)
- 26 Skill
- 4,500+ MCP Server listesi

### Karar: Direkt kullanılamaz ⚠️

**Neden:**
- Farklı mimari (Claude Code ≠ OpenClaw)
- Farklı format ve dosya yapısı
- Doğrudan kurulum denemesi zaman kaybı

**Faydalı yönleri:**
- MCP Server listesi (4,500+) → OpenClaw'da test edilebilir
- Konsept/idea öğrenilebilir
- Agent prompt'ları okunup uyarlanabilir

---

## Özet Tablo

| Araç | Durum | Neden |
|------|-------|-------|
| **QuantMuse** | ❌ Kurulmadı | Karmaşık, mevcut setup yeterli |
| **NoteDiscovery** | ❌ Gerek yok | Obsidian zaten var |
| **Build with Claude** | ⚠️ Referans | Direkt kullanılamaz, fikir alınabilir |

---

**Sonuç:** Yeni araçlara kayıtsız şartsız hayır demek yerine mevcut setup'ı (OpenClaw + Obsidian + Simmer) optimize etmek daha verimli.
