---
title: "Sürekli Unuttuğun Şeyleri Otomatikleştiren 8 Claude Code Hook'u - Direk Claude a Verebilirsin"
source: "https://x.com/Techburhan/status/2040869682912297196"
author:
  - "[[@Techburhan]]"
published: 2026-04-05
created: 2026-04-07
description: "Muhtemelen denk gelmişsindir: Claude Code’a bir şey söylüyorsun ama bazen kendi kafasına göre takılıyor.“Kodu formatla” diyorsun, yok. “Şu..."
tags:
  - "clippings"
---
Muhtemelen denk gelmişsindir: Claude Code’a bir şey söylüyorsun ama bazen kendi kafasına göre takılıyor. “Kodu formatla” diyorsun, yok. “Şu dosyaya dokunma” diyorsun, gidip yine dokunuyor. “Bitirmeden önce testleri çalıştır” diyorsun, onu da es geçiyor.

İlk başta garip geliyor ama sebebi aslında basit: CLAUDE.md bir kural değil, öneri. Okuyor, çoğu zaman da uyuyor ama garanti değil.

Hook’lar ise tamamen farklı çalışıyor.

Claude bir dosyayı değiştirdiğinde, bir komut çalıştırdığında ya da işi bitirdiğinde otomatik tetiklenen şeyler bunlar. Yani “belki yapar” değil — direkt yapıyor.

Ben de bir noktadan sonra şunu fark ettim:

yazdığım hiçbir şey %100 çalışmıyor, ama hook yazınca konu kapanıyor.

O yüzden aşağıya, direkt settings.json’a koyup bir daha uğraşmayacağın 8 hook bırakıyorum 👇 👇

Başlamadan önce — AI ve kodlama üzerine günlük notlarımı topluluğumda paylaşıyorum: [https://www.skool.com/doa](https://www.skool.com/doa)

\## Hook'lar Nasıl Çalışır (30 Saniyede)

\*\*Hook nedir?\*\*

```text
{
  "hooks": {
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/auto-commit.sh"
          }
        ]
      }
    ]
  }
}
```

Hook'lar, Claude Code bir şey yaptığında — mesela bir dosyayı düzenlediğinde veya bir komut çalıştırdığında — her seferinde otomatik olarak çalışan aksiyonlardır. Bir kez kurarsın ve arka planda sen düşünmeden çalışırlar.

\*\*En çok kullanacağın ikisi:\*\*

\*\*PreToolUse\*\* — Claude bir şey yapmadan önce çalışır. Aksiyonu inceleyebilir ve exit code 2 döndürerek engelleyebilirsin. Bir kapıdaki bouncer gibi düşün.

\*\*PostToolUse\*\* — Claude bir şey yaptıktan sonra çalışır. Temizlik, formatlama, test veya loglama yapabilirsin. Üretim hattındaki kalite kontrol gibi düşün.

\*\*Hook'lar nerede bulunur:\*\*

\`\`\`

.claude/settings.json proje seviyesi (git ile paylaşılır)

~/.claude/settings.json kullanıcı seviyesi (tüm projeler)

.claude/settings.local.json sadece yerel (commit edilmez)

\`\`\`

Proje kökünde \`.claude/settings.json\` içinde yapılandırırsın. Bu dosya git'e commit edilir, yani tüm ekibin aynı hook'ları otomatik olarak alır.

Dokümantasyon: [https://code.claude.com/docs/en/hooks](https://code.claude.com/docs/en/hooks)

\## 1. Claude'un Dokunduğu Her Dosyayı Otomatik Formatla

\*\*Problem:\*\* Claude doğru kod yazar ama formatlama kurallarını bozar. CLAUDE.md'ye "her zaman Prettier çalıştır" eklersin ve çoğu zaman çalışır, ama her zaman değil.

\*\*Hook:\*\* Prettier her dosya yazma veya düzenleme işleminden sonra otomatik olarak çalışır.

```text
json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path' | xargs npx prettier --write 2>/dev/null; exit 0"
          }
        ]
      }
    ]
  }
}
```

"hooks":

```text
{
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path' | xargs npx prettier --write 2>/dev/null; exit 0"
          }
        ]
      }
    ]
  }
}
```

\`\`\`

\`npx prettier --write\` yerine kullandığın formatter'ı koy: Python için \`black\`, Go için \`gofmt\`, Rust için \`rustfmt\`. Kalıp aynı.

Bu kurduğum ilk hook'tu ve dürüst olarak her proje için varsayılan olması gerekiyor. Artık "Claude formatlamayı unuttu" commit'leri yok.

\## 2. Tehlikeli Komutları Engelle

\*\*Problem:\*\* Claude \`rm -rf\`, \`git reset --hard\`, \`DROP TABLE\` veya rastgele URL'lere \`curl\` çalıştırabilecek kadar güçlü. Muhtemelen yapmaz, ama üretim veritabanın söz konusu olduğunda "muhtemelen" yeterli değil.

\*\*Hook:\*\* Yıkıcı komutları çalıştırılmadan önce engelle.

\`.claude/hooks/block-dangerous.sh\` dosyasını oluştur:

\`\`\`bash

#!/usr/bin/env bash

set -euo pipefail

cmd=$(jq -r '.tool\_input.command // ""')

dangerous\_patterns=(

"rm -rf"

"git reset --hard"

"git push.\*--force"

"DROP TABLE"

"DROP DATABASE"

"curl.\*|.\*sh"

"wget.\*|.\*bash"

)

for pattern in "${dangerous\_patterns\[@\]}"; do

if echo "$cmd" | grep -qiE "$pattern"; then

echo "Engellendi: '$cmd' tehlikeli kalıp '$pattern' ile eşleştirildi. Daha güvenli bir alternatif öner." >&2

exit 2

fi

done

exit 0

\`\`\`

Sonra \`settings.json\` dosyana ekle:

```text
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/block-dangerous.sh"
          }
        ]
      }
    ]
  }
}
```

\`\`\`

Exit code 2 burada anahtar. Aksiyonu engeller ve hata mesajını Claude'a geri gönderir, böylece daha güvenli bir yaklaşım deneyebilir. Exit code 0 "devam et" demek. Başka herhangi bir şey uyarı loglar ama engellemez.

\## 3. Hassas Dosyaları Düzenlemelerden Koru

\*\*Problem:\*\* Claude projedeki herhangi bir dosyayı okuyup düzenleyebilir. Buna \`.env\`, \`package-lock.json\`, config dosyaları ve dokunmasını tercih etmediğin her şey dahil.

\*\*Hook:\*\* Dokunulmaz olması gereken dosyalara yapılan düzenlemeleri engelle.

\`.claude/hooks/protect-files.sh\` dosyasını oluştur:

\`\`\`bash

#!/usr/bin/env bash

set -euo pipefail

file=$(jq -r '.tool\_input.file\_path // .tool\_input.path // ""')

protected=(

".env\*"

".git/\*"

"package-lock.json"

"yarn.lock"

"\*.pem"

"\*.key"

"secrets/\*"

)

for pattern in "${protected\[@\]}"; do

if echo "$file" | grep -qiE "^${pattern//\\\*/.\*}$"; then

echo "Engellendi: '$file' koruma altında. Bu düzenlemenin neden gerekli olduğunu açıkla." >&2

exit 2

fi

done

exit 0

\`\`\`

\`\`\`json

```text
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/protect-files.sh"
          }
        ]
      }
    ]
  }
}
```

\`\`\`

\## 4. Her Düzenlemeden Sonra Testleri Çalıştır

\*\*Problem:\*\* Claude bir değişiklik yapar, "tamam" der ve sen 20 dakika sonra commit etmeye çalıştığında testlerin kırılmış olduğunu keşfedersin.

\*\*Hook:\*\* Her kod değişikliğinden sonra test suite'ini otomatik çalıştır. Testler başarısız olursa Claude hatayı görür ve hemen düzeltebilir.

\`\`\`json

```text
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "npm run test --silent 2>&1 | tail -5; exit 0"
          }
        ]
      }
    ]
  }
}
```

\`\`\`

\`tail -5\` çıktıyı kısa tutar, Claude'un context'ini doldurmaz. Claude'un 200 satırlık tam test çıktısını değil, "3 test başarısız" mesajını görmesini istiyorsun.

Claude Code'un yaratıcısı Boris Cherny, Claude'a böyle bir geri bildirim döngüsü vermenin çıktı kalitesini 2-3 kat artırdığını söylüyor. Kod yazıp çalışmasını ummak yerine, Claude kod yazar, test sonuçlarını görür ve hataları kendi başına düzeltir.

\## 5. PR Oluşturmadan Önce Geçen Testleri Zorunlu Kıl

\*\*Problem:\*\* Claude bir özelliği bitirir ve hemen PR oluşturur. Testler başarısız. Reviewer kırmızı CI görür ve geri gönderir.

\*\*Hook:\*\* Tüm testler geçmedikçe PR oluşturmayı engelle.

\`.claude/hooks/require-tests-for-pr.sh\` dosyasını oluştur:

\`\`\`bash

#!/usr/bin/env bash

set -euo pipefail

if npm run test --silent; then

exit 0

else

echo "Testler başarısız. PR oluşturmadan önce tüm test hatalarını düzelt." >&2

exit 2

fi

\`\`\`

\`\`\`json

```text
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "mcp__github__create_pull_request",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/require-tests-for-pr.sh"
          }
        ]
      }
    ]
  }
}
```

\`\`\`

Bu sert bir kapıdır. Yeşil testler yoksa PR yok. Claude önce hataları düzeltecek çünkü exit code 2 aksiyonun engellendiğini ve nedenini bildirir.

\## 6. Otomatik Lint ve Hata Raporlama

\*\*Problem:\*\* Claude çalışan ama ESLint kurallarını, stil kılavuzunu veya tip kontrollerini ihlal eden kod yazar. Review sırasında yakalanır ve geri gönderirsin.

\*\*Hook:\*\* Her düzenlemeden sonra lint çalıştır. Lint başarısız olursa Claude hataları görür ve sen koda bakmadan önce düzeltir.

\`\`\`json

```text
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "npx eslint --fix $(jq -r '.tool_input.file_path') 2>&1 | tail -10; exit 0"
          }
        ]
      }
    ]
  }
}
```

\`\`\`

Bunu 1 numaradaki otomatik formatlama hook'u ile zincirleyebilirsin. Prettier önce çalışır, sonra ESLint. Sen kodu gördüğünde formatlanmış ve lint-temiz olur.

\## 7. Claude'un Çalıştırdığı Her Komutu Logla

\*\*Problem:\*\* Claude bir oturum sırasında bir sürü shell komutu çalıştırır. Bir şeyler ters giderse ne yaptığını ve ne zaman yaptığını tam olarak bilmek istersin.

\*\*Hook:\*\* Her Bash komutunu zaman damgalarıyla bir log dosyasına ekle.

\`.claude/hooks/log-commands.sh\` dosyasını oluştur:

\`\`\`bash

#!/usr/bin/env bash

set -euo pipefail

cmd=$(jq -r '.tool\_input.command // ""')

printf '%s %s\\n' "$(date -Is)" "$cmd" >> .claude/command-log.txt

exit 0

\`\`\`

\`\`\`json

```text
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/log-commands.sh"
          }
        ]
      }
    ]
  }
}
```

\`\`\`

Artık Claude'un çalıştırdığı her komutun zaman damgalı bir denetim izi var. \`.claude/command-log.txt\` dosyasını \`.gitignore\`'una ekle ki repoyu kirletmesin.

Bu özellikle hata ayıklama için faydalı: Claude üç oturum önce bir şeyi bozduysa, loga bakıp tam olarak ne zaman ve ne çalıştırdığını bulabilirsin.

\## 8. Tamamlanan Her Görevden Sonra Otomatik Commit

\*\*Problem:\*\* Claude bir görevi bitirir ve sen commit etmeyi unutursun. Sonra başka bir göreve başlar ve şimdi iki ilgisiz değişiklik tek bir commit'te karışık halde olur.

\*\*Hook:\*\* Claude bir görev üzerinde çalışmayı bitirdiğinde tüm değişiklikleri otomatik olarak commit et.

\`.claude/hooks/auto-commit.sh\` dosyasını oluştur:

\`\`\`bash

#!/usr/bin/env bash

set -euo pipefail

git add -A

if ! git diff --cached --quiet; then

git commit -m "chore(ai): Claude düzenlemesi uygulandı"

fi

exit 0

\`\`\`

Claude her yanıt vermeyi bitirdiğinde değişiklikler otomatik olarak commit edilir. Git geçmişin günün sonunda tek bir devasa "Claude değişiklikleri" bloğu yerine görev başına atomik commit'lerle temiz kalır.

Bunu \`claude -w feature-branch\` (worktree) özelliğiyle birleştir ve her görev için izole, otomatik commit edilen feature branch'lerin olsun.

\## Komple settings.json

İşte her şeyin tek bir dosyada birleştirilmiş hali. Bu dosyayı \`.claude/settings.json\` içine kopyala, hook scriptlerini \`.claude/hooks/\` altında oluştur, \`chmod +x .claude/hooks/\*.sh\` ile çalıştırma izni ver ve her şeyi git'e commit et. Tüm ekibin aynı güvenlik ağlarını otomatik olarak alır.

\`\`\`json

```text
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          { "type": "command", "command": ".claude/hooks/block-dangerous.sh" },
          { "type": "command", "command": ".claude/hooks/log-commands.sh" }
        ]
      },
      {
        "matcher": "Edit|Write",
        "hooks": [
          { "type": "command", "command": ".claude/hooks/protect-files.sh" }
        ]
      },
      {
        "matcher": "mcp__github__create_pull_request",
        "hooks": [
          { "type": "command", "command": ".claude/hooks/require-tests-for-pr.sh" }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          { "type": "command", "command": "jq -r '.tool_input.file_path' | xargs npx prettier --write 2>/dev/null; exit 0" },
          { "type": "command", "command": "npx eslint --fix $(jq -r '.tool_input.file_path') 2>&1 | tail -10; exit 0" }
        ]
      }
    ],
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          { "type": "command", "command": ".claude/hooks/auto-commit.sh" }
        ]
      }
    ]
  }
}
```

\`\`\`

İyi bir Claude Code kurulumu ile muhteşem bir Claude Code kurulumu arasındaki fark model veya prompt'lar değil. Hook'lardır. Sen dikkat etmezken çalışan, code review sırasında yoksa daha kötüsü üretimde bulacağın hataları yakalayan kısımdır.

Bugün 1 numarayı (otomatik formatlama) ve 2 numarayı (tehlikeli komutları engelle) kur. Bu tek başına en yaygın Claude Code hatalarından seni kurtaracak. Geri kalanını ihtiyaç duydukça ekle.

AI ve otomasyon üzerine günlük notlarımı topluluğumda paylaşıyorum: [https://www.skool.com/doa](https://www.skool.com/doa)

Okuduğun için teşekkürler 🙏🏼

\*Burhan Kocabıyık\*