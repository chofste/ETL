import json, textwrap, re
from jinja2 import Environment, FileSystemLoader

# Load configuration
with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

# Set up Jinja2 environment with the template directory (e.g., 'templates')
env = Environment(loader=FileSystemLoader('templates'))

# Mapping of processing steps to template files
step_templates = {
    "read_csv": "read_csv.jinja2",
    "read_mariadb": "read_mariadb.jinja2",
    "join": "join.jinja2",
    "filter": "filter.jinja2",
    "group": "group.jinja2",
    "write_csv": "write_csv.jinja2",
    "write_mariadb": "write_mariadb.jinja2",
    "merge": "merge.jinja2"  # New merge step template
}

# Lists to collect code segments and branch function definitions
code_segments = []
branch_function_defs = []

# Variable to store branch names from the last split step
last_split_branch_names = []

# Preamble: basic imports (module-level)
preamble = """import pandas as pd
from sqlalchemy import create_engine
from concurrent.futures import ThreadPoolExecutor
import datetime
"""

# Process the defined steps from the configuration
steps = config.get("steps")
if steps is None:
    raise KeyError("Die Konfiguration muss einen 'steps'-Key enthalten, der die Verarbeitungsschritte definiert.")

for step in steps:
    step_type = step["step"]

    if step_type == "read":
        # Process read steps (e.g. CSV or MariaDB)
        source_type = step["source"]["type"]
        if source_type == "csv":
            template_name = step_templates["read_csv"]
        elif source_type == "mariadb":
            template_name = step_templates["read_mariadb"]
        else:
            raise ValueError(f"Unbekannter Source-Typ: {source_type}")
        template = env.get_template(template_name)
        rendered = template.render(step=step, config=config)
        code_segments.append(rendered)

    elif step_type == "write":
        # Process global write steps (outside branches)
        if isinstance(step["target"], list):
            if step.get("concurrent_write", False):
                segment = "with ThreadPoolExecutor(max_workers={}) as executor:\n".format(config.get("threads", 1))
                segment += "    futures = []\n"
                for i, target in enumerate(step["target"]):
                    target_type = target["type"]
                    if target_type == "csv":
                        template_name = step_templates["write_csv"]
                    elif target_type == "mariadb":
                        template_name = step_templates["write_mariadb"]
                    else:
                        raise ValueError(f"Unbekannter Target-Typ: {target_type}")
                    # Determine the source dataframe variable.
                    if "branch" in target:
                        source_df = "result_" + target["branch"]
                    elif last_split_branch_names and i < len(last_split_branch_names):
                        source_df = "result_" + last_split_branch_names[i]
                    else:
                        source_df = "df"
                    template = env.get_template(template_name)
                    rendered = template.render(step={"target": target, "source_df": source_df}, config=config)
                    clean_code = textwrap.dedent(rendered.strip())
                    segment += (
                        "    futures.append(executor.submit((lambda code, src: exec(code, globals(), {{'{0}': src}})), "
                        "'''{1}''', {0}))\n"
                    ).format(source_df, clean_code)
                segment += "    for future in futures:\n"
                segment += "        future.result()\n"
                code_segments.append(segment)
            else:
                for i, target in enumerate(step["target"]):
                    target_type = target["type"]
                    if target_type == "csv":
                        template_name = step_templates["write_csv"]
                    elif target_type == "mariadb":
                        template_name = step_templates["write_mariadb"]
                    else:
                        raise ValueError(f"Unbekannter Target-Typ: {target_type}")
                    if "branch" in target:
                        source_df = "result_" + target["branch"]
                    elif last_split_branch_names and i < len(last_split_branch_names):
                        source_df = "result_" + last_split_branch_names[i]
                    else:
                        source_df = "df"
                    template = env.get_template(template_name)
                    rendered = template.render(step={"target": target, "source_df": source_df}, config=config)
                    code_segments.append(rendered)
        else:
            target = step["target"]
            target_type = target["type"]
            if target_type == "csv":
                template_name = step_templates["write_csv"]
            elif target_type == "mariadb":
                template_name = step_templates["write_mariadb"]
            else:
                raise ValueError(f"Unbekannter Target-Typ: {target_type}")
            if "branch" in target:
                source_df = "result_" + target["branch"]
            elif last_split_branch_names:
                source_df = "result_" + last_split_branch_names[0]
            else:
                source_df = "df"
            template = env.get_template(template_name)
            rendered = template.render(step={"target": target, "source_df": source_df}, config=config)
            code_segments.append(rendered)

    elif step_type in ["join", "filter", "group"]:
        template_name = step_templates[step_type]
        template = env.get_template(template_name)
        rendered = template.render(step=step, config=config)
        code_segments.append(rendered)

    elif step_type == "merge":
        # Process merge steps to reunite branch results
        template_name = step_templates["merge"]
        template = env.get_template(template_name)
        rendered = template.render(step=step, config=config)
        code_segments.append(rendered)

    elif step_type == "split":
        # Process split steps: execute branches concurrently and capture their results
        segment = "# Split step: Execute branches concurrently and capture their results\n"
        if step.get("parallel", False):
            segment += "with ThreadPoolExecutor(max_workers={}) as executor:\n".format(config.get("threads", 1))
            for branch in step["branches"]:
                branch_name = branch["name"]
                segment += "    future_{0} = executor.submit(branch_{0}, df)\n".format(branch_name)
            for branch in step["branches"]:
                branch_name = branch["name"]
                segment += "    result_{0} = future_{0}.result()\n".format(branch_name)
        else:
            for branch in step["branches"]:
                branch_name = branch["name"]
                segment += "result_{0} = branch_{0}(df)\n".format(branch_name)
        code_segments.append(segment)
        # Capture branch names for later steps (if needed)
        last_split_branch_names = [branch["name"] for branch in step["branches"]]

        # Generate the functions for each branch (defined at module level)
        for branch in step["branches"]:
            branch_name = branch["name"]
            branch_func = "def branch_{0}(df):\n    df_local = df.copy()\n".format(branch_name)
            for sub_step in branch["steps"]:
                sub_step_type = sub_step["step"]
                if sub_step_type in step_templates:
                    template_name = step_templates[sub_step_type]
                    template = env.get_template(template_name)
                    rendered = template.render(step=sub_step, config=config)
                    # Replace occurrences of the global variable 'df' with 'df_local'
                    rendered_local = re.sub(r'\bdf\b', 'df_local', rendered)
                    indented = "\n".join("    " + line for line in rendered_local.splitlines())
                    branch_func += indented + "\n"
                elif sub_step_type == "write":
                    # Process branch-level write steps
                    target = sub_step["target"]
                    if target["type"] == "csv":
                        template_name = step_templates["write_csv"]
                    elif target["type"] == "mariadb":
                        template_name = step_templates["write_mariadb"]
                    else:
                        raise ValueError(f"Unbekannter Target-Typ in Branch {branch_name}: {target['type']}")
                    template = env.get_template(template_name)
                    rendered = template.render(step={"target": target, "source_df": "df_local"}, config=config)
                    indented = "\n".join("    " + line for line in rendered.splitlines())
                    branch_func += indented + "\n"
                else:
                    raise ValueError(f"Unbekannter Verarbeitungsschritt in Branch {branch_name}: {sub_step_type}")
            branch_func += "    return df_local\n"
            branch_function_defs.append(branch_func)

    else:
        raise ValueError(f"Unbekannter Verarbeitungsschritt: {step_type}")

# Create the final code with the preamble, branch functions, and the main() function.
final_code = ""
final_code += preamble + "\n"  # Module-level imports first.
for branch_func in branch_function_defs:
    final_code += branch_func + "\n"
final_code += "def main():\n"
final_code += "    # Read and prepare the main dataframe\n"
for segment in code_segments:
    for line in segment.splitlines():
        final_code += "    " + line + "\n"
final_code += "\nif __name__ == '__main__':\n    main()\n"

with open("generated_script.py", "w", encoding="utf-8") as f:
    f.write(final_code)

print("Python-Code wurde erfolgreich generiert und in 'generated_script.py' gespeichert.")