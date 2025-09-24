import csv

# ----------------- Customer Class -----------------
class Customer:
    def __init__(self, id, first_name, last_name, password, checking, savings, active, overdraft_count):
        self.id = id
        self.first_name = first_name.strip()
        self.last_name = last_name.strip()
        self.password = password.strip()
        self.checking = False if str(checking).lower() == "false" else float(checking)
        self.savings = False if str(savings).lower() == "false" else float(savings)
        self.active = str(active).strip().lower() == "true"
        self.overdraft_count = int(overdraft_count)

       
        self.checking_overdrafts = 0
        self.savings_overdrafts = 0

    def display(self, acct_type=None):
        print(f"\n--- Account Information for {self.first_name} {self.last_name} ---")
        if acct_type == "checking" and self.checking is not False:
            print(f"Checking Balance: ${self.checking:.2f}")
        elif acct_type == "savings" and self.savings is not False:
            print(f"Savings Balance: ${self.savings:.2f}")
        else:
            if self.checking is not False:
                print(f"Checking Balance: ${self.checking:.2f}")
            if self.savings is not False:
                print(f"Savings Balance: ${self.savings:.2f}")
        print(f"Active: {self.active}")
        print(f"Overdraft Count: {self.overdraft_count}")
        if not self.active:
            print("Both accounts are locked due to excessive overdrafts.")


# ----------------- Transfer Class -----------------
class Transfer:
    overdraft_fee = 35
    max_withdrawal = -100
    max_overdrafts = 2

    def __init__(self, customer, bank):
        self.customer = customer
        self.bank = bank

 
    def withdraw(self, acct_type, amount):
        if amount <= 0:
            print("Withdrawal amount must be positive.")
            return False

        balance = getattr(self.customer, acct_type)
        if balance is False:
            print(f"No {acct_type} account found.")
            return False

        if balance - amount < self.max_withdrawal:
            print(f"Cannot withdraw. Balance cannot go below ${self.max_withdrawal}.")
            return False

        balance -= amount

       
        logout_flag = False
        if balance < 0:
            if acct_type == "checking":
                self.customer.checking_overdrafts += 1
            else:
                self.customer.savings_overdrafts += 1

            balance -= self.overdraft_fee
            total_overdrafts = self.customer.checking_overdrafts + self.customer.savings_overdrafts
            print(f"Overdraft! ${self.overdraft_fee} fee applied. Total overdrafts: {total_overdrafts}")

            if total_overdrafts >= self.max_overdrafts:
                self.customer.active = False
                print("Account deactivated due to excessive overdrafts!")
                logout_flag = True

        setattr(self.customer, acct_type, balance)
        self.bank.save_customers()
        print(f"Withdrawal successful. New {acct_type} balance: ${balance:.2f}")

        if logout_flag:
            print("Logging out due to inactive account...")
            return "logout"

        return True

 
    def deposit(self, acct_type, amount):
        if amount <= 0:
            print("Deposit amount must be positive.")
            return False

        balance = getattr(self.customer, acct_type)
        if balance is False:
            print(f"No {acct_type} account found.")
            return False

        balance += amount
        setattr(self.customer, acct_type, balance)
        print(f"Deposit successful. New {acct_type} balance: ${balance:.2f}")

        self.try_reactivate()
        self.bank.save_customers()
        return True

   
    def transfer_between_accounts(self, from_acct, to_acct, amount):
        if from_acct == to_acct:
            print("Cannot transfer to the same account.")
            return False
        result = self.withdraw(from_acct, amount)
        if result == "logout":
            return "logout"
        self.deposit(to_acct, amount)
        print(f"Transferred ${amount:.2f} from {from_acct} to {to_acct}.")
        return True

   
    def transfer_to_other(self, to_customer, from_acct, to_acct, amount):
        result = self.withdraw(from_acct, amount)
        if result == "logout":
            return "logout"
        balance = getattr(to_customer, to_acct)
        if balance is False:
            print(f"{to_customer.first_name} does not have a {to_acct} account.")
            self.deposit(from_acct, amount)  
            return False
        setattr(to_customer, to_acct, balance + amount)
        print(f"Transferred ${amount:.2f} from your {from_acct} to {to_customer.first_name}'s {to_acct}.")
        self.bank.save_customers()
        return True

    
    def try_reactivate(self):
        checking_ok = self.customer.checking is False or self.customer.checking >= 0
        savings_ok = self.customer.savings is False or self.customer.savings >= 0

        if checking_ok and savings_ok and not self.customer.active:
            self.customer.active = True
            self.customer.checking_overdrafts = 0
            self.customer.savings_overdrafts = 0
            self.customer.overdraft_count = 0
            print("Account(s) successfully reactivated!")


# ----------------- Bank Class -----------------
class Bank:
    def __init__(self, file_name):
        self.file_name = file_name
        self.customers = []
        self.load_customers()

    def load_customers(self):
        self.customers = []
        with open(self.file_name, 'r', newline='') as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader)
            for row in csvreader:
                if not row:
                    continue
                customer = Customer(*row)
                self.customers.append(customer)

    def save_customers(self):
        with open(self.file_name, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["id","first_name","last_name","password","checking","savings","active","overdraft_count"])
            for c in self.customers:
                writer.writerow([c.id, c.first_name, c.last_name, c.password, c.checking, c.savings, c.active, c.overdraft_count])

    
    def create_account(self, customer=None):
        if customer is None:
            new_id = str(max([int(c.id) for c in self.customers], default=10000) + 1)
            first = input("Enter first name: ")
            last = input("Enter last name: ")
            password = input("Set a password: ")

            print("Choose account type:\n1. Checking\n2. Savings\n3. Both")
            choice = input("Enter choice (1/2/3): ")

            checking = False
            savings = False
            if choice == "1": checking = 0.0
            elif choice == "2": savings = 0.0
            elif choice == "3": checking = 0.0; savings = 0.0
            else: print("Invalid choice"); return

            customer = Customer(new_id, first, last, password, checking, savings, True, 0)
            self.customers.append(customer)
            self.save_customers()
            print(f"Account created! Your ID is {new_id}")
        else:
            if customer.checking is False:
                if input("Add Checking account? (y/n): ").lower() == "y":
                    customer.checking = 0.0
                    print("Checking account added.")
            if customer.savings is False:
                if input("Add Savings account? (y/n): ").lower() == "y":
                    customer.savings = 0.0
                    print("Savings account added.")
        self.save_customers()

  
    def login(self, user_id, password):
        for customer in self.customers:
            if customer.id.strip() == user_id.strip() and customer.password.strip() == password.strip():
                if not customer.active:
                    print("Account is inactive due to excessive overdrafts.")
                    react = input("Do you want to reactivate by depositing money? (y/n): ").lower()
                    if react == "y":
                        self.reactivate_account(customer)
                    else:
                        return None

                if customer.checking is not False and customer.savings is not False:
                    choice = input("Login to (1) Checking or (2) Savings? ")
                    acct_type = "checking" if choice == "1" else "savings" if choice == "2" else None
                    if acct_type is None:
                        print("Invalid choice.")
                        return None
                    return customer, acct_type
                elif customer.checking is not False:
                    return customer, "checking"
                elif customer.savings is not False:
                    return customer, "savings"

        print("Invalid ID or password.")
        return None

    def reactivate_account(self, customer):
        print("\n--- Reactivate Account ---")
        deposits = {}
        for acct in ["checking", "savings"]:
            balance = getattr(customer, acct)
            if balance is not False and balance < 0:
                need = -balance
                while True:
                    try:
                        dep = float(input(f"Enter deposit for {acct} (need at least ${need:.2f}): "))
                        if dep >= need:
                            deposits[acct] = dep
                            break
                        else:
                            print(f"You need to deposit at least ${need:.2f}.")
                    except:
                        print("Invalid input.")
        transfer = Transfer(customer, self)
        for acct, dep in deposits.items():
            transfer.deposit(acct, dep)

    def withdraw(self, customer, acct_type, amount):
        transfer = Transfer(customer, self)
        return transfer.withdraw(acct_type, amount)


    def deposit(self, customer, acct_type, amount):
        transfer = Transfer(customer, self)
        return transfer.deposit(acct_type, amount)

   
    def transfer_between_accounts(self, customer, from_acct, to_acct, amount):
        transfer = Transfer(customer, self)
        return transfer.transfer_between_accounts(from_acct, to_acct, amount)

    
    def transfer_to_other(self, from_customer, to_customer_id, from_acct, to_acct, amount):
        to_customer = next((c for c in self.customers if c.id == to_customer_id), None)
        if not to_customer:
            print("Recipient not found.")
            return False
        transfer = Transfer(from_customer, self)
        return transfer.transfer_to_other(to_customer, from_acct, to_acct, amount)


    def menu(self):
        print("🏦 Welcome to the Bank!")
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
                result = self.login(user_id, password)
                if result:
                    customer, acct_type = result
                    self.customer_menu(customer, acct_type)
            elif choice == "3":
                print("Goodbye!")
                self.save_customers()
                break
            else:
                print("Invalid choice, try again.")

 
    def customer_menu(self, customer, acct_type):
        while True:
            print(f"\n--- {customer.first_name}'s Menu --- ({acct_type.capitalize()} Account)")
            print("1. View Account Info")
            print("2. Withdraw Money")
            print("3. Deposit Money")
            print("4. Transfer Between Own Accounts")
            print("5. Transfer To Another Customer")
            if customer.checking is False or customer.savings is False:
                print("6. Add Another Account")
            print("7. Logout")

            choice = input("Enter choice: ")

            if choice == "1":
                customer.display(acct_type)
            elif choice == "2":
                try: amount = float(input("Enter amount to withdraw: "))
                except: print("Invalid amount"); continue
                result = self.withdraw(customer, acct_type, amount)
                if result == "logout":
                    break
            elif choice == "3":
                try: amount = float(input("Enter amount to deposit: "))
                except: print("Invalid amount"); continue
                self.deposit(customer, acct_type, amount)
            elif choice == "4":
                if customer.checking is False or customer.savings is False:
                    print("You must have both accounts for this operation.")
                    continue
                from_acct = "checking" if acct_type == "checking" else "savings"
                to_acct = "savings" if from_acct == "checking" else "checking"
                try: amount = float(input(f"Enter amount to transfer from {from_acct} to {to_acct}: "))
                except: print("Invalid amount"); continue
                result = self.transfer_between_accounts(customer, from_acct, to_acct, amount)
                if result == "logout":
                    break
            elif choice == "5":
                to_id = input("Enter recipient ID: ")
                to_acct = input("Enter recipient account (checking/savings): ").lower()
                try: amount = float(input("Enter amount to transfer: "))
                except: print("Invalid amount"); continue
                result = self.transfer_to_other(customer, to_id, acct_type, to_acct, amount)
                if result == "logout":
                    break
            elif choice == "6" and (customer.checking is False or customer.savings is False):
                self.create_account(customer)
            elif choice == "7":
                print("Logging out...")
                break
            else:
                print("Invalid choice.")


# ----------------- Main -----------------
if __name__ == "__main__":
    bank = Bank("bank.csv")
    bank.menu()