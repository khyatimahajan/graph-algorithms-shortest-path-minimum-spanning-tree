import numpy as np
import heapq
from collections import defaultdict
from pprint import pprint

def read_input(textfile):
	''' Helper function to read input from text file'''
	init_graph = []
	with open(textfile, 'r') as rd:
		for line in rd:
			init_graph.append(line.split())
	return init_graph

def gather_info(graph):
	''' Helper function to extract information about graph '''
	source = 'dummy'
	v, u, gtype = graph[0]
	v = int(v)
	u = int(u)
	if (len(graph[-1]) == 1):
		source = graph[-1][0]
	return [v, u, gtype, source]

def build_graph(graph):
	''' Stores information about graph in adjacency list format '''
	v, u, gtype, source = gather_info(graph)

	adjacency_list = {}
	for i in range(1, u + 1):
		a, b, c = graph[i]
		if a not in adjacency_list.keys():
			adjacency_list[a] = {b: int(c)}
		else:
			adjacency_list[a].update({b: int(c)})
		if b not in adjacency_list.keys():
			adjacency_list[b] = {}
	
	# if the graph is undirected add the edges in the reverse order as well
	if gtype == 'U':
		for i in range(1, u + 1):
			a, b, c, = graph[i]
			adjacency_list[b].update({a: int(c)})

	return adjacency_list, source

def shortest_path_djikstra(adjacency_list, source):
	''' Shortest path according to Djikstra's algorithm '''
	shortest_path = {}

	# initialize all vertices distances and set the source to 0
	for vertex in adjacency_list.keys():
		shortest_path[vertex] = {'distance': np.inf, 'parent': ''}
	shortest_path[source] = {'distance': 0, 'parent': '-'}
	
	# maintain a lookup for updating distances
	entry_lookup = {}
	# priority queue for shortest path to vertex
	priority_queue = []

	# initialize heap with priority queue
	for vertex, info in shortest_path.items():
		entry = [info['distance'], vertex]
		entry_lookup[vertex] = entry
		heapq.heappush(priority_queue, entry)

	# run till the heap is not empty
	while len(priority_queue) > 0:
		# get the minimum distance vertex
		current_distance, current_vertex = heapq.heappop(priority_queue)
		# update distances to all neighbors of the current minimum distance vertex
		for neighbor_vertex, neighbor_distance in adjacency_list[current_vertex].items():
			distance = shortest_path[current_vertex]['distance'] + neighbor_distance
			# if distance of neighbors is lesser than current distance of neighbors, update distances
			# and add neighbor vertex to queue
			if distance < shortest_path[neighbor_vertex]['distance']:
				shortest_path[neighbor_vertex]['distance'] = distance
				shortest_path[neighbor_vertex]['parent'] = current_vertex
				entry_lookup[neighbor_vertex][0] = distance
				heapq.heappush(priority_queue, [distance, neighbor_vertex])

	return shortest_path

def minimum_spanning_tree_prim(adjacency_list, source):
	''' Minimum Spanning Tree according to Prim's algorithm '''
	minimum_spanning_tree = defaultdict(set)

	# initialize all edges in the graph
	visited = set([source])
	edges = [(cost, source, to) for to, cost in adjacency_list[source].items()]
	# heapify edges to get the shortest edge distances
	heapq.heapify(edges)

	# run till all edges are traversed
	while edges:
		print(edges)
		# get minimum weight edge
		cost, parent, to = heapq.heappop(edges)
		# if the other end vertex is has not been visited yet, visit it
		if to not in visited:
			visited.add(to)
			# update MST to include the minimum weight edge
			minimum_spanning_tree[parent].add((cost, to))
			# heapify the neighbors of the recently visited neighbor node
			for to_next, cost in adjacency_list[to].items():
				# if the other end vertex is has not been visited yet, add neighbours to heap
				if to_next not in visited:
					heapq.heappush(edges, (cost, to, to_next))

	return minimum_spanning_tree

def choose_graph(chosen):
	graphs = {	'1': 'sample_graph.txt',
				'2': 'test_graph_undirected_1.txt',
				'3': 'test_graph_undirected_2.txt',
				'4': 'test_graph_undirected_3.txt',
				'5': 'test_graph_directed_1.txt',
				'6': 'test_graph_directed_2.txt',
				'7': 'test_graph_directed_3.txt'}
	if len(chosen) == 1:
		graph = read_input(graphs[chosen])
	else:
		graph = read_input(chosen)
	return graph, graphs[chosen]

chosen = input("Choose a graph to run by choosing a number between 1 to 7. If you would like to enter another text file, enter the name of the text file here:\n")
graph, chosen_graph = choose_graph(chosen)
print("\nThe chosen graph is: ", chosen_graph)
adjacency_list, source = build_graph(graph)

print("\nAdjacency list representation of graph:")
pprint(adjacency_list)

if (source == 'dummy'):
	print("Error: Source node not provided for single source shortest path. Choosing a vertex as the source instead.")
	source = list(adjacency_list.keys())[0]

print("\nSource: ", source)
print()

x = shortest_path_djikstra(adjacency_list, source)
print('Shortest path:')
for key in sorted(x):
	print(key, ':', x[key])
print()

y = minimum_spanning_tree_prim(adjacency_list, source)
total_cost = 0
print('MST:')
for key in sorted(y):
	print(key, ':', y[key])
	for element in y[key]:
		total_cost += element[0]
print('Total cost: ', total_cost)