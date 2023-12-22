from app.dependencies import get_session
from app.model import crud, schemas
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session


api_router = APIRouter()

# ------- Client Routes -------
@api_router.get("/clients", response_model=list[schemas.ClientOut] , status_code=200)
async def get_clients(session: Session = Depends(get_session)):
    """
    Get all clients

    Args:
        session (Session, optional): Database session. Defaults to Depends(get_session).

    Returns:
        list[schemas.ClientOut]: List of clients    
    """

    clients = crud.get_clients(session=session)
    clients = [schemas.ClientOut.from_orm(client) for client in clients]
    return clients
    

@api_router.get("/clients/{client_id}", response_model=schemas.ClientOut, status_code=200)
async def get_client(client_id: int, session: Session = Depends(get_session)):

    """
    Get a client by id

    Args:
        client_id (int): Client id
        session (Session, optional): Database session. Defaults to Depends(get_session).

    Returns:
        schemas.ClientOut: Client

    """

    client = crud.get_client_by_id(session=session, client_id=client_id)
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")

    return schemas.ClientOut.from_orm(client)

@api_router.post("/clients", status_code=201)
async def create_client(client: schemas.ClientIn, session: Session = Depends(get_session)):
    """
    Create a client

    Args:
        client (schemas.ClientIn): Client to create
        session (Session, optional): Database session. Defaults to Depends(get_session).

    Returns:
        dict: Status of the operation
    """

    try:   
        client = crud.create_client(session=session, client=client)
        return {"status": "ok"}
    except Exception:
        return {"status": "error"}
    
@api_router.get("/clients-to-do-follow-up", status_code=200)
async def get_clients_to_do_follow_up(session: Session = Depends(get_session)):
    """
    Get all clients that need to be followed up

    Args:
        session (Session, optional): Database session. Defaults to Depends(get_session).

    Returns:
        list[schemas.ClientOut]: List of clients to follow up    
    """

    clients = crud.get_clients(session=session)
    clients = [schemas.ClientOut.from_orm(client) for client in clients if client.followUp()]
    return clients

@api_router.get("/clients/{client_id}/score", status_code=200)
async def get_clients_score(client_id: str, session: Session = Depends(get_session)):

    """
    Get a client score by id

    Args:
        client_id (int): Client id
        session (Session, optional): Database session. Defaults to Depends(get_session).

    Returns:
        schemas.ClientOut: Client

    """

    client = crud.get_client_by_id(session=session, client_id=client_id)
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    
    return client.get_score(credit_amount=10000000, base_amount=10000000)
