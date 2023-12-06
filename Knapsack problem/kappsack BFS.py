import queue
import timeit

#node class with arguments for the weight, benefit, parent, depth, and included(True / False wether a node is included in
#the solution or not)
class node:
    def __init__(self, weight, benefit, parent, depth, included): # depth also matches the tulpe index of the tuple list items
        self.included = included
        self.benefit = benefit
        self.parent = parent
        self.depth = depth
        self.weight = weight
    def __repr__(self):
        return "node(" + repr(self.benefit) + "," + repr(self.weight) + "," + repr(self.parent) + "," + repr(self.depth) + "," + repr(self.included) + ")"

# create a queue class that inherits from the queue class
# use the __repr__ method to print the queue and debug
class kueue(queue.Queue):
    def __repr__(self):
        return "queue(" + repr(self.queue) + ")"

def read_items_from_file(file_path):
    items = []
    with open(file_path, "r") as file:
        lines = file.readlines() # reads all the lines in the opened file and stores them as a list of strings in the lines variable

        for line in lines[1:]:  # Skip the header line
            _, benefit, weight = line.strip().split() # splits the cleaned-up line into a list of substrings based on whitespace.
            items.append((int(weight), int(benefit))) #dont include the ID

    return items

def knapsack(items, capacity):
    q = kueue()
    root = node(0, 0, None, -1, False)
    q.put(root)
    max_benefit = 0
    best_solution = None

    while not q.empty():
        current = q.get()
        depth = current.depth + 1

        if current.benefit > max_benefit and current.weight <= capacity: # if the current node's benefit is larger than the
            # max benefit and if there is still room in the knapsack
            max_benefit = current.benefit # update the max benefit
            best_solution = current # update the best solution which is stored in the current node

        if depth >= len(items): # if the depth is larger than the number of items in the list
            continue # continue to the next iteration

        # Create a new node including the current item
        new_weight = current.weight + items[depth][0] # the weight of the current item + the weight of the previous item extracted from the tuple list
        new_benefit = current.benefit + items[depth][1] # the benefit of the current item + the benefit of the previous item extracted from the tuple list
        new_node = node(new_weight, new_benefit, current, depth, True) # create a new node with the new weight, benefit, parent, depth and included from the node class
        q.put(new_node) # put the new node in the queue as it is included in the path/solution

        # Create a new node excluding the current item
        new_node = node(current.weight, current.benefit, current, depth, False) # dont add the current item to the solution, the previous item keeps its value
        q.put(new_node) # put the new node in the queue as it is not included in the path/solution

    # Construct the solution
    # Create a list of 0s with the same length as the number of items in the given problem.
    # the solution will be a list of 0s and 1s where 1 means that the item is included in the solution
    solution = [0] * len(items)
    #the best_solution is the leaf node with the highest benefit that fits in the knapsack
    # the while loop will go through the tree from the leaf node to the root node
    # by backtracking the path the algorithm took to find the best solution
    # when the best solution is set to the root node, the loop will stop
    while best_solution is not None:
        # checks if the current node in the path was included in the solution
        # it means that the item at the current depth / level in the tree is included in the solution
        if best_solution.included:
            # in the solution list, the corresponding item at the current depth / level in the tree is set to 1
            # the index in the solution list is the same as the depth of the current node
            solution[best_solution.depth] = 1
        # the best_solution is set to the parent of the current node
        # this makes it possible to backtrack the path the algorithm took to find the best solution
        best_solution = best_solution.parent

    total_weight = 0
    for i in range(len(items)):
        if solution[i] == 1:
            total_weight += items[i][0]

    return max_benefit, solution, total_weight



if __name__ == "__main__":
    item_list = read_items_from_file("items.txt")
    knapsackTimeOnly = lambda: knapsack(item_list, 420)
    elapsed_time = timeit.timeit(knapsackTimeOnly, number=1)
    max_ben, sol, tot_weight = knapsack(item_list, 420)
    print(f"the original tuple list of weight and benefit {item_list}")
    print(f"the max benefit: {max_ben}")
    print(f"the total weight: {tot_weight}")
    print(f"the solution: {sol}")
    print(f"time taken: {elapsed_time:.4f} seconds")
