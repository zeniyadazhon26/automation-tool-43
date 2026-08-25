[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# automation-tool-43

automation-tool-43 is a Python command-line tool for orchestrating multi-step automation workflows. It allows users to define and execute sequences of tasks using simple configuration files without writing custom scripts for each job.

## Features
- Define workflows in YAML with support for shell commands, HTTP requests, and file operations
- Built-in error handling, retries, and conditional step execution
- Automatic logging with timestamps and structured output for every run
- Cron-style scheduling for recurring tasks directly from the configuration

## Installation

```bash
git clone https://github.com/Developer/automation-tool-43.git
cd automation-tool-43
pip install -e .
```

## Usage

Create a `workflow.yaml` file:

```yaml
name: daily_data_sync
steps:
  - name: fetch_data
    type: http
    url: https://api.example.com/export
    method: GET
  - name: process_files
    type: shell
    command: python process.py
```

Run the workflow:

```bash
automation-tool-43 execute workflow.yaml
```