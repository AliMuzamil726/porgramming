#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <sstream>
using namespace std;

string DB_FILE = "bank_database.doc";

// ---------------------- STRUCT ----------------------
struct Account {
    int accNo;
    string name;
    double balance;
};

// ---------------------- LOAD ACCOUNTS ----------------------
vector<Account> loadAccounts() {
    vector<Account> list;
    ifstream file(DB_FILE);

    if (!file.good())
        return list;

    string line;
    getline(file, line); // Skip header

    while (getline(file, line)) {
        if (line.size() < 5) continue;

        Account acc;
        string temp;

        stringstream ss(line);

        getline(ss, temp, '|');
        acc.accNo = stoi(temp.substr(temp.find(":") + 1));

        getline(ss, temp, '|');
        acc.name = temp.substr(temp.find(":") + 1);

        getline(ss, temp, '|');
        acc.balance = stod(temp.substr(temp.find(":") + 1));

        list.push_back(acc);
    }
    return list;
}

// ---------------------- SAVE ACCOUNTS ----------------------
void saveAccounts(const vector<Account>& list) {
    ofstream file(DB_FILE);
    file << "Bank Management System\n";

    for (auto &acc : list) {
        file << "Account:" << acc.accNo
             << " | Name:" << acc.name
             << " | Balance:" << acc.balance << "\n";
    }
}

// ---------------------- CREATE DATABASE ----------------------
void createDatabase() {
    ifstream f(DB_FILE);
    if (!f.good()) {
        ofstream file(DB_FILE);
        file << "Bank Management System\n";
    }
}

// ---------------------- ADD ACCOUNT ----------------------
void addAccount() {
    vector<Account> list = loadAccounts();
    Account acc;

    cout << "Enter Account Number: ";
    cin >> acc.accNo;
    cin.ignore();

    cout << "Enter Name: ";
    getline(cin, acc.name);

    cout << "Enter Initial Balance: ";
    cin >> acc.balance;

    list.push_back(acc);
    saveAccounts(list);

    cout << "Account created successfully.\n";
}

// ---------------------- VIEW ACCOUNTS ----------------------
void viewAccounts() {
    vector<Account> list = loadAccounts();
    if (list.empty()) {
        cout << "No accounts found.\n";
        return;
    }

    cout << "\n--- All Accounts ---\n";
    for (auto &acc : list) {
        cout << "Account No: " << acc.accNo
             << " | Name: " << acc.name
             << " | Balance: " << acc.balance << "\n";
    }
}

// ---------------------- SEARCH ACCOUNT ----------------------
void searchAccount() {
    vector<Account> list = loadAccounts();
    int accNo;

    cout << "Enter account number to search: ";
    cin >> accNo;

    for (auto &acc : list) {
        if (acc.accNo == accNo) {
            cout << "\nAccount Found:\n";
            cout << "Name: " << acc.name << endl;
            cout << "Balance: " << acc.balance << endl;
            return;
        }
    }
    cout << "Account not found.\n";
}

// ---------------------- DEPOSIT ----------------------
void deposit() {
    vector<Account> list = loadAccounts();
    int accNo;
    double amount;

    cout << "Enter account number: ";
    cin >> accNo;

    cout << "Enter amount to deposit: ";
    cin >> amount;

    for (auto &acc : list) {
        if (acc.accNo == accNo) {
            acc.balance += amount;
            saveAccounts(list);
            cout << "Amount deposited.\n";
            return;
        }
    }
    cout << "Account not found.\n";
}

// ---------------------- WITHDRAW ----------------------
void withdrawMoney() {
    vector<Account> list = loadAccounts();
    int accNo;
    double amount;

    cout << "Enter account number: ";
    cin >> accNo;

    cout << "Enter amount to withdraw: ";
    cin >> amount;

    for (auto &acc : list) {
        if (acc.accNo == accNo) {
            if (acc.balance < amount) {
                cout << "Insufficient balance.\n";
                return;
            }
            acc.balance -= amount;
            saveAccounts(list);
            cout << "Withdrawal successful.\n";
            return;
        }
    }
    cout << "Account not found.\n";
}

// ---------------------- DELETE ACCOUNT ----------------------
void deleteAccount() {
    vector<Account> list = loadAccounts();
    int accNo;

    cout << "Enter account number to delete: ";
    cin >> accNo;

    vector<Account> newList;
    bool deleted = false;

    for (auto &acc : list) {
        if (acc.accNo != accNo)
            newList.push_back(acc);
        else 
            deleted = true;
    }

    saveAccounts(newList);

    if (deleted)
        cout << "Account deleted.\n";
    else
        cout << "Account not found.\n";
}

// ---------------------- UPDATE ACCOUNT ----------------------
void updateAccount() {
    vector<Account> list = loadAccounts();
    int accNo;

    cout << "Enter account number to update: ";
    cin >> accNo;
    cin.ignore();

    for (auto &acc : list) {
        if (acc.accNo == accNo) {
            cout << "Enter new name: ";
            getline(cin, acc.name);

            cout << "Enter new balance: ";
            cin >> acc.balance;

            saveAccounts(list);
            cout << "Account updated.\n";
            return;
        }
    }
    cout << "Account not found.\n";
}

// ---------------------- MENU ----------------------
void menu() {
    cout << "\n--- BANK MANAGEMENT SYSTEM ---\n";
    cout << "1. Add Account\n";
    cout << "2. View All Accounts\n";
    cout << "3. Search Account\n";
    cout << "4. Deposit\n";
    cout << "5. Withdraw\n";
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
            case 5: withdrawMoney(); break;
            case 6: deleteAccount(); break;
            case 7: updateAccount(); break;
            case 0: cout << "Goodbye!\n"; return 0;
            default: cout << "Invalid choice.\n";
        }
    }
}
