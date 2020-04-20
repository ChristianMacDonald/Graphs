from room import Room
from player import Player
from world import World

import random
from ast import literal_eval
from collections import deque

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

def reverse(direction):
    if direction == 'n':
        return 's'
    elif direction == 's':
        return 'n'
    elif direction == 'e':
        return 'w'
    elif direction == 'w':
        return 'e'
    else:
        raise ValueError

class TraversalGraph(dict):
    def add_room(self, room_id, room_exits):
        if room_id not in self:
            self[room_id] = {}
            for room_exit in room_exits:
                self[room_id][room_exit] = '?'
    
    def add_connection(self, first_room_id, second_room_id, direction):
        self[first_room_id][direction] = second_room_id
        self[second_room_id][reverse(direction)] = first_room_id
    
    def get_unexplored_exits(self, room_id):
        connections = self[room_id]
        return [direction for direction in connections if connections[direction] == '?']

def find_traversal_path(player):
    graph = TraversalGraph()
    path = []
    last_room = None
    
    while True:
        if player.current_room.id not in graph:
            graph.add_room(player.current_room.id, player.current_room.get_exits())

        if last_room:
            graph.add_connection(last_room.id, player.current_room.id, path[-1])

        currently_unexplored_exits = graph.get_unexplored_exits(player.current_room.id)

        if currently_unexplored_exits:
            last_room = player.current_room
            chosen_direction = random.choice(currently_unexplored_exits)
            path.append(chosen_direction)
            player.travel(chosen_direction)
        else:
            queue = deque()
            queue.append([('', player.current_room.id)])
            visited = set()
            path_to_unexplored_exit = []

            while len(queue) > 0:
                current_path = queue.popleft()
                current_room_id = current_path[-1][1]
                
                if current_room_id not in visited:
                    visited.add(current_room_id)
                    currently_unexplored_exits = graph.get_unexplored_exits(current_room_id)
                    
                    if currently_unexplored_exits:
                        path_to_unexplored_exit = [path_step[0] for path_step in current_path if path_step[0]]
                        break
                    else:
                        connections = graph[current_room_id]
                        
                        for direction in connections:
                            queue.append(current_path + [(direction, connections[direction])])
            
            if path_to_unexplored_exit:
                for direction in path_to_unexplored_exit:
                    last_room = player.current_room
                    path.append(direction)
                    player.travel(direction)
            else:
                break
    
    return path

traversal_path = find_traversal_path(player)

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
