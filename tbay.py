from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('postgresql://ubuntu:thinkful@localhost:5432/tbay')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)

    items = relationship("Item", backref="owner")
    bids = relationship("Bid", backref="bidder")


class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    start_time = Column(DateTime, default=datetime.utcnow)

    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    bids = relationship("Bid", backref="item")


class Bid(Base):
    __tablename__ = 'bids'
    id = Column(Integer, primary_key=True)
    price = Column(Float, nullable=False)

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    item_id = Column(Integer, ForeignKey('items.id'), nullable=False)


Base.metadata.create_all(engine)


# Add three users to the database
print("Three users added to the database")
pogi = User(username="Pogi Puppy", password="chickentreats")
tom = User(username="Tom Moochie", password="carnut")
alex = User(username="Alex Nedloh", password="pythonnut")
session.add_all([pogi, tom, alex])
session.commit()

# Make one user auction a baseball
print("Item baseball, owned by tom added to the database")
baseball = Item(name="baseball", description="Mickey Mantle memorabilia", owner=tom)
print("baseball.owner.username", baseball.owner.username)
session.add(baseball)
session.commit()

# Have each other user place two bids on the baseball
print("Two people bid on baseball.")
alexbid = Bid(price=45, item=baseball, bidder=alex)
pogibid = Bid(price=50, item=baseball, bidder=pogi)
session.add_all([alexbid, pogibid])
session.commit()

# Perform a query to find out which user placed the highest bid
maxbid = baseball.bids[0].price
maxbidder = baseball.bids[0].bidder.username
for bid in baseball.bids:
    print("{} bid {} on the baseball".format(bid.bidder.username, bid.price))
    if bid.price > maxbid:
        maxbid = bid.price
        maxbidder = bid.bidder.username
print("The highest bidder is {} with a bid of {}.".format(maxbidder, maxbid))