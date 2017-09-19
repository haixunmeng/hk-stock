# encoding: utf-8
"""
@file: db.py
@time: 2017/6/27 14:51
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Float, String, DateTime, Date


engine = create_engine("mysql://%s:%s@%s:%s/%s?charset=utf8" % ('root', 'ict645', '127.0.0.1', '3306', 'hk_stock'), encoding="utf-8")
SessionCls = sessionmaker(bind=engine)
db_session = SessionCls()

Base = declarative_base()


class Evaluation(Base):
    __tablename__ = 'hk_stock_evaluation'
    id = Column(String, primary_key = True)
    stock_code = Column(String)
    stock_name = Column(String)
    department_code = Column(String)
    department_name = Column(String)
    eva_rank = Column(String)
    aim_price = Column(Float)
    time = Column(Date)
    url = Column(String)
    create_time = Column(DateTime)

    def __repr__(self):
        return "<Evaluation(stock_code=%s, stock_name=%s, department_code=%s, department_name=%s, eva_rank=%s, " \
               "aim_price=%s, time=%s, url=%s, create_time=%s)>" % \
               (self.stock_code,
                self.stock_name,
                self.department_code,
                self.department_name,
                self.eva_rank,
                self.aim_price,
                self.time,
                self.url,
                self.create_time)


def insert_department_eva(eva):
    try:
        db_session.add(eva)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    pass
