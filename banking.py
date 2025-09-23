import csv

class Customer:
    def __init__(self, id, first_name, last_name, password, checking, savings, active, overdraft_count):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.checking = False if str(checking).lower() == "false" else float(checking)
        self.savings = False if str(savings).lower() == "false" else float(savings)
        self.active = str(active).strip().lower() == "true"
        self.overdraft_count = int(overdraft_count)



    def display(self):
        print(f"\n--- Account Information for {self.first_name} {self.last_name} ---")

        if self.checking is not False:
            print(f"Checking Balance: ${self.checking:.2f}")
    
        if self.savings is not False:
            print(f"Savings Balance : ${self.savings:.2f}")
            
        print(f"Active: {self.active}")
        print(f"Overdraft Count: {self.overdraft_count}")


class Bank:
    def __init__(self, file_name):
        self.file_name = file_name
        self.customers = []
        self.load_customers()

    def load_customers(self):
        self.customers = []
        with open(self.file_name, 'r', newline='') as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader)  # skip header
            for row in csvreader:
                if not row:
                    continue
                customer = Customer(*row)
                self.customers.append(customer)

    def save_customers(self):
        with open(self.file_name, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["id", "first_name", "last_name", "password", "checking", "savings", "active", "overdraft_count"])
            for c in self.customers:
                writer.writerow([
                    c.id, c.first_name, c.last_name, c.password,
                    c.checking, c.savings,
                    c.active, c.overdraft_count
                ])

    def create_account(self):
        new_id = str(int(self.customers[-1].id) + 1) if self.customers else "10001"
        first = input("Enter first name: ")
        last = input("Enter last name: ")
        password = input("Set a password: ")
       
        print("\nChoose account type:")
        print("1. Checking Account")
        print("2. Savings Account")
        print("3. Both")

        


        choice = input("Enter choice (1/2/3): ")
        checking = False
        savings = False

        if choice == "1":
            checking =0.0
        elif choice == "2":
            savings = 0.0
            checking = False
        elif choice == "3":
            checking = 0.0
            savings = 0.0
        else:
            print("Invalid choice, account creation canceled.")
            return

        customer = Customer(new_id, first, last, password, checking, savings, True, 0)
        self.customers.append(customer)
        self.save_customers()
        print(f"✅ Account created! Your ID is {new_id}")

    def login(self, user_id, password):
        for customer in self.customers:
            if customer.id == user_id and customer.password == password:
                if not customer.active:
                    print("⚠ Account is inactive.")
                    return None
                print(f"\nWelcome, {customer.first_name}!")
                return customer
        print("Invalid ID or password.")
        return None

    def menu(self):
        print(" Welcome to the Bank! ") 
        while True:
            print("\n--- Bank Menu ---")
            print("1. Create Account")
            print("2. Login")
            print("3. Exit")

            choice = input("Enter choice: ")
            if choice == "1":
                self.create_account()
            elif choice == "2":
                user_id = input("Enter ID: ")
                password = input("Enter Password: ")
                customer = self.login(user_id, password)
                if customer:
                    self.customer_menu(customer)
            elif choice == "3":
                print("Goodbye!")
                self.save_customers()
                break
            else:
                print("Invalid choice, try again.")

    def customer_menu(self, customer):
        while True:
            print(f"\n--- {customer.first_name}'s Menu ---")
            print("1. View Account Info")
            print("2. Logout")

            choice = input("Enter choice: ")
            if choice == "1":
                customer.display()
            elif choice == "2":
                print("Logging out...")
                break
            else:
                print("Invalid choice")
# class Transfer:
#     def withdraw():



if __name__ == "__main__":
    bank = Bank("bank.csv")
    bank.menu()
