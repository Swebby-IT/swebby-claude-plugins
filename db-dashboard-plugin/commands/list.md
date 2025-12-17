---
description: Lista tutti i report e dashboard generati, con opzione per aprire o eliminare
allowed-tools: Read, Bash
---

# Lista Report Generati

Mostra tutti i report e dashboard generati dal plugin.

## Azioni

1. **Lista file in `output/`**:
   ```bash
   ls -la output/ 2>/dev/null || echo "Nessun report trovato"
   ```

2. **Per ogni file trovato**, mostra:
   - Nome file
   - Data creazione
   - Dimensione
   - Tipo (report JSON / dashboard HTML)

3. **Formatta l'output** in una tabella leggibile:

   ```
   ╔══════════════════════════════════════════════════════════════╗
   ║                    Report Generati                           ║
   ╠══════════════════════════════════════════════════════════════╣
   ║  #  │ Tipo      │ Data       │ Dimensione │ File             ║
   ╠═════╪═══════════╪════════════╪════════════╪══════════════════╣
   ║  1  │ Report    │ 2024-01-15 │ 12.5 KB    │ report_xxx.json  ║
   ║  2  │ Dashboard │ 2024-01-15 │ 45.2 KB    │ dashboard_xxx.html║
   ╚══════════════════════════════════════════════════════════════╝
   ```

4. **Suggerisci azioni**:
   - Per aprire una dashboard: `open output/dashboard_xxx.html` (macOS) o `xdg-open` (Linux)
   - Per eliminare vecchi report: `/db-dashboard:cleanup`

## Se la directory è vuota

Messaggio: "Nessun report generato. Usa `/db-dashboard:dashboard <richiesta>` per crearne uno."
