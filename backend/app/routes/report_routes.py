from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Report, Event
from app.schemas import ReportCreate
import os
from fpdf import FPDF 
from fastapi.responses import FileResponse
from dotenv import load_dotenv
import spacy
import json

load_dotenv() 

router = APIRouter()

nlp = spacy.load("es_core_news_md")

def analyze_feedback(feedback: str):
    doc = nlp(feedback)

    
    entities = [(ent.text, ent.label_) for ent in doc.ents]

    # Extraer palabras clave
    keywords = [token.text for token in doc if token.is_alpha and not token.is_stop]

    return {
        "entities": entities,
        "keywords": keywords,
        "word_count": len(doc)
    }

# Prueba con un comentario de usuario
feedback = "El evento en la Quinta Marcelo's fue excelente. Los speakers como Ana Pérez dieron charlas muy inspiradoras."
print(analyze_feedback(feedback))

@router.post("/api/reports")
def generate_report(report: ReportCreate, db: Session = Depends(get_db)):
    
    event = db.query(Event).filter(Event.id == report.event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Evento no encontrado")

    required_fields = [report.organization, report.speaker_quality, report.venue_satisfaction, report.engagement, report.logistics]
    if any(field is None for field in required_fields):
        raise HTTPException(status_code=400, detail="Todos los campos deben tener valores")

    ai_summary = json.dumps(analyze_feedback(report.feedback))

    db_report = Report(
        event_id=report.event_id,
        rating=report.rating,
        organization=report.organization,
        speaker_quality=report.speaker_quality,
        venue_satisfaction=report.venue_satisfaction,
        engagement=report.engagement,
        logistics=report.logistics,
        feedback=report.feedback,
        ai_analysis=ai_summary
    )

    db.add(db_report)
    db.commit()
    db.refresh(db_report)

    return {"id": db_report.id, "message": "Reporte generado correctamente"}

def create_pdf(report: Report):
    
    pdf_dir = "reports"
    if not os.path.exists(pdf_dir):
        os.makedirs(pdf_dir)

    pdf_path = os.path.join(pdf_dir, f"event_{report.event_id}.pdf")

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "Reporte del Evento", ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Arial", "", 12)
    pdf.cell(200, 10, f"ID del Evento: {report.event_id}", ln=True)
    pdf.cell(200, 10, f"Calificación General: {report.rating}/5", ln=True)
    pdf.cell(200, 10, f"Organización: {report.organization}/5", ln=True)
    pdf.cell(200, 10, f"Calidad del Speaker: {report.speaker_quality}/5", ln=True)
    pdf.cell(200, 10, f"Satisfacción del Lugar: {report.venue_satisfaction}/5", ln=True)
    pdf.cell(200, 10, f"Interacción con Asistentes: {report.engagement}/5", ln=True)
    pdf.cell(200, 10, f"Logística: {report.logistics}/5", ln=True)
    pdf.ln(10)

    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, "Comentarios de los Asistentes:", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, report.feedback)
    pdf.ln(10)

    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, "Análisis del Evento (IA):", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, report.ai_analysis)

    pdf.output(pdf_path)
    return pdf_path

@router.get("/api/reports/download/{event_id}")
def download_report(event_id: int, db: Session = Depends(get_db)):
    """ Descarga el reporte en formato PDF. """
    report = db.query(Report).filter(Report.event_id == event_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")

    pdf_path = create_pdf(report)

    if not os.path.exists(pdf_path):
        raise HTTPException(status_code=500, detail="Error al generar el PDF")

    return FileResponse(pdf_path, filename=f"reporte_evento_{event_id}.pdf", media_type="application/pdf")
