from typing import List
import csv

#Employee = List[str]
Employees = []


def increase_payment_for_employees_on_position(employees: Employees, position: str, rate: float):
    for i in range(len(Employees)):
        if Employees[i][7] == position:
            Employees[i][5] = round(int(Employees[i][5]) * rate)



def parse_file(file_name: str) -> Employees:
    Employees = []
    reader = csv.reader(file_name, delimiter=";")
    for row in reader:
        Employees.append(row)
    return Employees


def save_to_file(file_name: str, data: Employees):
    writer = csv.writer(file_name, delimiter=";", lineterminator = "")
    for i in range(len(Employees)):
        print(Employees[i])
        writer.writerow(Employees[i])
        if i+1 < len(Employees):
            file_name.write("\n")
    pass

DB_FILE = "employees.csv"
POSITION = "Web developer junior"
RATE = 1.15

file = open(DB_FILE, "r", newline="")
try:
    Employees = parse_file(file)
    increase_payment_for_employees_on_position(Employees, POSITION, RATE)
finally:
    file.close()


file = open("employees2.csv", "w", newline="")
try:
    save_to_file(file, Employees)
finally:
    file.close()
