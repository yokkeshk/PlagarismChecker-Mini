FastAPI-based Backend for Managing and Analyzing Code Submissions
This project is a backend system designed to collect and manage code submissions from users in a structured database. It serves as the foundational layer for a plagiarism detection tool that could be used in coding contests or technical assessments.

The system is built using FastAPI for the web framework and SQLAlchemy as the ORM, with a SQLite database for local storage. The architecture is modular and clean, making it easy to scale or integrate with other services like user authentication, frontend interfaces, or advanced code comparison algorithms.

Project Overview
The main purpose of this project is to provide a system where code submissions from multiple users can be stored, accessed, and eventually analyzed to detect similarities or signs of plagiarism.

It supports receiving submissions through a RESTful API and storing them in a relational database, with key details like user identifiers, code snippets, and submission timestamps. This structured data can then be used for comparison and reporting.

How It Works
The backend exposes endpoints to handle basic operations like creating and retrieving code submissions. Each submission is recorded with metadata that could be useful for audit trails or similarity checks. A schema-based validation system ensures all data entering the system is clean and consistent.

A separate script is included to generate and populate the database with mock data, simulating multiple users and their submission attempts. This helps test the system under realistic conditions without relying on live contest data.

Use Case
This system is ideal for educational institutions, coding bootcamps, or companies conducting coding interviews. It allows administrators to collect all code submissions and lays the groundwork for implementing algorithms that can automatically flag suspiciously similar code.

Future Scope
The current structure is flexible and can be extended with:

A frontend dashboard for admins

User authentication and role management

Integration of code similarity algorithms

Export and reporting features

Support for additional languages or coding environments
