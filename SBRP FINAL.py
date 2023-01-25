 #@CSBRP ()
"""School Bus Routing Problem (SBRP)."""
#importing tools used in the code#
!pip install ortools
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import pandas as pd
import numpy as np
import csv

#import the duration csv file into an array
reader = csv.reader(open("/Users/stellenshun.li/Desktop/12th Grade/AP Research/Paper/Codes/Duration.csv", "r"), delimiter=",")
x = list(reader)
result = np.array(x).astype("float")

#store the data for this problem#
def create_data_model():
    data = {}
    data['distance_matrix'] = result
        #All stops:Hua, AC1, AC2, AC3, AC4, skl, YG, ACb, OV, DH, WY, HL, HT, TJY, OT, IB, TC, JLQ, HZL, LW, HY, LSY, SL, BD, MQ, KME
        #AC is divided into AC1-AC4 because AC has more than 100 students. But since the maximum capacity of a bus is at most 49,
        #4 buses are needed to visit AC
    #demands is the number of students at each stop
    data['demands'] = [2, 35, 35, 35, 34, 0, 4, 4, 1, 3, 1, 1, 1, 1, 3, 3, 3, 6, 3, 4, 10, 6, 3, 31, 3, 3]
    #vehicle_capacities has the maximum capacity data for all 9 buses
    data['vehicle_capacities'] = [45, 45, 45, 45, 45, 45, 49, 15, 15] 
    data['num_vehicles'] = 9
    #starting points
    data['starts'] = [0, 6, 7, 11, 12, 13, 16, 24, 25]
    #destination
    data['ends'] = [5, 5, 5, 5, 5, 5, 5, 5, 5]
    return data

#prints solution on console
def print_solution(data, manager, routing, solution):
    total_distance = 0
    total_load = 0
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
        route_distance = 0
        route_load = 0
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            route_load += data['demands'][node_index]
            plan_output += ' Stop {0} Students({1}) -> '.format(node_index, route_load)
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                  previous_index, index, vehicle_id)
        plan_output += 'Stop {}\n'.format(manager.IndexToNode(index))
        plan_output += 'Duration of the route: {} mins\n'.format(route_distance)
        plan_output += 'Number of students of the route: {}\n'.format(route_load)
        print(plan_output)
        total_distance += route_distance
        total_load += route_load
    print('Total duration of all routes: {} mins'.format(total_distance))
    print('Total number of students of all routes: {}'.format(total_load))

#solve the SBRP
def main():
    # Instantiate the data
    data = create_data_model()
    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'], data['starts'],
                                           data['ends'])
    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    # Create and register a transit callback.
    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]
    
    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
  
    #Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
    

    # Add Capacity constraint.
    def demand_callback(from_index):
        """Returns the demand of the node."""
        # Convert from routing variable Index to demands NodeIndex.
        from_node = manager.IndexToNode(from_index)
        return data['demands'][from_node]

    demand_callback_index = routing.RegisterUnaryTransitCallback(
        demand_callback)
    
    dimension_name = 'Capacity'
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,  # null capacity slack
        data['vehicle_capacities'],  # vehicle maximum capacities
        True,  # start cumul to zero
        dimension_name)
    # Add Distance constraint.
    dimension_name = 'Distance'
    routing.AddDimension(
        transit_callback_index,
        0,  # no slack
        100,  # minimize vehicle maximum travel duration
        True,  # start cumul to zero
        dimension_name)
    distance_dimension = routing.GetDimensionOrDie(dimension_name)
    distance_dimension.SetGlobalSpanCostCoefficient(100)

    # Setting first solution heuristic.
    for v in range(manager.GetNumberOfVehicles()):
          routing.ConsiderEmptyRouteCostsForVehicle(True, v)
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
    search_parameters.log_search = True
    search_parameters.time_limit.FromSeconds(5)

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution.
    if solution:
        print_solution(data, manager, routing, solution)
    else:
        print('no solution')

if __name__ == '__main__':
    main()
    data = create_data_model()
