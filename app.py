import json
import os
from datetime import date

FILE = "library.json"

def load_data():
    if os.path.exists(FILE):
        with open(FILE, "r") as f:
            return json.load(f)
    return {
        "books": [],
        "students": [],
        "records": []
    }

data = load_data()

def save_data():
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)

def add_book():
    bid = input("Enter Book ID: ")

    if any(b["id"] == bid for b in data["books"]):
        print("Book already exists!")
        return

    title = input("Enter Book Title: ")
    author = input("Enter Author: ")
    qty = int(input("Enter Quantity: "))

    if qty <= 0:
        print("Invalid quantity!")
        return

    data["books"].append({
        "id": bid,
        "title": title,
        "author": author,
        "total": qty,
        "available": qty
    })

    save_data()
    print("Book added successfully!")

def display_books():
    print("\n--- BOOK DETAILS ---")

    for b in data["books"]:
        print(
            b["id"], "|",
            b["title"], "|",
            b["author"], "| Available:",
            b["available"]
        )

def register_student():
    sid = input("Enter Student ID: ")

    if any(s["id"] == sid for s in data["students"]):
        print("Student already registered!")
        return

    name = input("Enter Student Name: ")
    department = input("Enter Department: ")

    data["students"].append({
        "id": sid,
        "name": name,
        "department": department
    })

    save_data()
    print("Student registered successfully!")

def issue_book():
    sid = input("Enter Student ID: ")
    bid = input("Enter Book ID: ")

    student = next(
        (s for s in data["students"]
         if s["id"] == sid), None
    )

    book = next(
        (b for b in data["books"]
         if b["id"] == bid), None
    )

    if not student:
        print("Student not found!")
        return

    if not book:
        print("Book not found!")
        return

    if book["available"] <= 0:
        print("Book not available!")
        return

    data["records"].append({
        "student_id": sid,
        "book_id": bid,
        "issue_date": str(date.today()),
        "return_date": None
    })

    book["available"] -= 1

    save_data()
    print("Book issued successfully!")

def return_book():
    sid = input("Enter Student ID: ")
    bid = input("Enter Book ID: ")

    record = next(
        (r for r in data["records"]
         if r["student_id"] == sid
         and r["book_id"] == bid
         and r["return_date"] is None),
        None
    )

    if not record:
        print("Borrowing record not found!")
        return

    record["return_date"] = str(date.today())

    book = next(
        (b for b in data["books"]
         if b["id"] == bid), None
    )

    if book:
        book["available"] += 1

    save_data()
    print("Book returned successfully!")

def search_book():
    keyword = input("Enter Book ID or Title: ").lower()

    for b in data["books"]:
        if keyword == b["id"].lower() or keyword in b["title"].lower():
            print(b)
            return

    print("Book not found!")

def borrowing_records():
    print("\n--- BORROWING HISTORY ---")

    for r in data["records"]:
        print(
            "Student:", r["student_id"],
            "| Book:", r["book_id"],
            "| Issued:", r["issue_date"],
            "| Returned:", r["return_date"] or "Pending"
        )

def main():
    while True:
        print("\n===== LIBRARY MANAGEMENT SYSTEM =====")
        print("1. Add Book")
        print("2. Display Books")
        print("3. Register Student")
        print("4. Issue Book")
        print("5. Return Book")
        print("6. Search Book")
        print("7. Borrowing Records")
        print("8. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_book()
        elif choice == "2":
            display_books()
        elif choice == "3":
            register_student()
        elif choice == "4":
            issue_book()
        elif choice == "5":
            return_book()
        elif choice == "6":
            search_book()
        elif choice == "7":
            borrowing_records()
        elif choice == "8":
            print("Thank you!")
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()