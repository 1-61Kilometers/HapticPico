import socket

def send_command(sock, command):
    try:
        # Send the command
        sock.sendall(command.encode())
        print(f'Command "{command}" sent successfully.')
    except Exception as e:
        print(f'An error occurred while sending the command: {str(e)}')

def main():
    # Replace with the IP address of your Raspberry Pi Pico W
    pico_ip = '10.0.0.188'
    pico_port = 80

    try:
        # Create a socket and connect to the Pico W
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((pico_ip, pico_port))
        print('Connected to the Raspberry Pi Pico W.')

        while True:
            # Get the command from the user
            command = input('Enter a command (green, yellow, red, or quit): ')
            if command.lower() == 'quit':
                print('Exiting the program.')
                break
            if command.lower() in ['green', 'yellow', 'red']:
                send_command(sock, command.lower())
            else:
                print('Invalid command. Please enter green, yellow, red, or quit.')

    except ConnectionError:
        print('Failed to connect to the Raspberry Pi Pico W.')
    except Exception as e:
        print(f'An error occurred: {str(e)}')
    finally:
        # Close the socket when the program exits
        sock.close()
        print('Disconnected from the Raspberry Pi Pico W.')

if __name__ == '__main__':
    main()
