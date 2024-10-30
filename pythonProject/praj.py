from sqlalchemy import create_engine, Column, Integer, String, CHAR, ForeignKey, Sequence, column
from sqlalchemy.orm import sessionmaker,relationship,declarative_base,session

Base=declarative_base()
class Person(Base):
    __tablename__="people"
    ssn=Column("ssn",Integer,primary_key=True)
    firstname=Column("firstname",String)
    lastname=Column("lastname",String)
    gender=Column("gender",CHAR)
    age=Column("age",Integer)
    def __init__(self,ssn,firstname,lastname,gender,age):
        self.ssn=ssn
        self.firstname=firstname
        self.lastname=lastname
        self.gender=gender
        self.age=age
    def __repr__(self):
        return f"({self.ssn}) {self.firstname} {self.lastname} ({self.gender},{self.age})"

class Thing(Base):
    __tablename__="thing"
    pid=Column("pid",Integer,primary_key=True)
    description=Column("description",String)
    owner=Column(Integer,ForeignKey("people.ssn"))
    def __init__(self,pid,description,owner):
        self.pid=pid
        self.description=description
        self.owner=owner
    def __repr__(self):
        return f"({self.pid}) {self.description} owned by {self.owner}"

engine=create_engine("sqlite:///mydb2.db",echo=True)
Base.metadata.create_all(bind=engine)

Session=sessionmaker(bind=engine)
session=Session()

p1=Person(111,"praj","wal","m",26)
p2=Person(121,"dars","han","m",25)
p3=Person(131,"sher","yas","m",22)
t1=Thing(1,"laptop",p1.ssn)
t2=Thing(2,"mobile",p3.ssn)
t3=Thing(3,"ps5",p2.ssn)
session.add(p1)
session.add(p2)
session.add(p3)
session.add(t1)
session.add(t2)
session.add(t3)

session.commit()
#session.delete(p2)
#session.commit()
result=session.query(Thing,Person).filter(Thing.owner==Person.ssn).filter(Person.firstname=="praj").all()
for r in result:
    print(r)
update=session.query(Person).filter(Person.ssn==111).first()
if update:
    update.firstname="prajjjj"
    session.commit()
update2=session.query(Thing).filter(Thing.pid==2).first()
if update2:
    update2.description="iphone"
    session.commit()
update3=session.query(Thing).filter(Thing.pid==3).first()
if update3:
    update3.description="ps4"
    session.commit()
# Sort by firstname in ascending order
result_asc = session.query(Thing, Person).join(Person).filter(Thing.owner == Person.ssn).order_by(Person.firstname.asc()).all()
print("Ascending Order by Firstname:")
for r in result_asc:
    print(r)

# Sort by firstname in descending order
result_desc = session.query(Thing, Person).join(Person).filter(Thing.owner == Person.ssn).order_by(Person.firstname.desc()).all()
print("\nDescending Order by Firstname:")
for r in result_desc:
    print(r)
    delete = "surya"
    deletename = session.query(Employee).filter(Employee.ename == delete).first()

    session.delete(deletename)
    session.commit()