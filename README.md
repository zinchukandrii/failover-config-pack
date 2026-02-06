# 🛡️ Failover Config Pack V2.0

## Zawartość:

### 1. `agents-config.json`
Konfiguracja agentów z fallback cascade:
- Primary: claude-opus-4-5-thinking
- 12 modeli fallback w 4 warstwach
- Timeout: 60 sekund
- maxConcurrent: 4 agents, 8 subagents

### 2. `TOOLS.md`
Manual probe commands - jak sprawdzić czy model żyje

### 3. `HEARTBEAT.md`
Dashboard statusu modeli - auto-aktualizowany

## Instalacja w OpenBot:

```bash
# 1. Merge agents config
cat agents-config.json  # skopiuj do swojego clawdbot.json

# 2. Skopiuj TOOLS.md do workspace
cp TOOLS.md ~/your-workspace/

# 3. Skopiuj HEARTBEAT.md do workspace
cp HEARTBEAT.md ~/your-workspace/
```

## Cron Job (ręcznie dodaj):
```
Name: model-health-probe
Schedule: */30 * * * *
Text: 🔬 MODEL HEALTH CHECK: Spawn sub-agents to verify TIER 1...
```
