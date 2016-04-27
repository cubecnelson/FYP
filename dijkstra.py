from collections import namedtuple, deque
from pprint import pprint as pp
 
 
inf = float('inf')
Edge = namedtuple('Edge', 'start, end, cost')
 
class Graph():
    def __init__(self, edges):
        self.edges = edges2 = [Edge(*edge) for edge in edges]
        self.vertices = set(sum(([e.start, e.end] for e in edges2), []))
 
    def dijkstra(self, source, dest):
        assert source in self.vertices
        dist = {vertex: inf for vertex in self.vertices}
        previous = {vertex: None for vertex in self.vertices}
        dist[source] = 0
        q = self.vertices.copy()
        neighbours = {vertex: set() for vertex in self.vertices}
        for start, end, cost in self.edges:
            neighbours[start].add((end, cost))
        #pp(neighbours)
 
        while q:
            u = min(q, key=lambda vertex: dist[vertex])
            q.remove(u)
            if dist[u] == inf or u == dest:
                break
            for v, cost in neighbours[u]:
                alt = dist[u] + cost
                if alt < dist[v]:                                  # Relax (u,v,a)
                    dist[v] = alt
                    previous[v] = u
        #pp(previous)
        s, u = deque(), dest
        while previous[u]:
            s.appendleft(u)
            u = previous[u]
        s.appendleft(u)
        return s
 
 
graph = Graph([('VP', 'VP', 3.7534179752515073), ('ADJP', 'PP', 0.7731898882334817), ('ADJP', 'VP', 1.3121863889661687), ('NP', 'NP', 1.4749844358346094), ('NP', 'PP', 1.3394389438383854), ('ADVP', 'NP', 0.579818495252942), ('PP', 'NP', 0.1840930364423367), ('PP', 'VP', 2.424802725718295), ('VP', 'ADVP', 3.0602707946915624), ('VP', 'PP', 1.7609878105613013), ('VP', 'NP', 0.3194307707663612), ('NP', 'ADJP', 2.768905476823485), ('NP', 'ADVP', 2.768905476823485), ('PP', 'ADJP', 3.34109345759245), ('VP', 'ADJP', 3.4657359027997265), ('ADVP', 'ADJP', 3.2188758248682006), ('NP', 'VP', 0.9577279217383282), ('ADJP', 'NP', 1.3121863889661687), ('ADVP', 'VP', 1.8325814637483102), ('PP', 'ADVP', 3.628775530044231), ('ADVP', 'PP', 1.4271163556401458), ('PP', 'PP', 4.034240638152395)])
pp(graph.dijkstra("VP", "ADJP"))