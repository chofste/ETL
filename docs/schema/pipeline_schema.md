# Data Pipeline Configuration Schema Documentation

This documentation describes the JSON schema used to configure data processing pipelines. The schema covers overall pipeline properties, detailed component configurations, and the data schemas flowing through each component. It is intended for users who need to set up, validate, and extend their data pipelines.

---

## Overview

The schema defines the structure for configuring pipelines by including properties such as:

- **Pipeline-level properties:** General settings like pipeline ID, description, execution mode, thread allocation, batch size, incremental processing, bulk processing, and timestamp information.
- **Step-level properties:** An ordered list of components (steps) that build the pipeline. Each step details its type (e.g., read, filter, split, group, join, write, hook, custom), relationships (parent and children), and data schema.
- **Component-specific configurations:** Options for data sources (CSV, JSON, or database), filtering, splitting (branching), grouping (aggregation), joining, writing output, hooks for external service calls, and custom processing using a Jinja2 template.

---

## Schema Breakdown

### 1. Pipeline-Level Properties

- **pipeline_id**:  
  A unique identifier for the entire pipeline configuration.

- **pipeline_description**:  
  A high-level description explaining the purpose and overview of the pipeline.

- **execution_mode**:  
  Specifies how the pipeline executes. Allowed values are:
  - `incremental`
  - `batch`
  - `stream`

- **threads**:  
  The number of threads allocated for the pipeline’s execution. Must be at least 1.

- **batch_size**:  
  The size of the data batches processed when in batch mode.

- **last_processed_timestamp**:  
  A date-time formatted string indicating the timestamp of the last processed data.

- **steps**:  
  An array that lists each pipeline component (or step). Each step has its own configuration which details how it interacts with the data.

---

### 2. Step-Level Properties

Each entry in the **steps** array represents a component in the pipeline and includes the following properties:

- **component_id**:  
  Unique identifier for the component.

- **description**:  
  (Optional) Text describing the purpose or behavior of the component.

- **parent**:  
  Identifier for the parent component. It is `null` if the component is a root element.

- **children**:  
  An array of identifiers for any child components.

- **step**:  
  Indicates the type of processing step. Allowed values are:
  - `read`
  - `filter`
  - `split`
  - `group`
  - `join`
  - `write`
  - `hook`
  - `custom`

- **component_schema**:  
  Describes the schema of the data flowing through the component.  
  It includes:
  - **columns**: An array of objects. Each object defines:
    - **name**: Name of the column.
    - **type**: Data type, with allowed values:
      - `string`
      - `number`
      - `boolean`
      - `date`
      - `timestamp`
      - `json`

---

### 3. Component-Specific Configurations

#### a. Source Configuration (for `read` steps)
- **source**:  
  Contains settings for reading data:
  - **type**: Specifies the data source type. Allowed values:
    - `csv`
    - `json`
    - `database`
  - **filepath**: The path to the source file or a database connection string.
  - **separator**: (Optional) The delimiter used in CSV files (limited to a single character).
  - **columns**: (Required if `type` is `database`) An array defining the database schema. Each entry includes:
    - **name**: Column name.
    - **data_type**: Data type (allowed values similar to the component schema).

#### b. Filter Configuration (for `filter` steps)
- **filter**:  
  Defines the conditions to filter data:
  - **column**: Column on which the filter is applied.
  - **condition**: Comparison operator with allowed values:
    - `>`, `<`, `==`, `!=`, `>=`, `<=`
  - **value**: The value to compare against (can be a string or number).

#### c. Split Configuration (for `split` steps)
- **split**:  
  Used to branch the pipeline:
  - **parallel**: A boolean indicating if branches should execute in parallel.
  - **branches**: An array of branch objects. Each branch includes:
    - **name**: The branch name.
    - **steps**: An array of steps specific to that branch.

#### d. Group Configuration (for `group` steps)
- **group**:  
  Handles data aggregation:
  - **column**: The column used to group the data.
  - **aggregation**: An array of aggregation operations. Each operation specifies:
    - **column**: The target column.
    - **function**: The aggregation function to apply (allowed values: `sum`, `mean`, `count`, `max`, `min`).

#### e. Join Configuration (for `join` steps)
- **join**:  
  Merges data from different components:
  - **with**: The identifier of the component to join with.
  - **on**: The column used as the join key.

#### f. Write Configuration (for `write` steps)
- **write**:  
  Configures the output data writing:
  - **concurrent_write**: A boolean that specifies if writing should be concurrent.
  - **target**: An array of target configurations. Each target object includes:
    - **type**: Output format, either `csv` or `json`.
    - **filepath**: The path to the output file.
    - **separator**: (Optional) Delimiter for CSV output files (limited to a single character).

#### g. Hook Configuration (for `hook` steps)
- **hook**:  
  Configures custom hooks that integrate with third-party services for data quality checks, notifications, or external validations. Useful properties include:
  - **url**: A string representing the endpoint URL for the hook call.
  - **method**: The HTTP method used to call the hook service. Allowed values: `GET`, `POST`, `PUT`, `DELETE`.
  - **headers**: An object containing key-value pairs for HTTP headers.
  - **payload**: An optional object representing the request payload (used with `POST` or `PUT`).
  - **timeout**: An integer specifying the timeout (in seconds) for the hook request.

#### h. Custom Component Configuration (for `custom` steps)
- **custom**:  
  Configures a custom processing component where users can define bespoke logic using a Jinja2 template. In addition to the standard component properties (ID, description, and schema), it includes:
  - **template**: A string containing the Jinja2 template used to process data.

---

## Complete JSON Schema

Below is the full JSON schema that combines all the elements discussed:

```json
{
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "Data Pipeline Configuration Schema",
    "description": "Schema for configuring data processing pipelines with detailed components, their relationships, and data schemas.",
    "type": "object",
    "properties": {
      "pipeline_id": {
        "type": "string",
        "description": "Unique identifier for the entire pipeline configuration."
      },
      "pipeline_description": {
        "type": "string",
        "description": "A high-level description of the pipeline and its purpose."
      },
      "execution_mode": {
        "type": "string",
        "enum": [
          "incremental",
          "batch",
          "stream"
        ],
        "description": "Mode in which the pipeline executes."
      },
      "threads": {
        "type": "integer",
        "minimum": 1,
        "description": "Number of threads allocated for pipeline execution."
      },
      "batch_size": {
        "type": "integer",
        "minimum": 1,
        "description": "Size of data batches processed in batch mode."
      },
      "incremental": {
        "type": "boolean",
        "description": "Flag indicating if the pipeline should run in incremental mode."
      },
      "last_processed_timestamp": {
        "type": "string",
        "format": "date-time",
        "description": "Timestamp of the last processed data."
      },
      "bulk_processing": {
        "type": "boolean",
        "description": "Flag indicating if bulk processing is enabled."
      },
      "steps": {
        "type": "array",
        "description": "Ordered list of pipeline components (steps) along with their relationships and data schemas.",
        "items": {
          "type": "object",
          "properties": {
            "component_id": {
              "type": "string",
              "description": "Unique identifier for the component."
            },
            "description": {
              "type": "string",
              "description": "A description of the component's purpose or behavior."
            },
            "parent": {
              "type": [
                "string",
                "null"
              ],
              "description": "Identifier of the parent component; null if this is a root component."
            },
            "children": {
              "type": "array",
              "description": "List of identifiers of child components.",
              "items": {
                "type": "string"
              }
            },
            "step": {
              "type": "string",
              "enum": [
                "read",
                "filter",
                "split",
                "group",
                "join",
                "write",
                "hook",
                "custom"
              ],
              "description": "The type of processing step."
            },
            "component_schema": {
              "type": "object",
              "description": "Schema of the data flowing through the component.",
              "properties": {
                "columns": {
                  "type": "array",
                  "description": "List of columns and their data types.",
                  "items": {
                    "type": "object",
                    "properties": {
                      "name": {
                        "type": "string",
                        "description": "The name of the column."
                      },
                      "type": {
                        "type": "string",
                        "enum": [
                          "string",
                          "number",
                          "boolean",
                          "date",
                          "timestamp",
                          "json"
                        ],
                        "description": "Data type of the column."
                      }
                    },
                    "required": [
                      "name",
                      "type"
                    ]
                  }
                }
              },
              "required": [
                "columns"
              ]
            },
            "source": {
              "type": "object",
              "description": "Source configuration for read steps.",
              "properties": {
                "type": {
                  "type": "string",
                  "enum": [
                    "csv",
                    "json",
                    "database"
                  ],
                  "description": "Type of the source data."
                },
                "filepath": {
                  "type": "string",
                  "description": "Path to the source file or database connection string."
                },
                "separator": {
                  "type": "string",
                  "maxLength": 1,
                  "description": "Delimiter used in CSV files."
                },
                "columns": {
                  "type": "array",
                  "description": "List of columns for a database source (defines the schema).",
                  "items": {
                    "type": "object",
                    "properties": {
                      "name": {
                        "type": "string",
                        "description": "Column name."
                      },
                      "data_type": {
                        "type": "string",
                        "enum": [
                          "string",
                          "number",
                          "boolean",
                          "date",
                          "timestamp",
                          "json"
                        ],
                        "description": "Data type of the column."
                      }
                    },
                    "required": [
                      "name",
                      "data_type"
                    ]
                  }
                }
              },
              "required": [
                "type",
                "filepath"
              ],
              "if": {
                "properties": {
                  "type": {
                    "const": "database"
                  }
                }
              },
              "then": {
                "required": [
                  "columns"
                ]
              }
            },
            "filter": {
              "type": "object",
              "description": "Filter configuration to apply conditions on data.",
              "properties": {
                "column": {
                  "type": "string",
                  "description": "Column on which the filter condition is applied."
                },
                "condition": {
                  "type": "string",
                  "enum": [
                    ">",
                    "<",
                    "==",
                    "!=",
                    ">=",
                    "<="
                  ],
                  "description": "Comparison operator for filtering."
                },
                "value": {
                  "type": [
                    "string",
                    "number"
                  ],
                  "description": "Value to compare the column against."
                }
              },
              "required": [
                "column",
                "condition",
                "value"
              ]
            },
            "split": {
              "type": "object",
              "description": "Split configuration to branch the pipeline.",
              "properties": {
                "parallel": {
                  "type": "boolean",
                  "description": "If branches should run in parallel."
                },
                "branches": {
                  "type": "array",
                  "description": "Branches in the split component.",
                  "items": {
                    "type": "object",
                    "properties": {
                      "name": {
                        "type": "string",
                        "description": "Name of the branch."
                      },
                      "steps": {
                        "type": "array",
                        "description": "List of steps within this branch.",
                        "items": {
                          "type": "object"
                        }
                      }
                    },
                    "required": [
                      "name",
                      "steps"
                    ]
                  }
                }
              },
              "required": [
                "parallel",
                "branches"
              ]
            },
            "group": {
              "type": "object",
              "description": "Group configuration to aggregate data.",
              "properties": {
                "column": {
                  "type": "string",
                  "description": "Column to group by."
                },
                "aggregation": {
                  "type": "array",
                  "description": "List of aggregation operations.",
                  "items": {
                    "type": "object",
                    "properties": {
                      "column": {
                        "type": "string",
                        "description": "Column on which to perform the aggregation."
                      },
                      "function": {
                        "type": "string",
                        "enum": [
                          "sum",
                          "mean",
                          "count",
                          "max",
                          "min"
                        ],
                        "description": "Aggregation function to apply."
                      }
                    },
                    "required": [
                      "column",
                      "function"
                    ]
                  }
                }
              },
              "required": [
                "column",
                "aggregation"
              ]
            },
            "join": {
              "type": "object",
              "description": "Join configuration to merge data from different components.",
              "properties": {
                "with": {
                  "type": "string",
                  "description": "Identifier of the component to join with."
                },
                "on": {
                  "type": "string",
                  "description": "Column used for joining data."
                }
              },
              "required": [
                "with",
                "on"
              ]
            },
            "write": {
              "type": "object",
              "description": "Write configuration for output data.",
              "properties": {
                "concurrent_write": {
                  "type": "boolean",
                  "description": "Indicates if data should be written concurrently."
                },
                "target": {
                  "type": "array",
                  "description": "List of target configurations for writing data.",
                  "items": {
                    "type": "object",
                    "properties": {
                      "type": {
                        "type": "string",
                        "enum": [
                          "csv",
                          "json"
                        ],
                        "description": "Type of the output target."
                      },
                      "filepath": {
                        "type": "string",
                        "description": "Path to the output file."
                      },
                      "separator": {
                        "type": "string",
                        "maxLength": 1,
                        "description": "Delimiter used in CSV output files."
                      }
                    },
                    "required": [
                      "type",
                      "filepath"
                    ]
                  }
                }
              },
              "required": [
                "concurrent_write",
                "target"
              ]
            },
            "hook": {
              "type": "object",
              "description": "Hook configuration for integrating third-party services for data quality checks or external validations.",
              "properties": {
                "url": {
                  "type": "string",
                  "description": "Endpoint URL for the hook call."
                },
                "method": {
                  "type": "string",
                  "enum": [
                    "GET",
                    "POST",
                    "PUT",
                    "DELETE"
                  ],
                  "description": "HTTP method used to call the hook service."
                },
                "headers": {
                  "type": "object",
                  "additionalProperties": {
                    "type": "string"
                  },
                  "description": "HTTP headers to include in the hook request."
                },
                "payload": {
                  "type": "object",
                  "description": "Optional payload for POST or PUT requests."
                },
                "timeout": {
                  "type": "integer",
                  "description": "Timeout in seconds for the hook request."
                }
              },
              "required": [
                "url",
                "method"
              ]
            },
            "custom": {
              "type": "object",
              "description": "Custom component configuration using a Jinja2 template for user-defined processing.",
              "properties": {
                "template": {
                  "type": "string",
                  "description": "A Jinja2 template used to process data."
                }
              },
              "required": [
                "template"
              ]
            }
          },
          "required": [
            "component_id",
            "step"
          ]
        }
      }
    },
    "required": [
      "pipeline_id",
      "pipeline_description",
      "execution_mode",
      "threads",
      "batch_size",
      "incremental",
      "last_processed_timestamp",
      "bulk_processing",
      "steps"
    ]
}