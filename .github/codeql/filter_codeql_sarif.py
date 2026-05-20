#!/usr/bin/env python3
import json
import os
import sys
from glob import glob


def load_sarif(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_sarif(data, path):
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


def read_file_lines(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.readlines()
    except Exception:
        return []


def code_contains_snippet(result, needle):
    """Check if the actual source code at the result location contains a string."""
    locations = result.get("locations", [])
    if not isinstance(locations, list):
        return False
    
    for location in locations:
        if not isinstance(location, dict):
            continue
        
        physical = location.get("physicalLocation", {})
        if not isinstance(physical, dict):
            continue
        
        artifact = physical.get("artifactLocation", {})
        if not isinstance(artifact, dict):
            continue
        
        file_path = artifact.get("uri")
        if not file_path:
            continue
        
        region = physical.get("region", {})
        if not isinstance(region, dict):
            continue
        
        start_line = region.get("startLine", 1)
        end_line = region.get("endLine", start_line)
        
        # Read the file and check if the configured snippet appears in the range
        lines = read_file_lines(file_path)
        if lines:
            # Convert 1-indexed line numbers to 0-indexed
            relevant_lines = lines[start_line - 1 : end_line]
            code_snippet = "".join(relevant_lines)
            if needle.lower() in code_snippet.lower():
                return True
    
    return False


def load_filter_config(path):
    if not os.path.isfile(path):
        return []

    try:
        with open(path, "r", encoding="utf-8") as f:
            config = json.load(f)
    except Exception as exc:
        print(f"Warning: failed to load filter config {path}: {exc}", file=sys.stderr)
        return []

    if not isinstance(config, list):
        print(f"Warning: filter config {path} must be a list of objects", file=sys.stderr)
        return []

    filters = []
    for item in config:
        if not isinstance(item, dict):
            continue
        rule_id = item.get("rule_id")
        needle = item.get("needle")
        if isinstance(rule_id, str) and isinstance(needle, str):
            filters.append({"rule_id": rule_id, "needle": needle})

    return filters


def should_adjust_result(result, filters):
    if not isinstance(result, dict):
        return False

    result_rule_id = result.get("ruleId")
    if not isinstance(result_rule_id, str):
        return False

    for filter_item in filters:
        rule_id = filter_item.get("rule_id")
        needle = filter_item.get("needle")
        if not isinstance(rule_id, str) or not isinstance(needle, str):
            continue
        if result_rule_id != rule_id:
            continue

        # Check if the actual source code contains the configured snippet
        if code_contains_snippet(result, needle):
            return True

    return False


def set_result_severity_low(result):
    if not isinstance(result, dict):
        return

    result["level"] = "note"
    if "properties" not in result or not isinstance(result.get("properties"), dict):
        result["properties"] = {}

    result["properties"]["problem.severity"] = "low"


def filter_sarif(data, filters):
    if not isinstance(data, dict) or "runs" not in data:
        return data, 0

    adjusted = 0
    for run in data.get("runs", []):
        results = run.get("results")
        if not isinstance(results, list):
            continue

        for result in results:
            if should_adjust_result(result, filters):
                set_result_severity_low(result)
                adjusted += 1

    return data, adjusted


def find_sarif_files(path):
    if os.path.isdir(path):
        candidates = glob(os.path.join(path, "*.sarif"))
        if not candidates:
            raise FileNotFoundError(f"No SARIF files found under directory: {path}")
        return sorted(candidates)
    if os.path.isfile(path):
        return [path]
    raise FileNotFoundError(f"Input path does not exist: {path}")


def main():
    if len(sys.argv) != 3:
        print("Usage: filter_codeql_sarif.py <input-sarif-file-or-dir> <output-sarif-file>")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]
    config_path = sys.argv[3] if len(sys.argv) == 4 else ".github/codeql/filter_config.json"

    sarif_files = find_sarif_files(input_path)
    if len(sarif_files) != 1:
        raise ValueError(
            "This filter currently supports exactly one SARIF file. "
            f"Found {len(sarif_files)}: {sarif_files}"
        )

    filters = load_filter_config(config_path)
    if not filters:
        print(f"Warning: no valid filters loaded from {config_path}. No results will be removed.", file=sys.stderr)

    sarif_file = sarif_files[0]
    data = load_sarif(sarif_file)
    filtered_data, adjusted = filter_sarif(data, filters)
    save_sarif(filtered_data, output_path)

    print(f"Filtered SARIF file: {sarif_file}")
    print(f"Wrote filtered SARIF to: {output_path}")
    print(f"Adjusted severity for {adjusted} result(s) using filters from {config_path}.")


if __name__ == "__main__":
    main()
