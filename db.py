from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy_imageattach.entity import Image, image_attachment
from sqlalchemy.orm import sessionmaker, relationship


engine = create_engine('sqlite:///database.db', echo=False)
Base = declarative_base()
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

class Shop(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    header = Column(String)
    text = Column(String)
    price = Column(Integer)
    avaliable = Column(Boolean) 
    #picture = image_attachment('ProductPicture')

    def add_product(self, header:str, text:str, price:int, avaliable:bool):
        new_data = Shop(header=header, text=text, price=price, avaliable=avaliable)
        session.add(new_data)
        session.commit()
    
    def check_shop(self):
        shares = session.query(Shop)
        shares = [x.serialize for x in shares.all()]
        return shares
    
    @property
    def serialize(self) -> dict:
        return {
            'header': self.header,
            'text': self.text,
            'price': self.price,
            'avaliable': self.avaliable,
            'id' : self.id,
        }    
        
    def __repr__(self):
       return "<User(user_id='%s', balance'%s' %s %s)>" % (
                               self.header, self.text, self.avaliable, self.price)

# class ProductPicture(Base, Image):
#     __tablename__ = 'product_picture'
#     product_id = Column(Integer, ForeignKey('product.id'), primary_key=True)
#     product = relationship('Shop')


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    balance = Column(String)

    def __repr__(self):
       return "<User(user_id='%s', balance'%s')>" % (
                               self.user_id, self.balance)