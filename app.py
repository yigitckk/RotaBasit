# This is the NEW app.py

from flask import Flask, render_template, jsonify, request
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

app = Flask(__name__)

# --- 1. Master Data (Our "Database") ---
# This data is now our permanent, master list.
# We will filter from this.
MASTER_LOCATION_DATA = {
    'Depot (Giriş)': [37.7744, 29.0929],  # Denizli center
    'Adres A': [37.7795, 29.0950],  # Near Pamukkale Univ. Hospital
    'Adres B': [37.7818, 29.0838],  # Near Servergazi
    'Adres C': [37.7681, 29.0886],  # Near Bus Station (Otogar)
    'Adres D': [37.7750, 29.1050]  # Near Çamlık
}
MASTER_LOCATION_NAMES = list(MASTER_LOCATION_DATA.keys())

MASTER_DISTANCE_MATRIX = [
    [0, 548, 776, 696, 582],  # Depot (0)
    [548, 0, 684, 801, 864],  # Adres A (1)
    [776, 684, 0, 992, 114],  # Adres B (2)
    [696, 801, 992, 0, 794],  # Adres C (3)
    [582, 864, 114, 794, 0],  # Adres D (4)
]


# --- 2. NEW: The Dynamic Data Model Builder ---
def create_dynamic_data_model(selected_location_names):
    """
    Creates a new, smaller data model based on the user's selected locations.
    """
    # 1. Get the *indices* of the selected locations from the master list
    selected_indices = [MASTER_LOCATION_NAMES.index(name) for name in selected_location_names]

    # 2. Build the new, smaller distance matrix
    new_distance_matrix = []
    for from_index in selected_indices:
        row = []
        for to_index in selected_indices:
            row.append(MASTER_DISTANCE_MATRIX[from_index][to_index])
        new_distance_matrix.append(row)

    # 3. Get the new (filtered) location names and coords
    new_location_names = selected_location_names
    new_location_coords = {name: MASTER_LOCATION_DATA[name] for name in new_location_names}

    # 4. Create the final data object for the solver
    data = {}
    data['distance_matrix'] = new_distance_matrix
    data['location_names'] = new_location_names
    data['location_coords'] = new_location_coords
    data['num_vehicles'] = 1
    # The depot is *always* the first item in the new list (index 0)
    data['depot'] = 0

    return data


# --- 3. The Routes ---
@app.route('/')
def home():
    """
    Renders the main HTML page.
    NEW: We pass the list of 'Adres A', 'B', 'C', 'D' to the
    HTML to create the checkboxes.
    """
    # Get all names *except* the Depot for the checkboxes
    address_names = [name for name in MASTER_LOCATION_NAMES if name != 'Depot (Giriş)']
    return render_template('index.html', address_names=address_names)


@app.route('/solve', methods=['POST'])
def solve():
    """
    Runs the VRP solver on a DYNAMICALLY built data model.
    """
    # --- 1. NEW: Get the selected locations from the JavaScript ---
    try:
        # Get the JSON data sent from the frontend
        post_data = request.get_json()
        selected_names_from_user = post_data['locations']

        # Create the full list, with 'Depot' always at the start
        # This is critical for the solver
        locations_for_solver = ['Depot (Giriş)'] + selected_names_from_user

        # If user selected no addresses, just return the depot
        if len(locations_for_solver) <= 1:
            depot_name = 'Depot (Giriş)'
            depot_coords = MASTER_LOCATION_DATA[depot_name]
            return jsonify({
                'status': 'success',
                'route': [{'name': depot_name, 'coords': depot_coords}]
            })

        # --- 2. NEW: Build the dynamic data model ---
        data = create_dynamic_data_model(locations_for_solver)

    except Exception as e:
        print(e)
        return jsonify({'status': 'error', 'message': 'Hatalı veri. Lütfen en az bir adres seçin.'})

    # --- 3. Setup the OR-Tools Routing Model (Same as before) ---
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'], data['depot'])
    routing = pywrapcp.RoutingModel(manager)

    # --- 4. Define the "Cost" (Distance) (Same as before) ---
    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterUnaryTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # --- 5. Set Search Parameters (Same as before) ---
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # --- 6. Solve the Problem! (Same as before) ---
    solution = routing.SolveWithParameters(search_parameters)

    # --- 7. Package the Solution (Same as before) ---
    if solution:
        route_result_with_coords = []
        index = routing.Start(0)

        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            # Use the DYNAMIC list of names
            location_name = data['location_names'][node_index]
            location_coords = data['location_coords'][location_name]

            route_result_with_coords.append({
                'name': location_name,
                'coords': location_coords
            })
            index = solution.Value(routing.NextVar(index))

        # Add the final depot stop
        depot_name = data['location_names'][data['depot']]
        depot_coords = data['location_coords'][depot_name]
        route_result_with_coords.append({
            'name': depot_name,
            'coords': depot_coords
        })

        return jsonify({'status': 'success', 'route': route_result_with_coords})
    else:
        return jsonify({'status': 'error', 'message': 'No solution found!'})


if __name__ == '__main__':
    app.run(debug=True)