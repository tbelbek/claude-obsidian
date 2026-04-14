# MCP Servers — İlginç Olanlar

**Kaynak:** davepoon/buildwithclaude (4,500+ MCP server)

**Not:** Bu server'lar Claude Code/Desktop için hazırlanmış. OpenClaw'da `mcporter` skill'i ile kullanılabilirliği test edilmeli.

---

## 🔍 Araştırma & Web

| Server | Kategori | Açıklama |
|--------|----------|----------|
| `brave-search` | API | Web arama (alternatif) |
| `exa` | Web Search | Web search + crawling |
| `arxiv-mcp-server` | AI Task | Akademik araştırma, arXiv paper'ları |
| `firecrawl` | AI Task | Güçlü web scraping ve arama |
| `dappier` | Web Search | Gerçek zamanlı web + premium data |
| `duckduckgo` | AI Task | Web search (alternatif) |

---

## 💾 Veritabanı & Storage

| Server | Kategori | Açıklama |
|--------|----------|----------|
| `chroma` | AI Task | Vector database (embeddings için) |
| `couchbase` | Database | Doküman DB + search |
| `clickhouse` | Database | Analitik database |
| `astra-db` | Database | Astra DB workloads |
| `elasticsearch` | AI Task | Elasticsearch indeksleri |

---

## ☁️ Cloud & DevOps

| Server | Kategori | Açıklama |
|--------|----------|----------|
| `docker` | AI Task | Docker kontrolü |
| `dockerhub` | Cloud Infra | Docker Hub entegrasyonu |
| `github` | Dev Tools | GitHub API (zaten gh CLI var) |
| `gitlab` | Dev Tools | GitLab API |
| `aws-cdk-mcp-server` | Cloud Infra | AWS CDK best practices |
| `aws-terraform` | Cloud Infra | Terraform on AWS |
| `azure` | Cloud Infra | Azure MCP |
| `grafana` | Dev Tools | Monitoring dashboard |
| `kubernetes` | Cloud Infra | K8s yönetimi |

---

## 🛠️ Developer Tools

| Server | Kategori | Açıklama |
|--------|----------|----------|
| `e2b` | AI Task | Kod çalıştırma sandbox |
| `desktop-commander` | AI Task | Terminal komutları + dosya yönetimi |
| `ast-grep` | Web Search | Kod yapısal arama/değiştirme |
| `git` | Dev Tools | Git repo otomasyonu |

---

## 🎯 AI & Üretim

| Server | Kategori | Açıklama |
|--------|----------|----------|
| `elevenlabs` | AI Task | Ses/TTS (TTS var mı kontrol et) |
| `glif` | AI Task | AI workflow'ları (image gen) |
| `everart` | API | Image generation |
| `openai` | AI Task | OpenAI API entegrasyonu |

---

## 📊 Productivity & Data

| Server | Kategori | Açıklama |
|--------|----------|----------|
| `airtable-mcp-server` | AI Task | Airtable entegrasyonu |
| `atlassian` | API | Jira + Confluence |
| `basic-memory` | AI Task | Bilgi yönetimi sistemi |
| `fetch` | Productivity | URL → markdown (web_fetch alternatifi) |
| `gdrive` | File System | Google Drive entegrasyonu |
| `filesystem` | File System | Yerel dosya sistemi erişimi |

---

## 🔧 API & Integration

| Server | Kategori | Açıklama |
|--------|----------|----------|
| `api-gateway` | AI Task | Herhangi bir API'yi MCP'ye dönüştürme |
| `apify-mcp-server` | Browser | Web scraping, data extraction |
| `brave-search` | API | Brave Search API |
| `box` | API | Box API entegrasyonu |

---

## Test Edilecekler

OpenClaw'da `mcporter` ile test edilmeye değer:

1. `filesystem` — Yerel dosya erişimi
2. `fetch` — Web'den veri çekme
3. `github` — GitHub otomasyonu (gh CLI alternatifi)
4. `chroma` — Vektör DB (semantic search için)
5. `airtable-mcp-server` — Eğer Airtable kullanıyorsan

---

## Kurulum

Claude Code için:
```bash
# settings.json'a ekle
{
  "mcpServers": {
    "server-name": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "mcp/server-name"]
    }
  }
}
```

OpenClaw için `mcporter` skill dokümantasyonuna bak.

---

**Liste Tarihi:** 21 Şubat 2026
