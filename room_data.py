import csv
import os

USERS_CSV = "users.csv"
ROOMS_CSV = "rooms.csv"

def init_csv_files():
    """Initializes empty CSV files with headers if they don't exist."""
    if not os.path.exists(USERS_CSV):
        with open(USERS_CSV, mode="w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "name", "reg_no", "password_hash", "role", "current_room_id"])
            # Seed default admin account
            from auth import hash_password
            writer.writerow(["U101", "Admin Warden", "ADMIN01", hash_password("admin123"), "ADMIN", ""])

    if not os.path.exists(ROOMS_CSV):
        with open(ROOMS_CSV, mode="w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "room_number", "block", "capacity", "occupied"])
            # Seed sample rooms
            writer.writerow(["R101", "101", "A-Block", "2", "0"])
            writer.writerow(["R102", "102", "A-Block", "2", "0"])

def load_users() -> list:
    """Loads all user records from CSV."""
    users = []
    if os.path.exists(USERS_CSV):
        with open(USERS_CSV, mode="r") as f:
            reader = csv.DictReader(f)
            users = list(reader)
    return users

def save_users(users: list):
    """Overwrites user records to CSV."""
    if users:
        fieldnames = users[0].keys()
        with open(USERS_CSV, mode="w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(users)

def load_rooms() -> list:
    """Loads room allocations from CSV."""
    rooms = []
    if os.path.exists(ROOMS_CSV):
        with open(ROOMS_CSV, mode="r") as f:
            reader = csv.DictReader(f)
            rooms = list(reader)
    return rooms

def save_rooms(rooms: list):
    """Overwrites room records to CSV."""
    if rooms:
        fieldnames = rooms[0].keys()
        with open(ROOMS_CSV, mode="w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rooms)
