import requests
from bs4 import BeautifulSoup
import time

page = 1

monthMap = dict(zip(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug",
                   "Sep", "Oct", "Nov", "Dec"], list(range(1, 13))))

numDecisions = 0
prevDecisions = 0

with open("gradInfo.csv","a") as f:
    #we add in the columns for our csv file
    #f.write("University,Subject,Decision,Month,Day,Year,Cycle,Cycle_year,international,Masters/PhD,GPA,GRE,GREV,GREAW\n")
    f.write("\n")
    while(True):
        
        if numDecisions - prevDecisions > 100:
            print("Results Scraped: " + str(numDecisions))
            prevDecisions = numDecisions
        
        passed = False

        #after around 100k results, I started getting an error saying I was sending too many requests so if the scraper gets those
        #it pauses and waits 5 minutes
        while(not passed):
            try:
                response = requests.get("https://www.thegradcafe.com/survey/index.php?page=" + str(page))
                passed = True
            except:
                print("Timed Out, Page: " + str(page) + " " + str(numDecisions) + " results scraped")
                time.sleep(300)

        
        soup = BeautifulSoup(response.text, "html.parser")

        
        decisions = soup.find_all("div", {"class": "col"})

        if not decisions:
            #if the page was empty then that means we have gotten all of the results and we can end the script
            break
        for decision in decisions:
            
            try:
                
                
                subject, university = decision.h6.text.split(",")[:2]
                university = university.strip()
                subject = subject.strip()
                date = decision.p.text[9:].split(" ")

                
                if len(date[2]) != 4 or not date[2].isdigit():
                    raise ValueError("Unable to find year decision was given, skipping!")
                year = date[2]


                spans = decision.div.find_all("span")
                
                decision_date = spans[0].text.replace("\t", "").replace("\n", "").split(" ")

                
                #the decision_date is usually given in the format _ on month, day with _ being Accepted or Rejected
                #there were a couple of posts where it just said Waitlisted or Interview. I decided to ignore those because
                #they didn't happen too often and I was mostly interested in just looking at applicants who were ultimately
                #accepted or rejected
                
                if len(decision_date) != 4 or decision_date[3] not in monthMap:
                    
                    raise ValueError('Location of admission decision not where expected to be, skipping!')
                
                
                admission = str(int(decision_date[0] == "Rejected"))

                day = decision_date[2]
                month = str(monthMap[decision_date[3]])

                    
                try:
                    #So around the 12000th page, I saw that my scraper was becoming really slow and it was getting maybe
                    #1 or 2 results per minute. I'm not sure why but posts before 2020 didn't have the cycle (like Fall or Spring)
                    #and the cycle_year in the posts. 
                    if len(spans[1].text.split(" ")) != 2:
                        raise ValueError("Location of cycle of admission not where expected to be!")
                    

                    cycle, cycle_year = spans[1].text.split(" ")
                
                    if cycle not in ["Fall", "Spring"] or (not cycle_year.isdigit()) or len(cycle_year) != 4:
                        raise ValueError("Unable to find application cycle!")

                #So if it couldn't find them, the script would try to figure out the admission cycle and year based on the month
                #and year that the applicant was rejected/admitted. This is kind of faulty for people who got decisions in December
                #because that could either be early decision for the Fall cycle or a decision for the Spring cycle but I'm not sure
                #if there's a good way around it.
                    
                except:
                    if int(month) < 8:
                        cycle = "1"
                        cycle_year = str(year)
                    else:
                        cycle = "0"
                        cycle_year = str(int(year) + 1)
                
                cycle = str(int(cycle == "Fall"))

                GPA = ""
                GREV = ""
                GREAW = ""
                GRE = ""
                international = ""
                masters = ""


                #for the rest of the fields, they can sometimes end up in different locations in the post
                for i in range(2, len(spans)):

                    #so for those we try to match each span to one of the fields we're looking for
                    listing = spans[i].text.split(" ")

                    if len(listing) == 1:
                        match listing[0]:
                            case "Masters":
                                masters = "1"
                            case "PhD":
                                masters = "0"
                            case "International":
                                international = "1"
                            case "American":
                                international = "0"
                            case _:
                                continue
                    
                    
                    key = " ".join(listing[:-1])

                    match key:
                        case "GPA":
                            GPA = listing[-1]
                        case "GRE":
                            GRE = listing[-1]
                        case "GRE V":
                            GREV = listing[-1]
                        case "GRE AW":
                            GREAW = listing[-1]
                

                f.write(",".join([university, subject, admission, month, day,
                                 year, cycle, cycle_year,international,masters, GPA, GRE, GREV, GREAW]) +"\n")
                numDecisions += 1
            except Exception as e:
                continue
        page += 1
