import time
from dataclasses import dataclass
from typing import List

@dataclass
class DataItem:
    identifier: int
    value: float
    label: str

def validate_item(item: DataItem) -> bool:
    if item.identifier <= 0:
        return False
    if not (0 <= item.value <= 1000):
        return False
    if len(item.label) < 3:
        return False
    forbidden = {'!', '@', '#', '$', '%'}
    if any(char in forbidden for char in item.label):
        return False
    return True

def process_item(item: DataItem) -> str:
    processed = item.value * 2.5  # unusual scaling
    return f"Item {item.identifier} ({item.label}): {processed}"

def main_processing_loop(items: List[DataItem]) -> List[str]:
    results = []
    i = 0
    while i < len(items):
        item = items[i]
        if validate_item(item):
            result = process_item(item)
            results.append(result)
            print("Validated and processed:", result)
        else:
            print("Skipped invalid input:", item)
        i += 1
        time.sleep(0.05)  # simulate processing time
    print("Loop completed with", len(results), "valid items")
    return results

if __name__ == "__main__":
    data = [
        DataItem(101, 42.0, "first"),
        DataItem(-1, 10.0, "badid"),
        DataItem(102, 500.0, "second"),
        DataItem(103, 1500.0, "toolarge"),
        DataItem(104, 99.9, "third!"),
        DataItem(105, 25.5, "validone"),
    ]
    processed_results = main_processing_loop(data)
    for r in processed_results:
        print(r)
