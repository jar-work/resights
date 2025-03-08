import json
import sys
from graph import generate_graph

if len(sys.argv) < 2:
    print("Usage: python main.py <company>")
    sys.exit(1)

companyFullName = ' '.join(sys.argv[1:])
company = ''.join(sys.argv[1:])
file = 'data/' + company + '.json'

try:
    with open(file, 'r') as f:
        graph = generate_graph(json.load(f))
except FileNotFoundError:
    print(f"File not found {file}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Invalid JSON format in {file}")
    sys.exit(1)
except Exception as e:
    print(f"An error occurred while reading {file}: {str(e)}")
    sys.exit(1)
