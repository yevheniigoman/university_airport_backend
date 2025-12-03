from services import FlightService
from models import Flight
from fpdf import FPDF

class FlightReportService:
    @staticmethod
    def to_pdf(flight: Flight) -> FPDF:
        """Generates flight report in pdf format"""
        pdf = FPDF()
        pdf.add_page()

        pdf.set_font("Helvetica", size=20, style="B")
        pdf.cell(text="Flight Report", center=True)
        pdf.ln(15)

        pdf.set_font("Helvetica", size=16)
        TABLE_DATA = (
            ("Flight number", flight.flight_number),
            ("Aircraft", flight.aircraft.model),
            ("Departure airport", flight.dep_airport.name),
            ("Arrival airport", flight.arr_airport.name),
            ("Departure time", flight.departure_time.strftime("%d.%m.%Y %H:%M:%S")),
            ("Arrival time", flight.arrival_time.strftime("%d.%m.%Y %H:%M:%S")),
            ("Economy price", f"{flight.economy_price} $"),
            ("Business price", f"{flight.business_price} $"),
            ("Total fuel", f"{FlightService.calculate_fuel(flight):.2f} tons")
        )
        
        with pdf.table(TABLE_DATA, first_row_as_headings=False) as table:
            pass

        return pdf
