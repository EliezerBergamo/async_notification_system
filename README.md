<img alt="email" src="https://github.com/user-attachments/assets/2c56642a-dc8f-481c-bfe2-d3983d9468e9" alt="logo" width="50"/>

<section>
  <div>
    <h1>Asynchronous Notification System</h1>
    <p align="justify">
      This project is an asynchronous message processing system that uses a pipeline architecture. It demonstrates the
      ability to build a resilient, scalable, and loosely coupled solution for processing notifications in the background,
      ensuring that API requests are responded to quickly and non-blockingly. The message pipeline was implemented with
      <b>RabbitMQ</b> to manage data flow across multiple queues, including retry mechanisms and <b>Dead Letter Queue (DLQ)</b>
      for fault handling.
    </p>
  </div>

  <div>
    <h2>Technologies</h2>
    <h4>Backend</h4>
    <ul>
      <li>Python 3.12+</li>
      <li>FastAPI</li>
      <li>Aio-pika</li>
      <li>Pydantic</li>
    </ul>
    <h4>Messaging</h4>
    <ul>
      <li>RabbitMQ</li>
    </ul>
    <h4>Tests</h4>
    <ul>
      <li>Pytest</li>
      <li>Unittest.mock</li>
    </ul>
  </div>

  <div>
    <h2>Features</h2>
    <ul>
      <li align="justify">
        Complete Messaging Pipeline: A pipeline architecture that routes messages through input, validation, retry,
        and <b>DLQ</b> queues, ensuring that messages are not lost.
      </li>
      <li align="justify">
        Asynchronous Processing: Use of <b>asyncio</b> and <b>aio-pika</b> to execute consumers concurrently and efficiently.
      </li>
      <li align="justify">
        Error Handling and Resilience: Implementation of failure logic and automatic routing to retry and <b>DLQ</b> queues,
        making the system robust.
      </li>
      <li align="justify">
        In-Memory Tracking: The status of each notification is persisted in memory for consultation via a <b>traceId</b>.
      </li>
      <li align="justify">
        Modular Design: Well-organized code, with separation of responsibilities into modules for API, messaging
        service, models, and persistence.
      </li>
      <li align="justify">
        Unit Testing with Mocks: Demonstrates the ability to test the service's business logic without the
        need for a real connection to <b>RabbitMQ</b>.
      </li>
    </ul>
  </div>

  <div>
    <h2>Getting used</h2>
    <h3>1. Setting up the virtual environment</h3>
  <p align="justify">
    The project requires a <b>Python</b> environment and access to a <b>RabbitMQ</b> instance.
    Create a virtual environment by doing the following in the CLI:

  ```
  pip install virtualenv
  ```

  ```
  python -m venv venv
  ```
  </p>

  <p align="justify">
    To activate the virtual environment, execute the command, if activated correctly,
    the name of the virtual environment will appear on the left in the terminal.

  ```
  \venv\Scripts\activate
  ```
  </p>

  <h3>2. Installing dependencies</h3>
  <p align="justify">
    With the virtual environment enabled, install the necessary libraries:

  ```
  pip install requirements.txt
  ```
  </p>

  <h3>3. Setting up environment variables</h3>
  <p align="justify">
    Its necessary to Create a <b>.env</b> file in the project root with the following variable, using the <b>RabbitMQ URL</b>.

  ```
  RABBITMQ_URL=amqps://[USER]:[PASSWORD]@[HOST]/[VHOST]
  ```
  </p>

  <h3>4. Executing the project</h3>
  <p align="justify">
    This project consists of two parts that must be executed on separate terminals: the API server (producer) and the consumers.
    <br><br> Terminal 1 (API): Launch the <b>FastAPI</b> server.
  
  ```
  uvicorn main:app --reload
  ```
  The server will be available at http://127.0.0.1:8000.

  Terminal 2 (Consumers): Start the consumer script.
  </p>

  ```
  python src/consumers.py
  ```
  There will be messages on the console indicating that consumers are connected and waiting.
  </div>

  <div>
    <h2>Tests</h2>
  <p align="justify">
    To run unit tests with mocks, execute the following command:
    
  ```
  pytest
  ```
  </p>
  </div>

  <div>
    <h2>Authors</h2>
    <ul>
      <li>
        Eliezer Bergamo
      </li>
    </ul>
  </div>

  <div>
    <h2>Versioning</h2>
    <p>1.0.0</p>
  </div>

  <footer>
    <p align="center">All rights reserved &copy Eliezer Bergamo</p>
  </footer>
</section>
