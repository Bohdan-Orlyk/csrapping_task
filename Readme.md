# Your App Name

## Overview

This is a simple application that parses a website, stores the data in a PostgreSQL database, and performs a daily database dump. The application is containerized using Docker, and the process is orchestrated using Docker Compose.

## Requirements

- Docker
- Docker Compose

## Getting Started

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Bohdan-Orlyk/csrapping_task

2. **Navigate to the project directory:**
   ```bash 
   cd app_folder_name
   
3. **Set up your environment variables:**
   Create a .env file in the project root.
4. **Build the Docker image:**
   ```bash 
   docker-compose build

5. **Start the application:**
   ```bash 
   docker-compose up -d
   ```
   ### The application will now start parsing the website daily at 12:00 and perform a database dump at 12:30.

## Configuration
- Update the .env file with the appropriate configurations for your application. 
- Adjust the schedule for parsing and database dump in the docker-compose.yml file under the cron service.

## Monitoring 
- ```bash 
   docker-compose logs
   ```
- Check the database for parsed data.