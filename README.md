Customer-Database-Server
A simple Python-based client/server system for managing customer records over a local network.
Originally built as a backend prototype for small-scale customer management, this project demonstrates
how lightweight, socket-based communication can be used to build a reliable and extensible data service.

#Features

Client–Server Architecture: Built with Python’s socket and socketserver modules.
CRUD Operations: Supports adding, updating, deleting, and searching for customer records.
In-memory Database: Stores and retrieves customer data efficiently during runtime.
Input Validation: Checks for missing or malformed data before committing updates.
Persistent Storage: Reads and writes data to a text or JSON file to maintain state across sessions.
Command-line Interface: Text-based UI for interacting with the database.
#Real-world Use This project simulates a lightweight Customer Relationship Management (CRM) backend for small businesses.
It’s designed to reflect real-world principles of:

Reliable network communication between client and server.
Data integrity and validation.
Maintainable architecture that could evolve into a REST API or connect to a web front end.
Such a design is practical for local business tools (e.g., hair salons, community centers, repair shops)
that need an offline system for managing clients without deploying a full SQL server.

customer-db/
├── client.py        # CLI client for sending commands and viewing responses
├── server.py        # Socket-based server handling requests and maintaining the database
├── customers.json   # Example local data store
├── README.md        # Project documentation

