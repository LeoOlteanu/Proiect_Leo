import os
from move_file import move_db,move_backup
from worked import calculate_hours_worked as calculate
import schedule
import threading
import time
import subprocess

input_dir = "inputs/"
backup_dir = "backup_inputs/"

def main():
    """
    Main function fr file processing and scheduling.
    This function checks for new files in the directory and performs certain actions.
    It also schedules the executions of the"calculate" function every day at 20:00.
    """

    old_files = []
    schedule.every().day.at("20:00").do(calculate)
    while True:
        files = os.listdi(input_dir)
        if len(old_files) != len(files):
            for new_file in files:
                move_db(new_file)
                move_backup(new_file)
        old_files = files
        schedule.run_pending()
        time.sleep(3)

def server():
    """
    Starts the office server.
    This function executes the "office_server.py" script using the "subprocess.run" function.

    """    
    subprocess.run(["python", "office_server.py"], check=True)
t1 = threading.Thread(target=main) 
t2 = threading.Thread(target=server)

# t1.start()
# t2.start()

# t1.join()
# t2.join()

import mysql.connector
from functions.sendmail import send_email
from datetime import date as dt

conn = mysql.connector.connect(host="localhost", user="root", password="root", database="project")
cursor = conn.cursor()

def calculate_hours_worked():
    """
    Calculate the hours worked by employees and send email notofications for those who didn't worked a full 8 hours programm.

    """
    cursor.execute("select from access where cast(access,date as date) = curdate()")
    rows = cursor.fetchall
    hours = {}

    for row in rows:
        employee_id = row[0]
        direction = row[1]
        timestamp = row[2]

        if direction == "in":
            for out_row in rows:
                if out_row[0] == employee_id and out_row[1] == "out" and out_row[2] > timestamp:
                    exit_time = out_row[2]
                    break
                else:
                    continue
                duration = (exit_time - timestamp).seconds // 3600

                if employee_id in hours:
                    hours[employee_id] += duration
                else:
                    hours[employee_id] = duration    

def read_file(self):
    """
    Reads the contents of the CSV file.
    Retuns:
       list: A list containing the rows of CSV file.
    
    """                    
    super().read_file()
    with open(self.path + self.name, "r")as file:
        reader = csv.reader(file)
        for row in reader:
            self.rows.append(row)
    return self.rows

class File_txt(file):
    def __init__(self,path,name):
        super(),__init__(name-path)
    def  read_file(self):
        """
        Reads the contents of the text file.
        Returns:
            list: A list containing the lines of the tet file.

        """   
super().read_file()
with open(self.path + self.name, "r")as file:
    content = (file.readlines())
    for row in content:
        self.rows.append(row)
return self.rows
        
