from models import Customer, Movie, Admin, RentalTransaction
from datetime import datetime, timedelta


class AdminManager:
    def __init__(self):
        self.admins = {}  # Database
        default_admin = Admin()
        self.admins[default_admin.username] = default_admin

    def authenticate_admin(self, username, password):
        if username in self.admins:
            return self.admins[username].authenticate_credentials(username, password), self.admins[username].name
        return False


class CustomerManager:
    def __init__(self):
        predef_customer = Customer("Marwan Elfiky", "Marwan Elfiky", "01010290195")
        self.customers = {
            predef_customer.username: predef_customer
        }

    def save_customer_to_system(self, name, username, phone):
        new_customer = Customer(name, username, phone)
        self.customers[new_customer.username] = new_customer
        return True, len(self.customers)

    def retrieve_customers_from_database(self):
        if not self.validate_database():
            return
        return self.customers

    def update_customer(self, old_username, new_name, new_username):
        if old_username not in self.customers:
            return False, "Not Found"
        customer = self.customers[old_username]
        customer.name = new_name

        if new_username and new_username != old_username:
            customer.username = new_username
            self.customers[new_username] = customer
            del self.customers[old_username]

        return True, "Updated Successfully"

    def delete_customer(self, username):
        if username not in self.customers:
            return False, "Not Found"
        del self.customers[username]
        return True, "success !"

    def validate_database(self):
        if not self.customers:
            return False
        return True

    def customer_exist(self, customer_id):
        if not self.validate_database():
            return
        for customer_username, customer in self.customers.items():
            if customer.id == customer_id:
                return True
        return False

    def get_customer_id(self, customer_name):
        for customer_username, customer in self.customers:
            if customer.name == customer_name:
                return self.customers[customer_username].id

    def get_customer_by_name(self, customer_name):
        """Get customer by name with proper validation"""
        if not customer_name:
            return None, "Customer name cannot be empty"

        if not self.validate_database():
            return None, "Customer database is empty"

        for customer_username, customer in self.customers.items():
            if customer.name == customer_name:
                return customer, None  # Return (customer, error)

        return None, "Customer Not Found"


class MovieManager:
    def __init__(self):
        self.movies = {}

    def save_to_database(self, name, number_of_copies, daily_fee, daily_overdue_fees, max_rental_days):
        new_movie = Movie(name, number_of_copies, daily_fee, daily_overdue_fees, max_rental_days)
        self.movies[new_movie.name] = new_movie
        return True, len(self.movies)

    def retrieve_movies_from_database(self):
        if not self.validate_database():
            return
        return self.movies

    def validate_database(self):
        if not self.movies:
            return False
        return True

    def get_movie_id(self, movie_name):
        return self.movies[movie_name].id

    def get_movie_by_name(self, movie_name):
        """Get movie by name with proper validation"""
        if not movie_name:
            return None, "Movie name cannot be empty"

        if not self.validate_database():
            return None, "Movie database is empty"

        if movie_name not in self.movies:
            return None, f"Movie '{movie_name}' not found"

        return self.movies[movie_name], None  # Return (movie, error)

    def get_available_copy(self, movie_name):
        available_copies = self.movies[movie_name].get_movie_copies()
        return available_copies


class RentalManager:
    def __init__(self, customer_manager, movie_manager):
        self.customer_manager = customer_manager
        self.movie_manager = movie_manager

        self.active_transactions = {}
        self.completed_transactions = {}
        self.customer_active_rentals = {}
        self.movie_rentals = {}
        self.overdue_transactions = set()
        self.employee_transactions = {}
        self.copy_rentals = {}  # Key: copy_id, Value: transaction_id

    def rent_movie(self, movie_name, customer_name, days_to_rent):
        """movie_name, customer_name"""
        first_available_copy_id, error = self.get_available_copy(movie_name)

        if error:
            return None, error

        customer, error = self.customer_manager.get_customer_by_name(customer_name)

        if error:
            return None, error

        movie, error = self.movie_manager.get_movie_by_name(movie_name)

        if error:
            return None, error

        if movie.available_for_rent() == 0:
            return None, "All copies are rented or unavailable"

        if days_to_rent > movie.max_rental_days:
            return None, f"Can't rent more than {movie.max_rental_days} days"

        # 1- Mark Copy as rented
        copy_rented = movie.copy_rented(first_available_copy_id)

        if not copy_rented:
            return None, "Failed to mark copy as rented"

        # 2- increase movie times rented by 1
        movie.times_rented += 1

        # Create Rental Transaction
        due_date = datetime.now() + timedelta(days=days_to_rent)

        transaction = RentalTransaction(
            customer_id=customer.id,
            movie_id=movie.movie_id,
            copy_id=first_available_copy_id,
            due_date=due_date,
            status="active"
        )
        transaction.movie_name = movie.name
        transaction.customer_name = customer.name
        transaction.days_to_rent = days_to_rent

        self.active_transactions[transaction.rental_id] = transaction
        customer.active_rentals.append(transaction.rental_id)

        # Customer tracking
        if customer.id not in self.customer_active_rentals:
            self.customer_active_rentals[customer.id] = []
        self.customer_active_rentals[customer.id].append(transaction.rental_id)

        # Movie tracking
        if movie.movie_id not in self.movie_rentals:
            self.movie_rentals[movie.movie_id] = []
        self.movie_rentals[movie.movie_id].append(transaction.rental_id)

        # Copy tracking
        self.copy_rentals[first_available_copy_id] = transaction.rental_id

        return True, None

    def return_movie(self):
        pass

    def get_available_copy(self, movie_name):
        """Get first available copy ID with validation"""
        movie, error = self.movie_manager.get_movie_by_name(movie_name)
        if error:
            return None, error

        available_copies = movie.get_movie_copies()
        if not available_copies:
            return None, f"No copies of '{movie_name}' are available"

        first_available_copy = None
        for copy_id, status in available_copies.items():
            if status == "available":
                first_available_copy = copy_id
                break

        return first_available_copy, None

    def get_customer_active_rental_by_id(self, customer_id):
        """Get all active rentals for a customer"""
        if customer_id not in self.customer_active_rentals:
            return []  # Customer has no active rentals

        rental_transactions = []
        rental_ids = self.customer_active_rentals[customer_id]  # This is a LIST

        for rental_id in rental_ids:  # Loop through the list
            if rental_id in self.active_transactions:
                transaction = self.active_transactions[rental_id]
                rental_info = {
                    'movie_name': transaction.movie_name,
                    'rental_date': transaction.rental_date.strftime("%Y-%m-%d"),
                    'due_date': transaction.due_date.strftime("%Y-%m-%d"),
                    'status': transaction.status,
                    'rental_id': rental_id
                }
                rental_transactions.append(rental_info)
        return rental_transactions


    def check_overdue_rentals(self):
        """Check all active transactions and update overdue tracking"""
        self.overdue_transactions.clear()
        for rental_id, transaction in self.active_transactions.items():
            if transaction.is_overdue():
                self.overdue_transactions.add(rental_id)
        return len(self.overdue_transactions)

    def get_overdue_transactions(self):
        """Get all overdue transactions"""
        self.check_overdue_rentals()
        overdue_list = []
        for rental_id in self.overdue_transactions:
            if rental_id in self.active_transactions:
                overdue_list.append(self.active_transactions[rental_id])
        return overdue_list

    def get_customer_overdue_rentals(self, customer_id):
        customer_rentals = self.get_customer_active_rental_by_id(customer_id)
        overdue_rentals = []

        for rental in customer_rentals:
            rental_id = rental['rental_id']
            if rental_id in self.active_transactions:
                transaction = self.active_transactions[rental_id]
                if transaction.is_overdue():
                    if transaction.is_overdue():
                        rental['days_late'] = transaction.days_late()
                        rental['is_overdue'] = True
                        overdue_rentals.append(rental)
        return overdue_rentals