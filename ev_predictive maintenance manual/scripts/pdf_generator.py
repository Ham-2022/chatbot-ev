from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO

def generate_pdf(voltage, current, temperature, state_of_charge, health_prediction):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    
    c.drawString(100, 750, "Battery Health Report")
    c.drawString(100, 730, f"Voltage: {voltage} V")
    c.drawString(100, 710, f"Current: {current} A")
    c.drawString(100, 690, f"Temperature: {temperature} °C")
    c.drawString(100, 670, f"State of Charge: {state_of_charge} %")
    c.drawString(100, 650, f"Predicted Battery Health: {health_prediction * 100:.2f} %")
    
    c.save()
    buffer.seek(0)
    
    return buffer
