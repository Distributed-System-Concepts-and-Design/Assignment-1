# Distributed Systems and Cloud Computing Assignments

## Group Members:
1) 2020002 - Aamleen Ahmed
2) 2020312 - Mohammad Sufyan Azam
3) 2020338 - Siddhant Singh

There are 3 mini-projects in this repository. Each of them is a distributed system and cloud computing project. Each of them are hosted and tested on Google Cloud. The details of each project are given below.

## e-Commerce Shopping Platform *Using GRPC*

### Commands to compile and run the code:

1) For Compilation: `python -m grpc_tools.protoc -I . --python_out=. --grpc_python_out=. market.proto notifyBuyer.proto notifySeller.proto`
2) On Market Machine: `python market.py` *to run the central market server*
3) On Seller Machine: `python seller.py` *to run the seller server*
4) On Buyer Machine: `python buyer.py` *to run the buyer server*

### Assumptions:
1) The seller/buyer programs will not quit in between.

### Features:
1) Market keeps track of all the products and their sellers
2) Seller can add a product, remove a product, update a product, and get a list of all the products that he has listed
3) Buyer can search for a product, wishlist a product, buy a product, and rate a product

## Group Messaging System on Cloud *Using ZeroMQ*

### Commands to compile and run the code:
1) pip install pyzmq
2) `python message_server.py` *to run the central server* where Central Server is hosted
3) `python groups.py` *to run the individual group servers* where Group Server is hosted
    1. Enter the group name, external IP, and port number of the server
4) `python client.py` *to run the client* where User is hosted
    1. Enter the user name, phone number and port number of the user side.
    2. Commands to perform any action will be: ACTION <message *if any* > @group_name *Case-Sensitive*. For example: `JOIN @group 1`, `LEAVE @group 1`, `SEND_MESSAGE Hello How are you @group1`, `GET_MESSAGES <timestamp> @group1`

### Assumptions:
1) The combination of group name and IP is unique
2) The user phone number is unique for each user. Using this as UUID for a more realistic approach.
3) The user can join multiple groups and send messages to multiple groups at the same time.
4) Since Group Server is binded for incoming messages, Ctrl+C will not work to stop the server. 

### Features:
1) Central Server keeps track of all the groups and their respective servers
2) Group Server keeps track of all the users in the group and their respective messages
3) User can join a group, leave a group, send a message to a group, and get the messages from a group
4) User can join multiple groups and send messages to multiple groups at the same time.

## Youtube Hosting Service *Using RabbitMQ*

### Commands to compile and run the code:
0) Update the external IP in the `Youtube.py` and `User.py` file in line 8 and 6, respectively. Give the external IP where `YoutubeServer.py` is hosted. 
1) `pip install pika`
2) Run `rmq_setup.sh` to setup the RabbitMQ server
3) `python YoutubeServer.py` *to run the central server* where Central Server is hosted
4) `python Youtube.py *youtuber_name* *Video name*` *to make the youtuber upload a video* where Youtuber is hosted
5) `python User.py user_name` *to login the user* where User is hosted
6) `python User.py user_name <s/u> <youtuber_name>` *to subscribe or unsubscribe to a youtuber* where User is hosted

### Assumptions:
1) The youtuber will have to upload atleast one video to exist and be subscribed to


### Features:
1) Central Server keeps track of all the youtubers and their respective videos
2) Youtuber can upload a video
3) User can subscribe to a youtuber and get notified of the new videos uploaded by the youtuber. They also get all the notifications of their subscribed youtuber, if they were offline at the time of the upload.
4) User can unsubscribe to a youtuber and stop getting notifications of the new videos uploaded by the youtuber.