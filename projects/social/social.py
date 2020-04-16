from random import shuffle
from collections import deque

class User:
    def __init__(self, name):
        self.name = name

class SocialGraph:
    def __init__(self):
        self.last_id = 0
        self.users = {}
        self.friendships = {}

    def add_friendship(self, user_id, friend_id):
        """
        Creates a bi-directional friendship
        """
        if user_id == friend_id:
            print("WARNING: You cannot be friends with yourself")
        elif friend_id in self.friendships[user_id] or user_id in self.friendships[friend_id]:
            print("WARNING: Friendship already exists")
        else:
            self.friendships[user_id].add(friend_id)
            self.friendships[friend_id].add(user_id)

    def add_user(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.last_id += 1  # automatically increment the ID to assign the new user
        self.users[self.last_id] = User(name)
        self.friendships[self.last_id] = set()

    def populate_graph(self, num_users, avg_friendships):
        """
        Takes a number of users and an average number of friendships
        as arguments

        Creates that number of users and a randomly distributed friendships
        between those users.

        The number of users must be greater than the average number of friendships.
        """
        # Reset graph
        self.last_id = 0
        self.users = {}
        self.friendships = {}
        # !!!! IMPLEMENT ME
        # Add users
        for user_id in range(1, num_users + 1):
            self.add_user(f'user_{user_id}')
        # Create friendships
        friendships = []
        for user in range(1, self.last_id + 1):
            for friend in range(user + 1, num_users):
                friendships.append((user, friend))
        shuffle(friendships)
        total_friendships = num_users * avg_friendships
        pairs_needed = total_friendships // 2
        random_friendships = friendships[:pairs_needed]
        for user_id, friend_id in random_friendships:
            self.add_friendship(user_id, friend_id)

    def get_all_social_paths(self, user_id):
        """
        Takes a user's user_id as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.
        """
        visited = {}  # Note that this is a dictionary, not a set
        # !!!! IMPLEMENT ME
        queue = deque()
        queue.append([user_id])
        while len(queue) > 0:
            current_path = queue.popleft()
            current_user_id = current_path[-1]
            
            if current_user_id not in visited:
                visited[current_user_id] = current_path
                friend_ids = self.friendships[current_user_id]
                for friend_id in friend_ids:
                    queue.append(current_path + [friend_id])

        return visited


if __name__ == '__main__':
    sg = SocialGraph()
    sg.populate_graph(1000, 5)
    print(sg.friendships)
    connections = sg.get_all_social_paths(1)
    print(connections)
    percentage_of_users_in_network = len(connections) / len(sg.users) * 100
    print(f"{percentage_of_users_in_network}% of users are in 1's network.")
    total_degree_of_separation = 0
    for connection in connections:
        total_degree_of_separation += len(connections[connection]) - 1
    print(f'Average degree of separation: {total_degree_of_separation / len(connections)}')
