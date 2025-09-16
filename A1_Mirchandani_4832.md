# Assignment 1 – Library Management System

**Name:** Armaan D. Mirchandani  
**Student ID (last 4 digits):** 4832  
**Group Number:** 3  

---

## Project Implementation Status

| Function | Requirement | Status | Notes |
|----------|-------------|--------|-------|
| `add_book_to_catalog` | R1 | ✅ Complete | Handles input validation, duplicate ISBN check, and inserts books correctly. |
| Catalog display (HTML templates) | R2 | ✅ Complete | Display implemented in templates; no direct business logic in `library_service.py`. |
| `borrow_book_by_patron` | R3 | ⚠️ Partial | Most logic works, but bug found: borrowing limit allows >5 books (should stop at 5). |
| `return_book_by_patron` | R4 | ❌ Not Implemented | Currently a placeholder that always returns "not implemented." |
| `calculate_late_fee_for_book` | R5 | ❌ Not Implemented | Placeholder only, no late fee calculation logic. |
| `search_books_in_catalog` | R6 | ❌ Not Implemented | Always returns an empty list. |
| `get_patron_status_report` | R7 | ❌ Not Implemented | Always returns an empty dictionary. |

---

## Test Case Summary


## R1: Add Book to Catalog  
- **Requirement:** Books must have valid title, author, ISBN, and positive copies. Duplicate ISBNs not allowed.  
- **Test Results:** ✅ All tests passed. Input validation and duplicate checks worked as intended.  
- **Status:** Pass.  

---

## R3: Borrow Book by Patron  
- **Requirement:**  
  - Patron ID must be 6 digits.  
  - Book must exist and have available copies.  
  - Patrons can borrow **up to 5 books maximum**.  
  - Borrow record created, due date set 14 days later, availability updated.  

- **Test Results:**  
  - ✅ Valid borrow: success.  
  - ✅ Invalid patron ID: rejected.  
  - ✅ Unavailable book: rejected.  
  - ❌ Borrow limit bug: A patron with 5 books already borrowed was allowed to borrow a 6th.  

- **Status:** **Fail (BUG FOUND).**  
- **Notes:** Bug in implementation: requirement says max 5, but code allows 6.  

---

## R4: Return Book  
- **Requirement:** Patrons should be able to return borrowed books, availability updated.  
- **Implementation Status:** Not implemented.  
- **Test Results:** ✅ Placeholder test passed (returns "Not implemented").  
- **Status:** Incomplete.  

---

## R5: Late Fee Calculation  
- **Requirement:** Late fees must be calculated based on days overdue.  
- **Implementation Status:** Not implemented.  
- **Test Results:** ✅ Placeholder test passed.  
- **Status:** Incomplete.  

---

## R6: Search Books  
- **Requirement:** Search by title/author/ISBN.  
- **Implementation Status:** Not implemented.  
- **Test Results:** ✅ Placeholder test passed.  
- **Status:** Incomplete.  

---

## R7: Patron Status Report  
- **Requirement:** Show patron’s borrowed books, due dates, late fees.  
- **Implementation Status:** Not implemented.  
- **Test Results:** ✅ Placeholder test passed.  
- **Status:** Incomplete.  

---

## ✅ Overall Summary  
- **Pytest Results:** 15 total tests → 14 passed, 1 failed.  
- The **failure is expected** and demonstrates a discovered bug (R3 borrowing limit).  
- Requirements R4–R7 are unimplemented placeholders, but tests confirm this.  
- **Conclusion:** Test suite successfully validated requirements, uncovered 1 real bug, and confirmed unimplemented features remain incomplete. 

---