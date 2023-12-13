import datetime

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import Integer, String, Boolean, ForeignKey, DateTime, func
from sqlalchemy.orm import mapped_column, Mapped

db = SQLAlchemy()
migrate = Migrate(db=db)

class LinkOffer(db.Model): # define link-offer db relation
    __tablename__ = "LinkOffer"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False)
    link: Mapped[str] = mapped_column(String, nullable=False)
    naviBar: Mapped[bool] = mapped_column(Boolean, nullable=False)
    offer: Mapped[str] = mapped_column(String, nullable=False)

class LinkStatistic(db.Model): # define statistic db relation
    __tablename__ = "LinkStatistic"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False)
    action: Mapped[str] = mapped_column(String, nullable=False)
    date: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    linkOffer = mapped_column(Integer, ForeignKey('LinkOffer.id'), nullable=False)
    linkstatistics = db.relationship("LinkOffer", backref='LinkStatistic', lazy=True)
