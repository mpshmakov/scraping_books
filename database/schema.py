"""
Database schema module.

This module defines the SQLAlchemy ORM models for the database tables.
"""

from sqlalchemy import CheckConstraint, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class AcademyAwardWinningFilms(Base):
    """
    SQLAlchemy ORM model for the academy_award_winning_films table.
    """

    __tablename__ = "academy_award_winning_films"

    id = Column(String(36), primary_key=True)
    film = Column(String(255), nullable=False)
    year = Column(Integer, nullable=True)
    awards = Column(Integer, nullable=True)
    nominations = Column(Integer, nullable=True)

    __table_args__ = (CheckConstraint("year >= 1888", name="check_year"),)

    def __init__(self, id: str, film: str, year=None, awards=None, nominations=None):
        """
        Initialize an AcademyAwardWinningFilms instance.

        Args:
            id (str): Unique identifier for the film.
            film (str): Name of the film.
            year (int, optional): Year of the award.
            awards (int, optional): Number of awards won.
            nominations (int, optional): Number of nominations received.
        """
        self.id = id
        self.film = film
        self.year = year
        self.awards = awards
        self.nominations = nominations


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
