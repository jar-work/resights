from fastapi import FastAPI, Request, HTTPException
import json
from graph import generate_graph, get_ownership_structure, Direction

app = FastAPI()

@app.get("/ownership")
async def get_ownership(request: Request):
    params = dict(request.query_params)
    company = params["company"]
    file = 'data/' + company + '.json'
    from_ = params["from"] if "from" in params else None
    to = params["to"] if "to" in params else None

    result = { }

    try:
        with open(file, 'r') as f:
            graph = generate_graph(json.load(f))
            if from_:
                result[f"Ownership structure from {from_} to {company}"] = list(get_ownership_structure(graph, from_, Direction.FROM))
            if to:
                result[f"Ownership structure from {company} to {to}"] = list(get_ownership_structure(graph, to, Direction.TO))

            return result
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"File not found: {file}")
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail=f"Invalid JSON format in file: {file}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while processing the request: {str(e)}")

