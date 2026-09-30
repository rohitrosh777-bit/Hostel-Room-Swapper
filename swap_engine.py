import json
import os
from room_data import load_rooms, load_users

REQUESTS_JSON = "requests.json"

def load_requests() -> list:
    """Reads all requests from JSON file."""
    if os.path.exists(REQUESTS_JSON):
        with open(REQUESTS_JSON, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_requests(requests: list):
    """Saves all requests to JSON file."""
    with open(REQUESTS_JSON, "w") as f:
        json.dump(requests, f, indent=4)

def create_change_request(student_id: str, target_room_id: str, reason: str):
    """Creates a room change request."""
    rooms = load_rooms()
    target_room = next((r for r in rooms if r["id"] == target_room_id), None)

    if not target_room:
        return False, "Target room does not exist."

    if int(target_room["occupied"]) >= int(target_room["capacity"]):
        return False, "Target room is currently full."

    requests = load_requests()
    req_id = f"REQ{len(requests) + 1:03d}"

    new_req = {
        "id": req_id,
        "student_id": student_id,
        "target_room_id": target_room_id,
        "target_student_id": None,
        "request_type": "CHANGE",
        "reason": reason,
        "status": "PENDING"
    }

    requests.append(new_req)
    save_requests(requests)
    return True, f"Room change request {req_id} submitted successfully."

def create_swap_request(student_id: str, target_student_id: str, reason: str):
    """Creates a mutual peer-to-peer swap request."""
    if student_id == target_student_id:
        return False, "Cannot initiate swap with yourself."

    users = load_users()
    target_user = next((u for u in users if u["id"] == target_student_id), None)

    if not target_user:
        return False, "Target student does not exist."

    requests = load_requests()
    req_id = f"REQ{len(requests) + 1:03d}"

    new_req = {
        "id": req_id,
        "student_id": student_id,
        "target_room_id": None,
        "target_student_id": target_student_id,
        "request_type": "SWAP",
        "reason": reason,
        "status": "PENDING"
    }

    requests.append(new_req)
    save_requests(requests)
    return True, f"Mutual swap request {req_id} submitted successfully."

def get_user_requests(student_id: str) -> list:
    """Retrieves all requests for a specific student."""
    requests = load_requests()
    return [r for r in requests if r["student_id"] == student_id or r["target_student_id"] == student_id]
