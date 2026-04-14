# Multi-Agent Altyapı Kurulumu

---

## 1. Multi-Agent Altyapı Kurmak

### 1a. Claude Code Hesap Satın Alma

**Hangi plan?**
- **Pro ($20/ay):** Tek kişilik kullanım, 5 saatlik kayan limit, tüm modeller (Opus dahil)
- **Team ($30/kişi/ay):** Takım çalışması, paylaşılan proje bağlamı, admin kontrolü
- **Tavsiye:** Tek çalışıyorsan Pro yeterli. 2+ kişi → Team.

**Takım olarak çalışma:**
- Team planında her üye aynı projeye bağlanabilir
- Ortak `CLAUDE.md` dosyası proje kökünde — herkes aynı kuralları görür
- Her geliştirici kendi agent oturumunu açar, ama kurallar ortak

**CLAUDE.md ortaklaştırma ve güncel tutma:**
- `CLAUDE.md` Git'te versiyonlanır — PR ile güncellenir, herkes review eder
- **Haftalık 15dk "Claude Cowork" task'ı:** "Bu hafta öğrendiğimiz pattern'leri CLAUDE.md'ye ekle"
- **Her sprint sonunda:** Kuralları gözden geçir, eskiyen maddeleri kaldır
- **Kural:** CLAUDE.md değişikliği = code review gerektirir (çünkü tüm agent davranışını etkiler)

**CLAUDE.md nedir ve nasıl çalışır:**

Claude Code her çalıştırıldığında otomatik olarak bu dosyaları arar ve birleştirir:
1. `~/.claude/CLAUDE.md` — Global (tüm projeler için geçerli)
2. `<proje-kökü>/CLAUDE.md` — Proje seviyesi
3. `<alt-dizin>/CLAUDE.md` — Dizin seviyesi (o dizinde çalışırken eklenir)

Örnek CLAUDE.md:
```markdown
# Proje: Fiks ITSM-UI

## Stack
- Angular 16, Bootstrap + SCSS, NgModules
- Design tokens: src/app/design-system/tokens/design-tokens.scss
- Zardui component library: ../zardui/

## Kurallar
- Angular 16 uyumlu — Signals API KULLANMA
- Bootstrap + SCSS — Tailwind KULLANMA
- OnPush change detection zorunlu
- Hard-coded text KULLANMA — translate pipe kullan
- Constructor injection kullan, inject() değil

## Test
- npx ng build --configuration development
- npm start → http://localhost:8081
```

`/add-memory` komutuyla da ekleme yapılabilir — Claude öğrendiği şeyleri buraya kaydeder.

---

### 1b. Ollama Altyapısı ile İlerleyebilir miyiz?

**Kısa cevap:** Evet, ama kalite farkı var.

**Nasıl çalışır:**
- **Ollama** lokal makinede LLM çalıştırır (ücretsiz)
- **OpenClaude** Claude Code'un fork'u — Ollama'ya bağlanır, aynı arayüzü kullanır
- Sonuç: Claude Code deneyimi, ama arkada lokal model çalışır

**Kalite karşılaştırması:**

| Kriter | Claude API (Sonnet) | Ollama Lokal (32B) | Ollama Lokal (14B) |
|--------|--------------------|--------------------|---------------------|
| Kod kalitesi | Mükemmel | İyi (ufak hatalar olabilir) | Orta (basit işler OK) |
| Karmaşık refactor | Güçlü | Sınırlı | Yetersiz |
| Hız | Hızlı (cloud) | 10-20 token/sn (donanıma bağlı) | 15-25 token/sn |
| Maliyet | $3-15/M token | **Ücretsiz** | **Ücretsiz** |
| Context window | 200K | 8-32K (model bağlı) | 8-32K |

**Donanım gereksinimleri:**

| Seviye | Donanım | Model | Deneyim |
|--------|---------|-------|---------|
| **Minimum** | 16 GB RAM | 7B Q4 | Sadece tamamlama, agent için yetersiz |
| **İş görür** | 32 GB RAM veya M2 24GB | 14B Q4 | Basit component'ler OK |
| **Önerilen** | 48 GB+ Apple Silicon veya RTX 4090 | **32B Q4** | Günlük agent kullanımı |
| **İdeal** | 64 GB+ Apple Silicon veya 2×RTX 4090 | 70B Q4 | Cloud kalitesine yakın |

**Mevcut Mac'in için:**
- M1/M2 8GB → 7B, agent için yetersiz
- M1/M2 16GB → 14B, basit işler OK
- M3/M4 Max 36-48GB → **32B, sweet spot**
- M4 Ultra 128GB → 70B, cloud kalitesinde

**Tavsiye:** Hibrit yaklaşım.
- **Basit işler (tamamlama, refactor, basit component):** Ollama lokal — ücretsiz
- **Karmaşık işler (mimari, multi-file refactor, karmaşık form):** Claude API — kalite farkı belirgin
- **Gece/hafta sonu ağır işler:** Claude API yoğun olmayan saatlerde — daha ucuz

**Maliyet karşılaştırması:**

| Sağlayıcı | 1M Token Maliyeti | Karşılaştırma |
|-----------|-------------------|--------------|
| Claude Sonnet | $3-15 | Referans |
| DeepSeek-V3 | $0.27-1.10 | **%90 ucuz** |
| Gemini Flash | $0.10-0.40 | **%95 ucuz** |
| Ollama (lokal) | **$0** | **Ücretsiz** |

**OpenClaude — Lokal Claude Code Deneyimi:**

Claude Code'un herhangi bir LLM sağlayıcısıyla çalışan fork'u. OpenAI-uyumlu API shim'i ile Ollama, DeepSeek, GPT-4o, Gemini ve 200+ model destekliyor.

- **Link:** https://github.com/Gitlawb/openclaude
- **Kurulum:** `npm install -g @gitlawb/openclaude`
- **Desteklenen özellikler:** Tam araç desteği (Bash, dosya okuma/yazma, grep, glob, agent'lar, MCP), gerçek zamanlı token streaming, çoklu adımlı araç zincirleri, slash komutları (/commit, /review, /compact), alt-agent'lar, kalıcı bellek sistemi
- **Kısıtlamalar:** Extended thinking yok, Anthropic prompt caching yok, maks 32K token çıktı
- **En iyi modeller:** GPT-4o (mükemmel), DeepSeek-V3 (çok iyi), Qwen2.5-Coder 32B (iyi, lokal)

**Detaylı Donanım Gereksinimleri:**

Model bazlı bellek ihtiyacı (Q4 quantization):

| Model | Disk | RAM/VRAM | Kodlama Kalitesi |
|-------|------|----------|-----------------|
| Qwen2.5-Coder 7B | ~4.5 GB | ~6-7 GB | Tamamlama için iyi, agent için sınırlı |
| Qwen2.5-Coder 14B | ~9 GB | ~11-12 GB | Genel kodlama için güçlü |
| Codestral 22B (Mistral) | ~13 GB | ~15-16 GB | Python/JS'de güçlü |
| **Qwen2.5-Coder 32B** | **~20 GB** | **~22-24 GB** | **Bu segmentte en iyi açık kaynak** |
| Llama 3.3 70B | ~40 GB | ~44-48 GB | Mükemmel genel + kodlama |

Kural: Q4 quantization'da `(parametre_milyar × 0.5) + 2 GB` ≈ RAM ihtiyacı.

Apple Silicon performansı:

| Çip | Unified Memory | En İyi Model | Hız (token/sn) |
|-----|---------------|-------------|----------------|
| M1 (8 GB) | 8 GB | 7B Q4 | 8-12 |
| M1 Pro/Max (32 GB) | 32 GB | 14B Q5 veya 32B Q3 | 10-18 / 5-8 |
| M3 Max (36-48 GB) | 36-48 GB | 32B Q5 veya 70B Q3 | 15-22 / 8-14 |
| M4 Max (48-64 GB) | 48-64 GB | **70B Q4** | 8-12 |
| M4 Ultra (128-192 GB) | 128-192 GB | 70B Q6+ | 12-18 |

Apple Silicon avantajı: Unified memory = GPU tüm RAM'e erişebilir. 64 GB M4 Max, x86'da $1600'lık GPU gerektiren 70B modelini çalıştırabilir.

GPU performansı:

| GPU | VRAM | En İyi Model | Kullanım |
|-----|------|-------------|---------|
| RTX 4060 | 8 GB | 7B Q4 | Agent için yetersiz |
| RTX 4070 | 12 GB | 14B Q4 | Sınırlı agent |
| RTX 4080 | 16 GB | 14B Q5, 32B Q3 | İdare eder |
| **RTX 4090** | **24 GB** | **32B Q4-Q5** | **Lokal agent sweet spot** |
| RTX A6000 | 48 GB | 70B Q4 | Bulut kalitesine yakın |

CPU-only performansı:

| Model Boyutu | Yüksek-End CPU (DDR5) | Eski CPU (DDR4) |
|-------------|----------------------|-----------------|
| 7B | 15-25 token/sn | 8-15 token/sn |
| 14B | 8-15 token/sn | 4-8 token/sn |
| 32B | 3-7 token/sn | 1-4 token/sn |
| 70B | 1-4 token/sn | <1 token/sn |

CPU-only ile 14B'den büyük modellerde interaktif kullanım zor. Agent iş akışı için minimum 10+ token/sn gerekiyor.

---

### 1c. Agent'ları Oluşturma, Skill'leri Ekleme

**3 Agent yapısı (oluşturuldu ✅):**

```
┌─────────────────────────────────────────────────────────────┐
│                    UI MİMAR AGENT                            │
│     Figma/Gereksinimler → Component Spec, Tipler, Routing   │
│     Araçlar: Read, Glob, Grep, WebFetch (salt-okunur)        │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              ANGULAR GELİŞTİRİCİ AGENT (ITSM-UI)            │
│     Component Spec → Tam Angular 16 Kodu                     │
│     Zardui adaptasyonu, Bootstrap+SCSS, NgModules             │
│     Araçlar: Read, Write, Edit, Bash, Glob, Grep             │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                CI/CD & TEST AGENT                            │
│     Testler (Unit, Component, E2E) + GitHub Actions           │
│     Araçlar: Read, Write, Edit, Bash, Glob, Grep             │
└─────────────────────────────────────────────────────────────┘
```

**Neden 5 yerine 3 agent:** Template/Style/Logic ayrımı birleştirme çatışmalarına neden oluyordu. Tek geliştirici agent'ı tutarlı componentler yazıyor. QA yerine otomatik test yazan CI/CD agent'ı var.

**Agent dosyaları (mevcut):**
```
angular-agents/
├── AGENTS.md                        ← Orkestrasyon tablosu
├── ui-architect-agent/
│   ├── SOUL.md                      ← Kimlik, kurallar
│   └── AGENTS.md                    ← İş akışı, araçlar
├── angular-developer-agent/
│   ├── SOUL.md                      ← ITSM-UI spesifik pattern'ler
│   └── AGENTS.md                    ← Zardui dönüşüm tablosu
└── cicd-testing-agent/
    ├── SOUL.md                      ← TDD, Jest/Playwright
    └── AGENTS.md                    ← Pipeline template'leri
```

**Projeye nasıl uygulanır:**
```bash
# Agent config'leri projeye kopyala
mkdir -p .claude/agents .claude/commands
cp angular-agents/ui-architect-agent/AGENTS.md .claude/agents/ui-architect.md
cp angular-agents/angular-developer-agent/AGENTS.md .claude/agents/angular-developer.md
cp angular-agents/cicd-testing-agent/AGENTS.md .claude/agents/cicd-testing.md
```

**Slash komutları oluşturma:**
```
.claude/commands/
├── new-component.md     → /new-component [ComponentName]
├── run-tests.md         → /run-tests
└── review-code.md       → /review-code
```

Örnek `/new-component`:
```markdown
Yeni Angular component oluştur: $ARGUMENTS

1. Zardui'da karşılığını bul: ../zardui/libs/zard/src/lib/
2. ITSM-UI pattern'leriyle implement et (Bootstrap+SCSS, Angular 16)
3. shared-ui.module.ts'e ekle
4. Design token'ları güncelle
5. Test yaz
```

**Orkestrasyon — hangi durumda hangi agent:**

| Durum | Agent |
|-------|-------|
| Yeni UI feature / sayfa tasarımı | UI Mimar |
| Spec'ten component implement et | Angular Geliştirici |
| Mevcut component değiştir | Angular Geliştirici |
| Test yaz / düzelt | CI/CD & Test |
| Build hatası | CI/CD & Test |
| Pipeline kur / güncelle | CI/CD & Test |
| Mimari soru (implementation sırasında) | UI Mimar |

**Araç kısıtlamaları:**

| Agent | Read | Write | Edit | Bash | Web |
|-------|------|-------|------|------|-----|
| UI Mimar | ✅ | ❌ | ❌ | ❌ | ✅ |
| Angular Geliştirici | ✅ | ✅ | ✅ | ✅ | ❌ |
| CI/CD & Test | ✅ | ✅ | ✅ | ✅ | ❌ |

**Model seçimi:**

| Görev | Model | Neden |
|-------|-------|--------|
| Basit component | Haiku | Hızlı, ucuz |
| Karmaşık component (form, state) | Sonnet | Kalite gerekli |
| Mimari karar | Opus | Derin akıl yürütme |
| Basit test | Haiku | Pattern takibi |
| E2E / pipeline | Sonnet | Karmaşık setup |

**İş akışı (Faz 1-4):**

```
Faz 1: MİMARİ
└── Kullanıcı Figma tasarımını paylaşır veya gereksinimleri anlatır
    └── UI Mimar: component spec, tip tanımları, routing planı oluşturur

Faz 2: UYGULAMA
└── Angular Geliştirici tüm componentleri implement eder
    ├── Template'ler (Angular 16, *ngIf/*ngFor)
    ├── Stiller (Bootstrap + SCSS, design tokens)
    ├── Mantık (TypeScript, @Input/@Output, servisler, DI)
    ├── Formlar (Reactive forms, ControlValueAccessor)
    ├── İkonlar (Bootstrap Icons, iconMap güncellemesi)
    ├── Çeviriler (tr.ts / en.ts güncelleme)
    └── Module declarations (shared-ui.module.ts)

Faz 3: KALİTE
└── CI/CD & Test Agent
    ├── Unit testler (Jest/Karma)
    ├── Component testler (Angular Testing Library)
    ├── E2E testler (Playwright)
    ├── GitHub Actions workflow (lint → test → build)
    └── Kapsam raporu + kalite kararı

Faz 4: ÇIKTI
└── Üretime hazır Angular componentler + testler + CI pipeline
```

**Agent sorumlulukları detay:**

**UI Mimar Agent:**
- Figma tasarımlarını veya kullanıcı gereksinimlerini analiz et
- Diyagramlarla component hiyerarşisi oluştur
- Input/output'lar için TypeScript interface'leri tanımla
- State yönetimini planla (BehaviorSubject, servisler)
- Tasarım token'ları için Bootstrap/SCSS class'larını eşleştir
- Her component için erişilebilirlik gereksinimlerini belirle
- **Asla implementasyon kodu yazmaz**

**Angular Geliştirici Agent (ITSM-UI spesifik):**
- Zardui logic'ini ITSM-UI yapısına adapte et (Tailwind→Bootstrap, Signals→@Input/@Output)
- Tam Angular componentler yaz (template + stil + mantık)
- Bootstrap + SCSS + design tokens ile responsive tasarım
- ControlValueAccessor ile form kontrolleri
- Reactive forms + getXError() validasyon pattern'i
- Translation key'leri (tr.ts / en.ts)
- shared-ui.module.ts güncelleme
- Loading, hata ve boş durumlarını yönet

**CI/CD & Test Agent:**
- Unit testler yaz (component mantığı, servisler)
- Component testler yaz (render, kullanıcı etkileşimi)
- E2E testler yaz (kritik senaryolar için Playwright)
- GitHub Actions yapılandır (lint → test → build → deploy)
- Build hatalarını ve düzensiz testleri düzelt
- Pre-commit hook'ları kur (Husky + lint-staged)

**Claude Code Plugin Yapısı — Projeye Uygulama:**

```
Proje Kökü/
├── CLAUDE.md                    ← Proje bağlamı (stack, kurallar) — herkes tarafından okunur
├── AGENTS.md                    ← Agent kataloğu + orkestrasyon tablosu (opsiyonel)
├── .claude/
│   ├── agents/                  ← Agent config dosyaları
│   │   ├── ui-architect.md      ← Salt-okunur, tasarım analizi
│   │   ├── angular-developer.md ← Tam yetkili, kod yazımı
│   │   └── cicd-testing.md      ← Test + pipeline
│   └── commands/                ← Slash komutları
│       ├── new-component.md     → /new-component [Name]
│       ├── run-tests.md         → /run-tests
│       └── review-code.md       → /review-code
├── src/
│   └── app/
│       └── ...
├── angular.json
└── package.json
```

Agent dosyası formatı (YAML frontmatter + markdown gövde):
```markdown
---
name: angular-developer-itsm
description: ITSM-UI Angular 16 component implement eder. Use when...
tools: ["Read", "Write", "Edit", "Bash", "Glob", "Grep"]
model: sonnet
---

# Angular Developer Agent
Sen Angular 16 ile production-kalite component yazan geliştiricisin.
...
```

Frontmatter alanları:

| Alan | Zorunlu | Açıklama |
|------|---------|----------|
| `name` | Evet | Agent benzersiz adı |
| `description` | Evet | Ne zaman kullanılacağı — "Use when..." formatı |
| `tools` | Hayır | İzin verilen araçlar dizisi |
| `model` | Hayır | `haiku`, `sonnet`, `opus` |

Akış: `CLAUDE.md` proje kurallarını yükler → Agent routing tablosu duruma göre doğru agent'ı seçer → Agent'ın YAML frontmatter'ı araç/model kısıtlamalarını uygular → Slash komutları hızlı erişim sağlar.

---

### 1d. Lokal Setup — Adım Adım

#### Adım 1: Ollama Kur
```bash
# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.ai/install.sh | sh
```

#### Adım 2: Model İndir
```bash
# Donanıma göre seç:
ollama pull qwen2.5-coder:14b    # 32 GB RAM yetiyorsa
ollama pull qwen2.5-coder:32b    # 48 GB+ RAM varsa (önerilen)

# Sunucuyu başlat
ollama serve
```

#### Adım 3: OpenClaude Kur
```bash
npm install -g @gitlawb/openclaude
```

#### Adım 4: Proje Yapısını Hazırla
```bash
cd /path/to/fiks-ITSM-ui

# CLAUDE.md oluştur
cat > CLAUDE.md << 'EOF'
# Fiks ITSM-UI
Angular 16, Bootstrap+SCSS, NgModules, Design Tokens
Zardui referans: ../zardui/
NO Tailwind, NO Signals, NO standalone
EOF

# Agent config'lerini kopyala
mkdir -p .claude/agents .claude/commands
cp <bu-repo>/angular-agents/*/AGENTS.md .claude/agents/
```

#### Adım 5: Environment Ayarla
```bash
# Lokal Ollama ile
export CLAUDE_CODE_USE_OPENAI=1
export OPENAI_BASE_URL=http://localhost:11434/v1
export OPENAI_API_KEY=ollama
export OPENAI_MODEL=qwen2.5-coder:32b
```

#### Adım 6: Çalıştır
```bash
# Lokal model ile
openclaude

# veya orijinal Claude API ile
claude
```

#### Adım 7: Test Et
```
/new-component LoginForm
```
→ Mimar spec oluşturur → Geliştirici implement eder → Test agent testleri yazar

---

## 2. Token Yönetimi — Limitlere Takılmamak İçin

| # | Kural | Neden |
|---|-------|-------|
| 1 | **Prompt'u düzenle, yeni mesaj atma** | 31. mesaj 1.'den 31x pahalı. "Edit" ile düzelt. |
| 2 | **Her 15-20 mesajda yeni sohbet aç** | Token'ların %98.5'i geçmiş okumaya gidiyor. Özet çıkart → yeni chat. |
| 3 | **Soruları tek mesajda topla** | 3 ayrı mesaj = 3 ayrı context yüklemesi. |
| 4 | **Dosyaları Projects'e yükle** | Aynı dosya her sohbette yeniden tokenize olmasın. |
| 5 | **Memory/ayarları kullan** | "Samimi dil, kısa paragraf" gibi talimatları her sohbette yazma. |
| 6 | **Kullanmadığın özellikleri kapat** | Web arama, explore, Advanced Thinking — sadece gerekirse aç. |
| 7 | **Basit iş = Haiku, derin düşünme = Opus** | Model seçimi en önemli maliyet kararı. |
| 8 | **Gün içine yayarak kullan** | 5 saatlik kayan limit. Sabah/öğle/akşam böl. |
| 9 | **Yoğun saatler dışında kullan** | ABD sabahları (Avrupa öğleni) daha pahalı. |
| 10 | **Overage'ı güvenlik ağı olarak aç** | Limit bitince kullanım bazlı ödeme — aylık üst limit koy. |

**Maliyet büyümesi:**

| Mesaj | Token (ort. 500/mesaj) | Artış |
|-------|----------------------|-------|
| 5 | 7.5K | Normal |
| 10 | 27.5K | 3.7x |
| 20 | 105K | 14x |
| 30 | 232K | **31x** |

---

## 3. Referans Repolar

### agency-agents (msitarzewski)
**Link:** https://github.com/msitarzewski/agency-agents
- 55 agent, 9 bölüm, şirket yapısı
- Orkestratör pipeline: PM → Mimar → [Dev ↔ QA] → Entegrasyon
- Kalite kapıları + maks 3 retry + eskalasyon
- **Kullandığımız pattern:** Routing tablosu, araç kısıtlaması, fazlar arası geçiş

### everything-claude-code (affaan-m)
**Link:** https://github.com/affaan-m/everything-claude-code
- Dosya hiyerarşisi: SOUL.md → AGENTS.md → RULES.md → CLAUDE.md
- YAML frontmatter: name, description, tools, model
- TDD zorunlu, "When NOT to Use" routing
- **Kullandığımız pattern:** Agent dosya formatı, model katmanlama, araç kısıtlama

### Claude Code Resmi (Anthropic)
**Link:** https://github.com/anthropics/claude-code
- 7 fazlı workflow: Keşif → Tarama → Sorular → Tasarım → Uygulama → İnceleme → Özet
- Paralel agent başlatma, onay kapıları
- **Kullandığımız pattern:** Faz yapısı, paralel inceleme

### OpenClaude (Gitlawb)
**Link:** https://github.com/Gitlawb/openclaude
- Claude Code fork'u, herhangi bir LLM sağlayıcısı ile çalışır
- Ollama, DeepSeek, GPT-4o, Gemini, 200+ model desteği
- Tam araç desteği (Bash, dosya, grep, agent'lar, MCP)
- **Kısıtlamalar:** Extended thinking yok, prompt caching yok, maks 32K çıktı

---

## 4. Ek Araçlar

- **Lightpanda:** Chrome'dan 11x hızlı headless tarayıcı
- **Portless:** Localhost için isimli URL'ler
- **browser-whisper:** Tarayıcıda çevrimdışı konuşma-metin
- **awesome-openclaw-tips:** https://github.com/alvinreal/awesome-openclaw-tips
- **prompts.chat:** https://github.com/f/prompts.chat

---

*Etiketler: #multi-agent #angular #ui-development #figma #token-optimization #local-llm #claude-code #ollama #openclaude*
