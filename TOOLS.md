# TOOLS.md - Local Notes

Skills define *how* tools work. This file is for *your* specifics — the stuff that's unique to your setup.

---

## 🔬 Model Health Probe (Manual)

Użyj tego przed ważną operacją lub gdy podejrzewasz martwy model:

### Quick Probe (pojedynczy model)
```
/spawn task="Odpowiedz tylko: ALIVE" model=google-antigravity/gemini-3-pro-high
```

### Full TIER 1 Probe
```
/spawn task="Odpowiedz: ALIVE + nazwa modelu" model=google-antigravity/claude-opus-4-5-thinking
/spawn task="Odpowiedz: ALIVE + nazwa modelu" model=google-antigravity/gemini-3-pro-high
/spawn task="Odpowiedz: ALIVE + nazwa modelu" model=copilot-proxy/claude-opus-4.5
/spawn task="Odpowiedz: ALIVE + nazwa modelu" model=openai-codex/gpt-5.2
```

### Interpretacja wyników:
- ✅ `ALIVE` w <30s = Model działa
- ⚠️ Timeout/brak odpowiedzi = Model MARTWY → użyj fallback
- ❌ Błąd 429/401 = Rate limit/Auth problem

---

## 🛡️ Emergency Failover Commands

Jeśli obecny model nie odpowiada:
```
/model google-antigravity/claude-sonnet-4-5-thinking
/model copilot-proxy/claude-opus-4.5
/model openai-codex/gpt-5.2
```

---

## 📊 Model Status Check

Sprawdź aktualny model i providery:
```
/model status
/models
```

---

## What Goes Here

Things like:
- Camera names and locations
- SSH hosts and aliases  
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras
- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH
- home-server → 192.168.1.100, user: admin

### TTS
- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.
