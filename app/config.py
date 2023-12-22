from dotenv import dotenv_values

config = dotenv_values(".env")  

USER=config.get('USER')
PASS=config.get('PASS')
HOST=config.get('HOST')
DATABASE_NAME=config.get('DATABASE_NAME')

ORIGINS: list = [
    "*"
]