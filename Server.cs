using System;
using System.Net;
using System.Net.Sockets;
using System.Text;

class Program
{
    static void SendCommand(Socket socket, string command)
    {
        try
        {
            // Send the command
            byte[] buffer = Encoding.ASCII.GetBytes(command);
            socket.Send(buffer);
            Console.WriteLine($"Command \"{command}\" sent successfully.");
        }
        catch (Exception ex)
        {
            Console.WriteLine($"An error occurred while sending the command: {ex.Message}");
        }
    }

    static void Main(string[] args)
    {
        // Replace with the IP address of your Raspberry Pi Pico W
        string picoIp = "10.0.0.188";
        int picoPort = 80;

        try
        {
            // Create a socket and connect to the Pico W
            IPAddress ipAddress = IPAddress.Parse(picoIp);
            IPEndPoint remoteEP = new IPEndPoint(ipAddress, picoPort);
            Socket socket = new Socket(ipAddress.AddressFamily, SocketType.Stream, ProtocolType.Tcp);
            socket.Connect(remoteEP);
            Console.WriteLine("Connected to the Raspberry Pi Pico W.");

            while (true)
            {
                // Get the command from the user
                Console.Write("Enter a command (green, yellow, red, or quit): ");
                string command = Console.ReadLine().ToLower();
                if (command == "quit")
                {
                    Console.WriteLine("Exiting the program.");
                    break;
                }
                if (command == "green" || command == "yellow" || command == "red")
                {
                    SendCommand(socket, command);
                }
                else
                {
                    Console.WriteLine("Invalid command. Please enter green, yellow, red, or quit.");
                }
            }

            // Close the socket when the program exits
            socket.Shutdown(SocketShutdown.Both);
            socket.Close();
            Console.WriteLine("Disconnected from the Raspberry Pi Pico W.");
        }
        catch (SocketException)
        {
            Console.WriteLine("Failed to connect to the Raspberry Pi Pico W.");
        }
        catch (Exception ex)
        {
            Console.WriteLine($"An error occurred: {ex.Message}");
        }
    }
}
