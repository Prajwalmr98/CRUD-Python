from sqlalchemy import create_engine, Integer, String, CHAR, ForeignKey, Column, Sequence, column
from sqlalchemy.orm import sessionmaker, relationship, declarative_base, Session


Base=declarative_base()

class Person(Base):
    __tablename__='people'
    ssn=Column("ssn",Integer,primary_key=True)
    firstname=Column("firstname",String)
    lastname=Column("lastname",String)
    gender=Column("gender",CHAR)
    age=Column("age",Integer)
    def __init__(self,ssn,first,last,gender,age):
        self.ssn=ssn
        self.firstname=first
        self.lastname=last
        self.gender=gender
        self.age=age
    def __repr__(self):
        return f"({self.ssn}) {self.firstname} {self.lastname}({self.gender},{self.age})"

class Thing(Base):
    __tablename__="things"
    tid=Column("tid",Integer,primary_key=True)
    description =Column("description",String)
    owner=Column(Integer,ForeignKey("people.ssn"))
    def __init__(self,tid,description,owner):
        self.tid=tid
        self.description=description
        self.owner=owner
    def __repr__(self):
        return f"({self.tid}) {self.description} owned by{self.owner}"


engine=create_engine("sqlite:///mydb.db",echo=True)
Base.metadata.create_all(bind=engine)

Session=sessionmaker(bind=engine)
session=Session()

person=Person(111,"prajju","gowda","m",26)
session.add(person)
session.commit()

p1=Person(121,"darsu","achari","m",24)
p2=Person(131,"barsu","achari","m",27)
p3=Person(141,"garsu","sing","m",28)

session.add(p1)
session.add(p2)
session.add(p3)
session.commit()

t1=Thing(1,"laptop",p1.ssn)
t2=Thing(2,"mobile",p2.ssn)
t3=Thing(3,"ps5",p3.ssn)
t4=Thing(4,"earbuds",person.ssn)

session.add(t1)
session.add(t2)
session.add(t3)
session.add(t4)
session.commit()
result=session.query(Thing,Person).filter(Thing.owner==Person.ssn).filter(Person.firstname =="prajju").all()
for r in result:
    print(r)



