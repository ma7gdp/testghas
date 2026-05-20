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


def code_contains_decrypt(result):
    """Check if the actual source code at the result location contains 'decrypt'."""
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
        
        # Read the file and check if 'decrypt' appears in the range
        lines = read_file_lines(file_path)
        if lines:
            # Convert 1-indexed line numbers to 0-indexed
            relevant_lines = lines[start_line - 1 : end_line]
            code_snippet = "".join(relevant_lines)
            if "decrypt" in code_snippet.lower():
                return True
    
    return False


def should_remove_result(result):
    if not isinstance(result, dict):
        return False

    rule_id = result.get("ruleId")
    if rule_id != "py/weak-cryptographic-algorithm":
        return False

    # Check if the actual source code contains 'decrypt'
    return code_contains_decrypt(result)


def filter_sarif(data):
    if not isinstance(data, dict) or "runs" not in data:
        return data, 0

    removed = 0
    for run in data.get("runs", []):
        results = run.get("results")
        if not isinstance(results, list):
            continue

        filtered = []
        for result in results:
            if should_remove_result(result):
                removed += 1
                continue
            filtered.append(result)

        run["results"] = filtered

    return data, removed


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

    sarif_files = find_sarif_files(input_path)
    if len(sarif_files) != 1:
        raise ValueError(
            "This filter currently supports exactly one SARIF file. "
            f"Found {len(sarif_files)}: {sarif_files}"
        )

    sarif_file = sarif_files[0]
    data = load_sarif(sarif_file)
    filtered_data, removed = filter_sarif(data)
    save_sarif(filtered_data, output_path)

    print(f"Filtered SARIF file: {sarif_file}")
    print(f"Wrote filtered SARIF to: {output_path}")
    print(f"Removed {removed} py/weak-cryptographic-algorithm result(s) from code containing 'decrypt'.")


if __name__ == "__main__":
    main()
