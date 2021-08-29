import json
# First networkx library is imported
# along with matplotlib
import networkx as nx
from pyvis.network import Network
import matplotlib.pyplot as plt

from bokeh.io import output_notebook, show, save
from bokeh.models import Range1d, Circle, ColumnDataSource, MultiLine
from bokeh.plotting import figure
from bokeh.plotting import from_networkx

from datetime import datetime

# Defining a Class
class GraphVisualization:

    def __init__(self):
        # visual is a list which stores all
        # the set of edges that constitutes a
        # graph
        self.visual = []

    # addEdge function inputs the vertices of an
    # edge and appends it to the visual list
    def addEdge(self, a, b):
        temp = [a, b]
        self.visual.append(temp)

    # In visualize function G is an object of
    # class Graph given by networkx G.add_edges_from(visual)
    # creates a graph with a given list
    # nx.draw_networkx(G) - plots the graph
    # plt.show() - displays the graph
    def visualize(self):
        G = nx.Graph()
        G.add_edges_from(self.visual)
        print("Edges add to graph")
        #nx.draw(G)
        #nx.draw_networkx(G)
        nx.write_gexf(G, "some_graph.gexf")
        nt = Network(height='750px', width='100%')
        # populates the nodes and edges data structures
        nt.from_nx(G)
        print("Network build done")
        nt.show('nx.html')
        #plt.show()

    def save(self, dirPath, fileName):
        G = nx.Graph()
        G.add_edges_from(self.visual)
        #print("Edges add to graph")
        graphFilePath = dirPath + '/graph/' + fileName + '.gexf'
        nx.write_gexf(G, graphFilePath)
        nt = Network(height='750px', width='100%')
        nt.from_nx(G)
        #print("Network build done")
        nt.save_graph(dirPath + '/graph/' + fileName + '.html')


    def visualize1(self):

        G = nx.Graph()
        G.add_edges_from(self.visual)
        print("Edges add to graph")

        # Choose a title!
        title = 'Game of Thrones Network'

        # Establish which categories will appear when hovering over each node
        HOVER_TOOLTIPS = [("Character", "@index")]

        # Create a plot — set dimensions, toolbar, and title
        plot = figure(tooltips=HOVER_TOOLTIPS,
                      tools="pan,wheel_zoom,save,reset", active_scroll='wheel_zoom',
                      x_range=Range1d(-10.1, 10.1), y_range=Range1d(-10.1, 10.1), title=title)

        # Create a network graph object with spring layout
        # https://networkx.github.io/documentation/networkx-1.9/reference/generated/networkx.drawing.layout.spring_layout.html
        print("plot initialized")
        network_graph = from_networkx(G, nx.spring_layout, scale=10, center=(0, 0))
        print("Network imported")
        # Set node size and color
        network_graph.node_renderer.glyph = Circle(size=15, fill_color='skyblue')
        print("Network rendered")
        # Set edge opacity and width
        network_graph.edge_renderer.glyph = MultiLine(line_alpha=0.5, line_width=1)

        # Add network graph to the plot
        plot.renderers.append(network_graph)
        print("Graph appended")
        show(plot)
        # save(plot, filename=f"{title}.html")

IdtoTimeMap = {}
rootID = 59736485
def convertTwitterTime(time_val) :
    new_datetime = datetime.strftime(datetime.strptime(time_val, '%a %b %d %H:%M:%S +0000 %Y'), '%Y-%m-%d %H:%M:%S')
    timestamp = datetime.timestamp(datetime.strptime(new_datetime, '%Y-%m-%d %H:%M:%S'))
    return timestamp

def test() :
    filePath = 'D:/Twitter/FakeNewsNet-master/FakeNewsNet-master/code/fakenewsnet_dataset/politifact/fake/politifact14745/retweets/929507659073687552.json'
    with open(filePath) as f:
        retweet_dict = json.load(f)

    for retweet in retweet_dict['retweets'] :
        root_time_val = retweet['retweeted_status']['created_at']
        print(root_time_val)
        break
    IdtoTimeMap[rootID] = convertTwitterTime(root_time_val)
    print(IdtoTimeMap[rootID])

def createIdtoTimeMap() :
    filePath = 'D:/Twitter/FakeNewsNet-master/FakeNewsNet-master/code/fakenewsnet_dataset/politifact/fake/politifact14745/retweets/929507659073687552.json'
    with open(filePath) as f:
        retweet_dict = json.load(f)

    print("Json loaded")
    for retweet in retweet_dict['retweets']:
        root_time_val = retweet['retweeted_status']['created_at']
        print(root_time_val)
        break
    IdtoTimeMap[rootID] = convertTwitterTime(root_time_val)
    print("Root timestamp = ", IdtoTimeMap[rootID])

    for retweet in retweet_dict['retweets']:
        id = retweet['user']['id']
        time_val = retweet['created_at']
        print(time_val)
        IdtoTimeMap[id] = convertTwitterTime(time_val)

def getLevelfromTime(timestamp) :
    #print("timestamp = ", timestamp)
    level = (timestamp - IdtoTimeMap[rootID])
    print("level = ", level)
    return level / 5000

pos = 1
def addDistantEdge(G, a, b) :
    #if b not in IdtoTimeMap:
    #    return
    #print(type(b))
    #print((IdtoTimeMap[40708919]))
    #print(IdtoTimeMap)
    timestamp = IdtoTimeMap[int(b)]
    level = getLevelfromTime(timestamp)
    start = a
    global pos
    for i in range(0,int(level)) :
        end = pos
        G.addEdge(start, end)
        start = pos
        pos = pos + 1
    G.addEdge(start, b)
    print("Pos = ", pos)


def makeGraph() :

    createIdtoTimeMap()

    # Driver code
    G = GraphVisualization()

    filePath = 'Id2Followers.json'
    with open(filePath) as f:
        ids_dict = json.load(f)

    print("Id2Followers Json loaded")


    for key in ids_dict :
        # Iterating over values
        #print("Building graph for ID = ", key)
        for id, friends in ids_dict.items():
            # Add connection between retweet IDs
            if (key in friends):
                print("Edge detected")
                G.addEdge(key, id)

    '''
    counter = 0
    for id, friends in ids_dict.items():
        counter = counter + 1
        if counter == 5 :
            break
        print("Building graph for friends of  ID = ", id)
        for frnd in friends :
            count = 0
            for id_1, friends_1 in ids_dict.items():
                if(count == 1) :
                    break
                if (frnd in friends_1) & (id != id_1) :
                    count = count + 1
                    #print("detected")
                    G.addEdge(frnd, id_1)
                    G.addEdge(id, frnd)
            #if count != 0 :
            #    print(count)
    '''


    # Add conncetion with primary
    for id, friends in ids_dict.items():
        if (59736485 in friends):
            print("[Primary] Edge detected")
        else :
            print("Adding distand edge = ", id)
            addDistantEdge(G, 59736485, id)
            #G.addEdge(59736485, id)

    print("Graph building done...")
    G.visualize()
    print("Program Ended")
