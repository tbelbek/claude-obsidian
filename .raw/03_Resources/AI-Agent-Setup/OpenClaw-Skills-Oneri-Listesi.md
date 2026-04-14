# OpenClaw Skills — Öneri Listesi

**Kaynak:** VoltAgent/awesome-openclaw-skills (3,002 skill arasından filtrelenmiş)

---

## 🎯 En Öncelikli (Hemen Kurulmalı)

| Skill | Kategori | Açıklama |
|-------|----------|----------|
| `simmer-ai-divergence` | Trading | Mevcut Simmer kurulumunu genişletir — AI fiyat sapmalarını bulur |
| `telegram-ascii-table` | Communication | Telegram'da temiz tablo formatı (borsa/BRF verisi için) |
| `llm-supervisor-agent` | AI | Rate limit'te otomatik Ollama'ya geçiş — maliyet optimizasyonu |
| `content-recycler` | Media | Medium yazılarını Twitter/LinkedIn thread'e dönüştürür |
| `video-transcript-downloader` | Media | YouTube → transcript → Medium blog pipeline'ı |

---

## 📅 Takvim & E-posta

| Skill | Açıklama |
|-------|----------|
| `google-calendar` | GCal API entegrasyonu |
| `email-triage` | IMAP + AI sınıflandırma (mevcut email monitor'u güçlendirir) |
| `morning-email-rollup` | Sabah e-posta özeti |
| `email-to-calendar` | E-postadan otomatik takvim etkinliği çıkarma |
| `calendly` | Scheduling entegrasyonu |

---

## 🔍 Araştırma & AI

| Skill | Açıklama |
|-------|----------|
| `perplexity` | Daha güçlü web araştırması (borsa, gayrimenkul için) |
| `gemini-deep-research` | Derinlemesine tarama (BRF analizi, piyasa araştırması) |
| `ollama-local` | Hassas işler için yerel LLM (Linux uyumlu) |
| `xai` / `search-x` | Grok ile gerçek zamanlı X/Twitter araması |

---

## 💰 Finans & Trading

| Skill | Açıklama |
|-------|----------|
| `yahoo-data-fetcher` | Gerçek zamanlı hisse fiyatları |
| `ceorater` | S&P 500 CEO analitikleri (borsa edge'i) |
| `sharesight-skill` | Portföy takibi |
| `ynab` | Bütçe yönetimi |
| `expense-tracker-pro` | Doğal dil ile harcama takibi |

---

## 💬 İletişim

| Skill | Açıklama |
|-------|----------|
| `whatsapp-ultimate` | Tam WhatsApp entegrasyonu (medya, ses, FTS5 arama) |
| `bird-dms` | X/Twitter DM'lerini oku (mevcut bird eklentisi) |
| `twitter-bookmark-sync` | Kayıtlı tweetleri düzenle (bird tamamlayıcısı) |
| `linkedin-cli` | LinkedIn CLI (network/iş için) |

---

## 💻 Geliştirme & Otomasyon

| Skill | Açıklama |
|-------|----------|
| `gitai-skill` | AI destekli commit mesajı + PR özeti |
| `container-debug` | Docker container debug |
| `context-checkpoint` | Konuşma durumunu kaydet (context sıkışmadan önce) |
| `supabase` | Backend/database (Hemnet tracker / BRF checker için) |
| `n8n` | Self-hosted workflow otomasyonu |
| `diagram-generator` | Mimari/sistem diyagramları |

---

## 📺 İçerik & Medya

| Skill | Açıklama |
|-------|----------|
| `tubescribe` / `tldw` | YouTube video özetleri |
| `spotify-web-api` | Spotify kontrolü |
| `content-recycler` | İçerik dönüştürme (cross-platform) |

---

## 📝 Notlar & PKM

| Skill | Açıklama |
|-------|----------|
| `obsidian` | Obsidian vault'ları ile çalışma (✅ Zaten kurulu) |
| `readwise` | Okuma özetlerini PKM'e entegre et |
| `hn-digest` | Hacker News özeti (AI/LLM haberleri) |
| `knowledge-base` | SQLite + FTS5 yerel bilgi tabanı |

---

## 📄 Doküman & PDF

| Skill | Açıklama |
|-------|----------|
| `nano-pdf` | PDF düzenleme (paperless-ngx'i tamamlar) |
| `mineru-pdf` | Yerel PDF → Markdown (cloud yok) |
| `excel` | .xlsx okuma/yazma (BRF finansal tabloları) |
| `docx` | Rapor oluşturma (BRF health checker için) |
| `invoice-generator` | JSON'dan profesyonel PDF fatura |

---

## 🚌 İsveç'e Özel

| Skill | Açıklama |
|-------|----------|
| `skanetrafiken` | Skåne toplu taşıma planlayıcı |
| `vasttrafik` / `wheels-router` | Göteborg toplu taşıma |

---

## Kurulum Komutu

```bash
npx clawhub@latest install <skill-slug>
```

**Önerilen Sıra:**
1. `simmer-ai-divergence`
2. `telegram-ascii-table`
3. `llm-supervisor-agent`
4. `content-recycler`
5. `video-transcript-downloader`

---

**Liste Tarihi:** 21 Şubat 2026  
**Toplam Öneri:** ~45 skill
