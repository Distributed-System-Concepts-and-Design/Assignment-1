import zmq

class UserClient:
    def __init__(self, name, phone_number):
        self.groups = {}  # Dictionary to store group_names and sockets
        self.uuid = phone_number  # Unique identifier for the user
        self.name = name  # User's name

    def __connect_to_group(self, group_name, ip_address):
        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        socket.connect(f"tcp://{ip_address}")  # Connect to group server
        self.groups[group_name] = socket

    def __get_grp_lists(self):
        msg_srvr_ip = "34.131.27.141:5555"
        context_msg_Server = zmq.Context()
        msg_srvr_sckt = context_msg_Server.socket(zmq.REQ)
        msg_srvr_sckt.connect(f'tcp://{msg_srvr_ip}')  # Connect to message server
        msg_srvr_sckt.send_string(f'GET_GROUP_LIST {self.uuid}')
        group_list = msg_srvr_sckt.recv_string()
        msg_srvr_sckt.disconnect(f'tcp://{msg_srvr_ip}')
        msg_srvr_sckt.close()
        return group_list

    def join_group(self):
        group_list = self.__get_grp_lists().split("\n")

        print("Available Active groups:")
        # Print the list of available groups with index
        for i, group in enumerate(group_list):
            print(f"{i + 1}. {group}")
        group_no = input("Enter the group index number to join: ").strip()
        group_name = group_list[int(group_no) - 1].split(" - ")[0]
        group_ip_ = group_list[int(group_no) - 1].split(" - ")[1].split(":")
        if group_ip_[0] == "*":
            group_ip_[0] = "localhost"
        group_ip = group_ip_[0] + ":" + group_ip_[1]

        if group_name in self.groups:
            print("You are already part of this group")
            return
        
        # print(f"Joining group {group_name} - {group_ip}...")

        # Creating a new connection to the group server
        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        socket.connect(f"tcp://{group_ip}")  # Connect to group server

        # print(f'Socket connected to ip: {group_ip}')
        
        message = f"JOIN_GROUP {self.uuid}"
        # print('Sending message: ', message)
        socket.send_string(message)
        # print('Message sent')
        response = socket.recv_string()
        
        if response == "SUCCESS":
            self.groups[group_name] = socket
        return response

    def leave_group(self, group_name):
        if group_name in self.groups.keys():
            socket = self.groups[group_name]
            message = f"LEAVE_GROUP {self.uuid}"
            socket.send_string(message)
            response = socket.recv_string()
            # socket.disconnect(f"tcp://{group_name}")
            socket.close()
            if response == "SUCCESS":
                self.groups.pop(group_name)
            return response
        else:
            return f"You are not part of the group {group_name}"

    def get_messages(self, group_name, timestamp=None):
        if group_name not in self.groups:
            return f"You are not part of the group {group_name}"

        if timestamp:
            # Fetch messages after the specified timestamp
            message = f"GET_MESSAGES {self.uuid} {timestamp}"
        else:
            # Fetch all messages
            message = f"GET_MESSAGES {self.uuid}"

        socket = self.groups[group_name]
        socket.send_string(message)
        response = socket.recv_string()
        return response

    def send_message(self, group_name, message_content):
        # print('Sending message to group: ', group_name)
        # print('Groups: ', self.groups.items())
        # group_name = 'ro'
        if group_name not in self.groups:
            return f"You are not part of the group {group_name}"
        # Send message to the group server
        message = f"SEND_MESSAGE {self.uuid} {message_content}"
        socket = self.groups[group_name]
        socket.send_string(message)
        response = socket.recv_string()
        return response

    def get_joined_groups(self):
        return list(self.groups.keys()) 

    def leave_all_groups(self):
        groups_ = list(self.groups.keys())
        for group in groups_:
            self.leave_group(group)

def main():
    user_name = input("Enter your name: ")
    user_phone = input("Enter your phone number: ") # This will be the user's unique identifier

    try:
        user_client = UserClient(user_name, user_phone)

        print(f'Welcome {user_name}! Your phone number is {user_phone}')
        while True:
            # User interaction loop
            print('\n----------------------------------------------------------------')
            print("Available commands: JOIN, LEAVE, GET_MESSAGES, SEND_MESSAGE, EXIT") # Command example: COMMAND <args> @group_name
            print('Joined groups: \n', user_client.get_joined_groups())
            command = input("Enter command: ").strip()

            if command.startswith("JOIN"): 
                response = user_client.join_group()
                print(response)

            elif command.startswith("LEAVE"):
                # Group name is at last and starts with the last index of @
                # Finding last index of @
                group_name = command[command.rfind('@')+1:].strip()
                response = user_client.leave_group(group_name)
                print(response)

            elif command.startswith("GET_MESSAGES"):
                group_name = command[command.rfind('@')+1:].strip()
                command = command[0:command.rfind('@')]
                command_parts = command.split()
                if len(command_parts) > 1:
                    timestamp = command_parts[1]
                    response = user_client.get_messages(group_name, timestamp)
                else:
                    response = user_client.get_messages(group_name)
                print(response)

            elif command.startswith("SEND_MESSAGE"):
                group_name = command[command.rfind('@')+1:].strip()
                command = command[0:command.rfind('@')]
                message_content = command.split(' ', 1)[1].strip()
                response = user_client.send_message(group_name, message_content)
                print(response)

            elif command == "EXIT":
                # Leave all groups and exit
                user_client.leave_all_groups()
                print('\n----------------------------------------------------------------')
                print('Thank you for using the chat application! Your secret is safe with us! ;)')
                break

            else:
                print("Invalid command")

    except KeyboardInterrupt:
        # Handle keyboard interrupt
        print("Leaving All Groups...")
        user_client.leave_all_groups()
        print("Exiting...")
        exit()


if __name__ == "__main__":
    main()
