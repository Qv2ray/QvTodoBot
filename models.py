from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from db import session, Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    todo = relationship("Todo", backref="user")

    def insert(self) -> None:
        session.add(self)
        session.commit()

    def update(self) -> None:
        session.commit()

    def delete(self) -> None:
        session.delete(self)

    def __repr__(self) -> str:
        return f"user_id={self.user_id}, todo={self.todo}"


class Todo(Base):
    __tablename__ = "todo"

    id = Column(Integer, primary_key=True)
    item = Column(String)
    completed = Column(Boolean)
    user_id = Column(Integer, ForeignKey("user.id"))

    def insert(self) -> None:
        session.add(self)
        session.commit()

    def update(self) -> None:
        session.commit()

    def delete(self) -> None:
        session.delete(self)

    def __repr__(self) -> str:
        return f"item={self.item}, completed={self.completed}"
