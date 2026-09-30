# Problem Statement: Hostel Room Change & Swap System

## 1. Executive Summary
Managing student hostel room allocations and room change requests manually often leads to administrative overhead, delayed approvals, data discrepancies, and lack of transparency. The **Hostel Room Change & Swap System** is a lightweight, secure, CLI-based solution designed to digitize and automate the room transfer and mutual swap workflow for students and hostel administrators.

---

## 2. Background & Problem Description
In traditional educational institution hostels:
- **Paper-based/Manual Tracking**: Room transfers are tracked using physical registers or unorganized emails, leading to lost requests or unrecorded room moves.
- **Unauthorized Swaps**: Students often swap rooms mutually without official records, creating discrepancy between physical room occupancy and central database records.
- **Occupancy Mismatches**: Lack of real-time validation leads to room over-allocation beyond maximum capacity.
- **Lack of Transparency**: Students have no visibility into the approval status of their transfer or swap requests.
- **Missing Audit Trails**: Warden decisions (approvals/rejections) lack timestamped audit ledgers for compliance and historical tracking.

---

## 3. Project Objectives
The objective of this project is to build a reliable, file-backed management platform that:
1. **Provides Role-Based Access Control (RBAC)** for Students and Hostel Wardens (Admins).
2. **Automates Mutual Swaps & Room Transfers** with immediate validity checks (room capacity, existing student IDs).
3. **Synchronizes Data Automatically** across users and room capacity registers upon request approval.
4. **Maintains Audit Ledgers and Application Logs** to log administrative actions for accountability.

---

## 4. Scope & Key Functional Requirements

### A. Authentication & Session Management
- **Role Support**: Student and Admin roles.
- **Data Security**: Secure password hashing via standard `SHA-256`.
- **Session Tokens**: Token-backed session verification for CLI operations.

### B. Student Workflows
- **Direct Room Change**: Submit a request for an available target room. System verifies target room existence and capacity before submission.
- **Mutual Peer Swap**: Initiate a swap request with another student using their unique User ID.
- **Status Tracking**: View all submitted requests and their current status (`PENDING`, `APPROVED`, `REJECTED`).

### C. Warden / Admin Workflows
- **Request Processing**: Review pending room change or swap requests and execute `APPROVE` or `REJECT` actions.
- **Automated Re-allocation**: Approving a request dynamically adjusts room occupancy counts and swaps student room IDs in persistent storage.
- **Audit Ledger Generation**: Export timestamped JSON summary snapshots (`audit_ledger.json`) containing system-wide totals and request metrics.
- **Activity Logging**: Maintain action logs (`app.log`) capturing timestamped administrative decisions.

---

## 5. Technical & Non-Functional Architecture
- **Language & Runtime**: Python 3.x using native standard libraries to ensure zero heavy external dependencies.
- **Persistence Layer**: 
  - `CSV` format for relational data (`users.csv`, `rooms.csv`).
  - `JSON` format for transactional data (`requests.json`, `audit_ledger.json`).
- **Data Integrity**: State validations prevent invalid transitions (e.g., self-swaps, transferring to non-existent rooms, double-processing requests).