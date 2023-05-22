# CS 520: Kashikoi-EleNA

# Problem Statement

Navigation Systems typically provide the shortest path between any two given points. These are not optimal for a lot of scenarios where the user is interested in finding a path which has the least elevation gain. Moreover, some users might be interested in finding a path which has elevation gain so that they can partake in an intense and time-constrained workout. To extend navigation systems to solve the above problems, we have designed a software system that takes two points as input and finds the optimal route between them that maximizes or minimizes elevation gain while limiting the total path distance to n% of the shortest path between these two points.

# Steps to Run the Application

1. Clone the repositors using git clone https://github.com/kavyaharlalka/kashikoi-elena-navigation.git
2. Run 'python3 -m pip install requirements.txt'
3. Run bash run.sh to start the server
4. After the server is running, go to the local host http://127.0.0.1:5000/

# Testing and Evaluation

There is a comprehensive test suite for our application to ensure that all the functions and modules are tested and all corner cases are covered. Unit tests have been written using pytest and we have ensured 100% line and branch coverage for the controller and model code. For integration tests, we have tested the API and have covered positive and negative cases that are possible with different sets of inputs.

## How to run unit tests

1. Run "pytest" in the root folder to run all the test cases
2. The test session summary has been provided in the design document and the evaluation report.

## Unit Test Results

![image19](https://github.com/kavyaharlalka/kashikoi-elena-navigation/assets/77462752/147fc9ba-ea98-42ce-a54d-f37740c0a94c)


## How to run integration tests

## Integration Test Results


