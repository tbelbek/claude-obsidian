# Kurulu Araçlar ve Servisler

**Ortam:** Linux (Ubuntu), Göteborg  
**Son Güncelleme:** 21 Şubat 2026

---

## Bookmark Yönetimi

### Karakeep
- **URL:** https://pins.tbelbek.com
- **API Key:** `ak2_d606e...` (TOOLS.md'de tam)
- **Kullanım:** List, search, add bookmarks

---

## Doküman Yönetimi

### Paperless-ngx
- **URL:** https://paperless.tbelbek.com
- **Token:** `163a2ecc...` (TOOLS.md'de tam)
- **Kullanım:** Upload only (wrapper), read via curl

---

## Sosyal Medya

### Bird (Twitter/X CLI)
- **Auth:** `~/.bashrc`'de (AUTH_TOKEN, CT0)
- **Kritik Kural:** X linkleri için `bird read` kullan — `web_fetch` çalışmaz

---

## Trading ve Finans

### Simmer (Prediction Markets)
- **API Key:** `sk_live_967136...`
- **Agent ID:** `ddd9d417-8730-47cd-9bf5-40d8c6b08852`
- **Bakiye:** $10,000 SIM (virtual)
- **Limitler:** Max $100/trade, $500/günlük
- **Dashboard:** https://simmer.markets/dashboard
- **Durum:** ✅ Aktif (Simmer trading), ❌ Real USDC (claim gerekli)

### Stock News Edge Tracker
- **Lokasyon:** `~/.openclaw/skills/stock-news-tracker/`
- **Discord:** #trade (`1468680534921187369`)
- **Threshold:** Edge ≥ 6/10 → alert
- **Durum:** ✅ Production ready

---

## Browser Otomasyon

### OpenClaw Browser
- **Profil:** `openclaw` (ZORUNLU)
- ❌ Chrome extension relay (`profile="chrome"`) YASAK
- **Komutlar:**
  ```bash
  browser start --profile openclaw
  browser open --profile openclaw --url "..."
  browser snapshot --profile openclaw --targetId ...
  ```

---

## Video Üretimi

### Remotion
- **Lokasyon:** `~/.clawdbot/skills/remotion-server`
- **Eksik:** `libatk1.0-0`, `libgbm-dev`, vb. (sudo gerekiyor)
- **Templates:** chat, title

---

## Diğer Kurulu Skill'ler

| Skill | Durum | Notlar |
|-------|-------|--------|
| blogwatcher | ✅ Aktif | RSS takip, Discord'a digest |
| karakeep | ✅ Aktif | Bookmarks |
| paperless | ✅ Aktif | Dokümanlar (upload only) |
| bird | ✅ Aktif | Twitter/X CLI |
| simmer | ✅ Aktif | Paper trading |
| stock-news-tracker | ✅ Aktif | Finans haberleri |
| medium-blog-writer | ✅ Aktif | Blog otomasyonu |
| compound-engineering | ✅ Aktif | Nightly review |
| self-improvement | ✅ Aktif | Learning capture |
| proactive-agent | ✅ Aktif | Proaktif davranış |
| ontology | ✅ Aktif | Knowledge graph |
| para-second-brain | ✅ Aktif | PARA metodolojisi |
| markitdown | ✅ Aktif | PDF → Markdown |
| remotion-server | 🟡 Kurulu | Paketler eksik |
| humanizer | ✅ Aktif | AI text'i insanileştir |
| promptify | ✅ Aktif | Prompt optimizasyonu |
| skills-search | ✅ Aktif | Skill arama |
| crypto-trade-bot | ✅ Aktif | Paper trading bot |

---

## GitHub

**Obsidian Vault:** https://github.com/tbelbek/obsidian-vault (private)  
**Commit son:** `4598bdd` (21 Şubat 2026)

---

**Bu liste:** TOOLS.md'den derlenmiştir. Detaylar için oraya bak.

**Son Güncelleme:** 21 Şubat 2026
