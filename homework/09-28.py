import itertools as it

size = 2
area = size**2
n = 2

graph = []

def to_node_label(xs):
    return str(xs).replace(
        "[","(").replace(
        "]",")")

def add_node(xs, ys, label):
    xs = list(sorted(xs))
    ys = list(sorted(ys))
    graph.append((
        to_node_label(xs),
        to_node_label(ys),
        str(label)))

def singlediff(xs, ys):
    mxs = xs if len(xs) >= len(ys) else ys
    for i in mxs:
        if (not i in xs) or (not i in ys):
            return i

for i in range(0,n):

    if i == 0:
        for j in range(area):
            add_node((),(j,), j)

    if i == 1:
        for comb_2 in it.combinations(range(area), 2):
            for x in comb_2:
                add_node((x,), comb_2, singlediff(comb_2, (x,)))

    if i == 2:
        for comb_3 in it.combinations(range(area), 3):
            for comb_2 in it.combinations(comb_3, 2):
                add_node(comb_2, comb_3, singlediff(comb_3, comb_2))

with open("09-28_new.dot", "w+") as file:
    file.write("digraph {\n\n")
    file.write("    graph [ratio=1; splines=false]")
    
    for n in graph:
        file.write(
            f"    \"{n[0]}\" -> \"{n[1]}\" " +
            f"[label=\"{n[2]}\"]\n")

    file.write("}\n")

