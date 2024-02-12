import grpc
from concurrent import futures
import time
import market_pb2
import market_pb2_grpc

_ONE_DAY_IN_SECONDS = 24 * 60 * 60

class MarketServicer(market_pb2_grpc.SellerServiceServicer): # market_pb2_grpc.NotifyClientServicer):

    def __init__(self):
        # Initialize data structures or any other necessary setup
        self.items = {}  # Placeholder for item data
        self.sellers = {}  # Placeholder for registered sellers
        self.item_id = 0
        self.wishlist = {} # Placeholder for wishlist data


    # SellerService implementations
    def RegisterSeller(self, request, context):
        print(f"Seller join request from {request.address}, uuid = {request.uuid}")

        if request.address in self.sellers:
            print("ERROR: Seller already present")
            return market_pb2.RegisterSellerResponse(status=market_pb2.RegisterSellerResponse.FAILED)

        self.sellers[request.address] = request.uuid
        return market_pb2.RegisterSellerResponse(status=market_pb2.RegisterSellerResponse.SUCCESS)


    def SellItem(self, request, context):
        print(f"Sell Item request from {request.sellerAddress}")

        if request.sellerAddress not in self.sellers.keys():
            print("ERROR: Seller not registered")
            return market_pb2.SellItemResponse(status=market_pb2.SellItemResponse.FAILED)
        elif request.sellerUUID != self.sellers[request.sellerAddress]:
            print("ERROR: Seller UUID does not match")
            return market_pb2.SellItemResponse(status=market_pb2.SellItemResponse.FAILED)

        # Add item to inventory
        # self.item_id = self.item_id + 1
        # seller_item = {
        #     "productName": request.productName,
        #     "category": request.category,
        #     "quantity": request.quantity,
        #     "description": request.description,
        #     "sellerAddress": request.sellerAddress,
        #     "pricePerUnit": request.pricePerUnit,
        #     "rating": 0  # Placeholder for rating
        # }
        # A seller can not sell the same item twice        
        # self.items[self.item_id] = seller_item
        return market_pb2.SellItemResponse(status=market_pb2.SellItemResponse.SUCCESS, itemId=self.item_id, rating=0)


    def UpdateItem(self, request, context):
        print(f"Update Item {request.itemId} request from {request.sellerAddress}")

        if (request.sellerAddress not in self.sellers.keys()):
            print("ERROR: Seller not registered")
            return market_pb2.UpdateItemResponse(status=market_pb2.UpdateItemResponse.FAILED)
        elif (request.itemId not in self.items):
            print("ERROR: Item not found")
            return market_pb2.UpdateItemResponse(status=market_pb2.UpdateItemResponse.FAILED)
        elif (self.items[request.itemId]["sellerAddress"] != request.sellerAddress):
            print(f"ERROR: Seller {request.sellerAddress} does not own the item")
            return market_pb2.UpdateItemResponse(status=market_pb2.UpdateItemResponse.FAILED)
        elif (request.sellerUUID != self.sellers[request.sellerAddress]):
            print("ERROR: Seller UUID does not match")
            return market_pb2.UpdateItemResponse(status=market_pb2.UpdateItemResponse.FAILED)
        elif (request.newQuantity < 0):
            print("ERROR: Quantity can not be negative")
            return market_pb2.UpdateItemResponse(status=market_pb2.UpdateItemResponse.FAILED)
        elif (request.newPrice < 0):
            print("ERROR: Price can not be negative")
            return market_pb2.UpdateItemResponse(status=market_pb2.UpdateItemResponse.FAILED)
        
        # Update item details
        self.items[request.itemId]["pricePerUnit"] = request.newPrice
        self.items[request.itemId]["quantity"] = request.newQuantity
        # self.notify_clients(f"Item ID: {request.itemId} has been updated.")
        return market_pb2.UpdateItemResponse(status=market_pb2.UpdateItemResponse.SUCCESS)


    def DeleteItem(self, request, context):
        print(f"Delete Item {request.itemId} request from {request.sellerAddress}")

        if request.sellerAddress not in self.sellers.keys():
            print("ERROR: Seller not registered")
            return market_pb2.DeleteItemResponse(status=market_pb2.DeleteItemResponse.FAILED)
        elif request.itemId not in self.items.keys():
            print("ERROR: Item not found")
            return market_pb2.DeleteItemResponse(status=market_pb2.DeleteItemResponse.FAILED)
        elif self.items[request.itemId]["sellerAddress"] != request.sellerAddress:
            print(f"ERROR: Seller {request.sellerAddress} does not own the item")
            return market_pb2.DeleteItemResponse(status=market_pb2.DeleteItemResponse.FAILED)
        elif request.sellerUUID != self.sellers[request.sellerAddress]:
            print("ERROR: Seller UUID does not match")
            return market_pb2.DeleteItemResponse(status=market_pb2.DeleteItemResponse.FAILED)
        
        # Remove item from inventory
        del self.items[request.itemId]
        return market_pb2.DeleteItemResponse(status=market_pb2.DeleteItemResponse.SUCCESS)


    def DisplaySellerItems(self, request, context):
        print(f"Display Items request from {request.sellerAddress}")

        if request.sellerAddress not in self.sellers.keys():
            print("ERROR: Seller not registered")
            return market_pb2.DisplaySellerItemsResponse()
        
        # elif request.sellerUUID != self.sellers[request.sellerAddress]:
        #     print("ERROR: Seller UUID does not match")
        #     return market_pb2.SellItemResponse(status=market_pb2.SellItemResponse.FAILED)

        response = market_pb2.DisplaySellerItemsResponse()
        for item_id, item_details in self.items.items():
            if item_details["sellerAddress"] == request.sellerAddress:
                item = response.items.add()
                item.itemId = item_id
                item.productName = item_details["productName"]
                item.price = item_details["pricePerUnit"]
                item.category = item_details["category"]
                item.description = item_details["description"]
                item.quantityRemaining = item_details["quantity"]
                item.sellerAddress = item_details["sellerAddress"]
                item.rating = item_details["rating"]
        return response


    # BuyerService implementations
    def SearchItem(self, request, context):
        print(f"Search request for Item name: '{request.itemName}', Category: '{request.itemCategory}'")

        response = market_pb2.SearchItemResponse()
        for item_id, item_details in self.items.items():

            if (request.itemName == "") or (request.itemName.lower().strip() in item_details["productName"].lower().strip()):

                if (request.itemCategory == 3) or (request.itemCategory == item_details["category"]):

                    item = response.items.add()
                    item.itemId = item_id
                    item.productName = item_details["productName"]
                    item.price = item_details["pricePerUnit"]
                    item.category = item_details["category"]
                    item.description = item_details["description"]
                    item.quantityRemaining = item_details["quantity"]
                    item.rating = item_details["rating"]
                    item.sellerAddress = item_details["sellerAddress"]


        return response


    def BuyItem(self, request, context):
        print(f"Buy request {request.quantity} of item {request.itemId}, from {request.buyerAddress}")

        if request.itemId not in self.items:
            print(f"ERROR: Item {request.itemId} not found")
            return market_pb2.BuyItemResponse(status=market_pb2.BuyItemResponse.FAILED)
        elif request.quantity > self.items[request.itemId]["quantity"]:
            print(f"ERROR: Insufficient quantity of item {request.itemId}")
            return market_pb2.BuyItemResponse(status=market_pb2.BuyItemResponse.FAILED)
        elif request.buyerAddress != self.items[request.itemId]["sellerAddress"]:
            print(f"ERROR: Seller {request.buyerAddress} does not posess the item {request.itemId}")
            return market_pb2.BuyItemResponse(status=market_pb2.BuyItemResponse.FAILED)

        # Update item quantity
        self.items[request.itemId]["quantity"] -= request.quantity
        # self.notify_seller(request.itemId, request.buyerAddress)
        return market_pb2.BuyItemResponse(status=market_pb2.BuyItemResponse.SUCCESS)


    def AddToWishList(self, request, context):
        print(f"Wishlist request of item {request.itemId}, from {request.buyerAddress}")

        if request.itemId not in self.items:
            print(f"ERROR: Item {request.itemId} not found")
            return market_pb2.AddToWishListResponse(status=market_pb2.AddToWishListResponse.FAILED)
        
        # Add item to wishlist
        if request.buyerAddress in self.wishlist:
            self.wishlist[request.buyerAddress].append(request.itemId)
        else:
            self.wishlist[request.buyerAddress] = [request.itemId]

        return market_pb2.AddToWishListResponse(status=market_pb2.AddToWishListResponse.SUCCESS)


    def RateItem(self, request, context):
        print(f"{request.buyerAddress} rated item {request.itemId} with {request.rating} stars.")

        if request.itemId not in self.items:
            return market_pb2.RateItemResponse(status=market_pb2.RateItemResponse.FAILED)

        # Update item rating
        self.items[request.itemId]["rating"] = request.rating
        return market_pb2.RateItemResponse(status=market_pb2.RateItemResponse.SUCCESS)

    # NotifyClient implementation
    # def SendNotification(self, request, context):
    #     print("#######")
    #     print("The Following Item has been updated:")
    #     print(request.updatedItemDetails)
    #     print("#######")
    #     return market_pb2.NotificationResponse(status=market_pb2.NotificationResponse.SUCCESS)

    # def notify_clients(self, updated_item_details):
    #     # Notify all clients about the item update
    #     for seller_address in self.sellers.keys():
    #         self.SendNotification(market_pb2.NotificationRequest(updatedItemDetails=updated_item_details), None)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    market_pb2_grpc.add_SellerServiceServicer_to_server(MarketServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
