from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from textblob import TextBlob

app = FastAPI(title="AI Linguistic Analyzer")

class TextData(BaseModel):
    text: str
    target_language: str = "es"

@app.get("/")
def home():
    return {"message": "API de Análisis Lingüístico activa localmente"}

@app.post("/analyze")
def analyze_text(data: TextData):
    if not data.text:
        raise HTTPException(status_code=400, detail="El texto no puede estar vacío")
    
    analysis = TextBlob(data.text)
    # Procesamiento de datos: Cálculo de polaridad (-1 a 1)
    sentiment_score = analysis.sentiment.polarity
    
    sentiment = "Positivo" if sentiment_score > 0 else "Negativo" if sentiment_score < 0 else "Neutro"
    
    return {
        "original_text": data.text,
        "sentiment": sentiment,
        "score": round(sentiment_score, 2),
        "language_detected": analysis.detect_language() if len(data.text) > 3 else "unknown"
    }