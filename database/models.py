# Imports
import datetime as dt
# DataBase
from sqlalchemy import Column, Integer, String, Boolean, DateTime
# Project Modules
from database.database_game import DataBaseGame

db = DataBaseGame()


class GameResult(db.base):
    __tablename__ = "gameresult"

    id = Column(Integer, primary_key=True, unique=True)
    date = Column(DateTime, default=dt.datetime.utcnow())
    p1_name = Column(String(40))
    p2_name = Column(String(40))
    p1_score = Column(Integer)
    p2_score = Column(Integer)
    p1_win = Column(Boolean)
    total_turns = Column(Integer)

    def __init__(self):
        db.base.metadata.create_all(db.engine)

    def set_result_game(self, **kwargs):
        """Fill the Game Result Objet"""
        self.p1_name = kwargs.get('p1_name')
        self.p2_name = kwargs.get('p2_name')
        self.p1_score = kwargs.get('p1_score')
        self.p2_score = kwargs.get('p2_score')
        self.p1_win = kwargs.get('p1_win')
        self.total_turns = kwargs.get('p1_win')

    def save(self):
        db.session.add(self)
        db.session.commit()

