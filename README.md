# ETL Code Generator

ETL Code Generator is a Python-based tool that dynamically generates executable ETL (Extract, Transform, Load) pipelines. Using Jinja2 templates, the tool reads a JSON configuration file to create custom Python code, which can then be executed on a different machine. The project also features a web-based GUI built with FastAPI that provides a multiuser, drag-and-drop interface for configuring pipeline components.

---

## Overview

The ETL Code Generator comprises two main parts:

- **Core Engine:**  
  Parses the `config.json` file—defining the order and settings for each ETL operation—and uses Jinja2 templates to generate a complete Python script for executing the ETL pipeline. This engine supports various processing steps including reading from CSV files or databases, filtering, grouping, joining, splitting, and writing data. It also handles custom operations via hooks and user-defined Jinja2 templates.

- **Web Frontend:**  
  A FastAPI-based server provides a graphical user interface (GUI) that supports:
  - Multiuser capabilities.
  - A simple drag-and-drop system for configuring pipeline components.

---

## Project Structure

- **docs/**  
  Documentation and additional setup guides (including on-premise setup)
- **core/**  
  Core ETL engine, code generation logic, and Jinja2 templates
- **server/**  
  FastAPI server for the web-based GUI and backend services
- **tests/**  
  Unit and integration tests for the project
- **README.md**  
  Project overview and development setup instructions
---

## Getting Started

### Prerequisites

- **Python 3.8+**  
- Required Python packages (listed in `requirements.txt`):
  - `jinja2`
  - `pandas`
  - `sqlalchemy`
  - `fastapi`
  - `uvicorn`
  - `pre-commit`
  - `pytest`
  - `pathlib`

### Development Setup

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/chofste/ETL.git
    cd ETL
    ```

2. **Create and Activate a Virtual Environment (Optional but Recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Configure Your Pipeline:**

    - Edit the `config.json` file to define the pipeline steps and settings.
    - Refer to the documentation in the `docs/` folder for details on the configuration schema and available processing components.

---

## How to Start the Project

### Running the ETL Code Generator (Core)

The core engine is responsible for reading the configuration and generating the ETL Python script.

1. **Generate the ETL Script:**

    Navigate to the core directory and run the generator:

    ```bash
    python core/core.py
    ```

    This command parses `config.json`, processes the steps using the Jinja2 templates in `core/templates/`, and outputs the generated script as `generated_script.py`.

2. **Review the Generated Script:**

    The output script includes:
    - Module-level imports and preamble code.
    - Function definitions for any branch processing (from split steps).
    - A main function that executes the entire pipeline.

### Running the Web Server

The FastAPI server provides the interactive GUI for configuring and managing ETL pipelines.

1. **Start the Server:**

    Navigate to the server directory and run:

    ```bash
    python server/server.py
    ```

    The server will start at [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

2. **Access the GUI:**

    - Open your web browser and go to the server URL.

---

## Troubleshooting & Next Steps

- **Configuration Issues:**  
  Ensure that your `config.json` adheres to the provided JSON schema. Detailed documentation is available in the `docs/` folder.

- **Template Rendering Problems:**  
  Verify that all Jinja2 templates are correctly formatted and located in the `core/templates/` directory.

- **Server Errors:**  
  Check console logs for any error messages when starting the FastAPI server.

### Future Enhancements
- Use the drag-and-drop interface to configure your ETL pipeline. Changes made via the GUI update the configuration dynamically, enabling collaborative multiuser support.

- Extend the configuration schema to support additional processing steps.
- Enhance custom hook functionality for third-party integrations (e.g., data quality checks).
- Improve the web GUI with real-time collaboration features.
- Optimize the code generation process for better performance and scalability.

For on-premise deployment instructions, please refer to the separate `setup.md` in the `docs/` folder.

---

## Contributions

Contributions are welcome! Please review the contribution guidelines in the repository and submit pull requests for any enhancements or fixes.

---

## License

This project is licensed under the [AGPL](LICENSE).

---

Happy ETLing!
