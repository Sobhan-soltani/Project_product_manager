from datetime import datetime

from model import *

user = User(1, "ali","alipour", "2000-01-01", "1234567890", "09178505323", "ali", "ali123")
print(user)

product1 = Product(1, "mobile", "S24", "samsung", 1800, None)
product2 = Product(2, "laptop", "ROG", "asus", 2500, None)

print(product1)
print(product2)

item1 = OrderItem(1, product1, 3,1850)
item2 = OrderItem(2, product2,4,1950)

print(item1)
print(item2)

order = Order(1,user, datetime.now())
order.add_item(item1, item2)
print(order)
