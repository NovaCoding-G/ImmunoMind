"""Testi Wiki in-app. © G.Roscino / NovaCoding."""

WIKI_SECTIONS = [
    {
        "title": "Cos’è ImmunoMind",
        "paragraphs": [
            "ImmunoMind è un simulatore didattico (modello semplificato) che visualizza come patogeni e sistema immunitario possono interagire nel tempo.",
            "Non è un software medico né un modello clinico: lo scopo è capire concetti e dinamiche (innata vs adattativa, carica patogena, farmaci, anticorpi, feedback sull’ambiente).",
            "Le regole sono intenzionalmente semplici: invece di riprodurre ogni dettaglio biologico, il simulatore usa probabilità, soglie e parametri globali per mostrare cause/effetti in modo chiaro.",
        ],
    },
    {
        "title": "Come leggere lo schermo",
        "paragraphs": [
            "Area di simulazione (sinistra): vedi cellule e patogeni muoversi, inseguirsi e interagire. Il click aggiunge patogeni (batteri o virus in base allo scenario).",
            "HUD (destra): riepiloga conteggi (popolazioni), ambiente (temperatura/ossigeno), farmaci e anticorpi. Ti dà anche un indicatore sintetico dello stato dell’infezione.",
            "Tutorial iniziale: quando avvii una simulazione, appare una guida breve a step. Puoi tornare alla Home con ESC.",
        ],
    },
    {
        "title": "Scenari disponibili",
        "paragraphs": [
            "Batterica: rappresenta un’infezione batterica (E. coli) con risposta innata forte; l’antibiotico (penicillina) aumenta la probabilità di eliminazione dei batteri.",
            "Virale: rappresenta un’infezione virale (influenza, modello semplificato). Gli antibiotici non funzionano; gli antivirali riducono replicazione/sopravvivenza virale.",
            "Vaccino / Memoria: parte con anticorpi già presenti e una risposta adattativa più rapida; utile per confrontare i tempi di controllo dell’infezione.",
            "Ferita / Infiammazione: aumenta i segnali infiammatori (semplificati) e modifica l’ambiente; utile per vedere come l’infiammazione cambia la dinamica.",
        ],
    },
    {
        "title": "Gravità (cosa cambia davvero)",
        "paragraphs": [
            "La gravità aumenta la carica iniziale (e/o la pressione dell’infezione) rendendo più difficile il controllo con la sola innata.",
            "A gravità alta, potresti vedere crescita più rapida dei patogeni e maggiore febbre: nel modello è un effetto “macroscopico” legato al numero di patogeni.",
            "Usa la gravità per fare esperimenti: stessa strategia (farmaco/tempo) su gravità diversa e confronta l’andamento nel tempo.",
        ],
    },
    {
        "title": "Entità nella simulazione (chi fa cosa)",
        "paragraphs": [
            "Globuli rossi: elementi di sfondo e movimento; non eliminano patogeni ma aiutano a percepire il “flusso”.",
            "Neutrofili: prima linea dell’immunità innata. Nel simulatore inseguono patogeni e li eliminano con regole semplificate di fagocitosi.",
            "Macrofagi: fagociti residenti. Nel modello contribuiscono alla rimozione e possono agire come supporto contro patogeni (anche virus, in modo semplificato).",
            "Linfociti T: parte dell’adattativa. Entrano più tardi (dopo un tempo di attivazione) e migliorano la clearance, soprattutto nello scenario virale.",
            "Linfociti B: parte dell’adattativa. Nel modello aumentano la produzione di anticorpi (che potenziano l’eliminazione dei patogeni).",
            "Batteri e virus: patogeni che possono duplicarsi finché non vengono eliminati o finché il sistema immunitario non li controlla.",
        ],
    },
    {
        "title": "Immunità innata vs adattativa",
        "paragraphs": [
            "Innata: risposta rapida e non specifica. Neutrofili e macrofagi intervengono subito; è efficace nelle fasi iniziali, ma può essere sopraffatta da cariche alte o replicazione rapida.",
            "Adattativa: risposta più lenta all’inizio ma più potente e specifica. Linfociti T/B e anticorpi aumentano l’efficacia nel tempo.",
            "Nel simulatore l’adattativa si attiva dopo una soglia temporale: in alcuni scenari (vaccino) questa soglia è ridotta per imitare la memoria immunitaria.",
        ],
    },
    {
        "title": "Fagocitosi (nel simulatore)",
        "paragraphs": [
            "La fagocitosi è rappresentata come un processo semplificato: un fagocita rileva patogeni vicini, li insegue e li elimina con probabilità/condizioni definite dal modello.",
            "Nella realtà entrano molti fattori (recettori, opsonine, complemento, microambiente). Qui è riassunto per far emergere il concetto: più ‘difensori’ e più segnali → più eliminazione.",
        ],
    },
    {
        "title": "Anticorpi (opsonizzazione semplificata)",
        "paragraphs": [
            "Gli anticorpi nel simulatore aumentano l’efficacia globale contro patogeni: più anticorpi → maggiore probabilità di eliminazione (sia batteri che virus, con fattori diversi).",
            "Nel mondo reale gli anticorpi possono neutralizzare virus, opsonizzare batteri, attivare complemento e facilitare fagocitosi. Qui è tutto compattato in un singolo effetto quantitativo.",
        ],
    },
    {
        "title": "Temperatura / febbre (ambiente)",
        "paragraphs": [
            "La temperatura rappresenta un indicatore di infiammazione: cresce con la carica patogena e tende a rientrare quando l’infezione viene controllata.",
            "È una semplificazione: nella realtà la febbre dipende da citochine (es. IL‑1, IL‑6, TNF), prostaglandine e regolazione centrale.",
        ],
    },
    {
        "title": "Farmaci nel simulatore (modello didattico)",
        "paragraphs": [
            "Penicillina (antibiotico): nel modello aumenta la probabilità che i batteri muoiano nel tempo. Concetto chiave: funziona sui batteri, non sui virus.",
            "Oseltamivir (antivirale): nel modello riduce la sopravvivenza/replicazione dei virus. Concetto chiave: gli antivirali agiscono su passaggi della replicazione virale.",
            "Aciclovir (antivirale didattico): nel modello è un ulteriore effetto antivirale semplificato (non rappresenta spettro e farmacologia reale).",
            "Nota: qui non c’è farmacocinetica clinica completa (assorbimento/distribuzione/eliminazione reali). Serve per sperimentare: dose → concentrazione → efficacia.",
        ],
    },
    {
        "title": "Controlli (cosa puoi fare)",
        "paragraphs": [
            "Click nell’area di simulazione: aggiunge patogeni (batteri o virus in base allo scenario).",
            "SPAZIO: pausa.  ESC: torna alla Home.  R: reset simulazione.",
            "+ / - : velocità simulazione.",
            "1: penicillina, 2: oseltamivir, 3: aciclovir.",
            "E: esporta dati in CSV (se sono disponibili dati sufficienti).",
        ],
    },
    {
        "title": "Dati ed esportazione (CSV)",
        "paragraphs": [
            "Il simulatore può registrare statistiche nel tempo (popolazioni, ambiente, farmaci, anticorpi) e salvarle in CSV.",
            "Usa l’esportazione per confrontare esperimenti: ad esempio ‘stesso scenario’ con/ senza farmaco, oppure gravità 1 vs 5.",
            "Interpretazione consigliata: osserva trend (patogeni che salgono/scendono, temperatura che segue l’infezione, anticorpi che crescono nella fase adattativa).",
        ],
    },
    {
        "title": "Limiti del modello (importante)",
        "paragraphs": [
            "Non rappresenta: varianti patogene reali, resistenze antibiotiche realistiche, recettori specifici, tessuti e organi dettagliati, immunopatologie, e molti meccanismi molecolari.",
            "È pensato come ‘laboratorio visivo’ per concetti: se vedi qualcosa di strano, spesso è una conseguenza della semplificazione.",
            "Se vuoi, alcune estensioni possibili sono: resistenza, immunità più specifica, distretti/tessuti, e parametri regolabili da UI.",
        ],
    },
    {
        "title": "Crediti",
        "paragraphs": [
            "ImmunoMind è un progetto educativo sviluppato da G.Roscino per NovaCoding.",
            "Il software è distribuito a scopo didattico. Codice e contenuti sono di proprietà di G.Roscino / NovaCoding.",
        ],
    },
]

