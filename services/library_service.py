"""
Library Service Module - Business Logic Functions
Contains all the core business logic for the Library Management System
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from database import (
    get_book_by_id, get_book_by_isbn, get_patron_borrow_count,
    insert_book, insert_borrow_record, update_book_availability,
    update_borrow_record_return_date, get_all_books, get_patron_borrowed_books,
    get_db_connection, init_database 
)
import os

# Ensure DB exists before any operations
if not os.path.exists("library.db"):
    init_database()

def add_book_to_catalog(title: str, author: str, isbn: str, total_copies: int) -> Tuple[bool, str]:
    """
    Add a new book to the catalog.
    Implements R1: Book Catalog Management
    
    Args:
        title: Book title (max 200 chars)
        author: Book author (max 100 chars)
        isbn: 13-digit ISBN
        total_copies: Number of copies (positive integer)
        
    Returns:
        tuple: (success: bool, message: str)
    """
    # Input validation
    if not title or not title.strip():
        return False, "Title is required."
    
    if len(title.strip()) > 200:
        return False, "Title must be less than 200 characters."
    
    if not author or not author.strip():
        return False, "Author is required."
    
    if len(author.strip()) > 100:
        return False, "Author must be less than 100 characters."
    
    if len(isbn) != 13:
        return False, "ISBN must be exactly 13 digits."
    
    if not isinstance(total_copies, int) or total_copies <= 0:
        return False, "Total copies must be a positive integer."
    
    # Check for duplicate ISBN
    existing = get_book_by_isbn(isbn)
    if existing:
        return False, "A book with this ISBN already exists."
    
    # Insert new book
    # Insert new book
    inserted = insert_book(title.strip(), author.strip(), isbn, total_copies, total_copies)
    if inserted:
        return True, "Book successfully added to the catalog."
    return False, "Database error occurred while adding the book."


def borrow_book_by_patron(patron_id: str, book_id: int) -> Tuple[bool, str]:
    """
    Allow a patron to borrow a book.
    Implements R3 as per requirements  
    """
    # Validate patron ID
    if not patron_id or not patron_id.isdigit() or len(patron_id) != 6:
        return False, "Invalid patron ID. Must be exactly 6 digits."

    # Get book details
    book = get_book_by_id(book_id)
    if not book:
        return False, "Book not found."

    # Check patron's borrow limit first
    current_borrowed = get_patron_borrow_count(patron_id)
    if current_borrowed >= 5:
        return False, "You have reached the maximum borrowing limit of 5 books."

    # Check availability
    if book.get("available_copies", 0) <= 0:
        return False, "This book is currently not available."

    # Create borrow record
    borrow_date = datetime.now()
    due_date = borrow_date + timedelta(days=14)

    borrow_success = insert_borrow_record(patron_id, book_id, borrow_date, due_date)
    if not borrow_success:
        return False, "Database error occurred while creating borrow record."

    availability_success = update_book_availability(book_id, -1)
    if not availability_success:
        return False, "Database error occurred while updating book availability."

    return True, f'Successfully borrowed "{book["title"]}". Due date: {due_date.strftime("%Y-%m-%d")}.'


def return_book_by_patron(patron_id: str, book_id: int) -> Tuple[bool, str]:
    """Process book return by a patron. Implements R4."""
    if not patron_id or not patron_id.isdigit() or len(patron_id) != 6:
        return False, "Invalid patron ID. Must be exactly 6 digits."

    book = get_book_by_id(book_id)
    if not book:
        return False, "Book not found."

    # Update return record
    return_date = datetime.now()
    updated = update_borrow_record_return_date(patron_id, book_id, return_date)
    if not updated:
        return False, "No active borrow record found for this patron and book."

    # Update availability
    availability_success = update_book_availability(book_id, +1)
    if not availability_success:
        return False, "Database error while updating availability."

    # Calculate fee
    fee_info = calculate_late_fee_for_book(patron_id, book_id)
    if fee_info["fee_amount"] > 0:
        return True, f'Book "{book["title"]}" returned. Late fee: ${fee_info["fee_amount"]:.2f}'
    else:
        return True, f'Book "{book["title"]}" returned successfully. No late fees.'

def calculate_late_fee_for_book(patron_id: str, book_id: int) -> Dict:
    """Calculate late fees for a specific book. Implements R5."""
    conn = get_db_connection()
    record = conn.execute('''
        SELECT borrow_date, due_date, return_date 
        FROM borrow_records 
        WHERE patron_id = ? AND book_id = ?
        ORDER BY id DESC LIMIT 1
    ''', (patron_id, book_id)).fetchone()
    conn.close()

    if not record:
        return {"fee_amount": 0.0, "days_overdue": 0, "status": "No borrow record found"}

    due_date = datetime.fromisoformat(record["due_date"])
    return_date = datetime.fromisoformat(record["return_date"]) if record["return_date"] else datetime.now()

    overdue_days = (return_date - due_date).days
    if overdue_days <= 0:
        return {"fee_amount": 0.0, "days_overdue": 0, "status": "On time"}

    fee = 0.0
    
    if overdue_days <= 7:
        fee = 0.5 * overdue_days
    else:
        fee = (0.5 * 7) + (1.0 * (overdue_days - 7))

    fee = min(fee, 15.0)

    return {
        "fee_amount": round(fee, 2),
        "days_overdue": overdue_days,
        "status": "Overdue"
    }

def search_books_in_catalog(search_term: str, search_type: str) -> List[Dict]:
    """Search for books in the catalog. Implements R6."""
    books = get_all_books()
    term = search_term.lower().strip()

    if search_type == "title":
        return [b for b in books if term in b["title"].lower()]
    elif search_type == "author":
        return [b for b in books if term in b["author"].lower()]
    elif search_type == "isbn":
        return [b for b in books if b["isbn"] == search_term]
    else:
        return []

def get_patron_status_report(patron_id: str) -> Dict:
    """Get status report for a patron. Implements R7."""
    if not patron_id or not patron_id.isdigit() or len(patron_id) != 6:
        return {"error": "Invalid patron ID"}

    # Current borrowed
    current = get_patron_borrowed_books(patron_id)
    count = get_patron_borrow_count(patron_id)

        # Borrow history
    conn = get_db_connection()
    result = conn.execute('''
        SELECT br.*, b.title, b.author
        FROM borrow_records br
        JOIN books b ON br.book_id = b.id
        WHERE br.patron_id = ?
        ORDER BY br.borrow_date
    ''', (patron_id,))

    # ✅ handle both list and sqlite cursor
    history = result if isinstance(result, list) else result.fetchall()

    conn.close()
    history = [dict(r) for r in history]

    total_fee = 0.0
    for r in history:
        fee_info = calculate_late_fee_for_book(patron_id, r["book_id"])
        total_fee += fee_info["fee_amount"]

    return {
        "currently_borrowed": current,
        "borrow_count": count,
        "total_late_fees": round(total_fee, 2),
        "borrow_history": history
    }


def pay_late_fees(patron_id: str, book_id: int, payment_gateway) -> Tuple[bool, str]:
    """
    Process a late fee payment for a specific book.
    Uses an external PaymentGateway service.
    Implements A3: Mocking external dependencies.
    
    Args:
        patron_id: 6-digit library card ID
        book_id: ID of the book being paid for
        payment_gateway: external payment service instance

    Returns:
        tuple: (success: bool, message: str)
    """
    # Input validation
    if not patron_id or not patron_id.isdigit() or len(patron_id) != 6:
        return False, "Invalid patron ID. Must be exactly 6 digits."

    # Calculate late fee
    fee_info = calculate_late_fee_for_book(patron_id, book_id)
    if fee_info["fee_amount"] <= 0:
        return False, "No outstanding late fee for this book."

    amount = fee_info["fee_amount"]

    # Attempt to process payment using external gateway
    try:
        response = payment_gateway.process_payment(patron_id, amount)
        if response.get("status") == "success":
            transaction_id = response.get("transaction_id", "UNKNOWN")
            return True, f"Late fee of ${amount:.2f} paid successfully. Transaction ID: {transaction_id}"
        else:
            return False, f"Payment failed: {response.get('error', 'Unknown error')}"
    except Exception as e:
        return False, f"Payment processing error: {str(e)}"


def refund_late_fee_payment(transaction_id: str, amount: float, payment_gateway) -> Tuple[bool, str]:
    """
    Refund a previously paid late fee.
    Uses an external PaymentGateway service.

    Args:
        transaction_id: The ID of the original payment transaction
        amount: Amount to refund
        payment_gateway: external payment service instance

    Returns:
        tuple: (success: bool, message: str)
    """
    if not transaction_id or not isinstance(transaction_id, str):
        return False, "Invalid transaction ID."

    if not isinstance(amount, (int, float)) or amount <= 0:
        return False, "Invalid refund amount."

    # Attempt refund
    try:
        response = payment_gateway.refund_payment(transaction_id, amount)
        if response.get("status") == "success":
            refund_id = response.get("refund_id", "UNKNOWN")
            return True, f"Refund of ${amount:.2f} issued successfully. Refund ID: {refund_id}"
        else:
            return False, f"Refund failed: {response.get('error', 'Unknown error')}"
    except Exception as e:
        return False, f"Refund processing error: {str(e)}"


