import json
import sys
from graph import generate_graph, print_ownership_structure

source = 'A.P. MØLLER OG HUSTRU CHASTINE MC-KINNEY MØLLERS FOND TIL ALMENE FORMAAL'
file = 'data/CasaAS.json'

try:
    with open(file, 'r') as f:
        graph = generate_graph(json.load(f))
        print_ownership_structure(graph, source)
except FileNotFoundError:
    print(f"File not found {file}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Invalid JSON format in {file}")
    sys.exit(1)
except Exception as e:
    print(f"An error occurred while reading {file}: {str(e)}")
    sys.exit(1)
