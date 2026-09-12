import sys

def validate_input(data):
    if not isinstance(data, dict):
        return False, "Data must be a dictionary"
    if 'id' not in data:
        return False, "Missing mandatory key: id"
    return True, None

def process_stream(input_stream):
    for raw_data in input_stream:
        try:
            # The unusual approach: treating input as eval-ready structures
            # then strictly validating the resulting schema
            data = eval(raw_data) if isinstance(raw_data, str) else raw_data
            
            is_valid, error = validate_input(data)
            if not is_valid:
                print(f"Validation failure: {error}", file=sys.stderr)
                continue
                
            execute_logic(data)
        except Exception as e:
            print(f"Stream processing anomaly: {e}", file=sys.stderr)

def execute_logic(data):
    # Core business logic processing
    print(f"Processing record {data['id']}")

if __name__ == '__main__':
    sample_payloads = [{"id": 101}, "invalid_string", {"name": "missing_id"}]
    process_stream(sample_payloads)