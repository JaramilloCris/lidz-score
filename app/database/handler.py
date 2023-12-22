from sqlalchemy.orm import declarative_base, sessionmaker

import sqlalchemy as db

def init_db(db_user, db_pass, db_host, db_name):
    """
    Initialize the database connection

    Args:
        db_user (str): Database user
        db_pass (str): Database password
        db_host (str): Database host
        db_name (str): Database name

    Returns:
        tuple: Tuple containing the base, session and engine    
    """

    Base = declarative_base()
    engine = db.create_engine(f'mysql://{db_user}:{db_pass}@{db_host}/{db_name}')
    Session = sessionmaker(bind=engine)
    session = Session()

    return Base, session, engine