from datetime import datetime, timedelta
import uuid


class Admin:
    def __init__(self, username="admin", password="admin", name="Marwan"):
        self.username = username
        self.password = password
        self.name = name

        self.permissions = ["full access"]
        self.can_approve_waivers = True

    def authenticate_credentials(self, username, password):
        return self.username == username and self.password == password

    def handle_permissions(self):
        pass

    def has_permission(self, permission_name):
        pass

    def can_approve_waiver_requests(self):
        pass



class Customer:
    def __init__(self, name, username, phone):
        self.name = name
        self.username = username
        self.phone = phone

        self.id = str(uuid.uuid4())
        self.active_rentals = []  # List of active RentalTransaction IDs
        self.rental_history = []  # List of completed RentalTransaction IDs
        self.total_late_fees_owed = 0.0
        self.account_status = "good"

    def __str__(self):
        return f"customer name: {self.name}\nusername: {self.username}\nID: {self.id}\nactive rentals: {self.active_rentals}\naccount status: {self.account_status}"

    def __repr__(self):
        return self.__str__()

    def get_active_rentals(self):
        pass

    def get_rental_history(self):
        pass

    def calculate_total_fees_owed(self):
        pass

    def can_rent_more(self):
        pass

    def has_overdue_items(self):
        pass


class Movie:
    def __init__(self, name, number_of_copies, daily_fee, daily_overdue_fees, max_rental_days):
        self.name = name
        self.number_of_copies = number_of_copies
        self.daily_fee = daily_fee
        self.daily_overdue_fees = daily_overdue_fees
        self.max_rental_days = max_rental_days

        self.times_rented = 0
        self.movie_id = str(uuid.uuid4())

        self.copies_id = [str(uuid.uuid4()) for _ in range(self.number_of_copies)]
        self.copies_status = ["available" for _ in range(self.number_of_copies)]
        self.movie_copies = dict(zip(self.copies_id, self.copies_status))


    def __str__(self):
        return (f"{self.name}', copies count: {self.number_of_copies}, daily fee: ${self.daily_fee}, daily overdue fee: {self.daily_overdue_fees}\n"
                f"max rental days: {self.max_rental_days}, times rented: {self.times_rented}, "
                f"movie id: {self.movie_id}, \ncopies: {self.movie_copies}")

    def __repr__(self):
        return self.__str__()

    def get_movie_copies(self):
        """Returns a list of available copies"""
        if self.movie_copies:
            return self.movie_copies

    def copy_rented(self, copy_id):
        """Mark copy as rented"""
        if copy_id in self.movie_copies:
            self.movie_copies[copy_id] = "rented"
            return True
        return False

    def copy_returned(self, copy_id):
        """Mark copy as available"""
        if copy_id in self.movie_copies:
            self.movie_copies[copy_id] = "available"
            return True
        return False

    def available_for_rent(self):
        available_copies = 0
        for copy_id, status in self.movie_copies.items():
            if status == "available":
                available_copies += 1
        return available_copies

    def get_current_rental(self):
        pass



class RentalTransaction:
    def __init__(self, customer_id, movie_id, copy_id, due_date, status):
        self.customer_id = customer_id
        self.movie_id = movie_id
        self.copy_id = copy_id
        self.status = status
        self.due_date = due_date

        self.movie_name = None
        self.customer_name = None

        self.rental_id = str(uuid.uuid4())
        self.rental_date = datetime.now()

        self.days_to_rent = 0
        self.daily_fee = 0.0
        self.rental_fee = self.days_to_rent * self.daily_fee

        self.return_date = None

        self.late_fee_amount = 0.0
        self.late_fee_status = "none"

        self.rented_by_employee = None
        self.returned_to_employee = None


    def calculate_late_fees(self):
        if self.return_date > self.due_date:
            self.late_fee_amount += 1

    def is_overdue(self):
        if self.status != "active":
            return
        current_Date = datetime.now()
        return current_Date.date() > self.due_date.date()

    def days_late(self):
        if not self.is_overdue():
            return 0
        current_date = datetime.now()
        return (current_date.date() - self.due_date.date()).days

    def can_request_waiver(self):
        pass



class WaiverRequest:
    def __init__(self, rental_transaction_id, customer_id, customer_name, late_fee_amount, reason, requesting_employee_username):
        self.rental_transaction_id = rental_transaction_id
        self.customer_id = customer_id
        self.customer_name = customer_name
        self.reason = reason
        self.late_fee_amount = late_fee_amount
        self.requesting_employee_username = requesting_employee_username

        self.request_id = str(uuid.uuid4())
        self.request_date = datetime.now()

        self.requesting_employee_name = ""
        self.status = "pending"
        self.admin_username = None
        self.admin_decision_date = None
        self.admin_notes = ""

    def approve(self, admin_username, notes=""):
        pass

    def deny(self, admin_username, notes=""):
        pass

    def is_pending(self):
        pass

    def days_pending(self):
        pass



class LateFee:
    def __init__(self, rental_transaction_id, customer_id, days_late, daily_rate):
        self.rental_transaction_id = rental_transaction_id
        self.customer_id = customer_id
        self.days_late = days_late

        self.fee_id = str(uuid.uuid4())
        self.calculated_date = datetime.now()
        self.total_amount = days_late * daily_rate

        self.daily_late_fee_rate = 2.0
        self.payment_date = None
        self.waived_date = None
        self.waiver_request_id = None
        self.waived_by_admin = None

    def calculate_fee(self, days_late, daily_rate):
        pass

    def mark_paid(self):
        pass

    def mark_waived(self, admin_username):
        pass

    def can_be_waived(self):
        pass

    def is_outstanding(self):
        pass
