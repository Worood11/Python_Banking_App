# 🏦 Python Banking System (Terminal)

## 📖 Project Description
This is a simple banking system built in **Python** that runs in the terminal.  
It allows users to:  

- 🆕 Create accounts  
- 🔑 Log in with ID & password  
- 💰 Deposit, withdraw, and transfer money  
- ⚠️ Handle overdrafts and inactive accounts  
- 💾 Save and load data from a CSV file  

The project demonstrates **object-oriented programming (OOP)**, **file handling**, and **CLI-based interaction**.

---

## 🛠️ Technologies Used
- 🐍 Python 3  
- 📄 CSV Module for data storage  
- 🏗️ Object-Oriented Programming (OOP) principles  
- 💻 Command Line Interface (CLI)  

---

## 📊 App Functionality

| Feature            | Description                                  |
|-------------------|----------------------------------------------|
| 🆕 Create Account     | Add new customer with unique ID             |
| 🔑 Login              | Authenticate using ID & password            |
| 💵 Deposit            | Add funds to checking/savings               |
| 💸 Withdraw           | Withdraw funds (with overdraft rules)       |
| 🔄 Transfer           | Transfer between checking/savings           |
| ⚠️ Overdraft Handling | Apply $35 fee and deactivate account after limit |
| 💾 Save/Load Data     | Store customer info in `bank.csv`           |

---

## 🚧 Challenges & Key Takeaways
- ⚠️ Handling overdraft rules (deactivating accounts after multiple overdrafts)  
- 🆔 Ensuring unique customer IDs when creating new accounts  

**💡 Key Learnings:**  
- 🏗️ Applied OOP concepts (classes for Customer, Bank, Transfer)  
- 🖥️ Practiced writing a menu-driven terminal application  

---

## 🧩 IceBox Features (Future Improvements)
- 🎨 Improve UI with the `curses` library for better terminal graphics  
- ✅ Add unit tests to ensure correctness  
 

---

## 💻 Usage
1. Run the app with:
```bash
python3 banking.py


