# Sistem Yapılandırması ve Ayarlar

**Ortam:** Linux (Ubuntu), Göteborg/Sweden  
**Workspace:** `/home/tughan/clawd`  
**Oturum Başlangıcı:** 26 Ocak 2026

---

## Model Yönetimi

| Model | Kullanım Alanı | Durum |
|-------|----------------|-------|
| **Claude Sonnet 4-6** | Karmaşık işler, kod, analiz | ✅ Ana model |
| **Kimi-coding/k2p5** | Blog araştırması, trend alert | ✅ Aktif |
| **Haiku** | Email/WhatsApp monitor, heartbeat | ✅ Izole cron |
| **Codex 5.1 Mini** | Rate limit fallback | ✅ Yedek |

**Not:** Kimi.com aboneliği aktif, Moonshot devre dışı.

---

## Önemli Konfigürasyonlar

### Gmail
- **Durum:** Read-only erişim (`gmail-readonly`)
- **Yetki:** Sadece okuma, taslak oluşturma YOK
- **Kanal:** Discord 1467854105207902429 (önemli mailler için)
- **Not:** Yazma yetkisi için yeniden yetkilendirme gerekli

### Environment Variables

**Karakeep (Bookmarks):**
```bash
KARAKEEP_URL="https://pins.tbelbek.com"
KARAKEEP_API_KEY="ak2_d606e..."
```

**Paperless-ngx:**
```bash
PAPERLESS_URL="https://paperless.tbelbek.com"
PAPERLESS_TOKEN="163a2ecc..."
```

**Bird (Twitter):**
```bash
AUTH_TOKEN=~/.bashrc'de
CT0=~/.bashrc'de
```

**Simmer:**
```bash
SIMMER_API_KEY="sk_live_967136..."
Agent ID: ddd9d417...
```

---

## Cron İşleri (Otomatik)

| İş | ID | Sıklık | Model | Açıklama |
|----|----|--------|-------|----------|
| compound-nightly | `ff06117a` | 22:30 | — | Günlük review |
| blog-morning-briefing | `0e51264c` | 09:00 | — | 5 trend konu |
| blog-trend-alert | `31e7d5d2` | Her 30 dk | — | Patlayan trend alarm |
| email-monitor | — | Her 30 dk | Haiku | Gmail izleme |
| whatsapp-monitor | — | Her 30 dk | Haiku | WhatsApp izleme |

---

## Prompt Caching Best Practice

Claude Code ekibinden öğrenilen: **static first, dynamic last**

- Prompt'ta sabit içerik (system prompt, docs) → başa koy
- Değişen içerik (user input, tool results) → sona koy
- Tool tanımlarını değiştirmek = cache miss

---

## Skill Değerlendirme Kriterleri

1. **Gerçek ihtiyaç var mı?** — mevcut workflow'da gap var mı
2. **Kurulum karmaşıklığı** — harici CLI / ücretli API gerektiriyor mu
3. **Redundant mı?** — zaten var olan bir araç bunu kapıyor mu
4. **Net utility**

**Atılanlar:** byterover, agent-browser, deep-research, process-watch, news-aggregator, auto-updater

---

## İletişim Tercihleri

- **Format:** Kısa, öz, sarkastik
- **Dil:** Türkçe veya İngilizce
- **Platform:** Telegram (primary), Discord (notifications)

---

## Güvenlik Notları

- WhatsApp/email/message göndermeden önce ONAY al
- Göster: recipient, content, bekle onay
- `trash` > `rm` (recoverable beats gone forever)

---

**Son Güncelleme:** 21 Şubat 2026
