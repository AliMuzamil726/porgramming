#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <ctime>

using namespace std;

string DB_FILE = "chat_database.txt";

// Create file if missing
void createDatabase() {
    ifstream f(DB_FILE);
    if (!f.good()) {
        ofstream out(DB_FILE);
        out << "Chat Board Database\n";
    }
}

// Read all lines
vector<string> readAllMessages() {
    vector<string> lines;
    ifstream file(DB_FILE);
    string line;

    while (getline(file, line))
        lines.push_back(line);

    return lines;
}

// Write message
void addMessage(const string &username, const string &message) {
    ofstream file(DB_FILE, ios::app);

    time_t now = time(0);
    tm *lt = localtime(&now);

    char buffer[20];
    strftime(buffer, 20, "%Y-%m-%d %H:%M:%S", lt);

    file << "[" << buffer << "] " << username << ": " << message << "\n";
}

// Search
void searchUser(const string &username) {
    auto lines = readAllMessages();
    bool found = false;

    for (const auto &l : lines) {
        if (l.find(username) != string::npos) {
            cout << l << endl;
            found = true;
        }
    }

    if (!found)
        cout << "No messages found.\n";
}

// Count
void countMessages() {
    auto lines = readAllMessages();
    cout << "Total messages: " << lines.size() - 1 << endl;
}

// Clear
void clearChat() {
    ofstream file(DB_FILE);
    file << "Chat Board Database\n";
    cout << "Chat cleared.\n";
}

// Export (copy file)
void exportChat(const string &name) {
    ifstream src(DB_FILE, ios::binary);
    ofstream dst(name + ".txt", ios::binary);
    dst << src.rdbuf();
    cout << "Chat exported as " << name << ".txt\n";
}

// Menu
void menu() {
    cout << "\n--- CHAT BOARD ---\n";
    cout << "1. Add Message\n";
    cout << "2. View Messages\n";
    cout << "3. Search by Username\n";
    cout << "4. Count Messages\n";
    cout << "5. Clear Chat\n";
    cout << "6. Export Chat\n";
    cout << "0. Exit\n";
    cout << "Choose: ";
}

int main() {
    createDatabase();
    int choice;

    while (true) {
        menu();
        cin >> choice;
        cin.ignore();

        if (choice == 0) break;

        string user, msg, file;

        switch (choice) {
            case 1:
                cout << "Username: ";
                getline(cin, user);
                cout << "Message: ";
                getline(cin, msg);
                addMessage(user, msg);
                break;

            case 2: {
                auto lines = readAllMessages();
                for (auto &l : lines) cout << l << endl;
                break;
            }

            case 3:
                cout << "Enter username: ";
                getline(cin, user);
                searchUser(user);
                break;

            case 4:
                countMessages();
                break;

            case 5:
                clearChat();
                break;

            case 6:
                cout << "Export file name (without extension): ";
                getline(cin, file);
                exportChat(file);
                break;

            default:
                cout << "Invalid choice.\n";
        }
    }

    return 0;
}
