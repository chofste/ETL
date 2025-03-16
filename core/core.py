import json
from jinja2 import Environment, FileSystemLoader

# Load the configuration from a JSON file
with open("config.json", "r") as f:
    config = json.load(f)

# Set up the Jinja2 environment using the
# 'templates' directory for template files
env = Environment(loader=FileSystemLoader("templates"))

# Define a mapping of processing step types to
# their corresponding Jinja2 template filenames
step_templates = {
    "read_csv": "read_csv.jinja2",
    "read_mariadb": "read_mariadb.jinja2",
    "join": "join.jinja2",
    "filter": "filter.jinja2",
    "group": "group.jinja2",
    "write_csv": "write_csv.jinja2",
    "write_mariadb": "write_mariadb.jinja2",
}

# Initialize a list to collect segments of the generated Python code
code_segments = []

# Create a preamble segment for the generated code
# including essential library imports
preamble = """import pandas as pd
from sqlalchemy import create_engine
"""
code_segments.append(preamble)

# Retrieve the list of processing steps from the configuration
steps = config.get("steps")
if steps is None:
    raise KeyError(
        "The configuration must contain a 'steps' key " "defining the processing steps."
    )

# Iterate through each processing step and generate
# the corresponding code using templates
for step in steps:
    step_type = step["step"]

    # Process 'read' steps by determining
    # the source type (e.g., CSV or MariaDB)
    if step_type == "read":
        print("Processing read step...")
        source_type = step["source"]["type"]
        if source_type == "csv":
            print("Detected CSV source.")
            template_name = step_templates["read_csv"]
            print(f"Using template: {template_name}")
        elif source_type == "mariadb":
            template_name = step_templates["read_mariadb"]
        else:
            raise ValueError(f"Unknown source type: {source_type}")

    # Process 'write' steps by determining
    # the target type (e.g., CSV or MariaDB)
    elif step_type == "write":
        print("Processing write step...")
        target_type = step["target"]["type"]
        if target_type == "csv":
            template_name = step_templates["write_csv"]
        elif target_type == "mariadb":
            template_name = step_templates["write_mariadb"]
        else:
            raise ValueError(f"Unknown target type: {target_type}")

    # For other step types such as 'join', 'filter', or 'group',
    # select the corresponding template
    elif step_type in ["join", "filter", "group"]:
        template_name = step_templates[step_type]
    else:
        raise ValueError(f"Unknown processing step: {step_type}")

    # Load the selected template and render it with the current step data
    template = env.get_template(template_name)
    rendered = template.render(step=step)
    code_segments.append(rendered)

# Combine all generated code segments into the final Python script
final_code = "\n".join(code_segments)

# Write the generated Python script to a file
with open("generated_script.py", "w") as f:
    f.write(final_code)

print(
    "Python code has been successfully generated " "and saved to 'generated_script.py'."
)
