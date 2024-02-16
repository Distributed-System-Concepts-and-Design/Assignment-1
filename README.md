# Distributed Systems and Cloud Computing Assignments

There are 3 mini-projects in this repository. Each of them is a distributed system and cloud computing project. Each of them are hosted and tested on Google Cloud. The details of each project are as follows:

## e-Commerce MarketPlace *Using GRPC*

### Commands to compile and run the code:
1) python -m grpc_tools.protoc -I . --python_out=. --grpc_python_out=. market_seller.proto
2) `python market.py` *to run the central market server*
3) `python seller.py` *to run the seller server*
4) `python buyer.py` *to run the buyer server*

### Assumptions:
1) ProductName+Category is unique for each product
2) `#` and `$` does not come in prdouctName or category
3) Currently the market seller`s function as a single unique distributed system, i.e., buyer can buy a product but he doesn't from which seller the product is going to come. Hence, the ratings for a single product will be reflected in every seller's copy of the product too!
4) New rating is taken as an average of the preceding rating which gives an approximate value of the actual mean of ratings. However, if a new seller comes with the same product which has been rated before then those ratings will not be reflected over here. This is a feature as the new seller should not be penalized (nor credited) on his products due to the already existing seller's ratings. This will ensure credibility and differentiability in product ratings too!

### Features:
1) Market keeps track of all the products and their sellers
2) Seller can add a product, remove a product, update a product, and get the ratings of a product
3) Buyer can wishlist a product, buy a product, and rate a product

## Group Messaging System on Cloud *Using ZeroMQ*

### Commands to compile and run the code:
1) pip install pyzmq
2) `python message_server.py` *to run the central server*
3) `python groups.py` *to run the individual group servers*
    a. Enter the group name, external IP, and port number of the server
4) `python client.py` *to run the client*
    a. Enter the user name, phone number and port number of the user side.
    b. Commands to perform any action will be: ACTION <message *if any* > @group_name *Case-Sensitive*. For example: `JOIN @group 1`, `LEAVE @group 1`, `SEND_MESSAGE Hello How are you @group1`, `GET_MESSAGES <timestamp> @group1`

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
3) `python YoutubeServer.py` *to run the central server*
4) `python Youtube.py *youtuber_name* *Video name*` *to make the youtuber upload a video*
5) `python User.py user_name` *to login the user*
6) `python User.py user_name <s/u> <youtuber_name>` *to subscribe or unsubscribe to a youtuber*

### Assumptions:
1) The youtuber will have to upload atleast one video to exist and be subscribed to


### Features:
1) Central Server keeps track of all the youtubers and their respective videos
2) Youtuber can upload a video
3) User can subscribe to a youtuber and get notified of the new videos uploaded by the youtuber. They also get all the notifications of their subscribed youtuber, if they were offline at the time of the upload.
4) User can unsubscribe to a youtuber and stop getting notifications of the new videos uploaded by the youtuber.