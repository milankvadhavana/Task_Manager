
#!/bin/bash

# Install ODBC dependencies
apt-get update && apt-get install -y \
    unixodbc \
    unixodbc-dev \
    g++ \
    curl

# Install Microsoft ODBC Driver
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list
apt-get update
ACCEPT_EULA=Y apt-get install -y msodbcsql17

# Install Python packages
pip install -r requirements.txt

# Start the app
gunicorn --bind 0.0.0.0:$PORT --timeout 600 app:app
