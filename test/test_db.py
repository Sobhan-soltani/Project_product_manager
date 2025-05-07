from repository.user_repository import UserRepository
from repository.product_repository import ProductRepository
from service.auth_service import AuthService
from service.product_service import ProductService

# Initialize repositories
user_repo = UserRepository()
product_repo = ProductRepository(user_repo.conn)

# Initialize services
auth_service = AuthService(user_repo)
product_service = ProductService(product_repo, user_repo)

# Test signup
user_id = None
try:
    user_id = auth_service.signup("John", "Doe", "1990-01-01", "1234567890", "1234567890", "johndoe", "password123")
    print(f"Created user with ID: {user_id}")
except Exception as e:
    print(f"Signup failed: {e}")

# Test login (as a fallback to get user_id if signup fails due to existing user)
user = auth_service.login("johndoe", "password123")
if user:
    print(f"Logged in user: {user}")
    user_id = user.id  # Use the user ID from login
else:
    print("Login failed")
    user_repo.close()
    exit(1)  # Exit if login fails, as we can't proceed without a user

# Test adding a product
try:
    product_id = product_service.add_product("Electronics", "Laptop", "Dell", 999.99, 10, "2025-12-31", user_id)
    print(f"Created product with ID: {product_id}")
except Exception as e:
    print(f"Add product failed: {e}")
    user_repo.close()
    exit(1)

# Test retrieving products
try:
    products = product_service.get_user_products(user_id)
    for p in products:
        print(p)
except Exception as e:
    print(f"Get products failed: {e}")
    user_repo.close()
    exit(1)

# Test purchasing a product
try:
    product, total_cost = product_service.purchase_product(product_id, 2)
    print(f"Purchased 2 units of {product.name}. Total cost: ${total_cost:.2f}")
    print(f"Updated product: {product}")
except Exception as e:
    print(f"Purchase failed: {e}")
    user_repo.close()
    exit(1)

# Clean up
user_repo.close()