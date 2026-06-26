from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import io

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# KANZI DATA KUBWA YA MAGONJWA YOTE NA MATIBABU YAKE
MAGONJWA_DATABASE = {
    "Mahindi - Kutu ya Majani (Corn Common Rust)": {
        "maelezo": "Ugonjwa wa kuvu unaosababishwa na vimelea vya Puccinia sorghi. Husababisha madoa ya hudhurungi kwenye majani na kupunguza uwezo wa mmea kutengeneza chakula.",
        "tiba": "Nyunyizia viuatilifu vya kuvu (Fungicides) vyenye viambata amilifu vya Mancozeb au Azoxystrobin. Zingatia mzunguko wa mazao shambani.",
        "pesticide_cost": "TSh 35,000 kwa ekari"
    },
    "Mahindi - Batobato (Maize Streak Virus)": {
        "maelezo": "Ugonjwa wa virusi unaosambazwa na wadudu aina ya minyoo ya majani (leafhoppers). Huonyesha mistari ya njano inayofuata mishipa ya majani.",
        "tiba": "Pandikiza mbegu zinazovumilia ugonjwa. Udhibiti wadudu wasambazaji kwa kutumia viuatilifu kama Imidacloprid mapema mwanzoni mwa msimu.",
        "pesticide_cost": "TSh 28,000 kwa ekari"
    },
    "Nyanya - Mnyanyuko wa Bakteria (Tomato Bacterial Wilt)": {
        "maelezo": "Ugonjwa hatari wa bakteria unaosababishwa na Ralstonia solanacearum. Mmea unanyauka ghafla ukiwa bado wa kijani kibichi kuanzia juu.",
        "tiba": "Hakuna tiba ya kemikali mara ugonjwa ukiingia. Ng'oa na choma mimea iliyoathirika. Hakikisha udongo una mifereji mizuri ya maji na fanya mzunguko wa mazao.",
        "pesticide_cost": "TSh 0 (Ng'oa na Choma)"
    },
    "Nyanya - Koga la Mapema (Tomato Early Blight)": {
        "maelezo": "Ugonjwa wa kuvu unaoanza na madoa meusi yenye duara kama shabaha (target spots) kwenye majani ya chini.",
        "tiba": "Nyunyizia dawa za Copper-based fungicides au Chlorothalonil kila baada ya siku 7-14. Punguza matawi ya chini ili kuongeza mzunguko wa hewa.",
        "pesticide_cost": "TSh 42,000 kwa ekari"
    },
    "Mihogo - Batobato (Cassava Mosaic Disease - CMD)": {
        "maelezo": "Ugonjwa wa virusi unaosababishwa na nzi weupe (Whiteflies). Majani yanajikunja, yanapoteza rangi ya kijani na kuwa na madoa ya njano (chlorosis).",
        "tiba": "Tumia vikwazo safi vya kupandikiza (clean cuttings) kutoka vyanzo vilivyothibitishwa kama TOSCI. Ng'oa mimea yote inayoonyesha dalili mapema.",
        "pesticide_cost": "TSh 15,000 (Kudhibiti Nzi Weupe)"
    },
    "Mihogo - Mnyanyuko wa Bakteria (Cassava Bacterial Blight)": {
        "maelezo": "Husababishwa na bakteria Xanthomonas. Dalili ni madoa yenye unyevu kama maji (water-soaked spots) chini ya majani yanayopelekea majani kukauka na kuanguka.",
        "tiba": "Tumia zana safi za kilimo zilizosafishwa kwa daktari wa mimea. Epuka kufanya kazi shambani kukiwa na umande au mvua ili kuzuia ueneaji.",
        "pesticide_cost": "TSh 20,000 kwa usafi wa vifaa"
    },
    "Mpunga - Kuvu ya Bakteria (Rice Bacterial Leaf Blight)": {
        "maelezo": "Ugonjwa unaosababishwa na Xanthomonas oryzae. Husababisha mistari ya njano-kijivu kuanzia ncha ya jani kushuka chini hadi jani lote likauke.",
        "tiba": "Epuka kuweka mbolea ya nitrojeni (urea) iliyozidi kiwango. Tumia mbegu zilizoboreshwa na nyunyizia dawa za kuzuia bakteria ikibidi.",
        "pesticide_cost": "TSh 48,000 kwa ekari"
    },
    "Kahawa - Chuo cha Matunda (Coffee Berry Disease)": {
        "maelezo": "Kuvu wanaoshambulia matunda mabichi ya kahawa na kuyasababisha yawe meusi na kuoza kabla ya kukomaa.",
        "tiba": "Nyunyizia dawa za kuzuia kuvu (Copper hydroxide au miunganisho ya kimfumo) kabla ya msimu wa mvua kuanza.",
        "pesticide_cost": "TSh 65,000 kwa ekari"
    },
    "Parachichi - Kuoza kwa Mizizi (Root Rot)": {
        "maelezo": "Husababishwa na kuvu wa udongoni aina ya Phytophthora cinnamomi. Majani yanakuwa madogo, ya manjano na mmea unaanza kukauka kuanzia matawi ya juu.",
        "tiba": "Boresha mfumo wa kupitisha maji ardhini ili kuzuia lami ya maji. Tumia viuatilifu vyenye viambata vya Phosphonate (Foliar sprays au trunk injections).",
        "pesticide_cost": "TSh 75,000 kwa mti/shamba"
    }
}

ORODHA_YA_MAGONJWA = list(MAGONJWA_DATABASE.keys())

html_content = """
<!DOCTYPE html>
<html lang="sw">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AgroAI Enterprise - Tanzania</title>
    <style>
        :root {
            --bg-color: #f4f7f5;
            --card-bg: #ffffff;
            --text-main: #2c3e50;
            --primary: #2e7d32;
            --primary-hover: #1b5e20;
            --border-color: #e0e0e0;
            --accent: #ff9800;
        }
        [data-theme="dark"] {
            --bg-color: #121212;
            --card-bg: #1e1e1e;
            --text-main: #e0e0e0;
            --primary: #81c784;
            --primary-hover: #a5d6a7;
            --border-color: #333333;
            --accent: #ffb74d;
        }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: var(--bg-color); color: var(--text-main); margin: 0; padding: 0; transition: 0.3s; }
        
        /* Navigation & Header */
        header { background: var(--card-bg); border-bottom: 1px solid var(--border-color); padding: 15px 30px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
        .logo-area { display: flex; align-items: center; gap: 10px; }
        .logo-area h1 { font-size: 22px; color: var(--primary); margin: 0; }
        .theme-btn { background: var(--primary); color: white; border: none; padding: 8px 15px; border-radius: 20px; cursor: pointer; font-weight: bold; font-size: 13px; }

        /* Layout Grid */
        .wrapper { max-width: 1200px; margin: 30px auto; padding: 0 20px; display: grid; grid-template-columns: 1fr 1.5fr; gap: 30px; }
        @media (max-width: 900px) { .wrapper { grid-template-columns: 1fr; } }

        .card { background: var(--card-bg); border-radius: 12px; padding: 25px; border: 1px solid var(--border-color); box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
        h3 { margin-top: 0; color: var(--primary); border-bottom: 2px solid var(--border-color); padding-bottom: 8px; }

        /* Upload Area */
        .upload-zone { border: 2px dashed var(--primary); background: rgba(46, 125, 50, 0.03); border-radius: 8px; padding: 40px 20px; text-align: center; cursor: pointer; position: relative; transition: 0.2s; }
        .upload-zone:hover { background: rgba(46, 125, 50, 0.07); }
        .upload-zone input[type="file"] { position: absolute; left: 0; top: 0; width: 100%; height: 100%; opacity: 0; cursor: pointer; }
        #preview { max-width: 100%; max-height: 200px; margin-top: 15px; border-radius: 6px; display: none; }
        .analyze-btn { background: var(--primary); color: white; border: none; width: 100%; padding: 12px; border-radius: 6px; font-size: 16px; font-weight: bold; cursor: pointer; margin-top: 15px; transition: 0.2s; }
        .analyze-btn:hover { background: var(--primary-hover); }

        /* Loader & Responses */
        .loader { display: none; color: var(--primary); font-weight: bold; margin: 15px 0; text-align: center; }
        .response-box { display: none; background: rgba(255, 152, 0, 0.08); border-left: 5px solid var(--accent); padding: 15px; border-radius: 4px; margin-top: 20px; }
        .disease-title { font-size: 18px; font-weight: bold; color: var(--accent); }
        
        /* Disease Directory Tab */
        .disease-list-item { padding: 10px; border-bottom: 1px solid var(--border-color); font-size: 14px; cursor: pointer; }
        .disease-list-item:hover { color: var(--primary); background: rgba(0,0,0,0.02); }

        /* Advanced Calculator & Features widget */
        .widget { margin-top: 20px; background: var(--card-bg); border: 1px solid var(--border-color); border-radius: 12px; padding: 20px; }
        .calc-input { width: 90%; padding: 8px; border-radius: 4px; border: 1px solid var(--border-color); background: var(--bg-color); color: var(--text-main); margin-bottom: 10px; }
    </style>
</head>
<body>

    <header>
        <div class="logo-area">
            <h2>🌱 AgroAI Enterprise</h2>
        </div>
        <button class="theme-btn" onclick="toggleTheme()">Badili Mandhari (Theme)</button>
    </header>

    <div class="wrapper">
        <!-- Upande wa kushoto: Uchambuzi na Zana -->
        <div>
            <div class="card">
                <h3>🔍 Chunguza Afya ya Jani</h3>
                <div class="upload-zone">
                    <p style="font-weight: bold; margin: 0;">📁 Bofya hapa au Vuta Picha Shambani</p>
                    <input type="file" id="leafInput" accept="image/*" onchange="handlePreview(event)">
                    <img id="preview" alt="Leaf Preview">
                </div>
                <button class="analyze-btn" onclick="processAnalysis()">Anza Uchambuzi wa AI</button>
                <div class="loader" id="loader">🔄 Akili Bandia inasoma vimelea vya maambukizi...</div>
                
                <div class="response-box" id="responseBox">
                    <div class="disease-title" id="resName"></div>
                    <p id="resDesc" style="font-size: 14px; margin: 10px 0;"></p>
                    <div style="background: var(--card-bg); padding: 10px; border-radius: 4px; font-size: 13px; border-top: 2px solid var(--primary);">
                        <strong>💡 Ushauri wa Tiba (Treatment Protocol):</strong>
                        <div id="resTreatment" style="margin-top:5px; color:#555;"></div>
                    </div>
                    <div id="resCost" style="margin-top: 10px; font-size: 13px; font-weight: bold; color: var(--primary);"></div>
                </div>
            </div>
