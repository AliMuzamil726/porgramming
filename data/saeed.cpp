#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <sstream>

using namespace std;

string DB_FILE = "event_database.doc";

// -------------------------- STRUCT --------------------------
struct Event {
    int id;
    string name;
    string date;
    string location;
};

// ---------------------- LOAD ALL EVENTS ----------------------
vector<Event> loadEvents() {
    vector<Event> list;
    ifstream file(DB_FILE);

    if (!file.good())
        return list;

    string line;
    getline(file, line); // Skip heading

    while (getline(file, line)) {
        if (line.size() < 5) continue;

        Event ev;
        string temp;

        stringstream ss(line);

        getline(ss, temp, '|'); // ID part
        ev.id = stoi(temp.substr(temp.find(":") + 1));

        getline(ss, temp, '|'); // Name part
        ev.name = temp.substr(temp.find(":") + 1);

        getline(ss, temp, '|'); // Date part
        ev.date = temp.substr(temp.find(":") + 1);

        getline(ss, temp, '|'); // Location part
        ev.location = temp.substr(temp.find(":") + 1);

        list.push_back(ev);
    }
    return list;
}

// ---------------------- SAVE ALL EVENTS ----------------------
void saveEvents(const vector<Event>& list) {
    ofstream file(DB_FILE);
    file << "Event Management System\n";
    for (auto &ev : list) {
        file << "EventID:" << ev.id
             << " | Name:" << ev.name
             << " | Date:" << ev.date
             << " | Location:" << ev.location << "\n";
    }
}

// ---------------------- CREATE DB IF MISSING ----------------------
void createDatabase() {
    ifstream f(DB_FILE);
    if (!f.good()) {
        ofstream file(DB_FILE);
        file << "Event Management System\n";
    }
}

// ---------------------- ADD EVENT ----------------------
void addEvent() {
    vector<Event> list = loadEvents();
    Event ev;

    cout << "Enter Event ID: ";
    cin >> ev.id;
    cin.ignore();

    cout << "Enter Event Name: ";
    getline(cin, ev.name);

    cout << "Enter Event Date (YYYY-MM-DD): ";
    getline(cin, ev.date);

    cout << "Enter Event Location: ";
    getline(cin, ev.location);

    list.push_back(ev);
    saveEvents(list);

    cout << "Event added successfully.\n";
}

// ---------------------- VIEW EVENTS ----------------------
void viewEvents() {
    vector<Event> list = loadEvents();
    if (list.empty()) {
        cout << "No events found.\n";
        return;
    }

    cout << "\n--- All Events ---\n";
    for (auto &ev : list) {
        cout << "Event ID: " << ev.id
             << " | Name: " << ev.name
             << " | Date: " << ev.date
             << " | Location: " << ev.location << "\n";
    }
}

// ---------------------- SEARCH EVENT ----------------------
void searchEvent() {
    vector<Event> list = loadEvents();
    string name;

    cin.ignore();
    cout << "Enter event name to search: ";
    getline(cin, name);

    bool found = false;

    for (auto &ev : list) {
        if (ev.name.find(name) != string::npos) {
            cout << "Event Found: "
                 << "ID: " << ev.id
                 << " | Date: " << ev.date
                 << " | Location: " << ev.location << "\n";
            found = true;
        }
    }

    if (!found)
        cout << "No event found.\n";
}

// ---------------------- UPDATE EVENT ----------------------
void updateEvent() {
    vector<Event> list = loadEvents();
    int id;

    cout << "Enter event ID to update: ";
    cin >> id;
    cin.ignore();

    for (auto &ev : list) {
        if (ev.id == id) {
            cout << "Enter new name: ";
            getline(cin, ev.name);

            cout << "Enter new date: ";
            getline(cin, ev.date);

            cout << "Enter new location: ";
            getline(cin, ev.location);

            saveEvents(list);
            cout << "Event updated.\n";
            return;
        }
    }
    cout << "Event not found.\n";
}

// ---------------------- DELETE EVENT ----------------------
void deleteEvent() {
    vector<Event> list = loadEvents();
    int id;

    cout << "Enter event ID to delete: ";
    cin >> id;

    vector<Event> newList;
    bool deleted = false;

    for (auto &ev : list) {
        if (ev.id != id) {
            newList.push_back(ev);
        } else {
            deleted = true;
        }
    }

    saveEvents(newList);

    if (deleted) cout << "Event deleted.\n";
    else cout << "Event not found.\n";
}

// ---------------------- MENU ----------------------
void menu() {
    cout << "\n--- EVENT MANAGEMENT SYSTEM ---\n";
    cout << "1. Add Event\n";
    cout << "2. View All Events\n";
    cout << "3. Search Event\n";
    cout << "4. Update Event\n";
    cout << "5. Delete Event\n";
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
            case 1: addEvent(); break;
            case 2: viewEvents(); break;
            case 3: searchEvent(); break;
            case 4: updateEvent(); break;
            case 5: deleteEvent(); break;
            case 0: cout << "Goodbye!\n"; return 0;
            default: cout << "Invalid choice.\n";
        }
    }
}
