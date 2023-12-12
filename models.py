from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

db = SQLAlchemy()

class LinkOffer(db.Model): # define link-offer db relation
    __tablename__ = "LinkOffer"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False)
    link: Mapped[str] = mapped_column(String, nullable=False)
    naviBar: Mapped[bool] = mapped_column(Boolean, nullable=False)
    offer: Mapped[str] = mapped_column(String, nullable=False)

class LinkStatistic(): # define statistic db relation
    __tablename__ = "LinkStatistic"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False)
    action: Mapped[str] = mapped_column(String, nullable=False)
    linkOffer = mapped_column(Integer, ForeignKey('linkoffer.id'), nullable=False)
    linkstatistics = db.relationship("LinkOffer", backref='LinkStatistic', lazy=True)
