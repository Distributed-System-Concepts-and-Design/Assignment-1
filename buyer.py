import grpc
import market_pb2
import market_pb2_grpc


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


if __name__ == "__main__":
    buyer = MarketBuyer('localhost:50051')
    # buyer.search_item(item_name="Orange", item_category="ANY")
    buyer.rate_item(1, "142.213.91.1:50051", 1)
    buyer.search_item(item_name="Orange", item_category="ANY")
    buyer.buy_item(item_id=1, quantity=5, buyer_address="142.213.91.1:50051")
    buyer.add_to_wishlist(1, "142.213.91.1:50051")
