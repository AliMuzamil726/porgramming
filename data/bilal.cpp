#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <sstream>
using namespace std;

string DB_FILE = "admissions.doc";

struct Student {
    int id;
    string name;
    int age;
    string email;
    string course;
};

// ------------------- LOAD STUDENTS -------------------
vector<Student> loadStudents() {
    vector<Student> list;
    ifstream file(DB_FILE);

    if (!file.good())
        return list;

    string line;
    getline(file, line); // skip header

    while (getline(file, line)) {
        if (line.size() < 5) continue;
        Student s;
        string temp;
        stringstream ss(line);

        getline(ss, temp, '|');
        s.id = stoi(temp.substr(temp.find(":") + 1));

        getline(ss, temp, '|');
        s.name = temp.substr(temp.find(":") + 1);

        getline(ss, temp, '|');
        s.age = stoi(temp.substr(temp.find(":") + 1));

        getline(ss, temp, '|');
        s.email = temp.substr(temp.find(":") + 1);

        getline(ss, temp, '|');
        s.course = temp.substr(temp.find(":") + 1);

        list.push_back(s);
    }

    return list;
}

// ------------------- SAVE STUDENTS -------------------
void saveStudents(const vector<Student>& list) {
    ofstream file(DB_FILE);
    file << "Admission System\n";
    for (auto &s : list) {
        file << "ID:" << s.id
             << " | Name:" << s.name
             << " | Age:" << s.age
             << " | Email:" << s.email
             << " | Course:" << s.course << "\n";
    }
}

// ------------------- CREATE DATABASE -------------------
void createDatabase() {
    ifstream f(DB_FILE);
    if (!f.good()) {
        ofstream file(DB_FILE);
        file << "Admission System\n";
    }
}

// ------------------- ADD APPLICATION -------------------
void addApplication() {
    vector<Student> list = loadStudents();
    Student s;
    cout << "Enter Application ID: ";
    cin >> s.id;
    cin.ignore();

    cout << "Enter Name: ";
    getline(cin, s.name);

    cout << "Enter Age: ";
    cin >> s.age;
    cin.ignore();

    cout << "Enter Email: ";
    getline(cin, s.email);

    cout << "Enter Course: ";
    getline(cin, s.course);

    list.push_back(s);
    saveStudents(list);

    cout << "Application submitted successfully.\n";
}

// ------------------- VIEW ALL APPLICATIONS -------------------
void viewApplications() {
    vector<Student> list = loadStudents();
    if (list.empty()) {
        cout << "No applications found.\n";
        return;
    }

    cout << "\n--- All Applications ---\n";
    for (auto &s : list) {
        cout << "ID:" << s.id
             << " | Name:" << s.name
             << " | Age:" << s.age
             << " | Email:" << s.email
             << " | Course:" << s.course << "\n";
    }
}

// ------------------- SEARCH APPLICATION -------------------
void searchApplication() {
    vector<Student> list = loadStudents();
    int searchId;
    cout << "Enter ID to search: ";
    cin >> searchId;

    for (auto &s : list) {
        if (s.id == searchId) {
            cout << "\nApplication Found:\n";
            cout << "ID:" << s.id
                 << " | Name:" << s.name
                 << " | Age:" << s.age
                 << " | Email:" << s.email
                 << " | Course:" << s.course << "\n";
            return;
        }
    }

    cout << "Application not found.\n";
}

// ------------------- UPDATE APPLICATION -------------------
void updateApplication() {
    vector<Student> list = loadStudents();
    int updateId;
    cout << "Enter ID to update: ";
    cin >> updateId;
    cin.ignore();

    for (auto &s : list) {
        if (s.id == updateId) {
            cout << "Enter new Name: ";
            getline(cin, s.name);

            cout << "Enter new Age: ";
            cin >> s.age;
            cin.ignore();

            cout << "Enter new Email: ";
            getline(cin, s.email);

            cout << "Enter new Course: ";
            getline(cin, s.course);

            saveStudents(list);
            cout << "Application updated.\n";
            return;
        }
    }

    cout << "Application not found.\n";
}

// ------------------- DELETE APPLICATION -------------------
void deleteApplication() {
    vector<Student> list = loadStudents();
    int deleteId;
    cout << "Enter ID to delete: ";
    cin >> deleteId;

    vector<Student> newList;
    bool deleted = false;

    for (auto &s : list) {
        if (s.id != deleteId)
            newList.push_back(s);
        else
            deleted = true;
    }

    saveStudents(newList);
    if (deleted)
        cout << "Application deleted.\n";
    else
        cout << "Application not found.\n";
}

// ------------------- MENU -------------------
void menu() {
    cout << "\n--- ONLINE ADMISSION SYSTEM ---\n";
    cout << "1. Apply for Admission\n";
    cout << "2. View All Applications\n";
    cout << "3. Search Application\n";
    cout << "4. Update Application\n";
    cout << "5. Delete Application\n";
    cout << "0. Exit\n";
    cout << "Enter choice: ";
}

// ------------------- MAIN -------------------
int main() {
    createDatabase();

    int choice;
    while (true) {
        menu();
        cin >> choice;
        cin.ignore();

        switch(choice) {
            case 1: addApplication(); break;
            case 2: viewApplications(); break;
            case 3: searchApplication(); break;
            case 4: updateApplication(); break;
            case 5: deleteApplication(); break;
            case 0: cout << "Exiting system.\n"; return 0;
            default: cout << "Invalid choice.\n";
        }
    }
}
