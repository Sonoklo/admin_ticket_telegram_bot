from database.db import get_ticket_text
def parse_ticket_text(ticket_id):
    text = ""
    num = 1
    for message in get_ticket_text(ticket_id):
        text += f"{num}) {message.text}\n"
        num += 1
    return text