import os
import sys
import networkx as nx
from queuelib import FifoDiskQueue

q = FifoDiskQueue("diskFile3")
completed = False
for root, dirs, files in os.walk(sys.argv[1]):
	for file in files:
		print file
		q.push(sys.argv[1] + file)
q.close()

print "-----------------"
while True:
	q = FifoDiskQueue("diskFile3")
	file1 = q.pop()
	file2 = q.pop()
	q.close()
	if file1 and file2:
		print file1
		print file2
		fileId1 = "_".join(file1.split("_")[1:5]).split(".")[0]
		fileId2 = "_".join(file2.split("_")[1:5]).split(".")[0]
		newFileId = sys.argv[2] + "_" + fileId1 + "_" + fileId2 + ".gpickle"
		print newFileId
		G1 = nx.read_gpickle(file1)
		G2 = nx.read_gpickle(file2)
		G1.add_nodes_from(G2.nodes(data=True))
		G1.add_edges_from(G2.edges(data=True))
		nx.write_gpickle(G1, newFileId)

		os.remove(file1)
		os.remove(file2)
		q = FifoDiskQueue("diskFile3")
		q.push(newFileId)
		q.close()
	else:
		break



