# Hostel Room Change & Swap System

It is a Python program that can be used on the command line and assists both hostel managers and students in swapping rooms without having to go through the usual difficulties associated with the paperwork.

---

## What It Does

– **Secure Accounts**: The passwords are hashed using SHA-256 and session management is carried out with the use of tokens for both students and wardens.

-The students have the opportunity to see the rooms and request a change of room.

– If you wish to swap rooms with a friend, you must fill in a swap request using your friend's Student ID.

- **Warden Dashboard**: The administrator features enable the warden to view, approve or reject requests that are pending.

– The room availability and the student profiles are immediately updated in all the records as soon as the request is approved.

– **Audit Logging**: The app.log file is kept up to date and summary reports together with timestamps are exported to audit_ledger.json for use as administrative records.

---

## How Its Built

The file main.py contains the menu system and is in charge of the command line interaction loop.

The program called `Auth.py` is in charge of managing sessions and also encrypts passwords.

The file Room_data.py is the one that looks after the CSV files which contain the room lists and the student accounts.

The `Swap_engine.py` program looks after the aspect of changing rooms and also keeps a record of the requests.

The program named `Admin_reports.py` is responsible for handling approvals and rejections as well as producing system audit reports.

The file called Users.csv contains the profiles of registered students and administrators.

The Rooms.csv file includes the room numbers, the capacity, and the number of people currently in each room.

Requests.json holds change and swap requests.

A snapshot of the system status has been generated and is included in a file called Audit_ledger.json.

The App.log contains the system activity log.

---

## Quick Setup

### 1. Requirements

Your system must have Python 3.7 or a later version installed.

### 2. Carry out the application

Using your terminal, navigate to the project directory and type:

```bash

python main.py

```

Section 3: First Login as an Administrator

When you run the program for the time the system creates the necessary CSV files and creates a default warden account:

- **Registration No:** `ADMIN01`

- **Password:** `admin123`

---

## Typical Workflow

1. **For Students**:

- You can set up an account or log in to an one that you already have.

- Should you want to make a request for moving to another room, choose Option 3.

If you want to carry out an room exchange with another student, you must choose Option 4 and enter their ID.

If you want to find out the status of the approval of your request, choose option 5.

2. **For Wardens / Admins**:

- Log in using the username ADMIN01.

To see the pending requests, select **Option 6** and then type either `APPROVE` or `REJECT`.

In order to export a system snapshot, choose option 7 and save the file as audit_ledger.json.