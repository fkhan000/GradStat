import gradQuery
import os
from datetime import datetime



def grabInfo(single = False):
    if single:
        unis = input("Please enter the name of the university you're applying to: ")

    else:
        unis = []
        while(True):
            unis.append(input("Please enter a university that you would like to be included in the plot or press enter to move on: "))

            if unis[-1] == "":
                break
        unis = unis[:-1]
    
    subject = input("Please enter your field of study: ")

    while(True):
        masters = input("Please enter 1 to see results for the master's program and 0 for the PhD program: ")

        if masters not in ["0", "1"]:
            print("\nInvalid input! Please try again\n")
            continue
        break
    
    while(True):
        international = input("Please enter 1 to filter results for only international students, 0 for only domestic students, and -1 for all students: ")

        if international not in ["-1", "0", "1"]:
            print("\nInvalid input! Please try again\n")
            continue
        break

    return unis, subject, int(masters), int(international)

def validDate(date):
    date = date.split("/")
    if len(date) != 3:
        return False
    date[0] = date[0].replace("0", "")
    
    if not date[0].isdigit() or int(date[0]) > 12:
        return False

    date[1] = date[1].replace("0", "")

    if not date[1].isdigit() or int(date[1]) > 31:
        return False

    return date[2].isdigit()

    

def getDateRange():

    while(True):
        dFrom = input("Please enter the start date that we should search for results from (MM/DD/YYYY): ")
        if validDate(dFrom):
            date = dFrom.split("/")
            dFrom = datetime(int(date[2]), int(date[0].replace("0", "")), int(date[1].replace("0", "")))
            break
        print("\nInvalid input! The date given either doesn't match the above format or is an invalid date. Please try again!\n")

    while(True):
        dTo = input("Please enter the end date that we should search for results to (MM/DD/YYYY): ")
        if validDate(dTo):
            date = dTo.split("/")
            dTo = datetime(int(date[2]), int(date[0].replace("0", "")), int(date[1].replace("0", "")))
            break
        print("\nInvalid input! The date given either doesn't match the above format or is an invalid date. Please try again!\n")

    return dFrom, dTo

        
        

def accRateUI():
    os.system('cls' if os.name == 'nt' else 'clear')

    unis, subject, masters, international = grabInfo()

    dFrom, dTo = getDateRange()    
    
    gradQuery.acceptanceRate(unis, subject, masters, international, dFrom, dTo)

    input("Press Enter when you're ready to return to the main page")


def decisionDateUI():

    os.system('cls' if os.name == 'nt' else 'clear')

    university, subject, masters, international = grabInfo(single = True)

    while(True):
        accepted = input("Press 0 if you're looking for when rejection letters are sent out and 1 for acceptance letters: ")

        if accepted in ["0", "1"]:
            break
        print("\nInvalid input! Please try again\n")
    
    dFrom, dTo = getDateRange()
    gradQuery.decisionHistogram(university, subject, int(accepted), masters, international, dFrom, dTo)
    
    input("Press Enter when you're ready to return to the main page")


def numAppUI():
    os.system('cls' if os.name == 'nt' else 'clear')

    unis, subject, masters, international = grabInfo()

    dFrom, dTo = getDateRange()
    
    
    gradQuery.numApps(unis[:-1], subject, masters, international, dFrom, dTo)


def gradesUI():
    os.system('cls' if os.name == 'nt' else 'clear')
    
    unis, subject, masters, international = grabInfo()
    
    while(True):
        accepted = input("Press 0 if you're looking for rejected applicants or 1 for accepted applicants: ")

        if accepted in ["0", "1"]:
            break
        print("\nInvalid input! Please try again\n")

    while(True):
        metric = input("What metric are you interested in looking at (GPA, GRE, GREV, GREAW): ")

        if metric in ["GPA","GRE", "GREV", "GREAW"]:
            break
        print("\nInvalid input! Please try again\n")

    dFrom, dTo = getDateRange()

    gradQuery.gradeDist(unis, subject, int(accepted), metric, masters, international, dFrom, dTo)



    input("Press Enter when you're ready to return to the main page")
    
if __name__ == "__main__":

    while(True):
        os.system('cls' if os.name == 'nt' else 'clear')

        print("\n\n**********Welcome to GradStat!**********\n\n")
        print("This is a service that allows users to view statistics regarding")
        print("graduate school admissions.\n")


        print("What would you like to know??")
        print("\n\t1.What are the acceptance rates of the programs I'm applying to?")
        print("\n\t2.When will I hear back from a school?")
        print("\n\t3.How popular are the programs I'm applying to?")
        print("\n\t4.What are the average GPA/GRE scores of people accepted/rejected to the programs I'm applying to?")
        print("\n\t5.Exit")


        question = input("\nPlease enter a number from 1-5 corresponding to the question you would like answered: ")

        match question:
            case "1":
                accRateUI()
            case "2":
                decisionDateUI()
            case "3":
                numAppUI()
            case "4":
                gradesUI()
            case "5":
                print("\nGoodbye!")
                break
            case _:
                print("\nUh-oh It looks like you entered an invalid argument. Please try again")
            
