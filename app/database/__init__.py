from app.database.handler import init_db
from app.config import USER, PASS, HOST, DATABASE_NAME
import sqlalchemy as db

Base, session, engine = init_db(USER, PASS, HOST, DATABASE_NAME)