# 0x00. Personal Data

## Overview

This project focuses on handling personal user data securely, emphasizing the importance of data privacy and protection. It includes functionalities for:

- Filtering sensitive information from logs.
- Custom logging with redaction capabilities.
- Secure database connections.
- Hashing and validating passwords.

## Features

- **Data Filtering:** Obfuscates specified fields in log messages to prevent sensitive data exposure.
- **Custom Logging:** Implements a logging formatter that redacts sensitive information.
- **Secure Database Connection:** Connects to a MySQL database using credentials from environment variables.
- **Password Handling:** Provides functions to hash passwords securely and validate them.

## Requirements

- Python 3.7
- `pycodestyle` compliance (version 2.5)
- All scripts are executable and end with a new line.
- Proper documentation for modules, classes, and functions.

## Setup

1. **Install Dependencies:**

   ```bash
   pip install mysql-connector-python bcrypt

