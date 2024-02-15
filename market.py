import grpc
from concurrent import futures
import time
import market_pb2
import market_pb2_grpc
import notifyBuyer_pb2
import notifyBuyer_pb2_grpc
import notifySeller_pb2
import notifySeller_pb2_grpc

_ONE_DAY_IN_SECONDS = 24 * 60 * 60

class MarketServicer(market_pb2_grpc.SellerServiceServicer):
    def __init__(self):
        self.items = {}         # Placeholder for item data
        self.sellers = {}       # Placeholder for registered sellers
        self.item_id = 0
        self.wishlist = {}      # wishlist = {buyerAddress : [itemID1, itemID2, ...]}
        self.buyerRating = {}
        self.categoryEnum = {0: "ELECTRONICS", 1: "FASHION", 2: "OTHERS", 3: "ANY"}


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

        
        # # Add item to inventory
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
        # # A seller can not sell the same item twice
        # if self.item_id in self.items:
        #     print(f"ERROR: Item already present with seller {request.sellerAddress}")
        #     return market_pb2.SellItemResponse(status=market_pb2.SellItemResponse.FAILED)
        # else:
        #     self.items[self.item_id] = seller_item

        
        # make the key as prod_unique_id$sellerAddress
        prod_unique_id = request.productName + "#" + str(request.category)
        key = prod_unique_id + "$" + request.sellerAddress
        
        # assign the item id according to the product name and category
        if key in self.items:
            print(f"ERROR: Item already present with seller {request.sellerAddress}")
            return market_pb2.SellItemResponse(status=market_pb2.SellItemResponse.FAILED)
        
        # search if the product is already present by its prod_unique_id with another seller
        for value in self.items.values():
            if value["productName"] == request.productName and value["category"] == request.category:
                itemID = value["itemID"]
                break
        else:
            self.item_id = self.item_id + 1
            itemID = self.item_id
        
        self.items[key] = {
            "itemID": itemID,
            "productName": request.productName,
            "category": request.category,
            "quantity": request.quantity,
            "description": request.description,
            "sellerAddress": request.sellerAddress,
            "pricePerUnit": request.pricePerUnit,
            "rating": 0  # Placeholder for rating
        }
        
        return market_pb2.SellItemResponse(status=market_pb2.SellItemResponse.SUCCESS, itemId=self.item_id)


    def UpdateItem(self, request, context):
        print(f"Update Item {request.itemId} request from {request.sellerAddress}")

        if (request.sellerAddress not in self.sellers.keys()):
            print("ERROR: Seller not registered")
            return market_pb2.UpdateItemResponse(status=market_pb2.UpdateItemResponse.FAILED)
        
        # make a reverse lookup dictionary for itemID, key
        itemID_to_key = {}
        for key, value in self.items.items():
            # if itemID is present then add the seller address to the key
            if value["itemID"] in itemID_to_key:
                itemID_to_key[value["itemID"]].append(key)
            else:
                itemID_to_key[value["itemID"]] = [key]
        
        if request.itemId not in itemID_to_key.keys():
            print("ERROR: Item not found")
            return market_pb2.UpdateItemResponse(status=market_pb2.UpdateItemResponse.FAILED)
        
        if request.sellerAddress not in [seller.split('$')[1] for seller in itemID_to_key[request.itemId]]:
            print(f"ERROR: Seller {request.sellerAddress} does not own the item")
            return market_pb2.UpdateItemResponse(status=market_pb2.UpdateItemResponse.FAILED)
        
        if (request.sellerUUID != self.sellers[request.sellerAddress]):
            print("ERROR: Seller UUID does not match")
            return market_pb2.UpdateItemResponse(status=market_pb2.UpdateItemResponse.FAILED)
        
        if (request.newQuantity < 0):
            print("ERROR: Quantity can not be negative")
            return market_pb2.UpdateItemResponse(status=market_pb2.UpdateItemResponse.FAILED)
        
        if (request.newPrice < 0):
            print("ERROR: Price can not be negative")
            return market_pb2.UpdateItemResponse(status=market_pb2.UpdateItemResponse.FAILED)
        
        # iterate over reverse lookup dictionary and update the item details
        product = {}
        for key in itemID_to_key[request.itemId]:
            # find the right key and update the details
            currentSeller = key.split('$')[1]
            if currentSeller == request.sellerAddress:
                self.items[key]["pricePerUnit"] = request.newPrice
                self.items[key]["quantity"] = request.newQuantity
                product = self.items[key]
                break
        
        
        # Get the buyerAddress from wishlist who has this product and notify them
        for buyerAddress, wishlist in self.wishlist.items():
            if request.itemId in wishlist:
                print(f"Buyer {buyerAddress} has {wishlist} in wishlist")
                self.notifyBuyer(buyerAddress, product)  


        return market_pb2.UpdateItemResponse(status=market_pb2.UpdateItemResponse.SUCCESS)


    def DeleteItem(self, request, context):
        print(f"Delete Item {request.itemId} request from {request.sellerAddress}")

        if request.sellerAddress not in self.sellers.keys():
            print("ERROR: Seller not registered")
            return market_pb2.DeleteItemResponse(status=market_pb2.DeleteItemResponse.FAILED)
        
        # make a reverse lookup dictionary for itemID, key
        itemID_to_key = {}
        for key, value in self.items.items():
            if value["itemID"] in itemID_to_key:
                itemID_to_key[value["itemID"]].append(key)
            else:
                itemID_to_key[value["itemID"]] = [key]
        
        if request.itemId not in itemID_to_key.keys():
            print("ERROR: Item not found")
            return market_pb2.DeleteItemResponse(status=market_pb2.DeleteItemResponse.FAILED)

        if request.sellerAddress not in [seller.split('$')[1] for seller in itemID_to_key[request.itemId]]:
            print(f"ERROR: Seller {request.sellerAddress} does not own the item")
            return market_pb2.DeleteItemResponse(status=market_pb2.DeleteItemResponse.FAILED)

        if request.sellerUUID != self.sellers[request.sellerAddress]:
            print("ERROR: Seller UUID does not match")
            return market_pb2.DeleteItemResponse(status=market_pb2.DeleteItemResponse.FAILED)
        
        # Remove item from inventory
        for key in itemID_to_key[request.itemId]:
            if key.split('$')[1] == request.sellerAddress:
                del self.items[key]
                break
        return market_pb2.DeleteItemResponse(status=market_pb2.DeleteItemResponse.SUCCESS)


    def DisplaySellerItems(self, request, context):
        print(f"Display Items request from {request.sellerAddress}")

        if request.sellerAddress not in self.sellers.keys():
            print("ERROR: Seller not registered")
            return market_pb2.DisplaySellerItemsResponse()
        elif request.sellerUUID != self.sellers[request.sellerAddress]:
            print("ERROR: Seller UUID does not match")
            return market_pb2.SellItemResponse(status=market_pb2.SellItemResponse.FAILED)

        response = market_pb2.DisplaySellerItemsResponse()
        for value in self.items.values():
            if value["sellerAddress"] == request.sellerAddress:
                item = response.items.add()
                item.itemId = value["itemID"]
                item.productName = value["productName"]
                item.price = value["pricePerUnit"]
                item.category = value["category"]
                item.description = value["description"]
                item.quantityRemaining = value["quantity"]
                item.sellerAddress = value["sellerAddress"]
                item.rating = value["rating"]
        return response


    # BuyerService implementations
    def SearchItem(self, request, context):
        print(f"Search request for Item name: '{request.itemName}', Category: '{self.categoryEnum[request.itemCategory]}'")

        response = market_pb2.SearchItemResponse()

        for value in self.items.values():
            if (request.itemName == "") or (request.itemName.lower().strip() in value["productName"].lower().strip()):
                if (request.itemCategory == 3) or (request.itemCategory == value["category"]):
                    item = response.items.add()
                    item.itemId = value["itemID"]
                    item.productName = value["productName"]
                    item.price = value["pricePerUnit"]
                    item.category = value["category"]
                    item.description = value["description"]
                    item.quantityRemaining = value["quantity"]
                    item.sellerAddress = value["sellerAddress"]
                    item.rating = value["rating"]

        return response


    def BuyItem(self, request, context):
        print(f"Buy request {request.quantity} of item {request.itemId}, from {request.buyerAddress}")
        
        # make a reverse lookup dictionary for itemID, key
        itemID_to_key = {}
        for key, value in self.items.items():
            if value["itemID"] in itemID_to_key:
                itemID_to_key[value["itemID"]].append(key)
            else:
                itemID_to_key[value["itemID"]] = [key]
        
        if request.itemId not in itemID_to_key.keys():
            print(f"ERROR: Item {request.itemId} not found")
            return market_pb2.BuyItemResponse(status=market_pb2.BuyItemResponse.FAILED)
        
        # calculate total quantity of the item
        total_quantity = 0
        for key in itemID_to_key[request.itemId]:
            total_quantity += self.items[key]["quantity"]
        
        if request.quantity > total_quantity:
            print(f"ERROR: Insufficient quantity of item {request.itemId}")
            return market_pb2.BuyItemResponse(status=market_pb2.BuyItemResponse.FAILED)

        # Update item quantity
        for key in itemID_to_key[request.itemId]:
            if self.items[key]["quantity"] >= request.quantity:
                self.items[key]["quantity"] -= request.quantity
                break
            else:
                request.quantity -= self.items[key]["quantity"]
                self.items[key]["quantity"] = 0
        
        # self.notify_seller(request.itemId, request.buyerAddress)
        return market_pb2.BuyItemResponse(status=market_pb2.BuyItemResponse.SUCCESS)


    def AddToWishList(self, request, context):
        print(f"Wishlist request of item {request.itemId}, from {request.buyerAddress}")

        all_itemIDs = {value["itemID"] : True for value in self.items.values()}
        if request.itemId not in all_itemIDs.keys():
            print(f"ERROR: Item {request.itemId} not found")
            return market_pb2.AddToWishListResponse(status=market_pb2.AddToWishListResponse.FAILED)
        
        # Add item to wishlist
        if request.buyerAddress in self.wishlist:
            if request.itemId not in self.wishlist[request.buyerAddress]:
                self.wishlist[request.buyerAddress].append(request.itemId)
            else:
                print(f"ERROR: Item {request.itemId} already present in wishlist for buyer {request.buyerAddress}")
                return market_pb2.AddToWishListResponse(status=market_pb2.AddToWishListResponse.FAILED)
        else:
            self.wishlist[request.buyerAddress] = [request.itemId]

        return market_pb2.AddToWishListResponse(status=market_pb2.AddToWishListResponse.SUCCESS)


    def RateItem(self, request, context):
        print(f"{request.buyerAddress} rated item {request.itemId} with {request.rating} stars.")
        
        # make a reverse lookup dictionary for itemID, key
        itemID_to_key = {}
        for key, value in self.items.items():
            if value["itemID"] in itemID_to_key:
                itemID_to_key[value["itemID"]].append(key)
            else:
                itemID_to_key[value["itemID"]] = [key]
        
        if request.itemId not in itemID_to_key.keys():
            print(f"ERROR: Item {request.itemId} not found")
            return market_pb2.RateItemResponse(status=market_pb2.RateItemResponse.FAILED)
        
        # buyerRating is of the form {buyerAddress : [itemID1, itemID2, ...]}
        if request.buyerAddress in self.buyerRating:
            if request.itemId in self.buyerRating[request.buyerAddress]:
                print(f"ERROR: Buyer {request.buyerAddress} already rated item {request.itemId}")
                return market_pb2.RateItemResponse(status=market_pb2.RateItemResponse.FAILED)
            else:
                self.buyerRating[request.buyerAddress].append(request.itemId)
        else:
            self.buyerRating[request.buyerAddress] = [request.itemId]

        # Update item rating
        for key in itemID_to_key[request.itemId]:
            if self.items[key]["rating"] == 0:
                self.items[key]["rating"] = request.rating
            else:
                self.items[key]["rating"] = (self.items[key]["rating"] + request.rating) / 2

        return market_pb2.RateItemResponse(status=market_pb2.RateItemResponse.SUCCESS)
    

    # NotifyClient implementations
    def notifyBuyer(self, buyerAddress, request):
        channel = grpc.insecure_channel(buyerAddress)
        stub = notifyBuyer_pb2_grpc.BuyerNotificationStub(channel)

        # print(f"Notification request to buyer {buyerAddress}")
        notification_request = notifyBuyer_pb2.NotifyBuyerRequest(
            itemId=request['itemID'],
            productName=request['productName'],
            category=request['category'],
            description=request['description'],
            quantityRemaining=request['quantity'],
            sellerAddress=request['sellerAddress'],
            price=request['pricePerUnit'],
            rating=request['rating']
        )
        # print(f"Notification response message prepared for buyer {buyerAddress}")
        response = stub.NotifyBuyer(notification_request)
        if response.status == notifyBuyer_pb2.NotifyBuyerResponse.SUCCESS:
            print(f"Notification sent to buyer {buyerAddress}")
        else:
            print(f"ERROR: Notification failed to send to buyer {buyerAddress}")
    
    
    # notify seller
    def notifySeller(self, sellerAddress, request):
        channel = grpc.insecure_channel(sellerAddress)
        stub = notifySeller_pb2_grpc.SellerNotificationStub(channel)

        # print(f"Notification request to seller {sellerAddress}")
        notification_request = notifySeller_pb2.NotifySellerRequest(
            itemId=request['itemID'],
            productName=request['productName'],
            category=request['category'],
            description=request['description'],
            quantityRemaining=request['quantity'],
            sellerAddress=request['sellerAddress'],
            price=request['pricePerUnit'],
            rating=request['rating']
        )
        # print(f"Notification response message prepared for seller {sellerAddress}")
        response = stub.NotifySeller(notification_request)
        if response.status == notifySeller_pb2.NotifySellerResponse.SUCCESS:
            print(f"Notification sent to seller {sellerAddress}")
        else:
            print(f"Notification failed to send to seller {sellerAddress}")


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
