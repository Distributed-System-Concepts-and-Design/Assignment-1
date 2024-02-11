import zmq

class MessageServer:
    def __init__(self):
        self.groups = {}  # Dictionary to store group information {ip_address: group_name}

    def register_group(self, group_name, ip_address):
        if ip_address in self.groups:
            return "Group already exists with this IP address"
        else:
            self.groups[ip_address] = group_name
            return "SUCCESS"
    
    def delete_group(self, group_name, ip_address):
        if ip_address in self.groups:
            del self.groups[ip_address]
            return "SUCCESS"
        else:
            return "Group does not exist with this IP address"


    def get_group_list(self):
        return "\n".join([f"{group_name} - {ip_address}" for ip_address, group_name in self.groups.items()])

def main():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")  

    message_server = MessageServer()

    print("Message server started at port 5555")

    while True:
        # Wait for incoming connections
        message = socket.recv_string()

        # Parse the message
        command, *args = message.split()

        if command == "REGISTER_GROUP":
            # Register a new group
            ip_address, *group_name_ = args
            group_name = " ".join(group_name_)
            response = message_server.register_group(group_name, ip_address)
            print(f"JOIN REQUEST FROM {group_name} - [{ip_address}]")
            socket.send_string(response)

        elif command == "GET_GROUP_LIST":
            # Get the list of available groups
            response = message_server.get_group_list()
            print(f"GET GROUP LIST REQUEST FROM {args[0]}")
            socket.send_string(response)
        
        elif command == "DELETE_GROUP":
            # Delete a group
            ip_address, *group_name_ = args
            group_name = " ".join(group_name_)
            response = message_server.delete_group(group_name, ip_address)
            print(f"DELETE GROUP REQUEST FROM {group_name} - [{ip_address}]")
            socket.send_string(response)

        else:
            # Invalid command
            socket.send_string("INVALID COMMAND")

if __name__ == "__main__":
    main()
