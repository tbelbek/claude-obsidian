# Multi-Agent Altyapı Kurulumu

[[_TOC_]]

---

## 1. Multi-Agent Altyapı Kurmak

### 1a. Claude Code Hesap Satın Alma

**Hangi plan?**

| Plan | Fiyat | Özellikler | Ne zaman |
|------|-------|-----------|----------|
| Pro | $20/ay | Tek kişi, 5 saatlik limit, Opus dahil | Tek çalışıyorsan |
| Team | $30/kişi/ay | Takım, paylaşılan bağlam, admin | 2+ kişi |

**Takım olarak çalışma:**
- Team planında her üye aynı projeye bağlanabilir
- Ortak `CLAUDE.md` dosyası proje kökünde — herkes aynı kuralları görür
- Her geliştirici kendi agent oturumunu açar, ama kurallar ortak

**CLAUDE.md ortaklaştırma ve güncel tutma (alternatif - best practise: plugin oluşturma -> 1c bölümünde):**
- `CLAUDE.md` Git'te versiyonlanır — PR ile güncellenir, herkes review eder
- **Haftalık 15dk "Claude Cowork" task'ı:** "Bu hafta öğrendiğimiz pattern'leri CLAUDE.md'ye ekle"
- **Her sprint sonunda:** Kuralları gözden geçir, eskiyen maddeleri kaldır
- **Kural:** CLAUDE.md değişikliği = code review gerektirir (çünkü tüm agent davranışını etkiler)

**CLAUDE.md nedir ve nasıl çalışır:**

Claude Code her çalıştırıldığında otomatik olarak bu dosyaları arar ve birleştirir:

1. `~/.claude/CLAUDE.md` — Global (tüm projeler için geçerli)
2. `<proje-kökü>/CLAUDE.md` — Proje seviyesi
3. `<alt-dizin>/CLAUDE.md` — Dizin seviyesi (o dizinde çalışırken eklenir)

**Örnek CLAUDE.md:**

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
| Kod kalitesi | Mükemmel | İyi (ufak hatalar) | Orta (basit işler OK) |
| Karmaşık refactor | Güçlü | Sınırlı | Yetersiz |
| Hız | Hızlı (cloud) | 10-20 token/sn | 15-25 token/sn |
| Maliyet | $3-15/M token | **Ücretsiz** | **Ücretsiz** |
| Context window | 200K | 8-32K | 8-32K |

**Donanım gereksinimleri:**

| Seviye | Donanım | Model | Deneyim |
|--------|---------|-------|---------|
| Minimum | 16 GB RAM | 7B Q4 | Sadece tamamlama, agent için yetersiz |
| İş görür | 32 GB RAM / M2 24GB | 14B Q4 | Basit component'ler OK |
| **Önerilen** | 48 GB+ Apple Silicon / RTX 4090 | **32B Q4** | Günlük agent kullanımı |
| İdeal | 64 GB+ Apple Silicon / 2xRTX 4090 | 70B Q4 | Cloud kalitesine yakın |

**Tavsiye: Hibrit yaklaşım**
- Basit işler (tamamlama, refactor, basit component) :arrow_right: Ollama lokal — ücretsiz
- Karmaşık işler (mimari, multi-file refactor, karmaşık form) :arrow_right: Claude API
- Gece/hafta sonu ağır işler :arrow_right: Claude API yoğun olmayan saatlerde

**OpenClaude — Lokal Claude Code Deneyimi:**
- **Link:** [github.com/Gitlawb/openclaude](https://github.com/Gitlawb/openclaude)
- **Kurulum:** `npm install -g @gitlawb/openclaude`
- **Desteklenen:** Tam araç desteği (Bash, dosya, grep, agent'lar, MCP), streaming, slash komutları, alt-agent'lar, kalıcı bellek
- **Kısıtlamalar:** Extended thinking yok, prompt caching yok, maks 32K çıktı
- **En iyi modeller:** GPT-4o (mükemmel), DeepSeek-V3 (çok iyi), Qwen2.5-Coder 32B (iyi, lokal)

**Detaylı Donanım Gereksinimleri:**

| Model | Disk | RAM/VRAM | Kodlama Kalitesi |
|-------|------|----------|-----------------|
| Qwen2.5-Coder 7B | ~4.5 GB | ~6-7 GB | Tamamlama iyi, agent sınırlı |
| Qwen2.5-Coder 14B | ~9 GB | ~11-12 GB | Genel kodlama güçlü |
| Codestral 22B | ~13 GB | ~15-16 GB | Python/JS güçlü |
| **Qwen2.5-Coder 32B** | **~20 GB** | **~22-24 GB** | **En iyi açık kaynak** |
| Llama 3.3 70B | ~40 GB | ~44-48 GB | Mükemmel genel + kodlama |

Kural: Q4'de `(parametre_milyar x 0.5) + 2 GB` = yaklaşık RAM ihtiyacı.

**Apple Silicon:**

| Çip | Memory | En İyi Model | Hız |
|-----|--------|-------------|-----|
| M1 (8 GB) | 8 GB | 7B Q4 | 8-12 t/s |
| M1 Pro/Max (32 GB) | 32 GB | 14B Q5 / 32B Q3 | 10-18 / 5-8 |
| M3 Max (36-48 GB) | 36-48 GB | 32B Q5 / 70B Q3 | 15-22 / 8-14 |
| M4 Max (48-64 GB) | 48-64 GB | **70B Q4** | 8-12 |

**GPU:**

| GPU | VRAM | Model | Kullanım |
|-----|------|-------|---------|
| RTX 4060 | 8 GB | 7B | Yetersiz |
| RTX 4070 | 12 GB | 14B | Sınırlı |
| **RTX 4090** | **24 GB** | **32B Q4** | **Sweet spot** |
| RTX A6000 | 48 GB | 70B Q4 | Cloud kalitesi |

**CPU-only:**

| Boyut | DDR5 | DDR4 |
|-------|------|------|
| 7B | 15-25 t/s | 8-15 t/s |
| 14B | 8-15 t/s | 4-8 t/s |
| 32B | 3-7 t/s | 1-4 t/s |
| 70B | 1-4 t/s | <1 t/s |

**Maliyet karşılaştırması:**

| Sağlayıcı | 1M Token | vs Claude |
|-----------|----------|-----------|
| Claude Sonnet | $3-15 | Referans |
| DeepSeek-V3 | $0.27-1.10 | %90 ucuz |
| Gemini Flash | $0.10-0.40 | %95 ucuz |
| Ollama (lokal) | **$0** | **Ücretsiz** |

---

### 1c. Agent'ları Oluşturma, Skill'leri Ekleme

**3 Agent yapısı:**

```
┌─────────────────────────────────────────────────────┐
│                 UI MİMAR AGENT                       │
│   Figma → Component Spec, Tipler, Routing            │
│   Araçlar: Read, Glob, Grep, WebFetch (salt-okunur)  │
└─────────────────────┬───────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────┐
│           ANGULAR GELİŞTİRİCİ AGENT (ITSM-UI)       │
│   Component Spec → Tam Angular 16 Kodu                │
│   Zardui adaptasyonu, Bootstrap+SCSS, NgModules       │
│   Araçlar: Read, Write, Edit, Bash, Glob, Grep        │
└─────────────────────┬───────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────┐
│              CI/CD & TEST AGENT                      │
│   Unit + Component + E2E Testler + GitHub Actions     │
│   Araçlar: Read, Write, Edit, Bash, Glob, Grep        │
└─────────────────────────────────────────────────────┘
```

**Neden 5 yerine 3 agent:** Template/Style/Logic ayrımı birleştirme çatışmalarına neden oluyordu. Tek geliştirici agent'ı tutarlı componentler yazıyor. QA yerine otomatik test yazan CI/CD agent'ı var.

**Agent dosyaları:**

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

**Projeye uygulama:**

```bash
# Agent config'leri projeye kopyala
mkdir -p .claude/agents .claude/commands
cp angular-agents/ui-architect-agent/AGENTS.md .claude/agents/ui-architect.md
cp angular-agents/angular-developer-agent/AGENTS.md .claude/agents/angular-developer.md
cp angular-agents/cicd-testing-agent/AGENTS.md .claude/agents/cicd-testing.md
```

**Slash komutları:**

```
.claude/commands/
├── new-component.md     → /new-component [ComponentName]
├── run-tests.md         → /run-tests
└── review-code.md       → /review-code
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
| UI Mimar | :white_check_mark: | :x: | :x: | :x: | :white_check_mark: |
| Angular Geliştirici | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :x: |
| CI/CD & Test | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :x: |

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
└── Kullanıcı Figma tasarımını paylaşır
    └── UI Mimar: component spec, tip tanımları, routing planı

Faz 2: UYGULAMA
└── Angular Geliştirici tüm componentleri implement eder
    ├── Template (Angular 16, *ngIf/*ngFor)
    ├── Stil (Bootstrap + SCSS, design tokens)
    ├── Mantık (TypeScript, @Input/@Output, servisler)
    ├── Formlar (Reactive forms, ControlValueAccessor)
    ├── İkonlar (Bootstrap Icons, iconMap)
    ├── Çeviriler (tr.ts / en.ts)
    └── Module declarations (shared-ui.module.ts)

Faz 3: KALİTE
└── CI/CD & Test Agent
    ├── Unit testler (Jest/Karma)
    ├── Component testler (Angular Testing Library)
    ├── E2E testler (Playwright)
    ├── GitHub Actions (lint → test → build)
    └── Kapsam raporu + kalite kararı

Faz 4: ÇIKTI
└── Üretime hazır componentler + testler + CI pipeline
```

**Agent sorumlulukları:**

| Agent | Sorumluluklar |
|-------|--------------|
| **UI Mimar** | Figma analizi, component hiyerarşisi, TypeScript interface, state planı, a11y gereksinimleri. **Kod yazmaz.** |
| **Angular Geliştirici** | Zardui adaptasyonu, Bootstrap+SCSS, Angular 16 component, ControlValueAccessor, Reactive forms, çeviriler, module güncelleme |
| **CI/CD & Test** | Unit/component/E2E test, GitHub Actions, build hata düzeltme, Husky+lint-staged, kapsam izleme |

**Claude Code Plugin Yapısı:**

```
Proje Kökü/
├── CLAUDE.md                    ← Proje bağlamı (stack, kurallar)
├── .claude/
│   ├── agents/                  ← Agent config dosyaları
│   │   ├── ui-architect.md
│   │   ├── angular-developer.md
│   │   └── cicd-testing.md
│   └── commands/                ← Slash komutları
│       ├── new-component.md     → /new-component
│       ├── run-tests.md         → /run-tests
│       └── review-code.md       → /review-code
```

Agent dosya formatı (YAML frontmatter):
```yaml
---
name: angular-developer-itsm
description: ITSM-UI Angular 16 component implement eder
tools: ["Read", "Write", "Edit", "Bash", "Glob", "Grep"]
model: sonnet
---
```

| Alan | Zorunlu | Açıklama |
|------|---------|----------|
| name | Evet | Agent benzersiz adı |
| description | Evet | Ne zaman kullanılacağı |
| tools | Hayır | İzin verilen araçlar |
| model | Hayır | haiku / sonnet / opus |

---

### 1d. Lokal Setup — Adım Adım

**Adım 1: Ollama Kur**
```bash
# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.ai/install.sh | sh
```

**Adım 2: Model İndir**
```bash
ollama pull qwen2.5-coder:14b    # 32 GB RAM yetiyorsa
ollama pull qwen2.5-coder:32b    # 48 GB+ RAM varsa (önerilen)
ollama serve
```

**Adım 3: OpenClaude Kur**
```bash
npm install -g @gitlawb/openclaude
```

**Adım 4: Proje Yapısını Hazırla**
```bash
cd /path/to/fiks-ITSM-ui

cat > CLAUDE.md << 'EOF'
# Fiks ITSM-UI
Angular 16, Bootstrap+SCSS, NgModules, Design Tokens
Zardui referans: ../zardui/
NO Tailwind, NO Signals, NO standalone
EOF

mkdir -p .claude/agents .claude/commands
cp <agent-repo>/angular-agents/*/AGENTS.md .claude/agents/
```

**Adım 5: Environment Ayarla**
```bash
export CLAUDE_CODE_USE_OPENAI=1
export OPENAI_BASE_URL=http://localhost:11434/v1
export OPENAI_API_KEY=ollama
export OPENAI_MODEL=qwen2.5-coder:32b
```

**Adım 6: Çalıştır ve Test Et**
```bash
openclaude            # lokal model ile
# veya
claude                # orijinal Claude API ile

# Test:
/new-component LoginForm
```

---

## 2. Token Yönetimi

| # | Kural | Neden |
|---|-------|-------|
| 1 | **Prompt'u düzenle, yeni mesaj atma** | 31. mesaj 1.'den 31x pahalı. "Edit" ile düzelt. |
| 2 | **Her 15-20 mesajda yeni sohbet aç** | Token'ların %98.5'i geçmiş okumaya gidiyor. |
| 3 | **Soruları tek mesajda topla** | 3 ayrı mesaj = 3 ayrı context yüklemesi. |
| 4 | **Dosyaları Projects'e yükle** | Her sohbette yeniden tokenize olmasın. |
| 5 | **Memory/ayarları kullan** | Talimatları her sohbette tekrar yazma. |
| 6 | **Kullanmadığın özellikleri kapat** | Web arama, explore — sadece gerekirse aç. |
| 7 | **Basit iş = Haiku, derin = Opus** | Model seçimi en önemli maliyet kararı. |
| 8 | **Gün içine yayarak kullan** | 5 saatlik kayan limit. 3 oturuma böl. |
| 9 | **Yoğun saatler dışında kullan** | ABD sabahları daha pahalı. |
| 10 | **Overage'ı güvenlik ağı olarak aç** | Limit bitince kullanım bazlı ödeme. |

**Token maliyet büyümesi:**

| Mesaj | Token | Artış |
|-------|-------|-------|
| 5 | 7.5K | Normal |
| 10 | 27.5K | 3.7x |
| 20 | 105K | 14x |
| 30 | 232K | **31x** |

---

## 3. Referans Repolar

| Repo | Link | Kullandığımız Pattern |
|------|------|----------------------|
| agency-agents | [GitHub](https://github.com/msitarzewski/agency-agents) | Routing tablosu, araç kısıtlaması, fazlar arası geçiş |
| everything-claude-code | [GitHub](https://github.com/affaan-m/everything-claude-code) | Agent dosya formatı, model katmanlama, YAML frontmatter |
| Claude Code Resmi | [GitHub](https://github.com/anthropics/claude-code) | Faz yapısı, paralel inceleme, onay kapıları |
| OpenClaude | [GitHub](https://github.com/Gitlawb/openclaude) | Lokal LLM desteği, Ollama bağlantısı, 200+ model |

---

## 4. Ek Araçlar

| Araç | Açıklama |
|------|----------|
| Lightpanda | Chrome'dan 11x hızlı headless tarayıcı |
| Portless | Localhost için isimli URL'ler |
| browser-whisper | Tarayıcıda çevrimdışı konuşma-metin |
| awesome-openclaw-tips | [GitHub](https://github.com/alvinreal/awesome-openclaw-tips) |
| prompts.chat | [GitHub](https://github.com/f/prompts.chat) |
