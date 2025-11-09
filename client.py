import socket
import os

HOST = "127.0.0.1"
PORT = 9999


def clear_screen():
    os.system("clear")


def press_key():
    input("\nPress Enter to continue...")


def send_and_receive(sock, msg):
    sock.sendall(msg.encode())
    response = sock.recv(4096).decode()
    print("\n" + response)
    press_key()


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        while True:
            clear_screen()
            print("=== Customer Database Menu ===")
            print("1. Find customer")
            print("2. Add customer")
            print("3. Delete customer")
            print("4. Update age")
            print("5. Update address")
            print("6. Update phone number")
            print("7. Print report")
            print("8. Exit")

            choice = input("Select: ").strip()
            if choice == "1":
                name = input("Enter customer name: ")
                send_and_receive(s, f"FIND|{name}")

            elif choice == "2":
                name = input("Name: ")
                age = input("Age: ")
                addr = input("Address: ")
                phone = input("Phone (###-#### or empty): ")
                send_and_receive(s, f"ADD|{name}|{age}|{addr}|{phone}")

            elif choice == "3":
                name = input("Enter name to delete: ")
                send_and_receive(s, f"DELETE|{name}")

            elif choice == "4":
                name = input("Enter name: ")
                new_age = input("Enter new age: ")
                send_and_receive(s, f"UPDATE_AGE|{name}|{new_age}")

            elif choice == "5":
                name = input("Enter name: ")
                new_addr = input("Enter new address: ")
                send_and_receive(s, f"UPDATE_ADDR|{name}|{new_addr}")

            elif choice == "6":
                name = input("Enter name: ")
                new_phone = input("Enter new phone (###-#### or empty): ")
                send_and_receive(s, f"UPDATE_PHONE|{name}|{new_phone}")

            elif choice == "7":
                send_and_receive(s, "REPORT")

            elif choice == "8":
                s.sendall("EXIT".encode())
                print("Good bye.")
                break
            else:
                print("Invalid selection.")
                press_key()


if __name__ == "__main__":
    main()
