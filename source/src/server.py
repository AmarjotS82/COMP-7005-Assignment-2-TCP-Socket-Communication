import socket
import sys
import time


def handle_arguments(args):
    if len(args) < 2:
        sys.exit("Error: no arguments provided")
    if len(args) > 3:
        sys.exit("Error: Too many arguments provided")
    try:
        index = args.index("-p")
    except ValueError:
        sys.exit("Error: need -p flag before port number")

    if (index+1) == len(args):
        sys.exit("Error: No port number provided!")
    
    return args
    

def parse_arguments(args):
    parsed_args = []
    index = args.index("-p")
    port_num = args[index + 1]
    try:
        int_rep_port_num = int(port_num)
    except ValueError:
        sys.exit("Error: Invalid port number!")
    parsed_args.append(int_rep_port_num)
    

    ip_address = socket.INADDR_ANY
    parsed_args.append(ip_address)
    return parsed_args 

def handle_client_connection(server_socket):
    conn, addr = server_socket.accept()
    if conn:
        print("accepted client connection...")
    return conn

def recieve_data(connection):
    data = ""
            
    while True: 
        recieved_data = connection.recv(1024)
        decoded_data =  recieved_data.decode("utf-8")
        ("reading data chunk...")
        if "EndofFile" in decoded_data : 
            print("End of file done recieveing")
            message_before_marker = decoded_data.split("EndofFile")[0].strip()
            data += message_before_marker
            handle_client_request(data, connection)
            break
        data += decoded_data

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
   
            print("Server is listening on port number " + str(port_num))
            connection = handle_client_connection(new_socket)
            recieve_data(connection)

        except KeyboardInterrupt:
            try:
                try: 
                    connection.send(str.encode("Error: Server disconnected"))
                    connection.close()
                except BrokenPipeError:
                    sys.exit("\nServer disconnected")
                    connection.close()
            except UnboundLocalError:
                sys.exit("\nServer disconnected")
                connection.close()
            sys.exit("\nServer disconnected")
            connection.close()
        
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
    # print(file_content)
    # time.sleep(10)
    num_of_letters = count_letters_case_sensitive(file_content)
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
