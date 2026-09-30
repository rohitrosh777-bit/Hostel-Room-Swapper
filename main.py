import sys
from room_data import init_csv_files, load_users, save_users
from auth import hash_password, verify_password, generate_token, authenticate_session
from swap_engine import create_change_request, create_swap_request, get_user_requests, load_requests
from admin_reports import process_request, generate_audit_ledger

def show_menu():
    print("\n===== HOSTEL ROOM CHANGE & SWAP SYSTEM =====")
    print("1. Login")
    print("2. Register Student")
    print("3. Submit Room Change Request")
    print("4. Submit Mutual Swap Request")
    print("5. View My Requests")
    print("6. [Admin] Process Pending Requests")
    print("7. [Admin] Generate Audit Ledger")
    print("8. Exit")

def main():
    init_csv_files()
    current_token = None

    while True:
        show_menu()
        choice = input("Enter choice (1-8): ").strip()

        if choice == "1":
            reg_no = input("Registration No: ").strip()
            pwd = input("Password: ").strip()
            users = load_users()
            user = next((u for u in users if u["reg_no"] == reg_no), None)

            if user and verify_password(pwd, user["password_hash"]):
                current_token = generate_token(user["id"], user["role"])
                print(f"Login Successful! Welcome, {user['name']} ({user['role']})")
            else:
                print("Error: Invalid credentials.")

        elif choice == "2":
            name = input("Name: ").strip()
            reg_no = input("Registration No: ").strip()
            pwd = input("Password: ").strip()
            users = load_users()

            if any(u["reg_no"] == reg_no for u in users):
                print("Error: Registration number already registered.")
                continue

            user_id = f"U{len(users) + 101}"
            users.append({
                "id": user_id,
                "name": name,
                "reg_no": reg_no,
                "password_hash": hash_password(pwd),
                "role": "STUDENT",
                "current_room_id": "R101" # Default initial allocation
            })
            save_users(users)
            print(f"Registration successful. Assigned User ID: {user_id}")

        elif choice in ["3", "4", "5"]:
            session = authenticate_session(current_token) if current_token else None
            if not session:
                print("Error: Please login first.")
                continue

            if choice == "3":
                target_room = input("Enter Target Room ID (e.g., R102): ").strip()
                reason = input("Enter Reason: ").strip()
                ok, msg = create_change_request(session["user_id"], target_room, reason)
                print(msg)

            elif choice == "4":
                target_student = input("Enter Target Student ID (e.g., U102): ").strip()
                reason = input("Enter Reason: ").strip()
                ok, msg = create_swap_request(session["user_id"], target_student, reason)
                print(msg)

            elif choice == "5":
                reqs = get_user_requests(session["user_id"])
                print("\nYour Requests:")
                for r in reqs:
                    print(r)

        elif choice in ["6", "7"]:
            session = authenticate_session(current_token) if current_token else None
            if not session or session["role"] != "ADMIN":
                print("Error: Admin access required.")
                continue

            if choice == "6":
                print("\nPending Requests:")
                pending = [r for r in load_requests() if r["status"] == "PENDING"]
                print(pending if pending else "No pending requests.")

                req_id = input("Enter Request ID to process: ").strip()
                action = input("Enter Action (APPROVE / REJECT): ").strip()
                ok, msg = process_request(req_id, action)
                print(msg)

            elif choice == "7":
                ledger = generate_audit_ledger()
                print("\nAudit Ledger Generated and saved to audit_ledger.json:")
                print(ledger)

        elif choice == "8":
            print("Exiting application. Goodbye!")
            sys.exit(0)

if __name__ == "__main__":
    main()
