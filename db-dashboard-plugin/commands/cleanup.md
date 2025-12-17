---
description: Elimina report e dashboard vecchi, mantenendo gli ultimi N (default 5)
argument-hint: [numero_da_mantenere] default 5
allowed-tools: Read, Bash
---

# Cleanup Report Vecchi

Elimina i report e dashboard più vecchi, mantenendo solo gli ultimi N.

## Parametri

- Numero report da mantenere: `$ARGUMENTS` (default: 5)

## Azioni

1. **Conta i file** nella directory `output/`:
   ```bash
   ls -1 output/*.json output/*.html 2>/dev/null | wc -l
   ```

2. **Se ci sono più file del limite**:
   - Ordina per data (più vecchi prima)
   - Calcola quanti eliminare
   - Chiedi conferma all'utente
   - Elimina i file più vecchi

3. **Comando per eliminare**:
   ```bash
   # Elimina i report JSON più vecchi (mantieni ultimi N)
   ls -1t output/report_*.json 2>/dev/null | tail -n +$((N+1)) | xargs -r rm
   
   # Elimina le dashboard HTML più vecchie (mantieni ultime N)
   ls -1t output/dashboard_*.html 2>/dev/null | tail -n +$((N+1)) | xargs -r rm
   ```

4. **Report finale**:
   - Quanti file eliminati
   - Quanti file rimasti
   - Spazio liberato

## Conferma

Prima di eliminare, mostra:
```
⚠️  Stai per eliminare X file:
- report_20240101_120000.json
- dashboard_20240101_120000.html
- ...

Vuoi procedere? (I file non potranno essere recuperati)
```

Procedi SOLO dopo conferma esplicita dell'utente.
