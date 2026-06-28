import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
print("Libraries Loaded")


#login system 

def login():
    username = input("Enter Username")
    password = input("Enter Password")
    if username == "sagar" and password =="2824":
        print("\nLogin Successful")
    else:
        print("\nInvaild username or password")
        exit()

#ENCAPSULATION
class Employeemanager:
    def __init__(self,file_path):
        self.__file_path = file_path
        self.df = None


#DATA LOAD
    def load_data(self):
        try:
            self.df = pd.read_csv(self.__file_path)
            self.df.columns = self.df.columns.str.strip()
            print("\nData Loaded Successfully")
            print(self.df.head())
            print(self.df.shape)
            print(self.df.columns)
            print(self.df.columns.tolist())
        except FileNotFoundError:
            print("\nFile Not Found")


# #DATA CLEAN 
#(ABSTRACTION)

    def clean_data(self):
        print("\nMissing Values")
        print(self.df.isnull().sum())
        self.df = self.df.dropna()

        print("\nDuplicate Values")
        print(self.df.duplicated().sum())
        self.df = self.df.drop_duplicates()
        
        print("\nData Cleaned Successfully")

#DATE FORMATE FIX

    def fix_date(self):
        self.df['Date_of_Joining'] = pd.to_datetime(
            self.df['Date_of_Joining'],
            errors='coerce'
        )
        self.df['month'] = self.df['Date_of_Joining'].dt.month_name()
        print("\nDate Column Fixed")
        print(self.df[['Date_of_Joining','month']].head())



    def fix_datatypes(self):
         self.df['Performance_Rating'] = pd.to_numeric(
             self.df['Performance_Rating'],
             errors='coerce'
         )

         self.df['Annual_Salary_INR'] = pd.to_numeric(
             self.df['Annual_Salary_INR'],
             errors='coerce'
         )
         print("\nNumeric Columns Fixed")
    
#CRUD
#create

    def add_employee(self):
        Employee_ID = input("Enter employee ID: ")
        Full_Name = input("Enter Full Name: ")
        Department = input("Enter Department: ")
        Job_Title = input("Enter Job Title: ")
        Date_of_Joining = input("Enter Date of Joining: ")
        Years_of_Experience = float(input("Enter Years of Experience: "))
        Annual_Salary_INR = input("Enter Annual Salary INR: ")
        City = input("Enter City: ")
        Employment_Status = input("Enter Employment Status: ")
        Performance_Rating = float(input("Enter Performance Rating: "))                       
        
        new_employee = {
             "Employee_ID": Employee_ID,
             "Full_Name": Full_Name,
             "Department": Department,
             "Job_Title": Job_Title,
             "Date_of_Joining": Date_of_Joining,
             "Years_of_Experience": Years_of_Experience,
             "Annual_Salary_INR": Annual_Salary_INR,
             "City": City,
             "Employment_Status": Employment_Status,
             "Performance_Rating":Performance_Rating,
        }
        self.df.loc[len(self.df)] = new_employee
        print("Employee Added Successfully")


#read
    def view_employee(self):
        print(self.df)

#update
    
    def update_employee(self):
        employee_id = input("Enter Employee ID to Update: ")
        if employee_id in self.df["Employee_ID"].values:
            new_city = input("Enter New Department: ")
            self.df.loc[
                self.df["Employee_ID"] == employee_id,
                "Department"
            ] = new_city
            print("Record Updated")
        else:
            print("Employee Not Found")

#delete
    
    def delete_employee(self):
         employee_id = input("Enter Employee ID to Delete: ")
         self.df = self.df[
             self.df["Employee_ID"] != employee_id
         ]
         print("Record Deleted")

    def save_changes(self):#save
        print("Saving to:", self.__file_path)
        self.df.to_csv(self.__file_path, index=False)
        print("Changes Saved Successfully")


# Department-wise Employee Count  
    def department_wise_count(self):
        count = self.df['Department'].value_counts()
        print("\nDepartment wise count")
        print(count)

# Department-wise Average Performance
    def department_wise_average_performance(self):
        performance = self.df.groupby('Department')['Performance_Rating'].mean()
        print("\nDepart wise average performance")
        print(performance)

# Highest Paid Employees with years of experience
    def highest_paid_employees(self):
        print(self.df['Annual_Salary_INR'].apply(type).value_counts())
        self.df['Annual_Salary_INR'] = pd.to_numeric(
            self.df['Annual_Salary_INR'],
            errors='coerce'
        )

        top_paid_employee = (
           self.df[['Full_Name',
                 'Annual_Salary_INR',
                 'Years_of_Experience']]
            .sort_values('Annual_Salary_INR', ascending=False)
            .head(10)
        )
        print("\Highest Paid Employee")
        print(top_paid_employee)


# CITY VS DEPARTMENT VS STATUS
    def city_department_status(self):
        status = (
            self.df.groupby(
                ['City','Department','Employment_Status']
            )['Employment_Status']
            .size()
            .reset_index(name='Employee_Count')
            .sort_values('Employee_Count',ascending=False)
            .head(10)
        )
        print("\nCity Department Status")
        print(status)

    
#SALARY ANALYSIS
    
    def salary_analysis(self):
        avg_salary = self.df['Annual_Salary_INR'].mean()
        max_salary = self.df['Annual_Salary_INR'].max()
        min_salary = self.df['Annual_Salary_INR'].min()
        dept_avg = self.df.groupby('Department')['Annual_Salary_INR'].mean()

        
        print("Average Salary:", avg_salary)
        print("Maximum Salary:", max_salary)
        print("Minimum Salary:", min_salary)
        print("\nDepartment-wise Average Salary:")
        print(dept_avg)

    
#CITY WISE RATING 

    def city_wise_performance(self):
       city = (
            self.df.groupby(['City','Department'])['Performance_Rating']
            .mean()
            .reset_index()
            .sort_values('Performance_Rating', ascending=False)
            .head(5)
       )
       print("\nCity Wise Performance")
       print(city)
        
         
         


#PIVOT
    def pivot_table(self):
        pivot = pd.pivot_table(
            self.df,
            values='Performance_Rating',
            index='City',
            columns='Department',
            aggfunc='mean',
            fill_value=0
        )
        print("\nPivot Table")
        print(pivot)


        pivot = pd.pivot_table(
            self.df,
            values='Annual_Salary_INR',
            index='City',
            columns='Department',
            aggfunc='mean',
            fill_value=0
        )
        print("\nPivot Table")
        print(pivot)


#VISUALSE
#BAR CHART

    def bar_chart(self):
        self.df.groupby(['City', 'Department'])['Performance_Rating'].sum().sort_values(ascending=False).head(10).plot(kind='bar')
        plt.title("Department Wise Performance")
        plt.xlabel("City & Department")
        plt.ylabel("Performance_Rating")
        plt.show()

#LINE CHART

    def line_chart(self):
 #       self.df['performance_rating'] = pd.to_datetime(self.df['performance_rating'], errors='coerce')
 #       self.df['joining_date'] = self.df['joining_date'].dt.month_name()

 #       df_clean = self.df.dropna(subset=['joining_date', 'performance_rating'])

        performance = (
             self.df.groupby('month')['Performance_Rating']
             .mean()
        )
        performance.plot(
              kind='line',
              marker='o',
              figsize=(10, 5)
        )
        plt.title("Monthly performance Trend")
        plt.xlabel("Month")
        plt.ylabel("Performance_Rating")
        plt.grid(True)
        plt.show()

def menu():
    login()
    obj = Employeemanager(
        r"C:\Users\samee\Downloads\employee_1000.csv"
    )
    obj.load_data()
    obj.clean_data()
    obj.fix_date()
    obj.fix_datatypes()


    while True:
         print("\nEMPLOYEE ANALYSIS MENU")
         print("1. ADD EMPLOYEE")
         print("2. VIEW EMPLOYEE")
         print("3. UPDATE EMPLOYEE")
         print("4. DELETE WISE EMPLOYEE")
         print("5. SAVE CHANGES")
         print("6. DEPARTMENT WISE COUNT")
         print("7. DEPARTMENT WISE AVERAGE PERFORMANCE")
         print("8. HIGHEST PAID EMPLOYEE WITH YEARS OF EXPERINCE")
         print("9. CITY DEPARTMENT STATUS")
         print("10. CITY WISE PERFORMANCE")
         print("11. PIVOT") 
         print("12. BAR CHART")
         print("13. LINE CHART")
         print("14. EXIT")


         choice = input("\nEnter Choice : ")
        
         if choice == '1':
             obj.add_employee()
         elif choice == '2':
             obj.view_employee()
         elif choice == '3':
             obj.update_employee()
         elif choice == '4':
             obj.delete_employee()
         elif choice == '5':
             obj.save_changes()
         elif choice == '6':
             obj.department_wise_count()
         elif choice == '7':
             obj.department_wise_average_performance()
         elif choice == '8':
             obj.highest_paid_employees()
         elif choice == '9':
             obj.city_department_status()
         elif choice == '10':
             obj.city_wise_performance()
         elif choice == '11':
             obj.pivot_table()
         elif choice == '12':
             obj.bar_chart()
         elif choice == '13':
             obj.line_chart()
         elif choice == '14':
             print("\nThank You")
             break
         else:
              print("\nInvalid Choice")
menu()
