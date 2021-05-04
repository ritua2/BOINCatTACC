# CLI interface for a user to select where to submit a job!
import mysql.connector as mysql_con

boinc_db = mysql_con.connect(host = 'localhost', port = 3306, user = "root", password = "root", database = 'boinc_sch')
cursor1 = boinc_db.cursor()
cursor2 = boinc_db.cursor()

print("Welcome to the job submission interface!")
print("Provide the requested details below to assist you in a job submission!")
print("----------------------------------------------------------------")

try:
    # Taking User input
    pay = input("Are you willing to use your credit to run a job?[Y/N]\n")
    run_time = int(input("what is anticipated job runtime in minutes? \n"))
    turnaround_time = int(input("what is the expected turnaround time(in minutes) for your job?\n"))

    #If User want's to use their credit
    if (pay =='Y' or pay =='y'):
        node = int(input("How many nodes required to submit a job? \n"))
        cores = int(input("How many cores required per Node to run a job?\n"))

        #check for stamppede/shamu cores restrictions
        if node == 1:
                if(1<= cores <=40):
                    #select query for node1 stamp/shamu
                    n1 = "select SysName,AVGWait,PredTime from sysinfo where Node='1'"
                    cursor1.execute(n1)
                    for x,r,z in cursor1:
                        print(" ------------------------------------------------------ ")
                        print("Based on the input You can submit job on Stampede2 (KNL-Normal Queue) or Shamu System!")
                        print("Average job wait time on %s System, is %s minutes !"%(x,int(r)))
                elif (41 <= cores <= 68):
                    # select query for node1 Stampede2
                    n1 = "select SysName,AVGWait,PredTime from sysinfo where Node='1' and SysName='Stampede2'"
                    cursor1.execute(n1)
                    for x, r, z in cursor1:
                        print(" ------------------------------------------------------ ")
                        print("Based on the input You can submit job on Stampede2 System!")
                        print("Average job wait time on %s System, is %s minutes !" % (x, int(r)))
                else:
                    print(" ------------------------------------------------------ ")
                    print("Based on the given input we DO NOT have any System to run your job!")
        elif node == 2:

            if (1 <= cores <= 40):
                #select node 2 stamp/shamu

                n2 = "select SysName,AVGWait,PredTime from sysinfo where Node='2'"
                cursor1.execute(n2)
                for x, r, z in cursor1:
                    print(" ------------------------------------------------------ ")
                    print("Based on the input You can submit job on Stampede2 (KNL-Normal Queue) or Shamu System!")
                    print("Average job wait time on %s System, is %s minutes !" %(x, int(r)))
            elif (41 <= cores <= 68):
                # select query for node2 Stampede2
                n1 = "select SysName,AVGWait,PredTime from sysinfo where Node='1' and SysName='Stampede2'"
                cursor1.execute(n1)
                for x, r, z in cursor1:
                    print(" ------------------------------------------------------ ")
                    print("Based on the input You can submit job on Shamu System!")
                    print("Average job wait time on %s System, is %s minutes !" % (x, int(r)))
            else:
                print(" ------------------------------------------------------ ")
                print("Based on the given input we DO NOT have any System to run your job!")

        else:

            if (1 <= cores <= 40):
                #select Node3 stamp/shamu
                n3 = "select SysName,AVGWait,PredTime from sysinfo where Node='3'"
                cursor1.execute(n3)
                for x, r, z in cursor1:
                    print(" ------------------------------------------------------ ")
                    print("Based on the input You can submit job on Stampede2 (KNL-Normal Queue) or Shamu System!")
                    print("Average job wait time on %s System, is %s minutes !" %(x, int(r)))
            elif (41 <= cores <= 68):
                # select query for node3 Stampede2
                n1 = "select SysName,AVGWait,PredTime from sysinfo where Node='1' and SysName='Stampede2'"
                cursor1.execute(n1)
                for x, r, z in cursor1:
                    print(" ------------------------------------------------------ ")
                    print("Based on the input You can submit job on Shamu System!")
                    print("Average job wait time on %s System, is %s minutes !" % (x, int(r)))
            else:
                print(" ------------------------------------------------------ ")
                print("Based on the given input we DO NOT have any System to run your job!")

    #if user does not want to use their credit
    elif (pay =='N' or pay =='n'):

        #asking for how many nodes and cores per node required for job submission
        node = int(input("How many nodes required to submit a job? \n"))
        cores = int(input("How many cores required per Node to run a job?\n"))

        if (node < 4 and cores < 4):
            memory = int(input("What is the input data size for this job(in MB)? \n"))

            #Boinc - as of now allowing only job with dataset size under 2048 MB!
            if (memory > 2048):
                print("To run a job without charges requires less than 2048 MB!")
                print("Please, try again with smaller datasets or use credit for job submission! ")
            else:
                print(" ------------------------------------------------------ ")
                print("Based on the information provided, Your job qualifies to run on Boinc System!")
                print("The Average Job Turnaround time on Boinc System has been around 12 hours!")
        else:
            print(" ------------------------------------------------------ ")
            print("To run a job without charges requires less Node and cores - under 3!")
            print("Please, try again with given suggestion or use credit for your job submission!")
    else:
        print("Please, Enter valid information & Try Again!")
except ValueError:
    print(" ------------------------------------------------------ ")
    print("It seems you might have entered incorrect information")
    print("Please, try again with correct information - provide correct user input as requested!")










