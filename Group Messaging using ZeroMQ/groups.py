import zmq
import threading
from datetime import datetime

class GroupServer:
    def __init__(self, group_name, ip_address_):
        self.group_name = group_name
        ip_parts = ip_address_.split(":")
        print(ip_parts)
        if len(ip_parts) == 2:
            self.ip_address = ip_address_
        else:
            self.ip_address = f"*:{ip_address_}"
        self.users = set()  # Set to store users currently part of the group
        self.messages = []  # List to store messages sent by users
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        print('Binding to ip: ', f"tcp://{self.ip_address}")
        self.socket.bind(f"tcp://{self.ip_address}")
        self.external_ip = "34.131.65.103" + ":" + ip_parts[1]

        self.register_group_with_message_server()
        print(f"Group {group_name} started at {self.ip_address}")

    def register_group_with_message_server(self):
        # message_server_ip = "localhost:5555"
        message_server_ip = "34.131.124.126:5555"  # External IP of the message server from Google Cloud
        try:
            context = zmq.Context()
            message_server_socket = context.socket(zmq.REQ)
            message_server_socket.connect(f'tcp://{message_server_ip}')  # Connect to message server
            message_server_socket.send_string(f"REGISTER_GROUP {self.external_ip} {self.group_name}")
            response = message_server_socket.recv_string()
            print(response)
        finally:
            if message_server_socket:
                message_server_socket.disconnect(f'tcp://{message_server_ip}')
                message_server_socket.close()

    def close_group(self):
        # message_server_ip = "localhost:5555"
        message_server_ip = "34.131.124.126:5555"  # External IP of the message server from Google Cloud
        try:
            context = zmq.Context()
            message_server_socket = context.socket(zmq.REQ)
            message_server_socket.connect(f'tcp://{message_server_ip}')  # Connect to message server
            message_server_socket.send_string(f"DELETE_GROUP {self.ip_address} {self.group_name}")
            response = message_server_socket.recv_string()
            print(response)
        finally:
            if message_server_socket:
                message_server_socket.disconnect(f'tcp://{message_server_ip}')
                message_server_socket.close()

    def join_group(self, user_uuid):
        self.users.add(user_uuid)
        return "SUCCESS"    

    def leave_group(self, user_uuid):
        if user_uuid in self.users:
            self.users.remove(user_uuid)
            return "SUCCESS"
        else:
            return "User not found in the group"

    def send_message(self, user_uuid, message_content):
        if user_uuid in self.users:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.messages.append((timestamp, user_uuid, message_content))
            return "SUCCESS"
        else:
            return "User not found in the group"

    def get_messages(self, timestamp=None):
        if timestamp:
            # print(f"Fetching messages after {timestamp}")
            # COnvert the timestamp to datetime object\
            # timestamp = datetime.strptime(timestamp_, "%Y-%m-%d %H:%M:%S")
            filtered_messages = [msg for msg in self.messages if msg[0] >= timestamp]
            return filtered_messages
        else:
            return self.messages

    def handle_user_request(self, message):
        # Parse the message
        command, *args = message.split()

        if command == "JOIN_GROUP":
            # Handle user joining group
            uuid = args[0] if args else None
            if uuid:
                response = self.join_group(uuid)
                print(f"JOIN REQUEST FROM {uuid}")
                self.socket.send_string(response)

        elif command == "LEAVE_GROUP":
            # Handle user leaving group
            uuid = args[0] if args else None
            if uuid:
                response = self.leave_group(uuid)
                print(f"LEAVE REQUEST FROM {uuid}")
                self.socket.send_string(response)

        elif command == "GET_MESSAGES":
            # Handle user fetching messages
            uuid = None
            timestamp = None
            if len(args) == 1:
                uuid = args[0]
            elif len(args) == 2:
                uuid, timestamp = args
                # Add today's date to the timestamp
                timestamp = f"{datetime.now().strftime('%Y-%m-%d')} {timestamp}"
            elif len(args) == 3:
                uuid, date, time = args
                timestamp = f"{date} {time}"

            if uuid:
                print(f"MESSAGE REQUEST FROM {uuid}")
                messages = self.get_messages(timestamp)
                messages_str = "\n".join([f"{msg[0]} - {msg[1]}: {msg[2]}" for msg in messages])
                self.socket.send_string(messages_str)

        elif command == "SEND_MESSAGE":
            # Handle user sending message
            if len(args) >= 2:
                uuid = args[0]
                message_content = " ".join(args[1:])
            else:
                print('FAIL: Missing arguments')
                self.socket.send_string("FAIL: Missing arguments")
            # print(uuid, message_content)
            if uuid and message_content:
                print(f"MESSAGE SEND FROM {uuid}")
                response = self.send_message(uuid, message_content)
                self.socket.send_string(response)
            else:
                # Invalid command or missing arguments
                # print(f"Invalid command: {message}")
                self.socket.send_string("FAIL")

        else:
            # Invalid command
            print(f'INVALID COMMAND: {message}')
            self.socket.send_string("INVALID COMMAND")

def main():
    group_name = input("Enter group name: ")
    group_ip = input("Enter group IP {Press Enter for localhost}: ")
    if not group_ip:
        group_ip = "*"
    group_port = input("Enter group port to bind: ")
    
    group_ip = f"{group_ip}:{group_port}"
    group_server = GroupServer(group_name, group_ip)

    try:
        while True:
            # Handle individual user requests
            message = group_server.socket.recv_string()

            # print(f"Received message: {message}")

            group_server.handle_user_request(message)

            # Start a new thread to handle the user request
            # threading.Thread(target=group_server.handle_user_request, args=(message,)).start()
            # break

    except KeyboardInterrupt:
        group_server.close_group()

if __name__ == "__main__":
    main()
