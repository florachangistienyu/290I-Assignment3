from fastapi import FastAPI, File, UploadFile
from typing_extensions import Annotated
import uvicorn
from utils import *
from dijkstra import dijkstra

# create FastAPI app
app = FastAPI()

# global variable for active graph
active_graph = None

@app.get("/")
async def root():
    return {"message": "Welcome to the Shortest Path Solver!"}


@app.post("/upload_graph_json/")
async def create_upload_file(file: UploadFile):
    if not file.filename.endswith(".json"):
        return {"Upload Error": "Invalid file type"}

    try:
        # create the graph using the helper function
        graph = create_graph_from_json(file)

        # store graph to global variable for later shortest path use
        global active_graph
        active_graph = graph

        return {"Upload Success": file.filename}
    except Exception as e:
        return {"Upload Error": str(e)}


@app.get("/solve_shortest_path/start_node_id={start_node_id}&end_node_id={end_node_id}")
async def get_shortest_path(start_node_id: str, end_node_id: str):
        # check if a graph has been uploaded
    global active_graph
    if 'active_graph' not in globals() or active_graph is None:
        return {"Solver Error": "No active graph, please upload a graph first."}

    graph = active_graph

    # check if start and end node IDs exist
    if start_node_id not in graph.nodes or end_node_id not in graph.nodes:
        return {"Solver Error": "Invalid start or end node ID."}

    # run Dijkstra's algorithm
    start_node = graph.nodes[start_node_id]
    end_node = graph.nodes[end_node_id]
    dijkstra(graph, start_node)

    # reconstruct shortest path
    path = []
    current = end_node
    if np.isinf(end_node.dist):
        path = None
        total_distance = None
    else:
        while current:
            path.insert(0, current.id)
            current = current.prev
        total_distance = end_node.dist

    return {
        "shortest_path": path,
        "total_distance": total_distance
    }


if __name__ == "__main__":
    print("Server is running at http://localhost:8080")
    uvicorn.run(app, host="0.0.0.0", port=8080)
    