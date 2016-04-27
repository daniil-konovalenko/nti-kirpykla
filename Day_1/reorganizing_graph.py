from Day_1.GraphParser import graphParser as gp

n_lines = 30
cols = ['from', 'to', 'links']
graph = gp.parseFolderBySchema('Task2/Task2/graph', n_lines, '', 'from', cols, True)
n_tot