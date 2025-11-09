import socket
import threading
import os
import json
HOST = "127.0.0.1"
PORT = 9999
DATA_FILE = "data.txt"

def load_data():
    try:
        with open('customers.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_data(data):
    with open('customers.json', 'w') as f:
        json.dump(data, f, indent=2)

def valid_phone(phone: str) -> bool:
    if phone == "":
        return True
    
    if len(phone) != 8 or phone[3] != "-":
        return False

    if phone[:3] not in {"394", "426", "901", "514"}:
        return False
    tail = phone[4:]
    return all('0' <= ch <= '9' for ch in tail)

def load_database(filename):
    db = {}
    skipped = []
    if not os.path.exists(filename):
        print(f"File {filename} not found.")
        return db, skipped

    f = open(filename, "r")
    try:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts_raw = line.split("|")
            parts = []
            # strip spaces at both ends and append
            for p in parts_raw:
                parts.append(p.strip())
            if len(parts) != 4:
                skipped.append(line)
                continue
            name, age, addr, phone = parts

            # name 
            if not name:
                skipped.append(line)
                continue
            # age 
            try:
                age_int = int(age)
                if age_int < 1 or age_int > 120:
                    skipped.append(line)
                    continue
            except ValueError:
                skipped.append(line)
                continue

            # phone 
            if not valid_phone(phone):
                skipped.append(line)
                continue

            # duplicate check 
            if name.lower() in [n.lower() for n in db.keys()]:
                skipped.append(line)
                continue

            db[name] = {"age": age_int, "address": addr, "phone": phone}
    finally:
        f.close()

    print("Skipped invalid records:")
    for r in skipped:
        print("  ", r)
    return db, skipped

def handle_client(conn, addr, db):
    print(f"Connected by {addr}")
    while True:
        data = conn.recv(1024).decode().strip()
        if not data:
            break

        parts = data.split("|")
        cmd = parts[0].upper()

        if cmd == "FIND":
            name = parts[1].strip()
            found = None
            for k, v in db.items():
                if k.lower() == name.lower():
                    found = v
                    name = k
                    break
            if found:
                msg = f"{name}|{found['age']}|{found['address']}|{found['phone']}"
            else:
                msg = "Customer not found."

        elif cmd == "ADD":
            if len(parts) != 5:
                msg = "Invalid ADD command format."
            else:
                name, age, addr, phone = [p.strip() for p in parts[1:]]
                if not name:
                    msg = "Error: name cannot be empty."
                elif name.lower() in [n.lower() for n in db.keys()]:
                    msg = "Error: customer already exists."
                else:
                    try:
                        age_int = int(age)
                        if age_int < 1 or age_int > 120:
                            msg = "Error: invalid age."
                        elif not valid_phone(phone):
                            msg = "Error: invalid phone."
                        else:
                            db[name] = {"age": age_int,
                                        "address": addr, "phone": phone}
                            msg = "Customer added successfully."
                    except ValueError:
                        msg = "Error: invalid age."

        elif cmd == "DELETE":
            name = parts[1].strip()
            deleted = False
            for k in list(db.keys()):
                if k.lower() == name.lower():
                    del db[k]
                    deleted = True
                    break
            msg = "Customer deleted." if deleted else "Customer does not exist."

        elif cmd == "UPDATE_AGE":
            name, new_age = parts[1].strip(), parts[2].strip()
            found_key = None
            for k in db.keys():
                if k.lower() == name.lower():
                    found_key = k
                    break
            if not found_key:
                msg = "Customer not found."
            else:
                try:
                    age_int = int(new_age)
                    if 1 <= age_int <= 120:
                        db[found_key]["age"] = age_int
                        msg = "Age updated."
                    else:
                        msg = "Invalid age range."
                except ValueError:
                    msg = "Invalid age format."

        elif cmd == "UPDATE_ADDR":
            name, new_addr = parts[1].strip(), parts[2].strip()
            found_key = None
            for k in db.keys():
                if k.lower() == name.lower():
                    found_key = k
                    break
            if not found_key:
                msg = "Customer not found."
            else:
                db[found_key]["address"] = new_addr
                msg = "Address updated."

        elif cmd == "UPDATE_PHONE":
            name, new_phone = parts[1].strip(), parts[2].strip()
            found_key = None
            for k in db.keys():
                if k.lower() == name.lower():
                    found_key = k
                    break
            if not found_key:
                msg = "Customer not found."
            elif not valid_phone(new_phone):
                msg = "Invalid phone format."
            else:
                db[found_key]["phone"] = new_phone
                msg = "Phone updated."

        elif cmd == "REPORT":
            sorted_items = sorted(db.items(), key=lambda x: x[0].lower())
            lines = ["Name       | Age | Address             | Phone"]
            lines.append("-----------------------------------------------")
            for name, info in sorted_items:
                lines.append(
                    f"{name:<10} | {info['age']:<3} | {info['address'][:20]:<20} | {info['phone']}"
                )
            msg = "\n".join(lines)

        elif cmd == "EXIT":
            msg = "Good bye"
            conn.sendall(msg.encode())
            break

        else:
            msg = "Unknown command."

        conn.sendall(msg.encode())

    conn.close()

def main():
    db, skipped = load_database(DATA_FILE)
    print(f"Loaded {len(db)} valid records.")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"Server running on {HOST}:{PORT}...")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr, db))
        thread.start()


if __name__ == "__main__":
    main()
