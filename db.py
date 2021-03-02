from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy import Boolean

engine = create_engine('sqlite:///heartfailure.db')
connection = engine.connect()
session = sessionmaker(bind=engine)()
Base = declarative_base()

class Params(Base):
    
    __tablename__ = 'datas'
    
    id = Column(Integer, primary_key=True)
    age = Column(Integer)
    anaemia = Column(Integer)
    creatinine_phosphokinase = Column(Integer)
    diabetes = Column(Integer)
    ejection_fraction = Column(Integer)
    high_blood_pressure = Column(Integer)
    platelets = Column(Integer)
    serum_creatinine = Column(Float)
    serum_sodium = Column(Integer)
    sex = Column(Integer)
    smoking = Column(Integer)
    time = Column(Integer)
    diagnostic = Column(Float)

def createDb():
    Base.metadata.create_all(engine)
    return True

def addOneToDb(param, diag):
    d_rows = []
    d_rows.append(Params(age = param[0][0], anaemia = param[0][1],
    creatinine_phosphokinase = param[0][2], diabetes = param[0][3],
    ejection_fraction = param[0][4], high_blood_pressure = param[0][5],
    platelets = param[0][6], serum_creatinine = param[0][7],
    serum_sodium = param[0][8], sex = param[0][9],
    smoking = param[0][10], time = param[0][11], diagnostic = diag[0][1]))
    session.add_all(d_rows)
    session.commit()

def addManyToDb(param, diag):
    for par, dia in zip(param, diag):
        print(par)
        d_rows = []
        d_rows.append(Params(age = par[0], anaemia = par[1],
        creatinine_phosphokinase = par[2], diabetes = par[3],
        ejection_fraction = par[4], high_blood_pressure = par[5],
        platelets = par[6], serum_creatinine = par[7],
        serum_sodium = par[8], sex = par[9],
        smoking = par[10], time = par[11], diagnostic = dia[1]))
        session.add_all(d_rows)
        session.commit()