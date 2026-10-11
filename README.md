# OpenTelemetry Demo — Automated Testing Framework

Automated testing framework for the OpenTelemetry Demo microservices application.

The project demonstrates API, UI, database, messaging, and end-to-end testing using Python. It includes automated test execution in CI/CD with GitHub Actions.

## Tech Stack

- Python
- Pytest
- Requests
- Playwright
- PostgreSQL
- Kafka
- Protocol Buffers
- Allure
- Docker
- GitHub Actions
- JSON Schema
- Faker
- pytest-xdist

## Project Goals

The main goals of this project are:

- Automate REST API testing.
- Validate business scenarios across multiple services.
- Verify data persistence in PostgreSQL.
- Validate asynchronous events published to Kafka.
- Automate UI scenarios with Playwright.
- Generate test reports with Allure.
- Run automated tests in CI/CD.
- Support parallel test execution.
- Improve debugging through logging and diagnostic attachments.

## Architecture

The test framework interacts with the OpenTelemetry Demo application and its supporting services.

```text
                    Pytest
                       |
          +------------+------------+
          |            |            |
        API Tests     UI Tests     E2E Tests
          |            |            |
       REST API     Playwright   Business Flow
          |                         |
          +------------+------------+
                       |
              Application Services
                       |
             +---------+---------+
             |         |         |
         PostgreSQL  Kafka    REST APIs
             |         |
         DB Checks  Event Checks
```

## Project Structure

```text
opentelemetry-demo-tests/
├── clients/
│   ├── base_client.py
│   ├── products_client.py
│   ├── cart_client.py
│   ├── checkout_client.py
│   ├── db_client.py
│   └── kafka_client.py
├── data/
│   ├── test_data.py
│   └── order_builder.py
├── repositories/
│   └── order_repository.py
├── schemas/
│   └── checkout_schema.py
├── tests/
│   ├── api/
│   ├── db/
│   ├── E2E/
│   ├── integration/
│   └── ui/
├── utils/
│   ├── assertions.py
│   └── allure_helpers.py
├── config.py
├── conftest.py
├── pytest.ini
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## Test Coverage

### API Testing

- Main page and currency endpoints
- Product retrieval
- Cart operations
- Checkout scenarios
- Positive and negative cases
- HTTP status validation
- JSON response validation
- JSON Schema validation

### Database Testing

- PostgreSQL connectivity
- Order persistence
- Order item validation
- Shipping data validation
- API response versus database comparison

### Kafka Testing

- Kafka consumer initialization
- Order event processing
- Event matching by order ID
- Invalid message handling
- Timeout handling

### UI Testing

- Main page availability
- Product catalog validation
- Checkout UI scenarios

### End-to-End Testing

The end-to-end scenario verifies an order creation flow across multiple components:

1. Retrieve application data.
2. Select a product.
3. Add the product to the cart.
4. Submit a checkout request.
5. Validate the API response.
6. Verify persisted order data in PostgreSQL.
7. Verify the corresponding Kafka event.

## Framework Features

### Logging

HTTP requests, responses, execution times, and relevant errors are logged to simplify troubleshooting.

### Test Data Builder

`OrderBuilder` generates checkout request bodies and supports customization of individual fields.

Faker is used to generate test data.

### Custom Assertions

Reusable assertions provide consistent validation and informative failure messages.

### JSON Schema Validation

Checkout responses are validated against a JSON Schema.

### Database Repository

`OrderRepository` encapsulates SQL queries used to retrieve order details from PostgreSQL.

### Kafka Helpers

Kafka utilities manage consumer lifecycle, wait for events, handle malformed messages, and enforce timeouts.

### Allure Reporting

Allure reports provide test execution details and diagnostic attachments, including API responses, database results, and Kafka events.

### Parallel Execution

The framework supports parallel execution through `pytest-xdist`.

## Prerequisites

- Python
- Docker Desktop
- Git
- Java runtime compatible with the installed Allure CLI, if generating reports locally
- Allure CLI

## Installation

Clone the repository:

```bash
git clone https://github.com/makarov3235/opentelemetry-demo-tests.git
cd opentelemetry-demo-tests
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Install Playwright browsers if they are not already installed:

```bash
playwright install chromium
```

## Running the Demo Application

Start the application using the project's Docker Compose configuration.

```bash
docker compose up -d
```

Check running containers:

```bash
docker compose ps
```

Wait until the application services are ready before running tests.

## Running Tests

Run the complete test suite:

```bash
pytest -v
```

Run API tests:

```bash
pytest tests/api -v
```

Run database tests:

```bash
pytest tests/db -v
```

Run UI tests:

```bash
pytest tests/ui -v
```

Run end-to-end tests:

```bash
pytest tests/E2E -v
```

Run tests in parallel using two workers:

```bash
pytest -n 2 -v
```

## Allure Reports

Run tests and collect Allure results:

```bash
pytest -v --alluredir=allure-results
```

Open the generated report:

```bash
allure serve allure-results
```

Allure attachments provide additional context for diagnosing failures.

## CI/CD

The project uses GitHub Actions to execute automated tests.

The workflow provides automated regression testing and reports the execution status directly in GitHub Actions.

[View GitHub Actions](https://github.com/makarov3235/opentelemetry-demo-tests/actions)

## Skills Demonstrated

- Python test automation
- Pytest framework design
- REST API testing
- UI automation with Playwright
- PostgreSQL validation
- Kafka event testing
- End-to-end integration testing
- JSON Schema validation
- Test data generation
- Logging and diagnostics
- Allure reporting
- Docker
- GitHub Actions CI/CD
- Parallel test execution

## Repository

[GitHub: opentelemetry-demo-tests](https://github.com/makarov3235/opentelemetry-demo-tests)