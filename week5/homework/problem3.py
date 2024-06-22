# A bipartite graph is a graph that can be colored with two colors such that no two neighboring nodes share the same
# color. Devise an arithmetic circuit scheme to show you have a valid witness of a 2-coloring of a graph.
# Hint: the scheme in this tutorial needs to be adjusted before it will work with a 2-coloring.

# r=1 g=2
# for each node we write
# 0 === (1 - x) * (2 - x)

# for each two neighboring nodes x and y we write
# 0 === (2 - x*y)