# TMG Backend 

This is a README.md file for a TMG Python backend project with a predefined folder structure.

## Table of Contents

- [Folder Structure](#folder-structure)
- [Creating a Virtual Environment](#creating-a-virtual-environment)
- [Installing Dependencies](#installing-dependencies)

## Folder Structure

project should follow this folder structure:

ROOT/
│
├── app/
│ ├── component1/
│ │ ├── model.py
│ │ ├── service.py
│ │ ├── route.py
│ │
│ ├── component2/
│ │ ├── model.py
│ │ ├── service.py
│ │ ├── route.py
│ │
│ ├── component3/
│ │ ├── model.py
│ │ ├── service.py
│ │ ├── route.py
│ │
│ ├── ...
│
├── requirements.txt
├── run.py
├── README.md

### Creating a Virtual Environment

To create a virtual environment for A project, open a terminal and run the following command:

```bash

python -m venv venv 

```
### TO Activate Virtual Environment

# On Windows
venv\Scripts\activate

# On macOS and Linux
source venv/bin/activate

### installing-dependencies

pip install -r requirements.txt

### Run command 
python run.py