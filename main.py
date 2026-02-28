from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from textblob import TextBlob
from deep_translator import GoogleTranslator

app = FastAPI(title="AI Linguistic Analyzer con Traducción")

class TextData(BaseModel):
    text: str

@app.post("/analyze")
def analyze_text(data: TextData):
    if not data.text:
        raise HTTPException(status_code=400, detail="El texto está vacío")
    
    try:
        # PASO DE CREATIVIDAD: Traducción automática al inglés
        # Esto asegura que palabras como "pésimo" sean detectadas correctamente
        translated_text = GoogleTranslator(source='auto', target='en').translate(data.text)
        
        # Procesamiento de datos con el texto traducido
        analysis = TextBlob(translated_text)
        sentiment_score = analysis.sentiment.polarity
        
        # Lógica de categorización
        if sentiment_score > 0.1:
            sentiment = "Positivo"
        elif sentiment_score < -0.1:
            sentiment = "Negativo"
        else:
            sentiment = "Neutro"
            
        return {
            "original_text": data.text,
            "translated_text": translated_text, # Evidencia del procesamiento
            "sentiment": sentiment,
            "score": round(sentiment_score, 2)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el procesamiento: {str(e)}")