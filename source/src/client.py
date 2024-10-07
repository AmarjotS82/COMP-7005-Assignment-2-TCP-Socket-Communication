import sys
import socket

def connect_to_server(port_num, ip_addr):
    new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        new_socket.connect((ip_addr, port_num))
    except ConnectionRefusedError:
        sys.exit("Error: Connection refused server is not listening")
    return new_socket

def send_file_content(fileName, connected_socket):
    i = 0
    with open(fileName) as f:
        while True:
            contents = f.read(1024)
            if not contents:
                print("Done reading")
                connected_socket.send(str.encode("EndofFile"))
                break
            print("Chunk: " + str(i))
            i +=1
            connected_socket.send(str.encode(contents))

def send_request(file, connected_socket):
    print("sending request...")
    send_file_content(file, connected_socket)
        
    # byte_of_contes = bytes(contents)
 
    # content_less_than_buffer = ""
    # for char in list(contents):
    #     if len(str.encode(content_less_than_buffer)) < 1024:
    #         content_less_than_buffer += char
    #     else:
    #         connected_socket.send(str.encode(content_less_than_buffer))
    #         content_less_than_buffer = ""

def recieve_request(connected_socket):
    print("recievieng request...")
    try:
        data = connected_socket.recv(1024)
    except ConnectionResetError:
        sys.exit("Error: Server disconnected")
    except KeyboardInterrupt:
        close_connection(connected_socket)
        sys.exit("\nYou have disconnected from the server")
    print(data.decode("utf-8"))

def handle_arguments(args):
    if len(args) == 1:
        sys.exit("Error: no arguments provided need -p server port number -i server ip address -f file ")
    
    flags = ["-p", "-i", "-f"]
    
    if len(args) > 7:
        sys.exit("Error: Too many arguments provided")
    
    for i in range(len(flags)):
        try:
            index = args.index(flags[i])
            arg_label = ""
            if i == 0:
                arg_label += "port number"
            elif i == 1:
                arg_label += "ip address" 
            else:
                 arg_label += "file" 
        except ValueError:
            sys.exit("Error: need " + flags[i] + " flag before " + arg_label)

        if len(args) == (index+1) or not args[(index+1)].strip():
            sys.exit("Error: no " + arg_label + " provided")   
    return args

def parse_arguments(args):
    flags = ["-p","-i","-f"]
    parsed_values = []
    for i in range(len(flags)):
        index = args.index(flags[i])
        parsed_value = args[index + 1]
        parsed_values.append(parsed_value)
    return parsed_values 

def close_connection(client_socket):
    client_socket.close()

def main():
    cmd_args = sys.argv
    validated_args = handle_arguments(cmd_args)
    parsed_values = parse_arguments(validated_args)

    port_num = int(parsed_values[0])
    ip_address = parsed_values[1]
    file = parsed_values[2]
    print(parsed_values)
    client_socket = connect_to_server(port_num, ip_address)
    print("Connected to server on port number " + str(port_num) + " at IP address " + ip_address)
    send_request(file, client_socket)
    recieve_request(client_socket)
    close_connection(client_socket)


main()