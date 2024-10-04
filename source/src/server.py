import socket
import sys



def handle_arguments(args):
    if len(args) < 2:
        sys.exit("Error: no arguments provided")
    if len(args) > 3:
        sys.exit("Error: Too many arguments provided")
    if "-p" in args:
        try:
            index = args.index("-p")
        except ValueError:
            sys.exit("Error: need -p flag before port number")

    
    return args
    

def parse_arguments(args):
    parsed_args = []
    index = args.index("-p")
    if (index+1) != len(args):
        port_num = args[index + 1]
        parsed_args.append(int(port_num))
    

    ip_address = socket.INADDR_ANY
    parsed_args.append(ip_address)
    return parsed_args 

def handle_client_connection(server_socket):
    conn, addr = server_socket.accept()
    print(conn)
    print(addr)
    if conn:
        print("accepted client connection...")
    return conn

def start_server(parsed_args):

    port_num = parsed_args[0]
    ip_address = parsed_args[1]

    new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        new_socket.bind((str(ip_address), port_num))
    except PermissionError:
        sys.exit("Permision denied! Use another port number!")
    new_socket.listen(10)
    while(True):
        try:
   
            print("Server is listening on port number " + str(port_num) + " at IP address " + str(ip_address))
            print(new_socket)
            connection = handle_client_connection(new_socket)

            # data = ""
            
            recieved_data = connection.recv(1024)
            decoded_data = recieved_data.decode("utf-8")
            #  while loop where keep going until all message sent(get by passing the length of the message and sending parts until the total size is length of message)
            # data += decoded_data
            # print("Data: " + data)
            handle_client_request(decoded_data, connection)
        except KeyboardInterrupt:
            try:
                try: 
                    connection.send(str.encode("Error: Server disconnected"))
                    connection.close()
                except BrokenPipeError:
                    sys.exit("\nServer disconnected")
            except UnboundLocalError:
                sys.exit("\nServer disconnected")
            sys.exit("\nServer disconnected")
        
def count_letters_case_sensitive(file_content):

    unique_letters = []
    content_as_letters = list(file_content)
    for char in content_as_letters:
        if char not in unique_letters and char.isalpha():
            unique_letters.append(char)
    
    number_of_unique_letters = len(unique_letters)
    return number_of_unique_letters
        


def handle_client_request(file_content, connection):
    print("handling client request...")
    num_of_letters = count_letters_case_sensitive(file_content)
    # time.sleep(20)
    try:
        str_num_of_letters  = str(num_of_letters)
        connection.send(str.encode(str_num_of_letters))
    except BrokenPipeError:
        print("Client Disconnected\n")


def main():
    cmd_args = sys.argv
    validated_args = handle_arguments(cmd_args)    
    parsed_args = parse_arguments(validated_args)
    start_server(parsed_args)
main()
