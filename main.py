from search.structure.graph import Graph
from search.strategy import Strategy as search

g = Graph(r'C:\Users\vicoo\PycharmProjects\Search_Algorithms\graph.gp')

path = search.a_star(g.list[0], g.list[-2])

print('fin')
