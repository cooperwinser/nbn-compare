# NBN Price Comparison App

## Overview
This web app is designed to help users compare pricing information from various NBN internet service providers. It utilizes Flask as the web framework, Supabase as the backend database, and Tailwind CSS for styling.

## Features
- Scrapes data from NBN internet service provider websites and APIs to obtain pricing information.
- Displays the collected data in an easy-to-read table within the app.
- Allows users to compare pricing plans from different providers.

## Technologies Used
- **Flask:** A lightweight web framework for Python that facilitates the development of web applications.
- **Supabase:** An open-source alternative to Firebase, providing a scalable and secure backend for your application.
- **Tailwind CSS:** A utility-first CSS framework that makes styling your app simple and efficient.

## Getting Started
### Prerequisites
- Python 3.x installed
- Python venv
- Tailwind
- Supabase account and API key

### Requirements
- Flask==3.0.1
- supabase==2.3.4
- requests==2.31.0
- python-dotenv==1.0.0
- httpx==0.25.2

### Installation
1. Clone the repository.
2. Create and activate a Python virtual enivronment (venv) and install the requirements via pip (see above).
3. Create a Supabase account and project.
4. Create a .env file in the project root and add the following:
    ```env
   SUPABASE_URL=<your-supabase-url>
   SUPABASE_KEY=<your-supabase-api-key>
   ```
5. Create the relevant database tables in Supabase.
   ![Supabase Schema](https://i.imgur.com/vcLjG2Y.png)
6. Start the application: ```flask --app app run --debug```