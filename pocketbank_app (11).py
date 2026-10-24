import webview

HTML_CODE = """
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PocketBank</title>
    <style>
        * {
            box-sizing: border-box;
            user-select: none;
            -webkit-user-select: none;
        }
        body {
            background-color: #0b0f19;
            color: white;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            margin: 0;
            padding: 20px;
            display: flex;
            justify-content: center;
            align-items: flex-start;
            min-height: 100vh;
        }
        .app-container {
            width: 100%;
            max-width: 380px;
        }
        .header-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }
        .header-sub { font-size: 10px; color: #6b7280; font-weight: bold; letter-spacing: 1px; }
        .header-title { font-size: 22px; font-weight: bold; margin: 0; }
        
        .reset-btn {
            background: #1f2937;
            color: #9ca3af;
            border: none;
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 11px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.2s;
        }
        .reset-btn:hover {
            background: #374151;
            color: white;
        }

        /* Hauptkarte mit dem fetten Pink/Lila Farbverlauf */
        .guthaben-card {
            background: linear-gradient(135deg, #7c3aed 0%, #ec4899 100%);
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 12px;
            box-shadow: 0 10px 25px -5px rgba(236, 72, 153, 0.25);
        }
        .guthaben-title { font-size: 11px; font-weight: bold; opacity: 0.9; letter-spacing: 0.5px; }
        .guthaben-amount { font-size: 32px; font-weight: bold; margin: 8px 0 16px 0; }
        .guthaben-row { display: flex; justify-content: space-between; font-size: 11px; }
        .guthaben-row span { display: block; opacity: 0.85; margin-bottom: 2px; }
        .guthaben-row b { font-size: 14px; }

        /* Sparziel Karte */
        .card {
            background: #111827;
            border: 1px solid #1f2937;
            border-radius: 14px;
            padding: 14px;
            margin-bottom: 10px;
        }
        .card-header { display: flex; justify-content: space-between; font-size: 11px; color: #22d3ee; font-weight: bold; margin-bottom: 6px; }
        .card-main { display: flex; justify-content: space-between; font-size: 15px; font-weight: bold; margin-bottom: 10px; }
        .card-sub { font-size: 12px; color: #9ca3af; font-weight: normal; }
        
        /* Fortschrittsbalken */
        .progress-bar-bg { background: #1f2937; height: 6px; border-radius: 3px; overflow: hidden; }
        .progress-bar-fill { background: #22d3ee; height: 100%; width: 0%; transition: width 0.3s ease; }

        .section-title { font-size: 10px; color: #6b7280; font-weight: bold; margin: 15px 0 8px 0; letter-spacing: 1px; }

        /* Eingabefelder */
        .input-card {
            background: #111827;
            border: 1px solid #1f2937;
            border-radius: 14px;
            padding: 10px 14px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 8px;
        }
        .input-label-main { font-size: 13px; font-weight: bold; }
        .input-label-sub { font-size: 11px; color: #9ca3af; }
        .input-box {
            background: #0b0f19;
            border-radius: 8px;
            padding: 6px 10px;
            display: flex;
            align-items: center;
            width: 110px;
        }
        .input-box input {
            background: transparent;
            border: none;
            color: white;
            font-size: 14px;
            font-weight: bold;
            width: 100%;
            text-align: right;
            outline: none;
        }

        input[type=number]::-webkit-inner-spin-button, 
        input[type=number]::-webkit-outer-spin-button { 
            -webkit-appearance: none;
            margin: 0; 
        }
    </style>
</head>
<body>

<div class="app-container">
    <div class="header-row">
        <div>
            <div class="header-sub">POCKETBANK</div>
            <h1 class="header-title">Meine Finanzen</h1>
        </div>
        <button class="reset-btn" onclick="resetApp()">Reset</button>
    </div>

    <!-- Haupt-Guthaben-Karte -->
    <div class="guthaben-card">
        <div class="guthaben-title">VERFÜMBARES GUTHABEN</div>
        <div class="guthaben-amount" id="guthaben-anzeige">0,00 €</div>
        <div class="guthaben-row">
            <div>
                <span>Monatlicher Rest</span>
                <b id="rest-anzeige">0,00 €</b>
            </div>
            <div style="text-align: right;">
                <span>Gesamtersparnis</span>
                <b id="ersparnis-anzeige" style="color: #34d399;">0,00 €</b>
            </div>
        </div>
    </div>

    <!-- Sparziel-Karte -->
    <div class="card">
        <div class="card-header">
            <span id="ziel-titel-anzeige">SPARZIEL</span>
            <span id="prozent-anzeige">0%</span>
        </div>
        <div class="card-main">
            <span id="ziel-name-anzeige">Gaming-PC</span>
            <span class="card-sub" id="ziel-status-anzeige">0,00 € / 0,00 €</span>
        </div>
        <div class="progress-bar-bg">
            <div class="progress-bar-fill" id="fortschritts-balken"></div>
        </div>
    </div>

    <div class="section-title">BETRÄGE ANPASSEN</div>

    <!-- Taschengeld -->
    <div class="input-card">
        <div>
            <div class="input-label-main" style="color: #60a5fa;">Taschengeld</div>
            <div class="input-label-sub">Pro Monat</div>
        </div>
        <div class="input-box">
            <span style="color: #9ca3af; font-size: 13px; margin-right: 4px;">€</span>
            <input type="number" id="taschengeld" value="0" oninput="berechnen()">
        </div>
    </div>

    <!-- Erspartes -->
    <div class="input-card">
        <div>
            <div class="input-label-main" style="color: #34d399;">Erspartes</div>
            <div class="input-label-sub">Bisheriges Guthaben</div>
        </div>
        <div class="input-box">
            <span style="color: #9ca3af; font-size: 13px; margin-right: 4px;">€</span>
            <input type="number" id="erspartes" value="0" oninput="berechnen()">
        </div>
    </div>

    <!-- Ausgaben -->
    <div class="input-card">
        <div>
            <div class="input-label-main" style="color: #f87171;">Ausgaben</div>
            <div class="input-label-sub">Geplantes Budget</div>
        </div>
        <div class="input-box">
            <span style="color: #9ca3af; font-size: 13px; margin-right: 4px;">€</span>
            <input type="number" id="ausgaben" value="0" oninput="berechnen()">
        </div>
    </div>

    <!-- Sparziel festlegen -->
    <div class="input-card" style="display: block; padding: 12px 14px;">
        <div style="color: #22d3ee; font-size: 13px; font-weight: bold; margin-bottom: 8px;">Sparziel festlegen</div>
        <div style="display: flex; gap: 8px;">
            <input type="text" id="ziel-name" placeholder="z.B. Neue Grafikkarte" oninput="berechnen()" style="background: #0b0f19; border: none; color: white; padding: 6px; border-radius: 6px; font-size: 12px; flex: 2; outline: none;">
            <input type="number" id="ziel-betrag" placeholder="Zielbetrag" oninput="berechnen()" style="background: #0b0f19; border: none; color: white; padding: 6px; border-radius: 6px; font-size: 12px; flex: 1; text-align: right; outline: none;">
        </div>
    </div>
</div>

<script>
    function loadData() {
        const data = JSON.parse(localStorage.getItem('pocketbank_data') || '{}');
        if (data.taschengeld !== undefined) document.getElementById('taschengeld').value = data.taschengeld;
        if (data.erspartes !== undefined) document.getElementById('erspartes').value = data.erspartes;
        if (data.ausgaben !== undefined) document.getElementById('ausgaben').value = data.ausgaben;
        if (data.zielName !== undefined) document.getElementById('ziel-name').value = data.zielName;
        if (data.zielBetrag !== undefined) document.getElementById('ziel-betrag').value = data.zielBetrag;
        berechnen();
    }

    function saveData() {
        const data = {
            taschengeld: document.getElementById('taschengeld').value,
            erspartes: document.getElementById('erspartes').value,
            ausgaben: document.getElementById('ausgaben').value,
            zielName: document.getElementById('ziel-name').value,
            zielBetrag: document.getElementById('ziel-betrag').value
        };
        localStorage.setItem('pocketbank_data', JSON.stringify(data));
    }

    function berechnen() {
        let taschengeld = parseFloat(document.getElementById('taschengeld').value) || 0;
        let erspartes = parseFloat(document.getElementById('erspartes').value) || 0;
        let ausgaben = parseFloat(document.getElementById('ausgaben').value) || 0;
        
        let zielName = document.getElementById('ziel-name').value.trim() || "Gaming-PC";
        let zielBetrag = parseFloat(document.getElementById('ziel-betrag').value) || 0;

        let rest = taschengeld - ausgaben;
        let gesamtersparnis = erspartes + rest;

        document.getElementById('rest-anzeige').innerText = rest.toFixed(2) + " €";
        document.getElementById('ersparnis-anzeige').innerText = gesamtersparnis.toFixed(2) + " €";
        document.getElementById('guthaben-anzeige').innerText = gesamtersparnis.toFixed(2) + " €";

        document.getElementById('ziel-name-anzeige').innerText = zielName;
        document.getElementById('ziel-titel-anzeige').innerText = zielName.toUpperCase();

        let prozent = 0;
        if (zielBetrag > 0) {
            prozent = (gesamtersparnis / zielBetrag) * 100;
            if (prozent > 100) prozent = 100;
            if (prozent < 0) prozent = 0;
        }

        document.getElementById('prozent-anzeige').innerText = Math.round(prozent) + "%";
        document.getElementById('ziel-status-anzeige').innerText = gesamtersparnis.toFixed(2) + " € / " + zielBetrag.toFixed(2) + " €";
        document.getElementById('fortschritts-balken').style.width = prozent + "%";

        saveData();
    }

    function resetApp() {
        document.getElementById('taschengeld').value = "0";
        document.getElementById('erspartes').value = "0";
        document.getElementById('ausgaben').value = "0";
        document.getElementById('ziel-name').value = "";
        document.getElementById('ziel-betrag').value = "";
        localStorage.removeItem('pocketbank_data');
        berechnen();
    }

    loadData();
</script>

</body>
</html>
"""

if __name__ == '__main__':
    window = webview.create_window(
        title='PocketBank',
        html=HTML_CODE,
        width=420,
        height=750,
        resizable=False
    )
    webview.start()