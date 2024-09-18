"""
Database schema module.
This module defines the SQLAlchemy ORM models for the database tables.
"""

from sqlalchemy import DECIMAL, CheckConstraint, Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Books(Base):
    """
    SQLAlchemy ORM model for the books table.
    """

    __tablename__ = "books"

    id = Column(String(36), primary_key=True)
    title = Column(String(255), nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    availability = Column(Integer, nullable=False)
    star_rating = Column(Integer, nullable=True)
    category = Column(String(70), nullable=False)

    __table_args__ = (
        CheckConstraint("price >= 0", name="check_price"),
        CheckConstraint("availability >= 0", name="check_availability"),
        CheckConstraint(
            "star_rating >= 0 AND star_rating <= 5", name="check_star_rating"
        ),
    )

    def __init__(
        self,
        id: str,
        title: str,
        price: float,
        availability: int,
        star_rating: int,
        category: str,
    ):
        """
        Initialize a Books instance.

        Args:
            id (str): Unique identifier for the book.
            title (str): Title of the book.
            price (float): Price of the book.
            availability (int): Number of copies available.
            star_rating (float, optional): Star rating of the book (0 to 5).
            category (str): Category of the book.
        """
        self.id = id
        self.title = title
        self.price = price
        self.availability = availability
        self.star_rating = star_rating
        self.category = category


class TestTable(Base):
    """
    SQLAlchemy ORM model for the TestTable.
    """

    __tablename__ = "TestTable"

    id = Column(String(36), primary_key=True)
    text = Column(String(255), nullable=False)

    def __init__(self, id: str, text: str):
        """
        Initialize a TestTable instance.

        Args:
            id (str): Unique identifier for the test entry.
            text (str): Text content for the test entry.
        """
        self.id = id
        self.text = text
