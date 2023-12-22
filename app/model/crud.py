from app.model import models, schemas
from datetime import datetime
from sqlalchemy.orm import Session


def get_clients(session: Session):
    """
    Get all clients

    Args:
        session (Session, optional): Database session. Defaults to Depends(get_session).

    Returns:
        list[schemas.ClientOut]: List of clients

    """

    clients = session.query(models.Client).all()
    return clients


def get_client_by_id(session: Session, client_id: int):
    """
    Get a client by id

    Args:
        client_id (int): Client id
        session (Session, optional): Database session. Defaults to Depends(get_session).

    Returns:
        schemas.ClientOut: Client

    """

    client = session.query(models.Client).filter(models.Client.id == client_id).first()
    return client


def create_client(session: Session, client: schemas.ClientIn):
    """
    Create a client

    Args:
        client (schemas.ClientIn): Client to create
        session (Session, optional): Database session. Defaults to Depends(get_session).

    Returns:
        dict: Status of the operation

    """

    # Create client
    new_client = models.Client(
        name=client.name,
        rut=client.rut,
        salary=client.salary,
        savings=client.savings,
    )
    session.add(new_client)
    session.commit()

    client_id = new_client.id

    # Create messages and debts
    for message in client.messages:
        create_message(session=session, message=message, client_id=client_id)

    for debt in client.debts:
        create_debt(session=session, debt=debt, client_id=client_id)

    session.commit()
    return new_client


def create_message(session: Session, message: schemas.MessageIn, client_id: int):
    """
    Create a message

    Args:
        message (schemas.MessageIn): Message to create
        session (Session, optional): Database session. Defaults to Depends(get_session).

    Returns:
        dict: Status of the operation
    """

    msgDate = datetime.fromisoformat(message.sentAt.replace("Z", "+00:00"))
    new_message = models.Message(
        text=message.text, role=message.role, sentAt=msgDate, client_id=client_id
    )
    session.add(new_message)
    session.commit()
    return new_message


def create_debt(session: Session, debt: schemas.DebtsIn, client_id: int):
    """
    Create a debt

    Args:
        debt (schemas.DebtsIn): Debt to create
        session (Session, optional): Database session. Defaults to Depends(get_session).

    Returns:
        dict: Status of the operation

    """

    debDate = datetime.fromisoformat(debt.dueDate.replace("Z", "+00:00"))
    new_debt = models.Debts(
        institution=debt.institution,
        amount=debt.amount,
        dueDate=debDate,
        client_id=client_id,
    )
    session.add(new_debt)
    session.commit()
    return new_debt
