import os
import sqlite3
import json
from datetime import datetime


class InvoiceDatabase:
    def __init__(self, db_path="../output/invoices.db"):
        self.db_path = db_path
        # Ensure the directory of the database file exists
        db_dir = os.path.dirname(os.path.abspath(self.db_path))
        if not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)
        # Create the tables if they don't exist
        self._create_tables()

    def _get_connection(self):
        """Create and return a new SQLite DB connection."""
        return sqlite3.connect(self.db_path)

    def _create_tables(self):
        """Create the invoice table if it does not exist."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS invoices (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    invoice_number TEXT UNIQUE,
                    vendor TEXT,
                    amount REAL,
                    tax REAL,
                    date TEXT,
                    status TEXT,
                    confidence TEXT,
                    created_at TEXT,
                    updated_at TEXT
                )
            """)
            conn.commit()

    def insert_invoice(self, invoice_data):
        """Insert a new invoice record. Return inserted row ID or None on failure."""
        try:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            confidence_json = json.dumps(invoice_data.get('confidence', {}))
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO invoices (
                        invoice_number, vendor, amount, tax, date, status,
                        confidence, created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    invoice_data.get('invoice_number'),
                    invoice_data.get('vendor'),
                    invoice_data.get('amount'),
                    invoice_data.get('tax'),
                    invoice_data.get('date'),
                    invoice_data.get('status'),
                    confidence_json,
                    now,
                    now
                ))
                conn.commit()
                return cursor.lastrowid
        except sqlite3.IntegrityError:
            # Handle duplicate invoice number or other constraint violation
            return None
        except Exception as e:
            print(f"Error inserting invoice: {e}")
            return None

    def get_all_invoices(self):
        """Retrieve all invoices ordered by creation timestamp descending."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, invoice_number, vendor, amount, tax, date, status, confidence, created_at, updated_at
                FROM invoices ORDER BY created_at DESC
            """)
            rows = cursor.fetchall()
            return rows

    def get_statistics(self):
        """Return summary statistics about the invoices in the database."""
        with self._get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM invoices")
            total_invoices = cursor.fetchone()[0] or 0

            cursor.execute("SELECT SUM(amount) FROM invoices")
            total_amount = cursor.fetchone()[0] or 0.0

            # Calculate average confidence across all invoices
            cursor.execute("SELECT confidence FROM invoices")
            confidences = cursor.fetchall()
            confidences_list = []
            for (conf_json,) in confidences:
                try:
                    conf_dict = json.loads(conf_json)
                    confidences_list.extend(conf_dict.values())
                except Exception:
                    continue

            avg_confidence = round(sum(confidences_list) / len(confidences_list), 2) if confidences_list else 0.0

            # Count invoices by status
            cursor.execute("SELECT status, COUNT(*) FROM invoices GROUP BY status")
            status_counts = dict(cursor.fetchall())

            return {
                'total_invoices': total_invoices,
                'total_amount': total_amount,
                'avg_confidence': avg_confidence,
                'by_status': status_counts
            }
