from sqlalchemy import create_engine,ForeignKey
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship,Session

engine = create_engine("sqlite:///task1.db")
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    user_id: Mapped[int] = mapped_column(nullable=False, unique=True)
    role: Mapped[str] = mapped_column(nullable=False, default="client") # client |  admin    
    state: Mapped[str] = mapped_column(nullable=False, default="idle")  # idle | in_dialog

    tickets: Mapped[list["Ticket"]] = relationship(
        back_populates="user", 
        foreign_keys="[Ticket.user_id]"
    )    

    assigned_tickets: Mapped[list["Ticket"]] = relationship(
        foreign_keys="[Ticket.admin_id]"
    )

    messages: Mapped[list["Message"]] = relationship(back_populates="user")

class Message(Base):
    __tablename__ = "messages"
    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    text: Mapped[str] = mapped_column(nullable=False)

    ticket_id: Mapped[int] = mapped_column(ForeignKey("tickets.id"))
    sender_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    user: Mapped["User"] = relationship(back_populates="messages")
    ticket: Mapped["Ticket"] = relationship(back_populates="messages")

class Ticket(Base):
    __tablename__ = "tickets"
    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    status: Mapped[str] = mapped_column(default="open") # 'close' | 'in_progress'
    
    messages: Mapped[list["Message"]] = relationship(back_populates="ticket")
   
    admin_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)
    admin: Mapped["User"] = relationship(
        foreign_keys="[Ticket.admin_id]"
    )

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(
        back_populates="tickets", 
        foreign_keys="[Ticket.user_id]"
    )

Base.metadata.create_all(engine)

def create_user(user_id, problem_text):
    with Session(engine) as session:
        user1 = session.query(User).filter(User.user_id==user_id).first()
        if user1:
            user1.state = "in_dialog"
        else:
            user1 = User(user_id = user_id, state = "in_dialog")
            session.add(user1)
        ticket = Ticket(user = user1)
        message = Message(user = user1, text = problem_text, ticket = ticket)
        session.add_all((ticket,message))
        session.commit()

def get_admin(user_id):
    with Session(engine) as session:
        admin = get_user(user_id)
        if admin:
            if admin.role != "admin":
                return None
            return admin
        return None
def get_user(user_id):
    with Session(engine) as session:
        user = session.query(User).filter(User.user_id == user_id).first()
        return user
    
def get_open_tickets():
    with Session(engine) as session:
        tickets_open = session.query(Ticket).filter(Ticket.status == "open").all()
        return tickets_open
    
def connect_admin_to_ticket(ticket_id, admin_id):
    with Session(engine) as session:
        ticket = session.query(Ticket).filter(Ticket.id == ticket_id).first()
        admin = session.query(User).filter(User.user_id == admin_id).first()
        if ticket:

            admin.state = "in_dialog"
            ticket.admin_id = admin_id
            ticket.status = "in_progress"
            session.commit()
    
def get_ticket_text(ticket_id):
    with Session(engine) as session:
        ticket = session.query(Ticket).filter(Ticket.id == ticket_id).first()
        if ticket:
            return ticket.messages
        return None
    
def get_user_ticket_by_user(user_id):
    with Session(engine) as session:
        user = session.query(User).filter(User.user_id == user_id).first()
        user_ticket = session.query(Ticket).filter(Ticket.user_id == user.id, Ticket.status == "in_progress").first()
        return user_ticket

def get_user_ticket_by_admin(user_id):
    with Session(engine) as session:
        user = session.query(User).filter(User.id == user_id).first()
        user_ticket = session.query(Ticket).filter(Ticket.user_id == user.id).first()
        return user_ticket

def add_message_to_ticket(text, ticket, user_id):
    with Session(engine) as session:
        ticket = session.query(Ticket).filter(Ticket.id==ticket.id).first()
        user = session.query(User).filter(User.user_id == user_id).first()
        message = Message(user=user, text=text, ticket=ticket)
        session.add(message)
        session.commit()

def get_user_id(ticket):
    with Session(engine) as session:
        user = session.query(User).filter(User.id == ticket.user_id).first()
        return user.user_id
    
def get_admin_open_ticket(admin_id):
    with Session(engine) as session:
        ticket = session.query(Ticket).filter(Ticket.admin_id == admin_id).first()
        return ticket
    
def close_ticket(user_id,admin_id):
    with Session(engine) as session:
        user = session.query(User).filter(User.user_id == user_id).first()
        admin = session.query(User).filter(User.user_id == admin_id).first()
        ticket = session.query(Ticket).filter(Ticket.admin_id == admin_id, Ticket.status == "in_progress").first()
        ticket.status = "close"
        user.state = "idle"
        admin.state = "idle"
        session.commit()

def in_dialog(ticket_id):
    with Session(engine) as session:
        ticket = session.query(Ticket).filter(Ticket.id == ticket_id).first()
        if ticket.status != "in_dialog":
            return True
        return False
    
def get_ticket_by_id(ticket_id):
    with Session(engine) as session:
        ticket = session.query(Ticket).filter(Ticket.id == ticket_id).first()
        return ticket 

def get_admin_in_progres_ticket(admin_id):
    with Session(engine) as session:
        ticket = session.query(Ticket).filter(Ticket.admin_id == admin_id, Ticket.status == "in_progress").first()
        return ticket
    
def get_user_ticket(user_id):
    with Session(engine) as session:
        user = session.query(User).filter(User.user_id == user_id).first()
        user_ticket = session.query(Ticket).filter(Ticket.user_id == user.id, Ticket.status != "close").first()
        return user_ticket
    
def ticket_close(ticket_id):
    with Session(engine) as session:
        ticket = session.query(Ticket).filter(Ticket.id == ticket_id).first()
        if ticket.status == "close":
            return False
        return True