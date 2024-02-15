import pika
import sys
import time

class User:
    def __init__(self, username):
        self.username = username
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('34.131.65.103'))        
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='user_actions')
        self.userNotifications = {} # {user: queue, ...}

    def update_subscription(self, youtuber, subscribe):
        # def callback(ch, method, properties, body):
        #     print(body.decode())
        try:
            message = f'{{"user": "{self.username}", "youtuber": "{youtuber}", "subscribe": "{subscribe}"}}'
            self.channel.basic_publish(exchange='', routing_key='user_actions', body=message)
            # self.channel.basic_consume(queue='user_actions', on_message_callback=callback, auto_ack=True)
            print('SUCCESS')
        except Exception as e:
            print(f'FAIL -- Error: {e}')
            self.connection.close()
            print('User Requests closed')

    def receive_notifications(self):
        def callback(ch, method, properties, body):
            print("New Notification:", body.decode())
        try:
            if self.username not in self.userNotifications.keys():
                self.userNotifications[self.username] = self.channel.queue_declare(queue=self.username+"queue")
            self.channel.basic_consume(queue=self.username+"queue", on_message_callback=callback, auto_ack=True)
            print('Surfing YouTube, and waiting. Press Ctrl+C to exit and get back to work.')
            # Start timing to calculate total time spent waiting
            start_time = time.time()
            self.channel.start_consuming()  
        except KeyboardInterrupt:
            end_time = time.time()
            time_mins = round((end_time - start_time) / 60, 2)
            self.channel.stop_consuming()
            self.connection.close()
            print(f'Total time wasted in procrastination: {time_mins} minutes. Get back to work!')
        except Exception as e:
            print(f'Error: {e}')
            self.connection.close()
            print('User Requests closed')

if __name__ == '__main__':
    # print(len(sys.argv))
    if len(sys.argv) == 2:
        user = User(sys.argv[1])
        action = 'login'
    elif len(sys.argv) == 4:
        user = User(sys.argv[1])
        action = sys.argv[2]
        youtuber = sys.argv[3]
    else:
        print('Invalid command arguments. Pass either 1 or 3 arguments.')
        sys.exit(0)

    if action == 's' or action == 'u':
            user.update_subscription(youtuber, 'True' if action == 's' else 'False')
    elif action == 'login':
        user.receive_notifications()
    else:
        print('Invalid command')
