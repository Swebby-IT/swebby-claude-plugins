# /review — Lancia una fase di verifica e review

Devi orchestrare una review del lavoro svolto. NON fare review tu stesso.

## Cosa verificare

$ARGUMENTS

## Istruzioni

1. **NON leggere codice, eseguire test o analizzare file** — delega ai Researcher
2. Identifica cosa va verificato:
   - Correttezza funzionale
   - Aderenza ai requisiti originali
   - Qualità del codice e best practice
   - Test e copertura
   - Regressioni
   - Sicurezza (se applicabile)
3. Lancia 1-2 Researcher Sonnet con brief mirati:
   - **Missione**: cosa verificare esattamente
   - **Input**: file/path da esaminare, requisiti originali
   - **Output atteso**: report strutturato PASS/FAIL per ogni punto
   - **Formato risposta**: RISULTATO → PROBLEMI → SUGGERIMENTI
4. Se emergono problemi:
   - Classifica gravità (BLOCKER / WARNING / INFO)
   - Per i BLOCKER → lancia Developer per fix specifico
   - Per i WARNING → segnala all'utente
5. Report finale:

```
📊 REVIEW REPORT
━━━━━━━━━━━━━━
✅ PASS: [lista punti ok]
⚠️ WARNING: [lista warning]
🔴 BLOCKER: [lista blocker + azioni correttive]
```

Procedi.
