# Review ve Vault Bakım Süreci

**Amaç:** Token verimliliği için düzenli içerik toplama ve organizasyon

---

## 🔄 Review Zamanlaması

**Frekans:** Her oturum sonunda (veya günde bir kez)  
**Süre:** ~5-10 dakika  
**Araç:** AI Assistant + Obsidian vault

---

## 📋 Review Adımları

### 1. Yeni Konuları Tespit Et
- Oturumdaki yeni konuşmaları gözden geçir
- Hangileri kalıcı değer taşıyor?
- Kategori belirle: Proje / Area / Resource / Inbox

### 2. Mevcut Notları Güncelle
- Var olan notlarla çakışan/ilişkili bilgi var mı?
- Ekleme mi, değiştirme mi gerekli?
- `INDEX.md`'de son güncelleme tarihini değiştir

### 3. Yeni Not Oluştur (Gerekirse)
- PARA yapısına uygun klasör seç
- Dosya adı: `Konu-Basligi-YYYY-MM-DD.md` formatında
- Başlık, tarih, özet bilgileri ekle

### 4. Index'i Güncelle
- `INDEX.md`'e yeni notu ekle
- Durum sembolünü belirle (🟡/✅/🟠/🔴)
- Son güncelleme tarihini güncelle

### 5. Git Commit + Push
```bash
cd ~/obsidian-vaults
git add .
git commit -m "Update: [kısa açıklama]"
git push
```

---

## 📝 Not Şablonları

### Proje Notu
```markdown
# [Proje Adı]

**Durum:** 🟡 Aktif / ✅ Tamam / 🟠 Eksik  
**Başlangıç:** [Tarih]  
**Lokasyon:** `/path/to/project/`

## Amaç
[Brief açıklama]

## Özellikler
- [özellik 1]
- [özellik 2]

## Durum
| Metrik | Değer |
|--------|-------|
| [Metrik] | [Değer] |

## Notlar
[Önemli notlar]

## TODO
- [ ] [Görev 1]
- [ ] [Görev 2]
```

### Area Notu (Sorumluluk Alanı)
```markdown
# [Alan Adı]

**Son Güncelleme:** [Tarih]

## Özet
[Kısa özet]

## Detaylar
[Detaylar]

## İlişkili Projeler
- [[Proje-Linki]]
```

### Resource Notu (Kaynak)
```markdown
# [Kaynak Adı]

**Kaynak:** [URL/Dosya]  
**Tarih:** [Ekleme tarihi]

## Özet
[Kısa açıklama]

## Detaylar
[Liste, tablo, vs.]

## Kullanım
[Nasıl kullanılır]
```

---

## 🏷️ Kategori Rehberi

**01_Projects/** → Aktif projeler, somut çıktıları olan işler
- Kod projeleri
- Automation sistemleri
- Trading botlar

**02_Areas/** → Sürekli sorumluluklar, bakım gerektiren alanlar
- Finans (gelir, yatırım, bütçe)
- Kariyer
- Sağlık

**03_Resources/** → Referans materyaller, araştırmalar
- OpenClaw skills
- MCP servers
- Araç karşılaştırmaları
- Sistem yapılandırmaları

**04_Archive/** → Tamamlanmış, pasif durumdaki projeler
- Eski versiyonlar
- İptal edilmiş projeler

**05_Knowledge_Base/** → Kalıcı bilgiler, evergreen notlar
- Nasıl yapılır rehberleri
- Konsept açıklamaları

**99_Inbox/** → Günlük loglar, hızlı capture
- Günlük oturum özetleri
- Geçici notlar

---

## ⚡ Hızlı Karar Ağacı

```
Yeni konu mu?
├── Evet → Proje mi?
│         ├── Evet → 01_Projects/
│         └── Hayır → Area mı?
│                   ├── Evet → 02_Areas/
│                   └── Hayır → Resource mı?
│                             ├── Evet → 03_Resources/
│                             └── Hayır → 99_Inbox/
└── Hayır → Mevcut notu güncelle
```

---

## 📊 Token Verimliliği İpuçları

✅ **Yap:**
- Özetleri INDEX.md'de tut, detaylar ayrı dosyalarda
- Cross-link kullan: `[[Dosya-Adi]]`
- Tablolar kullan (görsel, az token)
- Durum sembolleri ile hızlı scan

❌ **Yapma:**
- Her detayı AI'ye tekrarlatma
- Tekrar eden bilgileri çoğalt
- Uzun metinleri tek dosyada biriktir

---

**Süreç Başlangıç:** 21 Şubat 2026  
**Son Güncelleme:** 21 Şubat 2026
