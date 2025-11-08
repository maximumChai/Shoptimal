import json
import os

class Store:
    def __init__(self, name, aisle_map_file):
        self.name = name
        self.aisle_map_file = aisle_map_file
        self.aisle_map = self.load_aisle_map()

    def load_aisle_map(self):
        if os.path.exists(self.aisle_map_file):
            with open(self.aisle_map_file, "r") as f:
                return json.load(f)
        return {}

    def save_aisle_map(self):
        with open(self.aisle_map_file, "w") as f:
            json.dump(self.aisle_map, f, indent=2)

    def sort_items(self, items):
        sorted_list = []
        for item in items:
            item_lower = item.lower()
            if item_lower not in self.aisle_map:
                aisle = input(f"Enter aisle number for '{item}': ")
                try:
                    aisle_num = int(aisle)
                except ValueError:
                    aisle_num = 999  # Default if invalid input
                self.aisle_map[item_lower] = aisle_num
                self.save_aisle_map()
            sorted_list.append((item, self.aisle_map[item_lower]))
        # Sort by aisle
        sorted_list.sort(key=lambda x: x[1])
        return sorted_list

# Example: using the Store
tesco = Store("Tesco", "tesco_aisles.json")
sainsburys = Store("Sainsburys", "sainsburys_aisles.json")

items = ["milk", "apples", "bread", "pasta", "tea"]
sorted_items = tesco.sort_items(items)

print("Sorted list:")
for item, aisle in sorted_items:
    print(f"{item} (Aisle {aisle})")
