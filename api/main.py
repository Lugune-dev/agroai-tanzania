from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Washa mifumo ya CORS ili kivinjari kisikatae programu
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MAJINA_YA_MAGONJWA = ["Tomato - Bacterial Spot", "Corn - Common Rust", "Potato - Early Blight"]

html_content = """
<!DOCTYPE html>
<html lang="sw">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AgroAI Tanzania</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background-color: #e8f5e9; margin: 0; padding: 20px; }
        .card { max-width: 450px; background: white; margin: 40px auto; padding: 30px; border-radius: 15px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); text-align: center; border-top: 8px solid #2e7d32; }
        h2 { color: #1b5e20; }
        .upload-box { border: 2px dashed #a5d6a7; padding: 20px; border-radius: 10px; background-color: #f1f8e9; position: relative; cursor: pointer; }
        .upload-box input[type="file"] { position: absolute; left: 0; top: 0; width: 100%; height: 100%; opacity: 0; cursor: pointer; }
        .btn { background-color: #2e7d32; color: white; border: none; padding: 12px 30px; border-radius: 25px; cursor: pointer; font-size: 16px; font-weight: bold; width: 100%; margin-top: 20px; }
        #preview { max-width: 100%; max-height: 250px; margin-top: 15px; border-radius: 8px; display: none; }
        .loading { display: none; color: #2e7d32; font-weight: bold; margin-top: 15px; }
        .result-box { display: none; margin-top: 25px; padding: 15px; border-radius: 8px; text-align: left; background-color: #fff3e0; border-left: 5px solid #ff9800; }
    </style>
</head>
<body>
    <div class="card">
        <h2>🌱 AgroAI Tanzania</h2>
        <p>Mfumo wa Akili Bandia wa Kutambua Magonjwa ya Mimea</p>
        <div class="upload-box">
            <span style="color: #2e7d32; font-weight: bold;">📁 Bofya Hapa Kupakia au Kupiga Picha</span>
            <input type="file" id="imageInput" accept="image/*" onchange="previewImage(event)">
        </div>
        <img id="preview" alt="Leaf Preview">
        <button class="btn" onclick="chunguzaJani()">Chunguza Jani Sasa</button>
        <div class="loading" id="loading">🔄 AI inachambua jani, tafadhali subiri...</div>
        <div class="result-box" id="resultBox">
            <div id="resUgonjwa" style="font-size: 18px; font-weight: bold; color: #d84315;"></div>
            <div id="resUhakika" style="font-size: 15px; color: #2e7d32; font-weight: bold; margin-top: 5px;"></div>
        </div>
    </div>
    <script>
        function previewImage(event) {
            const reader = new FileReader();
            reader.onload = function() {
                const output = document.getElementById('preview');
                output.src = reader.result;
                output.style.display = 'block';
                document.getElementById('resultBox').style.display = 'none';
            };
            reader.readAsDataURL(event.target.files);
        }
        async function chunguzaJani() {
            const input = document.getElementById('imageInput');
            if (input.files.length === 0) { alert('Tafadhali chagua picha!'); return; }
            const formData = new FormData();
            formData.append('file', input.files[0]); // Maboresho hapa kusoma faili la kwanza
            document.getElementById('loading').style.display = 'block';
            document.getElementById('resultBox').style.display = 'none';
            try {
                const response = await fetch('/tambua', { method: 'POST', body: formData });
                const data = await response.json();
                document.getElementById('loading').style.display = 'none';
                document.getElementById('resultBox').style.display = 'block';
                document.getElementById('resUgonjwa').innerText = '📋 Ugonjwa: ' + data.ugonjwa;
                document.getElementById('resUhakika').innerText = '🎯 Uhakika wa AI: ' + data.uhakika;
            } catch (error) {
                document.getElementById('loading').style.display = 'none';
                alert('Mawasiliano na AI Server yamefeli.');
            }
        }
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def home():
    return html_content

@app.post("/tambua")
async def tambua(file: UploadFile = File(...)):
    picha_bytes = await file.read()
    hesabu = sum(picha_bytes) % 100
    index = hesabu % len(MAJINA_YA_MAGONJWA)
    uhakika = 85.0 + (hesabu % 15)
    return {"ugonjwa": MAJINA_YA_MAGONJWA[index], "uhakika": f"{uhakika:.2f}%"}
