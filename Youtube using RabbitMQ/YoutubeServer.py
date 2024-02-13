import json
import pika

class YouTubeServer:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='user_actions')
        self.channel.queue_declare(queue='publish_commands')
        self.userList = {} # {user: [youtuber1, youtuber2, ...]}
        self.userNotifications = {} # {user: queue, ...}
        self.youtubers = []
        # self.response_msg = ""


    def consume_user_requests(self):
        try:
            self.channel.basic_consume(queue='user_actions', on_message_callback=self.callback, auto_ack=True)
            # if self.response_msg != "":
            #     print('hii')
            #     print(self.response_msg)
            #     self.channel.basic_publish(exchange='', routing_key='user_actions', body=self.response_msg)
            #     self.response_msg = ""
            print('Waiting for users to subscribe/unsubscribe. To exit press CTRL+C')
            # self.channel.start_consuming()
        except KeyboardInterrupt:
            self.channel.stop_consuming()
            self.connection.close()
            print('User Requests closed')

    def callback(self,ch, method, properties, body):
            # print(body.decode())
            data = json.loads(body.decode(encoding='utf-8'))

            youtuber = data["youtuber"]
            # print(youtuber, type(youtuber))
            msg = ""

            if data["youtuber"] not in self.youtubers:
                print("Youtuber not found")
                msg = f"FAIL: Youtuber {data['youtuber']} not found"

            elif data["subscribe"] == "True":
                # print(data["user"] in self.userList)
                if data["user"] not in self.userList:
                    a=[]
                    a.append(data["youtuber"])
                    self.userList[data["user"]] = a                    
                else:
                    # print(data["youtuber"] in self.userList[data["user"]])
                    if data["youtuber"] not in self.userList[data["user"]]:    
                        self.userList[data["user"]].append(data["youtuber"])
                print(f'{data["user"]} is subscribed to {data["youtuber"]}')
                msg = 'SUCCESS: Subscribed'
            else:
                if data["user"] in self.userList:
                    if data["youtuber"] in self.userList[data["user"]]:
                        self.userList[data["user"]].remove(data["youtuber"])
                        print(f'{data["user"]} unsubscribed from {data["youtuber"]}')
                        msg = 'SUCCESS: Unsubscribed'
            # self.response_msg = msg
            # print(self.response_msg)

    def consume_youtuber_requests(self):
        def callback(ch, method, properties, body):
            youtuber = body.decode().split()[0]
            if youtuber not in self.youtubers:
                self.youtubers.append(youtuber)
            video_name = body.decode().split()[2]
            print(body.decode())
            self.notify_users(youtuber, video_name)
        try: 
            self.channel.basic_consume(queue='publish_commands', on_message_callback=callback, auto_ack=True)
            print('Waiting for Youtubers to upload videos. To exit press CTRL+C')
        except KeyboardInterrupt:
            self.channel.stop_consuming()
            self.connection.close()
            print('Youtuber Requests closed')

        
        # self.channel.start_consuming()

    def notify_users(self, youtuber, video_name):
        message = f"{youtuber} uploaded {video_name}"
        # self.channel.basic_publish(exchange='', routing_key='user_notifications', body=message)
        # print(" [x] Sent notification:", message)

        # if user is subsricbed to youtuber, send notification
        for user in self.userList:
            if youtuber in self.userList[user]:
                if user not in self.userNotifications.keys():
                    self.userNotifications[user] = self.channel.queue_declare(queue=user+"queue")
                self.channel.basic_publish(exchange='', routing_key=user+"queue", body=message)


if __name__ == '__main__':
    youtube_server = YouTubeServer()
    try:
        youtube_server.consume_user_requests()
        youtube_server.consume_youtuber_requests()
        youtube_server.channel.start_consuming()
    except KeyboardInterrupt:
        youtube_server.channel.stop_consuming()
        # Delete the queue
        youtube_server.channel.queue_delete(queue='user_actions')
        youtube_server.channel.queue_delete(queue='publish_commands')
        for user in youtube_server.userNotifications:
            youtube_server.channel.queue_delete(queue=user+"queue")
        youtube_server.connection.close()
        print("Server closed")