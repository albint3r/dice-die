# Imports
import datetime as dt
# DataBase
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
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
    win = Column(Integer)
    winner_name = Column(String(40))
    total_turns = Column(Integer)
    grid_result = relationship('GridsResult', backref='game_result', uselist=False)

    def __repr__(self):
        return f'GameResult=(id: {self.id}, p1_name: {self.p1_name}, p2_name: {self.p2_name}, win: {self.win}, winner_name: {self.winner_name})'

    def set_result_game(self, **kwargs):
        """Fill the Game Result Objet"""
        self.p1_name = kwargs.get('p1_name')
        self.p2_name = kwargs.get('p2_name')
        self.p1_score = kwargs.get('p1_score')
        self.p2_score = kwargs.get('p2_score')
        self.win = kwargs.get('win')
        self.winner_name = kwargs.get('winner_name')
        self.total_turns = kwargs.get('total_turns')

    def save(self):
        db.session.add(self)
        db.session.commit()


class GridsResult(db.base):
    __tablename__ = "gridresult"

    id = Column(Integer, primary_key=True, unique=True)
    date = Column(DateTime, default=dt.datetime.utcnow())
    # Player 1
    # Col1
    p1_row0_col1 = Column(Integer)
    p1_row1_col1 = Column(Integer)
    p1_row2_col1 = Column(Integer)
    # Col2
    p1_row0_col2 = Column(Integer)
    p1_row1_col2 = Column(Integer)
    p1_row2_col2 = Column(Integer)
    # Col3
    p1_row0_col3 = Column(Integer)
    p1_row1_col3 = Column(Integer)
    p1_row2_col3 = Column(Integer)
    # Player 2
    # Col1
    p2_row0_col1 = Column(Integer)
    p2_row1_col1 = Column(Integer)
    p2_row2_col1 = Column(Integer)
    # Col2
    p2_row0_col2 = Column(Integer)
    p2_row1_col2 = Column(Integer)
    p2_row2_col2 = Column(Integer)
    # Col3
    p2_row0_col3 = Column(Integer)
    p2_row1_col3 = Column(Integer)
    p2_row2_col3 = Column(Integer)
    match_id = Column(Integer, ForeignKey('gameresult.id'))

    def __repr__(self):
        return f'GridsResult(id: {self.id}, match_id: {self.match_id})'

    def set_result_grid(self, **kwargs):
        # Player 1
        # Col1
        self.p1_row0_col1 = kwargs.get('p1_row0_col1')
        self.p1_row1_col1 = kwargs.get('p1_row1_col1')
        self.p1_row2_col1 = kwargs.get('p1_row2_col1')
        # Col2
        self.p1_row0_col2 = kwargs.get('p1_row0_col2')
        self.p1_row1_col2 = kwargs.get('p1_row1_col2')
        self.p1_row2_col2 = kwargs.get('p1_row2_col2')
        # Col3
        self.p1_row0_col3 = kwargs.get('p1_row0_col3')
        self.p1_row1_col3 = kwargs.get('p1_row1_col3')
        self.p1_row2_col3 = kwargs.get('p1_row2_col3')
        # Player 2
        # Col1
        self.p2_row0_col1 = kwargs.get('p2_row0_col1')
        self.p2_row1_col1 = kwargs.get('p2_row1_col1')
        self.p2_row2_col1 = kwargs.get('p2_row2_col1')
        # Col2
        self.p2_row0_col2 = kwargs.get('p2_row0_col2')
        self.p2_row1_col2 = kwargs.get('p2_row1_col2')
        self.p2_row2_col2 = kwargs.get('p2_row2_col2')
        # Col3
        self.p2_row0_col3 = kwargs.get('p2_row0_col3')
        self.p2_row1_col3 = kwargs.get('p2_row1_col3')
        self.p2_row2_col3 = kwargs.get('p2_row2_col3')
        self.match_id = kwargs.get('match_id')

    def save(self):
        db.session.add(self)
        db.session.commit()


if __name__ == '__main__':
    # Create quick the database
    db.base.metadata.create_all(db.engine)

