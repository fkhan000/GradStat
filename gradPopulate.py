import pymongo
from datetime import datetime
from tqdm import tqdm

#####GRADSTAT DATABASE######

##Fields
#University: university applicant applied to (string)
#Subject: The subject of the program (string)
#Decision: Whether they were admitted (1) or rejected (0) (int)
#Cycle: If the application is for the Fall (1) or Spring Cycle (0) (int)
#Cycle_Year: The year that the applicant was applying for (int)
#International/Domestic: If they're an international (1) or domestic applicant (0) (int)
#Masters/PhD: If they're applying for a Masters (1) or PhD (0) program (int)
#GPA: Their GPA (float)
#GRE: Their GRE score (float)
#GREV: Their GREV score (float)
#GREAW: Their GREAW score (float)

############################

client = pymongo.MongoClient("mongodb://localhost:27017/")

client.drop_database("gradstat")

db = client["gradstat"]

collection = db["universities"]

with open("gradInfo.csv", "r") as f:

    fields = ["University", "Subject", "Decision", "Decision_Date", "Cycle", "Cycle_Year", "International/Domestic", "Masters/PhD", "GPA", "GRE", "GREV", "GREAW"]
    f.readline()
    for line in tqdm(f):
        line = line.strip()
        values = line.split(",")

        if sum([1 if val != "" else 0 for val in values]) <= 3:
            continue

        for i in [2, 6, 7, 8, 9]:
            if values[i] and values[i].isdigit():
                values[i] = int(values[i])
            else:
                values[i] = None

        
        try:
            values[3] = datetime(int(values[5]), int(values[3]), int(values[4]))
        except:
            continue
        values = values[:4] + values[6:]
        values[-4:] = [float(val) if val != "" else None for val in values[-4:]]

        
        entry = dict(zip(fields, values))

        collection.insert_one(entry)
