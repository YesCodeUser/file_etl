# file_etl

## Description
ETL pipeline for automated processing, validation, and storage of CSV data.  
The project is designed as a reusable core for future services that automate manual spreadsheet-based workflows.

The goal is to reduce hours of manual Excel work by providing a reliable, transactional data processing pipeline with detailed reporting.

## Use Case
Many small and medium businesses rely on CSV/Excel files for operational data.  
This project automates:
- data validation
- error detection
- structured storage
- reporting

Future access will be provided via API and Telegram bot.

## Input Data
- CSV files with a predefined schema (currently: `id`, `name`, `salary`)
- Architecture is designed to be easily adaptable to other schemas

## Validation
- Field presence validation
- Type validation for all fields
- Basic business rules validation
- Invalid data is rejected before persistence

## Persistence
- PostgreSQL
- All database writes are transactional
- Only validated data is persisted

## Architecture
- Clear separation of concerns:
  - parsing
  - validation
  - persistence
  - reporting
- Modular design for future extensions

## Output
- Console reports
- JSON reports (for easy integration with other systems)

## Roadmap
- SQL
- Dockerization
- REST API
- Telegram bot interface

## Status
Finish.
