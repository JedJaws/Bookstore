# 449_FinalProject
## Table of Contents
1. [Demonstration](https://github.com/JedJaws/449_FinalProject#demonstration)
2. [Documentation](https://github.com/JedJaws/449_FinalProject#objective)
3. [Members](https://github.com/JedJaws/449_FinalProject#members)


## Submission Checklist:
 - [ ] GitHub repository containing the source code for the project
 - [ ] Documentation on how to run and use the API with names of all the team
members. (README.txt)
 - [ ] A brief video on the project, including the design choices and implementation
details.


## Demonstration:

Demo Video:
https://www.youtube.com/watch?v=z1UZkkVxW4Q&t=9s
 
## How to run:
### Step 1: Setting up the working environment
* Utilize **git clone** for this repository and all **necessary packages and modules** should be provided within the virtual environment, **venv**.
* **Create a virtual environment** for the application.
### Step 2: Running Mongo
* **Connect to MongoDB** by opening one terminal running the command **mongod**
* Then utilize the terminal within the directory containing this repo with the venv activated.
* Use the command **uvicorn bookstore:app --reload** to run the localhost
* The link **http://127.0.0.1:8000** should appear as result of the command.
* Follow the link and you should be taken to a webpage, add **/docs#/** to the end of the link.
### Step 3: Aggregation and Endpoints
* The command **uvicorn bookstore:app --reload** should also print out the aggregation data within the terminal.
* The API endpoints can be seen and utilized within the localhost as mentioned in Step 2.
* From that web page, each endpoint can be accessed by clicking on its tab, then to be used, simply click **try out**
* If the endpoint requires parameters, input the parameters and click **Execute**. If there are not parameters, simply click **Execute**.
* The desired output will be printed below in **responses**

## Members:
* William Ye
* Christian Verry
