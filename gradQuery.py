import pymongo
import matplotlib.pyplot as plt
from datetime import datetime

#this module performs queries of interest on the database
#Currently it can get the average grades of rejected/accepted applicants,
#create a plot showing when decisions for a program usually come out,
#the acceptance rate of a program*
#and the popularity of a program based on the number of applications

#*you should take the acceptance rate with a grain of salt since there's probably
#a selection bias on the type of people who would post results on gradcafe. It might be good to
#use the acceptance rate as a relative metric so you could see how much more competitive one program is than
#another

client = pymongo.MongoClient("mongodb://localhost:27017/")

db = client["gradstat"]

collection = db["universities"]


#creates multiple box and whisker plots based on a given metric for all of the applicants for each university
#metric is a string that tells us what applicant statistic you want to look at. It can be 4 different values:
#GPA, GRE, GREV, and GREAW
def gradeDist(unis, subject, accepted, metric, masters, international, dFrom, dTo):

    
    grades = []

    if international == -1:
            inter_regex = {"$exists":True}
    else:
        inter_regex = international
    for uni in unis:
        uni_regex = {"$regex": uni}
        subject_regex = {"$regex": subject}
        metric_regex = {"$regex": "^.+$"}
        dRange = {"$gte": dFrom,
              "$lte": dTo}
        
    
        results = collection.find({"University":  uni_regex,
                                   "Subject" : subject_regex,
                                   "Masters/PhD": masters,
                                   "Decision": accepted,
                                   "International/Domestic": inter_regex,
                                  "Decision_Date": dRange},
                                  {metric:1})
    

        grades.append([])
        match metric:
            case "GPA":
                test = 0
            case "GRE":
                test = 1
            case "GREV":
                test = 2
            case "GREAW":
                test = 3

        for result in results:
            if result[metric]:
                #this removes some outliers that might have been accidentally put when submitting their scores
                #to gradcaf like sometimes users would submit GRE scores that were like 500 when it only goes up to 170
                #If we come across those kinds of outliers we skip them and move on to the next result
                if test == 0 and result[metric] > 4:
                    continue
                if test == 1 and (result[metric] > 170 or result[metric] < 130):
                    continue
                if test == 2 and (result[metric] > 170 or result[metric] < 130):
                    continue
                if test == 3 and (result[metric] > 6 or result[metric] < 0):
                    continue
                grades[-1].append(result[metric])


    if grades == [[] for i in range(len(unis))]:
        print("\nUh-oh we were unable to find any results for your query!")


    fig = plt.figure(figsize =(10, 7))
    ax = fig.add_subplot(111)
    
    bp = ax.boxplot(grades, patch_artist = True,
                notch ='True', vert = 0)

    ax.set_yticklabels(unis)

    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()

    decision = "Rejected"
    if accepted:
        decision = "Accepted"

    match international:
        case -1:
            title = metric + " of Applicants Who Were " + decision
        case 0:
            title = metric + " of Domestic Applicants Who Were " + decision
        case 1:
            title = metric + " of International Applicants Who Were " + decision
        
    plt.title(title)
    plt.xlabel(metric)
    plt.ylabel("Universities")

    plt.show()


#This creates a histogram that shows the number of decisions released by a university for every month
#according to gradcafe
def decisionHistogram(university, subject, accepted, masters, international, dFrom, dTo):
    uni_regex = {"$regex": university}
    subject_regex = {"$regex": subject}
    
    dRange = {"$gte": dFrom,
              "$lte": dTo}

    if international == -1:
        inter_regex = {"$exists":True}
    else:
        inter_regex = international
            
    results = collection.find({"University": uni_regex,
                               "Subject": subject_regex,
                               "Masters/PhD": masters,
                               "Decision": accepted,
                               "International/Domestic": inter_regex,
                               "Decision_Date": dRange},
                              {"Decision_Date" : 1})


    dates = [result["Decision_Date"].month + result["Decision_Date"].day/31 for result in results]

    if dates == []:
        print("\nUh-oh we were unable to find any results for your query!")
    plt.xlabel("Decision Date")
    plt.ylabel("Number of Decisions Given")

    result = "Admission"
    if accepted == "0":
        result = "Rejection"

    plt.title(result + " Dates for " + university + "'s " + subject + " Program")
    
    plt.hist(dates)
    plt.show()

#This gives the acceptance rate for multiple universities
def acceptanceRate(unis, subject, masters,international, dFrom, dTo):

    accRates = []
    universities = []

    if international == -1:
        inter_regex = {"$exists":True}
    else:
        inter_regex = international
    for uni in unis:
        uni_regex = {"$regex": uni}
        subject_regex = {"$regex": subject}
        
        dRange = {"$gte": dFrom,
                  "$lte": dTo}
        
        
        results = collection.find({"University": uni_regex,
                                   "Subject": subject_regex,
                                   "Masters/PhD": masters,
                                   "International/Domestic": inter_regex,
                                   "Decision_Date": dRange},
                                  {"Decision" : 1})

        count = 0
        accRate = 0
        b = 0
        
        for result in results:
            b += 1
            if result["Decision"] != "":
                accRate += int(result["Decision"])
                count += 1

        if count:
            universities.append(uni)
            accRates.append(accRate/count)

    if accRates == []:
        print("\nUh-oh we were unable to find any results for your query!")
    
    plt.xlabel("Universities")


    plt.ylabel("Acceptance Rate")

    
    plt.bar(universities, accRates)

    plt.show()

            
#Finally, this function gives us an idea of the popularity of multiple programs by finding
#the number of users who posted a decision on gradcafe. 
def numApps(unis, subject, masters, international, dFrom, dTo):

    numApplied = []

    if international == -1:
        inter_regex = {"$exists":True}
    else:
        inter_regex = international
        
    for uni in unis:
        uni_regex = {"$regex": uni}
        subject_regex = {"$regex": subject}
        dRange = {"$gte": dFrom,
              "$lte": dTo}

    
        numApplied.append(collection.count_documents({"University": uni_regex,
                                                      "Subject": subject_regex,
                                                      "Masters/PhD": masters,
                                                      "International/Domestic": inter_regex,
                                                      "Decision_Date": dRange}))
    if numApplied == [0 for i in range(len(unis))]:
        print("\nUh-oh we were unable to find any results for your query!")
    plt.bar(unis, numApplied)
    plt.show()
