import grpc
import market_pb2
import market_pb2_grpc
import notifyBuyer_pb2
import notifyBuyer_pb2_grpc
from concurrent import futures


class MarketBuyer:
    def __init__(self, server_address):
        self.channel = grpc.insecure_channel(server_address)
        self.stub = market_pb2_grpc.SellerServiceStub(self.channel)


    def search_item(self, item_name="", item_category="ANY"):
        request = market_pb2.SearchItemRequest(
            itemName=item_name,
            itemCategory=item_category
        )
        response = self.stub.SearchItem(request)
        # print(f"Search request for Item name: '{item_name}', Category: '{item_category}'")
        category = {0 : "ELECTRONICS", 1 : "FASHION", 2: "OTHERS"}
        # print(item.category)
        for item in response.items:
            print("--")
            print("Item ID:", item.itemId)
            print("Price:", item.price)
            print("Name:", item.productName)
            print("Category:", category[item.category])
            print("Description:", item.description)
            print("Quantity Remaining:", item.quantityRemaining)
            print("Rating:", item.rating)
            print("Seller:", item.sellerAddress)
            print("--")


    def buy_item(self, item_id, quantity, buyer_address):
        request = market_pb2.BuyItemRequest(
            itemId=item_id,
            quantity=quantity,
            buyerAddress=buyer_address
        )
        response = self.stub.BuyItem(request)
        if response.status == market_pb2.BuyItemResponse.SUCCESS:
            print("SUCCESS")
        else:
            print("FAIL")


    def add_to_wishlist(self, item_id, buyer_address):
        request = market_pb2.AddToWishListRequest(
            itemId=item_id,
            buyerAddress=buyer_address
        )
        response = self.stub.AddToWishList(request)
        if response.status == market_pb2.AddToWishListResponse.SUCCESS:
            print("SUCCESS")
        else:
            print("FAIL")


    def rate_item(self, item_id, buyer_address, rating):
        if rating < 1 or rating > 5:
            print("Rating should be between 1 and 5")
            return
        elif type(rating) != int:
            print("Rating should be an integer")
            return
        
        request = market_pb2.RateItemRequest(
            itemId=item_id,
            buyerAddress=buyer_address,
            rating=rating
        )
        response = self.stub.RateItem(request)
        if response.status == market_pb2.RateItemResponse.SUCCESS:
            print("SUCCESS")
        else:
            print("FAIL")


class BuyerNotificationServicer(notifyBuyer_pb2_grpc.BuyerNotificationServicer):
    def NotifyBuyer(self, request, context):
        print("\nNOTIFICATION RECEIVED FROM THE MARKET -")
        print("#######")
        print("The Following Item has been updated:")
        print(f"Item ID: {request.itemId}")
        print(f"Price: ${request.price}")
        print(f"Name: {request.productName}")
        print(f"Category: {request.category}")
        print(f"Description: {request.description}")
        print(f"Quantity Remaining: {request.quantityRemaining}")
        print(f"Rating: {request.rating}")
        print(f"Seller: {request.sellerAddress}")
        print("------------------------------------------\n")
        mainMenu(takeChoice=False)
        return notifyBuyer_pb2.NotifyBuyerResponse(status=notifyBuyer_pb2.NotifyBuyerResponse.SUCCESS)


def mainMenu(takeChoice=True):
    print("\n1. Search Item")
    print("2. Rate Item")
    print("3. Buy Item")
    print("4. Add to Wishlist")
    print("5. Exit")
    print("-------------------------------------------------")
    if takeChoice:
        choice = int(input("Enter your choice: "))
        print("-------------------------------------------------\n")
        return choice
    return None



if __name__ == "__main__":
    BUYER_MARKET_PORT = "50051"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    notifyBuyer_pb2_grpc.add_BuyerNotificationServicer_to_server(BuyerNotificationServicer(), server)
    try:
        # Connecting to the market as a client
        # buyer = MarketBuyer('34.28.67.70:'+BUYER_MARKET_PORT)
        # buyer = MarketBuyer('localhost:'+BUYER_MARKET_PORT)
        market_address = input("Enter the external IP address of the Market: ")
        buyer = MarketBuyer(market_address+':'+BUYER_MARKET_PORT)

        # Initializing the buyer notification server
        BUYER_NOTIFICATION_PORT = input("Enter the port number for running the Buyer Notification Server: ")
        server.add_insecure_port('[::]:'+BUYER_NOTIFICATION_PORT)
        server.start()

        # buyer_address = "103.28.253.123:"+BUYER_NOTIFICATION_PORT
        # buyer_address = "localhost:"+BUYER_NOTIFICATION_PORT
        buyer_address = input("Enter the external IP address of the Buyer: ")
        buyer_address = buyer_address+':'+BUYER_NOTIFICATION_PORT
        
        print("-------------------------------------------------")
        print("         Welcome to the Buyer platform!!         ")
        print("-------------------------------------------------")

        while(True):
            choice = mainMenu()

            if choice == 1:
                item_name = input("Enter the item name: ")
                item_category = input("Enter the item category (ELECTRONICS, FASHION, OTHERS, ANY): ")
                print('---------------------------------------------------')
                buyer.search_item(item_name, item_category)

            elif choice == 2:
                item_id = int(input("Enter the item ID: "))
                rating = int(input("Enter the rating (1-5): "))
                print('---------------------------------------------------')
                buyer.rate_item(item_id, buyer_address, rating)

            elif choice == 3:
                item_id = int(input("Enter the item ID: "))
                quantity = int(input("Enter the quantity: "))
                print('---------------------------------------------------')
                buyer.buy_item(item_id, quantity, buyer_address)

            elif choice == 4:
                item_id = int(input("Enter the item ID: "))
                print('---------------------------------------------------')
                buyer.add_to_wishlist(item_id, buyer_address)

            elif choice == 5:
                break
            else:
                print("Invalid choice. Try again.")
            
            print("--------------------Main Menu---------------------")
            print("--------------------------------------------------")
    
    except Exception as e:
        server.stop(0)
        print("Buyer Has Quit the Platform.")

