from tkinter.constants import FIRST

from sqlalchemy import column, Integer, String, CHAR, Sequence, ForeignKey, create_engine, Column, except_,func
from sqlalchemy.orm import declarative_base,relationship,session,sessionmaker

Base=declarative_base()
class Employee(Base):
    __tablename__="emp"
    eid=Column("eid",Integer,primary_key=True)
    ename=Column("ename",String)
    esal=Column("esal",Integer)
    dnum=Column(Integer,ForeignKey("dept.deptno"))
    def __init__(self,eid,ename,esal,dnum):
        self.eid=eid
        self.ename=ename
        self.esal=esal
        self.dnum=dnum
    def __repr__(self):
        return f"({self.eid}) {self.ename} {self.dnum}"
class Department(Base):
    __tablename__="dept"
    loc=Column("loc",String,nullable=False)
    dname=Column("dname",String)
    deptno=Column(Integer,primary_key=True)
    def __init__(self,loc,dname,deptno):
        self.loc=loc
        self.dname=dname
        self.deptno=deptno
    def __repr__(self):
        return f"({self.loc}) {self.dname} owned by {self.deptno}"

engine=create_engine("sqlite:///db3.db",echo=True)
Base.metadata.create_all(bind=engine)

Session=sessionmaker(bind=engine)
session=Session()

try:
    e1=Employee(1,"virat",100,10)
    e2=Employee(2,"rohit",90,20)
    e3=Employee(3,"jadeja",80,30)
    e4=Employee(4,"surya",50,20)
    d1=Department("banglore","batsman",10)
    d2=Department( "mumbai","captain",20)
    d3=Department( "chennai","spinner",30)
    session.add_all([e1,e2,e3,e4,d1,d2,d3])
    session.commit()
except Exception as e:
    session.rollback()
    print(f"an error occured: {e}")
finally:
    session.close()

session=Session()
result=session.query(Employee,Department).filter(Employee.dnum==Department.deptno).filter(Employee.eid==1).all()
for r in result:
       print(r)

update=session.query(Employee).filter(Employee.eid==1).first()
if update:
    update.esal=150
    session.commit()
maximum=session.query(func.max(Employee.esal)).scalar()
print(f" max sal is: {maximum}")
minimum=session.query(func.min(Employee.esal)).scalar()
print(f"the min sal is: {minimum}")
avg=session.query(func.avg(Employee.esal)).scalar()
print(f"the avg sal is: {avg}")
sum=session.query(func.sum(Employee.esal)).scalar()
print(f"the total sal is: {sum}")
count=session.query(func.count(Employee.eid)).scalar()
print(f"the total employee is: {count}")
def delete_employee_by_ename(ename):
    session = Session()
    try:
        employee_to_delete = session.query(Employee).filter(Employee.ename == ename).first()
        if employee_to_delete:
            session.delete(employee_to_delete)
            session.commit()
            print(f"Deleted employee with eid: {ename}")
        else:
            print(f"No employee found with eid: {ename}")
    except Exception as e:
        session.rollback()
        print(f"An error occurred while deleting employee: {e}")
    finally:
        session.close()
delete_employee_by_ename("surya")
