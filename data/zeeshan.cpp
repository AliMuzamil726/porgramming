#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>

using namespace std;

string DB_FILE = "bank_database.csv";

struct Account {
    string accNo;
    string name;
    double balance;
};

// ---------------------- Utility: Load all accounts ----------------------
vector<Account> loadAccounts() {
    vector<Account> accounts;
    ifstream file(DB_FILE);

    if (!file.good()) {
        return accounts;
    }

    string line;
    getline(file, line); // skip header

    while (getline(file, line)) {
        stringstream ss(line);
        Account acc;
        string bal;

        getline(ss, acc.accNo, ',');
        getline(ss, acc.name, ',');
        getline(ss, bal, ',');

        acc.balance = stod(bal);
        accounts.push_back(acc);
    }
    return accounts;
}

// ---------------------- Utility: Save all accounts ----------------------
void saveAccounts(const vector<Account>& accounts) {
    ofstream file(DB_FILE);
    file << "AccountNumber,Name,Balance\n";

    for (auto &acc : accounts) {
        file << acc.accNo << "," << acc.name << "," << acc.balance << "\n";
    }
}

// ---------------------- Create DB if missing ----------------------
void createDatabase() {
    ifstream f(DB_FILE);
    if (!f.good()) {
        ofstream file(DB_FILE);
        file << "AccountNumber,Name,Balance\n";
    }
}

// ---------------------- Add New Account ----------------------
void addAccount() {
    vector<Account> accounts = loadAccounts();
    Account acc;

    cout << "Enter Account Number: ";
    cin >> acc.accNo;
    cin.ignore();

    cout << "Enter Name: ";
    getline(cin, acc.name);

    cout << "Enter Initial Balance: ";
    cin >> acc.balance;

    // Check if account exists
    for (auto &a : accounts) {
        if (a.accNo == acc.accNo) {
            cout << "Account already exists!\n";
            return;
        }
    }

    accounts.push_back(acc);
    saveAccounts(accounts);

    cout << "Account created successfully.\n";
}

// ---------------------- View All Accounts ----------------------
void viewAccounts() {
    vector<Account> accounts = loadAccounts();

    if (accounts.empty()) {
        cout << "No accounts found.\n";
        return;
    }

    cout << "\n--- All Bank Accounts ---\n";
    for (auto &acc : accounts) {
        cout << "Account No: " << acc.accNo
             << " | Name: " << acc.name
             << " | Balance: " << acc.balance << endl;
    }
}

// ---------------------- Search Account ----------------------
void searchAccount() {
    string accNo;
    cout << "Enter Account Number to search: ";
    cin >> accNo;

    vector<Account> accounts = loadAccounts();

    for (auto &acc : accounts) {
        if (acc.accNo == accNo) {
            cout << "\nAccount Found:\n";
            cout << "Name: " << acc.name << endl;
            cout << "Balance: " << acc.balance << endl;
            return;
        }
    }
    cout << "Account not found.\n";
}

// ---------------------- Deposit Money ----------------------
void deposit() {
    string accNo;
    double amount;

    cout << "Enter Account Number: ";
    cin >> accNo;
    cout << "Enter Amount to Deposit: ";
    cin >> amount;

    vector<Account> accounts = loadAccounts();

    for (auto &acc : accounts) {
        if (acc.accNo == accNo) {
            acc.balance += amount;
            saveAccounts(accounts);
            cout << "Deposited successfully.\n";
            return;
        }
    }
    cout << "Account not found.\n";
}

// ---------------------- Withdraw Money ----------------------
void withdraw() {
    string accNo;
    double amount;

    cout << "Enter Account Number: ";
    cin >> accNo;

    cout << "Enter Amount to Withdraw: ";
    cin >> amount;

    vector<Account> accounts = loadAccounts();

    for (auto &acc : accounts) {
        if (acc.accNo == accNo) {
            if (acc.balance < amount) {
                cout << "Insufficient balance.\n";
                return;
            }
            acc.balance -= amount;
            saveAccounts(accounts);
            cout << "Withdrawal successful.\n";
            return;
        }
    }
    cout << "Account not found.\n";
}

// ---------------------- Delete Account ----------------------
void deleteAccount() {
    string accNo;
    cout << "Enter Account Number to delete: ";
    cin >> accNo;

    vector<Account> accounts = loadAccounts();
    bool deleted = false;

    vector<Account> newList;
    for (auto &acc : accounts) {
        if (acc.accNo != accNo) newList.push_back(acc);
        else deleted = true;
    }

    saveAccounts(newList);

    if (deleted)
        cout << "Account deleted.\n";
    else
        cout << "Account not found.\n";
}

// ---------------------- Update Account Name ----------------------
void updateAccount() {
    string accNo;
    string newName;

    cout << "Enter Account Number: ";
    cin >> accNo;
    cin.ignore();

    cout << "Enter New Name: ";
    getline(cin, newName);

    vector<Account> accounts = loadAccounts();

    for (auto &acc : accounts) {
        if (acc.accNo == accNo) {
            acc.name = newName;
            saveAccounts(accounts);
            cout << "Account updated.\n";
            return;
        }
    }

    cout << "Account not found.\n";
}

// ---------------------- Menu ----------------------
void menu() {
    cout << "\n--- BANK MANAGEMENT SYSTEM ---\n";
    cout << "1. Add New Account\n";
    cout << "2. View All Accounts\n";
    cout << "3. Search Account\n";
    cout << "4. Deposit Money\n";
    cout << "5. Withdraw Money\n";
    cout << "6. Delete Account\n";
    cout << "7. Update Account\n";
    cout << "0. Exit\n";
    cout << "Enter choice: ";
}

// ---------------------- MAIN ----------------------
int main() {
    createDatabase();

    int choice;

    while (true) {
        menu();
        cin >> choice;

        switch (choice) {
            case 1: addAccount(); break;
            case 2: viewAccounts(); break;
            case 3: searchAccount(); break;
            case 4: deposit(); break;
            case 5: withdraw(); break;
            case 6: deleteAccount(); break;
            case 7: updateAccount(); break;
            case 0: cout << "Goodbye!\n"; return 0;
            default: cout << "Invalid choice.\n";
        }
    }
}
