import requests
import json

class CMSDataHandler:
    def __init__(self, dataset_id):
        self.dataset_id = dataset_id
        self.data = None
    
    def fetch_data(self):
        """Fetch JSON data from CMS API."""
        url = f"https://data.cms.gov/provider-data/api/v1/dataset/{self.dataset_id}/items"
        response = requests.get(url)
        if response.status_code == 200:
            self.data = response.json()
            return self.data
        else:
            print(f"Error: {response.status_code}")
            return None

    def save_data(self, filename="data.json"):
        """Save JSON data to a file."""
        if self.data:
            with open(filename, "w") as f:
                json.dump(self.data, f, indent=2)
            print(f"Data saved to {filename}")

    def load_data(self, filename="data.json"):
        """Load JSON data from a file."""
        with open(filename, "r") as f:
            self.data = json.load(f)
        print("Data loaded successfully.")

    def filter_data(self, key, value):
        """Filter data by a key-value pair."""
        if not self.data:
            print("No data loaded.")
            return []
        
        return [entry for entry in self.data if entry.get(key) == value]

    def perform_action(self, action_type):
        """Dynamically perform an action based on user-defined choice."""
        if action_type == "filter":
            key = input("Enter the key to filter by: ")
            value = input("Enter the value to match: ")
            filtered = self.filter_data(key, value)
            print(json.dumps(filtered, indent=2))
        elif action_type == "summary":
            self.print_summary()
        elif action_type == "save":
            self.save_data()
        else:
            print("Unknown action.")

    def print_summary(self):
        """Provide a summary of the dataset."""
        if not self.data:
            print("No data available.")
            return
        
        total_entries = len(self.data)
        sample_entry = self.data[0] if total_entries > 0 else {}
        print(f"Total entries: {total_entries}")
        print("Sample Entry Keys:", list(sample_entry.keys()))

# Example usage
handler = CMSDataHandler("your_dataset_id_here")
handler.fetch_data()
handler.perform_action("summary")  # This allows ambiguity by letting the user define the action

# For further detail visit the CMS API reference at:
#https://data.cms.gov/provider-data/docs
