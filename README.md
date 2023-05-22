# CS 520: Kashikoi-EleNA

# Problem Statement

Navigation Systems typically provide the shortest path between any two given points. These are not optimal for a lot of scenarios where the user is interested in finding a path which has the least elevation gain. Moreover, some users might be interested in finding a path which has elevation gain so that they can partake in an intense and time-constrained workout. To extend navigation systems to solve the above problems, we have designed a software system that takes two points as input and finds the optimal route between them that maximizes or minimizes elevation gain while limiting the total path distance to n% of the shortest path between these two points.

# Steps to Run the Application

1. Clone the repositors using git clone https://github.com/kavyaharlalka/kashikoi-elena-navigation.git
2. Run bash run.sh to start the server

# Testing and Evaluation

There is a comprehensive test suite for our application to ensure that all the functions and modules are tested and all corner cases are covered. The unit tests are written using pytest and the integration tests are written using postman test suite runner.

## How to run unit tests

1. Run "pytest" in the root folder to run all the test cases
2. The test session summary has been provided in the design document and the evaluation report.

## How to run integration tests
