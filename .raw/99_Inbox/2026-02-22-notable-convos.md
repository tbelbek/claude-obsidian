# 2026-02-22 - Önemli Konuşmalar

- **Repo ayrımı**: `clawd` workspace istisnasız <https://github.com/tbelbek/clawd-workspace>'da tutuluyor; PARA notları ve referans dosyalar (HEARTBEAT, SOUL, TOOLS) artık yalnızca `obsidian-vault` kapsamında. Clawd içindeki filesın güncel halini remote'a push ettim.
- **Heartbeat/Soul/Tools**: Bu üç file clawd içinde kalacak şekilde ayarlandı; obsidian vault'tan kaldırıldı. Vault artık sadece not/knowledge base içeriyor.
- **Compound/Memory**: `compound-engineering` skill’i ve onun nightly cron’u .openclaw/skills dizininde yerli. Bellek (memory) distilasyonu bu skill üzerinden çalışıyor.
- **Vault’un temizliği**: Backups/logs gibi agent dosyaları clawd workspace’te kalmalı, obsidian vault’tan silindi. Vault’ta yalnızca PARA dizinleri, knowledge base notları ve index/README kaldı.

_Sunu unutma: Vault, notların arşivi; clawd ise çalıştırılabilir altyapı._

## Discord #finans – Kanal Özetleri

- **Discord → Obsidian entegrasyon fikri**  
  - #finans kanalındaki önemli konuşmaların Obsidian PARA yapısına otomatik düşmesi istendi.  
  - Hedef: Kanaldaki strateji/karar/plan içeren mesajlar “önemli” olarak filtrelenip uygun vault dosyalarına append edilecek.  
  - Önerilen skill: `discord-to-obsidian-finans` → son X mesajı okuyup önemli görülenleri Obsidian’a şu formatta yazacak:  
    - `## YYYY-MM-DD` altında timestamp + kullanıcı + kısa özet.

- **“Önemli konuşma” kriteri (taslak)**  
  - İçerik tipi: trade/finans stratejisi, plan, karar, net rakamlı hesaplama, sistem tanımı.  
  - Örnek sinyaller: `#not`, `#edge`, `#plan`, `TODO`, ⭐ gibi etiketler veya “bunu unutmayalım / bunu not al” cümleleri.  
  - İlk aşamada: manuel seçilmiş önemli mesajlar üzerinden gidilecek; sonrasında keyword/etiket tabanlı otomasyon.

- **Bird / Twitter skill durumu**  
  - `twitter-growth` skill’i aktif, arka planda `bird` CLI kullanıyor.  
  - Bird kurulu ve çalışır durumda, ancak X/Twitter için auth cookie (auth_token, ct0) gerekli.  
  - Şu anda: cookie otomatik okunamıyor; çözüm olarak tarayıcıdan X’e login + cookie’leri manuel/export ederek bird’e vermek planlandı.

- **Skills ve workspace envanter notları**  
  - Lokal skill dizini: `~/.openclaw/skills/` altında compound-engineering, humanizer, markitdown, medium-blog-writer, twitter-growth, stock-news-tracker vb.  
  - Global OpenClaw skilleri: `~/.npm-global/lib/node_modules/openclaw/skills/` altında (ör: `discord` skill’i).  
  - `clawd` workspace → aktif projeler, scriptler ve agent config;  
    Obsidian vault → PARA yapısında uzun vadeli not/knowledge base.

_Not: 21 Şubat’ta BoKlok/Vänskapen mortgage tartışmalarından çıkan karar ve hesaplamalar zaten `01_Projects/BoKlok-Vanskapen/` altına ayrı dosyalar olarak işlenmiş durumda; bu yüzden burada tekrar edilmedi._
