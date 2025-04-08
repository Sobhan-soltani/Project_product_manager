class InventoryManager:
    def __init__(self, product_id, product):
        self.product_id = product_id
        self.product = product
        self.products = []

    def add_product(self, product_name, product_id):

        product = {"name": product_name, "id": product_id}
        self.products.append(product)
        print(f"product '{product_name}' with id {product_id} added in warehouse.")

    def list_products(self):

        if not self.products:
            print("warehouse is empty.")
        else:
            print("warehouse inventory list:")
            for idx, product in enumerate(self.products, start=1):
                print(f"{idx}. name: {product['name']}, id: {product['id']}")
