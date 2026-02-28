from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from textblob import TextBlob

app = FastAPI(title="AI Linguistic Analyzer")

class TextData(BaseModel):
    text: str

@app.get("/")
def home():
    return {"message": "API de Análisis Lingüístico activa localmente"}

@app.post("/analyze")
def analyze_text(data: TextData):
    if not data.text:
        raise HTTPException(status_code=400, detail="El texto no puede estar vacío")
    
    # Procesamiento de datos con TextBlob
    analysis = TextBlob(data.text)
    sentiment_score = analysis.sentiment.polarity
    
    # Lógica de categorización
    if sentiment_score > 0:
        sentiment = "Positivo/Positive"
    elif sentiment_score < 0:
        sentiment = "Negativo/Negative"
    else:
        sentiment = "Neutro/Neutral"
    
    return {
        "original_text": data.text,
        "sentiment": sentiment,
        "score": round(sentiment_score, 2)
    }