# CS 520: Kashikoi-EleNA
Group name - Kashikoi
<br>
Group members - Divya Sharma, Astha Baranwal, Rohan Acharya, Kavya Harlalka
<br>
<br>
Pair programming Ids
<br>
kavyaharlalka - Astha Baranwal, Kavya Harlalka
<br>
Ast97 - Astha Baranwal, Kavya Harlalka
<br>
divya1974 - Divya Sharma, Rohan Acharya
<br>
r-acharya - Divya Sharma, Rohan Acharya

# Documentation
We have added the complete documentation in the `docs` folder in the repository.
* `docs` folder itself contains our Design Document, SRS document, User manual and Evaluation document.
* `api_docs` consists of documentation created for users who want to use our api directly for their own application (this is a feature presented by us, our api is independent and can be used without our UI). 
* `internal_docs` consists of the complete controller and model documentation generated automatically using sphinx.
* `presentation` consists of the presentation video and presentation slides.

# Problem Statement

Navigation Systems typically provide the shortest path between any two given points. These are not optimal for a lot of scenarios where the user is interested in finding a path which has the least elevation gain. Moreover, some users might be interested in finding a path which has elevation gain so that they can partake in an intense and time-constrained workout. To extend navigation systems to solve the above problems, we have designed a software system that takes two points as input and finds the optimal route between them that maximizes or minimizes elevation gain while limiting the total path distance to n% of the shortest path between these two points.

# Steps to Run the Application

1. Clone the repository using git clone https://github.com/kavyaharlalka/kashikoi-elena-navigation.git
2. Run 'pip install -r requirements.txt'
3. Go to kashikoi-elena-navigation/src/view/templates/index.html and replace <API_KEY_HERE> with your Google Map API Key
4. Go to kashikoi-elena-navigation/src/config.ini and enter your gmap_api_key
5. Run bash run.sh to start the server
6. After the server is running, go to the local host http://127.0.0.1:5000/

# Testing and Evaluation

We have performed comprehensive testing for our application to ensure that all the functions and modules are tested and all corner cases are covered. Unit tests have been written using pytest and we have ensured 100% line and branch coverage for the controller and model code. For integration tests, we have tested the API and have covered positive and negative cases that are possible with different sets of inputs.

We have also auto-generated documentation using Sphinx for all the module docstrings with module description, input parameters, and return parameters. Sphinx makes it possible to create intelligent and streamlined documentations to increase understandability. The generated documentation is split into API and internal documentation so that developers can see exactly how the API will be used and how the modules are structured.

## How to run unit tests

1. Run "pytest" in the root folder to run all the test cases
2. The test session summary has been provided in the design document and the evaluation report.

## Unit Test Results

![image19](https://github.com/kavyaharlalka/kashikoi-elena-navigation/assets/77462752/147fc9ba-ea98-42ce-a54d-f37740c0a94c)


## How to run integration tests

1. Go to the folder test/integration
2. Run "python3 -m pytest api_inttest.py"

## Integration Test Results

![WhatsApp Image 2023-05-22 at 8 15 28 PM](https://github.com/kavyaharlalka/kashikoi-elena-navigation/assets/77462752/9a13afb8-9ca8-48b7-a164-541aef7a0cf7)



