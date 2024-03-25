# GradStat

Welcome to GradStat! 

This is a project that allows you to look at statistics drawn from data scraped from the popular website: https://www.thegradcafe.com/. This is a website where graduate school applicants can post their admission results as well as things like their GPA, GRE scores, the date they received the decision and whether or not they are an international student. While this website is really useful, unfortunately, it doesn’t have a way to look at cumulative statistics like average GPA or the number of decisions released for a given month. For this reason, I wanted to use the information scraped from gradcafe to answer these types of questions. 

## Installation Instructions

To run this project you should have Python 3.11.5 or a later version. Additionally, you will also need to install the packages given in the requirements.txt file. To install them, go to the terminal and cd into the directory where this file is located. Then run the following command:


	pip install -r requirements.txt


You will also need to install docker which we will use to create our local MongoDB database. Once installed, you can then go to the terminal and run the following two commands:


	docker pull mongodb/mongodb-community-server:latest
	docker run —-name mongodb -p 27017:27017 -d mongodb/mongodb-community-server:latest



## Running The Program

Included in this submission is a csv file which contains all of the results scraped from gradcafe. To insert these results into the database, you can run the gradPopulate.py file which will take roughly 20 minutes to completely run. Once that finishes, you can then run the gradInterface.py file which provides you with an interface to ask questions regarding the data scraped. 



<img width="756" alt="GradStat_Options" src="https://github.com/fkhan000/GradStat/assets/78983433/a5b2de70-a6a3-4726-8571-5f96ddff38ec">
