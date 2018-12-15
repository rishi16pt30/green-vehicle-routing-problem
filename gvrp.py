
from utility import Node, PriorityQueue


def greenTravel(adj_mat,src):
    optimal_tour = []
    n = len(adj_mat)
    
    u = Node()
    PQ = PriorityQueue()
    optimal_length = 0
    v = Node(level=0, path=[0])
    min_length = float('inf')  
    v.bound = bound(adj_mat, v)
    
    PQ.put(v)
    while not PQ.empty():
        v = PQ.get()
        if v.bound < min_length:
            u.level = v.level + 1
            for i in filter(lambda x: x not in v.path, range(1, n)):
                u.path = v.path[:]
                u.path.append(i)
                if u.level == n - 2:
                    l = set(range(1, n)) - set(u.path)
                    u.path.append(list(l)[0])
              
                    u.path.append(0)

                    _len = length(adj_mat, u)
                    if _len < min_length:
                        min_length = _len
                        optimal_length = _len
                        optimal_tour = u.path[:]

                else:
                    u.bound = bound(adj_mat, u)
                    if u.bound < min_length:
                        PQ.put(u)
                u = Node(level=u.level)


    optimal_tour_src = optimal_tour
    if src is not 1:
        optimal_tour_src = optimal_tour[:-1]
        y = optimal_tour_src.index(src)
        optimal_tour_src = optimal_tour_src[y:] + optimal_tour_src[:y]
        optimal_tour_src.append(optimal_tour_src[0])

    return optimal_tour_src, optimal_length


def length(adj_mat, node):
    tour = node.path
    
    return sum([adj_mat[tour[i]][tour[i + 1]] for i in xrange(len(tour) - 1)])


def bound(adj_mat, node):
    path = node.path
    temp_bound = 0

    n = len(adj_mat)
    determined, last = path[:-1], path[-1]

    remain = filter(lambda x: x not in path, range(n))


    for i in range(len(path) - 1):
        temp_bound += adj_mat[path[i]][path[i + 1]]


    temp_bound += min([adj_mat[last][i] for i in remain])

    p = [path[0]] + remain

    for r in remain:
        temp_bound += min([adj_mat[r][i] for i in filter(lambda x: x != r, p)])
    
    return temp_bound
