import subprocess
import json

def generate_fake_data(schema_path):
    try:
        result = subprocess.run(
            ["node", "./scripts/generateFakeData.js", schema_path],
            check=True,
            capture_output=True,
            text=True
        )
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Node.js script failed: {e.stderr}")
    except json.JSONDecodeError as e:
        raise ValueError("Invalid JSON returned by Node.js script")

