@echo off
python -m grpc_tools.protoc -I . --python_out=. --grpc_python_out=. market.proto notifyBuyer.proto notifySeller.proto