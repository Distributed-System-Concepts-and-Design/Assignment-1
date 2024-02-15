from random import random
import grpc
import market_pb2
import market_pb2_grpc
import uuid
import notifySeller_pb2
import notifySeller_pb2_grpc
from concurrent import futures


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



class SellerNotificationServicer(notifySeller_pb2_grpc.SellerNotificationServicer):
    def NotifySeller(self, request, context):
        print("\n------------------------------------------------")
        print("Received notification from market:")
        print("#######")
        print("Buyer has bought the following item. Its updated details are -:")
        print(f"Item ID: {request.itemId}")
        print(f"Price: ${request.price}")
        print(f"Name: {request.productName}")
        print(f"Category: {request.category}")
        print(f"Description: {request.description}")
        print(f"Quantity Remaining: {request.quantityRemaining}")
        print(f"Rating: {request.rating}")
        print(f"Seller: {request.sellerAddress}")
        print("--------------------------------------------------")

        return notifySeller_pb2.NotifySellerResponse(status=notifySeller_pb2.NotifySellerResponse.SUCCESS)



def mainMenu():
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


def get_random_port():
    return str(int(random()*1000) + 50055)


if __name__ == "__main__":
    SELLER_MARKET_PORT = '50051'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    notifySeller_pb2_grpc.add_SellerNotificationServicer_to_server(SellerNotificationServicer(), server)
    
    # Connecting to the market as a client
    seller = MarketSeller('localhost:'+SELLER_MARKET_PORT)
    sellerAddress = None
    sellerUUID = None
    SELLER_NOTIFICATION_PORT = '50052'


    print("-------------------------------------------------")
    print("        Welcome to the Seller platform!!         ")
    print("-------------------------------------------------")
    while True:
        try:
            choice = mainMenu()
            if choice == 1:
                # Initializing the seller notification server
                SELLER_NOTIFICATION_PORT = input("Enter the port number for running the Seller Notification Server: ")
                # SELLER_NOTIFICATION_PORT = get_random_port()
                sellerAddress = "localhost:"+SELLER_NOTIFICATION_PORT
                sellerUUID = str(uuid.uuid1())
                
                server.add_insecure_port('[::]:'+SELLER_NOTIFICATION_PORT)
                server.start()
                
                seller.register_seller(sellerAddress, sellerUUID)

            elif choice == 2:
                product_name = input("Enter product name: ")
                # category = input("Enter category: ")
                # quantity = int(input("Enter quantity: "))
                # description = input("Enter description: ")
                # price_per_unit = float(input("Enter price per unit: "))
                # product_name = "Orange Frooti"
                category = "OTHERS"
                quantity = 500
                description = "This is Frooti, a mongo drink"
                price_per_unit = 20
                seller.sell_item(product_name, category, quantity, description, sellerAddress, price_per_unit, seller_uuid=sellerUUID)
                print('---------------------------------------------------')

            elif choice == 3:
                item_id = int(input("Enter item ID: "))
                new_price = float(input("Enter new price: "))
                new_quantity = int(input("Enter new quantity: "))
                # item_id = 1
                # new_price = 29
                # new_quantity = 99
                seller.update_item(item_id, new_price, new_quantity, seller_address=sellerAddress, seller_uuid=sellerUUID)
                print('---------------------------------------------------')

            elif choice == 4:
                item_id = int(input("Enter item ID: "))
                # item_id = 1
                seller.delete_item(item_id, seller_address=sellerAddress, seller_uuid=sellerUUID)
                print('---------------------------------------------------')

            elif choice == 5:
                seller.display_seller_items(seller_address=sellerAddress, seller_uuid=sellerUUID)
                print('---------------------------------------------------')

            elif choice == 6:
                break
            else:
                print("Invalid choice")
        
            print("--------------------Main Menu---------------------")
            print("--------------------------------------------------")
        except Exception as e:
            print("Error:", e)
            break
