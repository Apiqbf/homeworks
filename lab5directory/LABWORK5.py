####БЛОК1

####1
class User:
    def __init__(self,id,name,email):
        if "@" not in email:
            raise ValueError("No @ sign in email!")
        self._id=int(id)
        self._name=name.strip().title()
        self._email=email.lower()
    def __str__(self):
        return f"User(id:{self._id},name-{self._name},email:{self._email})"
    def __del__(self):
        return f"User <{self._name}> удален"

    @classmethod
    def from_string(cls,data):
        parts=data.split(",")

        if len(parts)!=3:
            raise ValueError("Неверный формат строки!")

        id=parts[0]
        name=parts[1]
        email=parts[2]

        return cls(id,name,email)

####3
class Product:
    def __init__(self,id,name,price,category):
        self.id=int(id)
        self.name=name.title()
        self.price=float(price)
        self.category=category.title()
    def __hash__(self):
        return hash(self.id)
    def __eq__(self, other):
        return self.id==other.id
    def __str__(self):
        return f"Product(id:{self.id},name-{self.name},price:{self.price},category-{self.category})"
    def __repr__(self):
        return self.__str__()
    def to_dict(self):
        return {
            "id":self.id,
            "name":self.name,
            "price":self.price,
            "category":self.category
        }

    @staticmethod
    def list_to_dict(products):
        return {p.id:p.to_dict() for p in products}


####4
class Inventory:
    def __init__(self):
        self._products={}
    def add_product(self,product):
        if product.id not in self._products:
            self._products[product.id]=product
    def remove_product(self,product_id):
        if product_id in self._products:
            del self._products[product_id]
    def get_product(self,product_id):
        return self._products.get(product_id,None)
    def get_all_products(self):
        return list(self._products.values())
    def unique_products(self):
        return set(self._products.values())
    def to_dict(self):
        return dict(self._products)
    def filter_by_price(self,min_price: float):
        is_more=lambda p:p.price>=min_price
        return [p for p in self._products.values() if is_more(p)]










####6
from datetime import datetime
class Logger:
    def action_log(self,user,action,product,filename):
        ts=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line=f"{ts};{user._id};{action};{product.id}\n"

        with open(filename,"w",encoding="utf-8")as f:
            f.write(line)

    def read_logs(self,filename):
        self.result=[]

        with open(filename,"r",encoding="utf-8")as f:
            for line in f:
                parts=line.split(";")

                ts=parts[0]
                user_id=parts[1]
                action=parts[2]
                product_id=parts[3]

                self.result.append({
                    "timestamp":ts,
                    "user_id":user_id,
                    "action":action,
                    "product_id":product_id
                })

        return self.result


user3=User(3,"name3","email@3")

logger=Logger()
logger.action_log(user3,"purchase",Product(3,"phone",1000,"electronics"),"lab5.log")

####7
class Order:
    def __init__(self,id,user,products=None):
        self.id=id
        self.user=user
        self.products=products if products is not None else []
    def add_product(self,product):
        if product.id not in [p.id for p in self.products]:
            self.products.append(product)
    def remove_product(self,product_id):
        self.products=[p for p in self.products
                       if product_id!=p.id]
    def total_price(self):
        return sum(p.price for p in self.products)
    def most_expensive_products(self,n):
        is_exp=lambda p:p.price>=n
        return [p.name for p in self.products if is_exp(p)]

    def __str__(self):
        product_names=",".join(p.name for p in self.products)

        return (
            f"Order(id={self.id},"
            f"user={self.user._name},"
            f"products=[{product_names}],"
            f"total={self.total_price()}"
        )

user1=User(1,"name1","email@1")
user2=User(2,"name2","email@2")

products1=[Product(1,"laptop",1200,"electronics"),
           Product(2,"gloves",100,"clothes")]

products2=[Product(3,"phone",1000,"electronics"),
           Product(1,"laptop",1200,"electronics")]

order1=Order(1,user1,products1)
order2=Order(2,user2,products2)

order1.remove_product(2)
order2.add_product(Product(4,"tshirt",300,"clothes"))

print(f"total price of order1:{order1.total_price()}")
print(f"total price of order2:{order2.total_price()}")

print(order1)

####9
def price_stream(products):
    for product in products:
        yield product.price

products=[Product(101,"mouse",100,"electronics"),
          Product(102,"watch",1300,"accessorries"),
          Product(103,"t-shirt",300,"clothes")]


# prices=price_stream(products)
#
# for price in prices:
#     print(price)

####10
class OrderIterator:
    def __init__(self,orders):
        self._orders=orders
        self._index=0
    def __iter__(self):
        return self
    def __next__(self):
        if self._index>=len(self._orders):
            raise StopIteration
        order=self._orders[self._index]
        self._index+=1
        return order



# order_iterator=OrderIterator(orders)
#
# for order in order_iterator:
#     print(order)












####БЛОК 2
####11
import numpy as n
p1=Product(1,"Laptop",1200.0,"Electronics")
p2=Product(2,"Mouse",25.0,"Electronics")
p3=Product(3,"Чехол",450,"Accessories")

products = [p1,p2,p3]
prices=n.array([p.price for p in products])

####12
prices_mean=prices.mean()
prices_median=n.median(prices)

####13

####14
categories=n.array([p.category for p in products])

####15
#print("Уникальных категорий:",len(set(categories)))

####16
numpy_products=n.array([p for p in products])
higher_than_avg=numpy_products[prices>prices.mean()]

#print("Выше среднего:",higher_than_avg)

####17
#print("10% скидка:",prices*0.9)

####18
u1=User(1,"Maulid","maulid@email")
u2=User(2,"Damir","damir@email")
u3=User(3,"Nabi","nabi@email")

orders = [Order(1,u1,[Product(1,"Laptop",1200.0,"Electronics")]),
          Order(2,u2,[Product(2,"Mouse",25.0,"Electronics"), Product(1,"Laptop",1200.0,"Electronics")]),
          Order(3,u3,[Product(1,"Laptop",1200,"Electronics"),Product(3,"IPhone",500,"Electronics")])]

# def sum_of_prices(orders):
#     return n.array([[order.total_sum()] for order in orders])
#
# result=sum_of_prices(orders)

#print(result)

####19
#avg_price=result.mean()
#print(avg_price)

####20
def expensive_order_indices(totals,threshold) -> list:
    return list(n.where(totals > threshold)[0])

#print(expensive_order_indices(result,100))

####БЛОК 3
####21
import pandas as pd
from datetime import datetime

users = [User(1,"John Doe","john@example.com"),
         User(2,"Alice","alice@example.com")]

user_data=[]

for user in users:
    user_data.append({
        "id":user._id,
        "name":user._name,
        "email":user._email,
        "registration date":datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

users_df=pd.DataFrame(user_data)

####22
products = [Product(1,"Laptop",1200.0,"Electronics"),
            Product(2,"T-Shirt",20.0,"Clothing")]

product_data=[]

for p in products:
    product_data.append({
        "id":p.id,
        "name":p.name,
        "category":p.category,
        "price":p.price
    })

products_df=pd.DataFrame(product_data)

####23
# orders_df=pd.DataFrame({
#     "order_id":[101,102],
#     "user_id":[1,2],
#     "total":[1200,25]
# })
#
# users_df=users_df.drop(columns=["email","registration date"])
#
# merged_df=pd.merge(orders_df,
#                    users_df,
#                    left_on="name",
#                    right_on="total")
#
# #print(merged_df)