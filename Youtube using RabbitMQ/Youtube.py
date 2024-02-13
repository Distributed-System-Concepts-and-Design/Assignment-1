import pika
import sys

class Youtuber:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='publish_commands')
        
    def publish_video(self, youtuber, video_name):
        print("Publishing video")
        message = f"{youtuber} uploaded {video_name}"
        self.channel.basic_publish(exchange='', routing_key='publish_commands', body=message)
        print(" [x] Sent video for publication:", message)

if __name__ == '__main__':
    # print("Publishing video")
    youtuber = Youtuber()
    youtuber.publish_video(sys.argv[1], ' '.join(sys.argv[2:]))