from __future__ import annotations

from app.database import Base
from datetime import datetime, timedelta
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    DateTime,
)

import math


class Client(Base):

    """
    Client model

    Args:
        Base (Base): Base class from sqlalchemy

    Attributes:

        id (int): Client id 
        name (str): Client name
        rut (str): Client rut
        salary (int): Client salary
        savings (int): Client savings
        messages (list[Message]): List of messages sent by the client
        debts (list[Debts]): List of debts of the client

    """


    __tablename__ = "client"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    rut = Column(String(255), nullable=False)
    salary = Column(Integer, nullable=False)
    savings = Column(Integer, nullable=False)
    messages = relationship("Message", backref="client")
    debts = relationship("Debts", backref="client")

    def follow_up(self):
        """
        Returns true if the client has sent a message in the 7 days after today

        Returns:
            bool: True if the client has sent a message in the 7 days after today
        """

        current_time = datetime.now()
        for message in self.messages:
            time_difference = current_time - message.sentAt
            if time_difference > timedelta(days=7):
                return True
        return False

    def messages_score(self):
        """
        Returns the score of the client based on the quantity of messages sent

        Returns:
            int: The score of the client based on the quantity of messages sent

        """

        quantity_messages = sum(
            1 for message in self.messages if message.role == "client"
        )
        if quantity_messages == 0:
            return 0

        decrement_factor = 0.5
        max_score = 100
        score = max_score / (
            1 + (math.exp(-decrement_factor * ((quantity_messages - 1))))
        )
        return math.floor(score)

    def savings_score(self, base_amount: int):
        """
        Returns the score of the client based on the savings

        Args:
            base_payment (int): The base payment of the credit

        Returns:    
            int: The score of the client based on the savings

        """

        max_score = 100

        # We will assume that the user has to have saved the initial payment for the full score 
        score_factor = self.savings / base_amount
        score_factor = min(1, score_factor)
        score = max_score * score_factor
        return math.floor(score)

    def salary_score(self, credit_amount: int):
        
        """
        Returns the score of the client based on the salary
        
        Args:
            credit_amount (int): The amount of credit that the client is requesting

        Returns:
            int: The score of the client based on the salary
        
        """
        max_score = 100

        # We assume that the loan will be paid in 300 payments (25 years).
        quota = credit_amount / 300
        # We assume that the ideal is that the credit installment does not exceed 30% of the salary
        score_factor = (self.salary * 0.3) / quota
        score_factor = min(1, score_factor)

        score = max_score * score_factor
        return math.floor(score)

    def debts_date_score(self):

        """
        Returns the score of the client based on the debts due date

        Returns:
            int: The score of the client based on the debts due date
        
        """
        max_score = 100
        score = 0
        for debt in self.debts:
            time_difference = datetime.now() - debt.dueDate
            if time_difference > timedelta(days=30):
                score += time_difference.days
        decrement_factor = -0.001
        score = max_score / (math.exp(-decrement_factor * score))
        return math.floor(score)

    def debts_mount_score(self):

        """
        Returns the score of the client based on the debts amount

        Returns:
            int: The score of the client based on the debts amount
        
        """        
        max_score = 100
        total_debt_amount = 0
        for debt in self.debts:
            time_difference = datetime.now() - debt.dueDate
            if time_difference > timedelta(days=30):
                total_debt_amount += debt.amount
        decrement_factor = -0.0000001
        score = max_score / (math.exp(-decrement_factor * total_debt_amount))
        return math.floor(score)
    
    def get_score(self, credit_amount: int, base_amount: int):

        """
        Returns the score of the client

        Args:
            credit_amount (int): The amount of credit that the client is requesting
            base_payment (int): The base payment of the credit

        Returns:
            int: The score of the client
        
        """
        score = (
            self.messages_score() * 0.1
            + self.savings_score(base_amount=base_amount) * 0.3
            + self.salary_score(credit_amount=credit_amount) * 0.3
            + self.debts_date_score() * 0.1
            + self.debts_mount_score() * 0.2
        )
        return math.floor(score)


class Message(Base):

    """
    Message model

    Args:
        Base (Base): Base class from sqlalchemy

    Attributes:
    
            id (int): Message id
            text (str): Message text
            role (str): Message role (client or advisor)
            sentAt (DateTime): Message sent date
            client_id (int): Client id

    """

    __tablename__ = "message"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(255), nullable=False)
    role = Column(String(255), nullable=False)
    sentAt = Column(DateTime, nullable=False)
    client_id = Column(Integer, ForeignKey("client.id"))


class Debts(Base):

    """
    Debts model

    Args:
        Base (Base): Base class from sqlalchemy

    Attributes:
        
        id (int): Debt id
        institution (str): Debt institution
        amount (int): Debt amount
        dueDate (DateTime): Debt due date
        client_id (int): Client id
    
    """

    __tablename__ = "debts"
    id = Column(Integer, primary_key=True, index=True)
    institution = Column(String(255), nullable=False)
    amount = Column(Integer, nullable=False)
    dueDate = Column(DateTime, nullable=False)
    client_id = Column(Integer, ForeignKey("client.id"))
