# Assignment-1

Command to generate the GRPC boiler plate code from .proto files: python -m grpc_tools.protoc -I . --python_out=. --grpc_python_out=. market_seller.proto

## GRPC Online SHopping Platform Assumptions:
1) ProductName+Category is unique for each product
2) '#' does not come in prdouctName or category
