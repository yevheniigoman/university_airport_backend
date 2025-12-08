from models import Ticket
from fpdf import FPDF


class TicketReportService:
    @staticmethod
    def to_pdf(ticket: Ticket) -> FPDF:
        """Generates ticket in pdf format"""
        pdf = FPDF()
        pdf.add_page()

        pdf.set_font("Helvetica", size=20, style="B")
        pdf.cell(text="Ticket", center=True)
        pdf.ln(15)

        pdf.set_font("Helvetica", size=16)

        seat_class = "Business" if ticket.seat.seat_class == 1 else "Econom"
        TABLE_DATA = (
            ("Ticket id", str(ticket.id)),
            ("Flight number", ticket.flight.flight_number),
            ("Seat number", ticket.seat.seat_number),
            ("Seat class", seat_class),
            ("Passanger", f"{ticket.first_name} {ticket.last_name}"),
            ("Purchase date", ticket.purchase_date.strftime("%d.%m.%Y %H:%M:%S")),
            ("Price", str(ticket.price))
        )

        with pdf.table(TABLE_DATA, first_row_as_headings=False) as table:
            pass

        return pdf
