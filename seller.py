from random import random
import grpc
import market_pb2
import market_pb2_grpc
import uuid

class MarketSeller:
    def __init__(self, server_address):
        self.channel = grpc.insecure_channel(server_address)
        self.stub = market_pb2_grpc.SellerServiceStub(self.channel)


    def register_seller(self, address, uuid):
        request = market_pb2.RegisterSellerRequest(
            address=address,
            uuid=uuid
        )
        response = self.stub.RegisterSeller(request)
        if response.status == market_pb2.RegisterSellerResponse.SUCCESS:
            print("SUCCESS")
        else:
            print("FAIL")


    def sell_item(self, product_name, category, quantity, description, seller_address, price_per_unit, seller_uuid):
        request = market_pb2.SellItemRequest(
            productName=product_name,
            category=category,
            quantity=quantity,
            description=description,
            sellerAddress=seller_address,
            pricePerUnit=price_per_unit,
            sellerUUID=seller_uuid
        )
        response = self.stub.SellItem(request)
        if response.status == market_pb2.SellItemResponse.SUCCESS:
            print("SUCCESS. Item ID:", response.itemId)
        else:
            print("FAIL")


    def update_item(self, item_id, new_price, new_quantity, seller_address, seller_uuid):
        request = market_pb2.UpdateItemRequest(
            itemId=item_id,
            newPrice=new_price,
            newQuantity=new_quantity,
            sellerAddress=seller_address,
            sellerUUID=seller_uuid
        )
        response = self.stub.UpdateItem(request)
        if response.status == market_pb2.UpdateItemResponse.SUCCESS:
            print("SUCCESS")
        else:
            print("FAIL")


    def delete_item(self, item_id, seller_address, seller_uuid):
        request = market_pb2.DeleteItemRequest(
            itemId=item_id,
            sellerAddress=seller_address,
            sellerUUID=seller_uuid
        )
        response = self.stub.DeleteItem(request)
        if response.status == market_pb2.DeleteItemResponse.SUCCESS:
            print("SUCCESS")
        else:
            print("FAIL")


    def display_seller_items(self, seller_address, seller_uuid):
        request = market_pb2.DisplaySellerItemsRequest(
            sellerAddress=seller_address,
            sellerUUID=seller_uuid
        )
        response = self.stub.DisplaySellerItems(request)
        # print(f"Display Items request from {seller_address}")

        for item in response.items:
            print("--")
            print("Item ID:", item.itemId)
            print("Product Name:", item.productName)
            print("Price:", item.price)
            category = {0 : "ELECTRONICS", 1 : "FASHION", 2: "OTHERS"}
            print("Category:", category[item.category])
            print("Description:", item.description)
            print("Quantity Remaining:", item.quantityRemaining)
            print("Seller Address:", item.sellerAddress)
            print("Rating:", item.rating)
            print("--")


    def getRandomAddress(self, port):
        # randomly generate a unique IP address
        address = "192.13." + str(int(random()*256)) + '.' + str(int(random()*256)) + ":" + port
        # generate UUID of the seller randomly
        uuid_seller = str(uuid.uuid1())
        return address, uuid_seller


def mainMenu():
    print("-------------------------------------------------")
    print("        Welcome to the Seller platform!!         ")
    print("-------------------------------------------------")
    print("\n1. Register Seller")
    print("2. Sell Item")
    print("3. Update Item")
    print("4. Delete Item")
    print("5. Display Seller Items")
    print("6. Exit")
    print("-------------------------------------------------")
    choice = int(input("Enter your choice: "))
    print("-------------------------------------------------\n")
    return choice


def demo():
    for _ in range(3):
        address, uuid_seller = seller.getRandomAddress(port)
        credentials.append([address, uuid_seller])
        seller.register_seller(address, uuid_seller)
    
    # seller.sell_item(product_name="iPhone", category="ELECTRONICS", quantity=5, description="This is iPhone 15.", seller_address=address, price_per_unit=5000, seller_uuid=uuid_seller)
    # seller.update_item(item_id=1, new_price=6000, new_quantity=3, seller_address=address, seller_uuid=uuid_seller)
    # seller.display_seller_items(address, uuid_seller)
    seller.sell_item(product_name="iPhone", category="ELECTRONICS", quantity=5, description="This is iPhone 15.", seller_address=credentials[0][0], price_per_unit=5000, seller_uuid=credentials[0][1])
    seller.sell_item(product_name="Samsung", category="ELECTRONICS", quantity=5, description="This is Samsung 15.", seller_address=credentials[0][0], price_per_unit=5000, seller_uuid=credentials[0][1])
    # seller.sell_item(product_name="iPhone", category="ELECTRONICS", quantity=5, description="This is iPhone 15.", seller_address=credentials[0][0], price_per_unit=5000, seller_uuid=credentials[0][1])
    # seller.sell_item(product_name="Nokia", category="FASHION", quantity=5, description="This is iPhone 15.", seller_address=credentials[1][0], price_per_unit=5000, seller_uuid=credentials[1][1])
    # seller.sell_item(product_name="Lumia", category="OTHERS", quantity=5, description="This is iPhone 15.", seller_address=credentials[1][0], price_per_unit=5000, seller_uuid=credentials[1][1])
    
    # seller.update_item(item_id=1, new_price=6000, new_quantity=3, seller_address=credentials[0][0], seller_uuid=credentials[0][1])
    # seller.display_seller_items(seller_address=credentials[2][0], seller_uuid=credentials[2][1])
    # seller.display_seller_items(seller_address=credentials[1][0], seller_uuid=credentials[1][1])
    # seller.display_seller_items(seller_address=credentials[0][0], seller_uuid=credentials[0][1])

    # seller.delete_item(item_id=5, seller_address=credentials[1][0], seller_uuid=credentials[1][1])
    # # ISSUE: The itemID is not bbeing managed from anyone.


def get_seller_info(credentials):
    available_sellers = []
    print("Available sellers: ")
    id = 1
    for key, value in credentials.items():
        print(f'{id}.', key.split('#')[0])
        available_sellers.append([key.split('#')[1], value[1]])
        id += 1
    try:
        # seller_choice = int(input("Enter seller choice: "))
        seller_choice = 1
        cred_address, cred_uuid = available_sellers[seller_choice-1][0], available_sellers[seller_choice-1][1]
        print('Address:', cred_address, 'UUID:', cred_uuid)
    except:
        cred_address = input("Enter seller address: ")
        cred_uuid = input("Enter seller UUID: ")
    print()
    return cred_address, cred_uuid


# Example usage
if __name__ == "__main__":
    seller = MarketSeller('localhost:50051')
    port = '5051'
    credentials = {}
    while True:
        # choice = mainMenu()
        choice = 5
        if choice == 1:
            address, uuid_seller = seller.getRandomAddress(port)
            # seller_name = input("Enter seller name: ")
            seller_name = "Sufyan"
            # ip = input("Enter IP address: ")
            # port = input("Enter port: ")
            # address = ip + ":" + port
            # uuid_seller = str(uuid.uuid1())
            credentials[seller_name+'#'+address] = [address, uuid_seller]
            seller.register_seller(address, uuid_seller)
            choice = 2

        if choice == 2:
            cred_address, cred_uuid = get_seller_info(credentials)
            
            # product_name = input("Enter product name: ")
            # category = input("Enter category: ")
            # quantity = int(input("Enter quantity: "))
            # description = input("Enter description: ")
            # price_per_unit = int(input("Enter price per unit: "))
            product_name = "Orange Frooti"
            category = "OTHERS"
            quantity = 500
            description = "This is Frooti, a mongo drink"
            price_per_unit = 20
            seller.sell_item(product_name, category, quantity, description, cred_address, price_per_unit, cred_uuid)
            choice = 3

        if choice == 3:
            cred_address, cred_uuid = get_seller_info(credentials)
            # cred_address = '192.13.79.14:5051'
            # cred_uuid = 'a4d12ce9-c9f4-11ee-b059-902e16f01b50'
            # item_id = int(input("Enter item ID: "))
            # new_price = int(input("Enter new price: "))
            # new_quantity = int(input("Enter new quantity: "))
            item_id = 1
            new_price = 29
            new_quantity = 99
            seller.update_item(item_id, new_price, new_quantity, cred_address, cred_uuid)
            choice = 5

        if choice == 4:
            cred_address, cred_uuid = get_seller_info(credentials)
            # item_id = int(input("Enter item ID: "))
            item_id = 1
            seller.delete_item(item_id, cred_address, cred_uuid)
            choice = 5

        if choice == 5:
            # cred_address, cred_uuid = get_seller_info(credentials)
            cred_address = '192.13.216.86:5051'
            cred_uuid = 'fa01f6bc-c9fd-11ee-bca1-902e16f01b50'
            # cred_address = '192.13.113.161:5051'
            # cred_uuid = 'e2fe5216-c9f7-11ee-98e4-902e16f01b50'
            # cred_address = '192.13.116.44:5051'
            # cred_uuid = 'e3dd4a19-c9f7-11ee-ba4d-902e16f01b50'
            seller.display_seller_items(cred_address, cred_uuid)
            choice = 6

        if choice == 6:
            break
        else:
            print("Invalid choice")
