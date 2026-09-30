import json
import logging
from datetime import datetime
from room_data import load_users, save_users, load_rooms, save_rooms
from swap_engine import load_requests, save_requests

logging.basicConfig(filename="app.log", level=logging.INFO, format="%(asctime)s - %(message)s")

def process_request(request_id: str, action: str):
    """Approves/Rejects requests and updates CSV allocations."""
    requests = load_requests()
    req = next((r for r in requests if r["id"] == request_id), None)

    if not req or req["status"] != "PENDING":
        return False, "Invalid or already processed request."

    if action.upper() == "REJECT":
        req["status"] = "REJECTED"
        save_requests(requests)
        logging.info(f"Request {request_id} REJECTED.")
        return True, "Request rejected."

    if action.upper() == "APPROVE":
        users = load_users()
        rooms = load_rooms()

        if req["request_type"] == "CHANGE":
            student = next(u for u in users if u["id"] == req["student_id"])
            old_room_id = student["current_room_id"]
            new_room_id = req["target_room_id"]

            # Decrease old room occupancy
            if old_room_id:
                old_room = next((r for r in rooms if r["id"] == old_room_id), None)
                if old_room and int(old_room["occupied"]) > 0:
                    old_room["occupied"] = str(int(old_room["occupied"]) - 1)

            # Increase new room occupancy & reassign student
            new_room = next(r for r in rooms if r["id"] == new_room_id)
            new_room["occupied"] = str(int(new_room["occupied"]) + 1)
            student["current_room_id"] = new_room_id

        elif req["request_type"] == "SWAP":
            s1 = next(u for u in users if u["id"] == req["student_id"])
            s2 = next(u for u in users if u["id"] == req["target_student_id"])

            # Swap room assignments
            s1["current_room_id"], s2["current_room_id"] = s2["current_room_id"], s1["current_room_id"]

        req["status"] = "APPROVED"

        # Commit updates
        save_users(users)
        save_rooms(rooms)
        save_requests(requests)

        logging.info(f"Request {request_id} APPROVED.")
        return True, "Request approved and room allocations updated in CSV."

    return False, "Invalid action choice."

def generate_audit_ledger():
    """Generates timestamped audit ledger in JSON."""
    users = load_users()
    rooms = load_rooms()
    requests = load_requests()

    summary = {
        "timestamp": datetime.now().isoformat(),
        "total_students": len([u for u in users if u["role"] == "STUDENT"]),
        "total_rooms": len(rooms),
        "pending_requests": len([r for r in requests if r["status"] == "PENDING"]),
        "approved_requests": len([r for r in requests if r["status"] == "APPROVED"])
    }

    # Write audit ledger
    with open("audit_ledger.json", "w") as f:
        json.dump(summary, f, indent=4)

    return summary
