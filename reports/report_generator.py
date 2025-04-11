import json

def generate_report(analysed_data, save_path="team_morale_report.json"):
    with open(save_path, "w") as f:
        json.dump(analysed_data, f, indent=2)
    print(f"✅ Report saved to {save_path}")