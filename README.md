# Assignment-1

Command to generate the GRPC boiler plate code from .proto files: python -m grpc_tools.protoc -I . --python_out=. --grpc_python_out=. market_seller.proto

## GRPC Online SHopping Platform Assumptions:
1) ProductName+Category is unique for each product
2) '#' and '$' does not come in prdouctName or category
3) Currently the market seller's function as a single unique distributed system, i.e., buyer can buy a product but he doesn't from which seller the product is going to come. Hence, the ratings for a single product will be reflected in every seller's copy of the product too!
4) New rating is taken as an average of the preceding rating which gives an approximate value of the actual mean of ratings.