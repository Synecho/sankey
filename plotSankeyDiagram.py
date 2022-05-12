'''
Created on Nov 19, 2021

@author: leo
'''

import plotly.graph_objects as go
import numpy as np
import palettable as pt

# Define node labels
nodeLabels = ["DIM", "DOM_S", "DOM_L", "TEP", "Det_S", "Det_L", "Phy", "Bac_FL", "Bac_PA", "HF", "Cil", "Leak"]

# Define node positions
nodePositions = {
    "DIM":(0.1, 0.6), 
    "DOM_S":(0.3, 0.6), 
    "DOM_L":(0.5, 0.6), 
    "TEP":(0.6, 0.8), 
    "Det_S":(0.7, 0.6), 
    "Det_L":(0.9, 0.6), 
    "Leak":(0.99, 0.6),
    "Phy":(0.2, 0.85), 
    "Bac_FL":(0.6, 0.4), 
    "Bac_PA":(0.8, 0.4), 
    "HF":(0.7, 0.3), 
    "Cil":(0.9,0.3), 
    }

# Define node categories (used for coloring - order matters)
colorpalette = pt.cartocolors.qualitative.Prism_10.colors
linkAlpha = 0.5
categories = ["DIM", "DOM", "TEP", "Det", "Phy", "Bac", "HF", "Cil", "Leak"]
categoryColors = dict(zip(categories, colorpalette))
nodeCategories = {
    "DIM":"DIM", 
    "DOM_S":"DOM", 
    "DOM_L":"DOM", 
    "TEP":"TEP", 
    "Det_S":"Det", 
    "Det_L":"Det", 
    "Phy":"Phy", 
    "Bac_FL":"Bac", 
    "Bac_PA":"Bac", 
    "HF":"HF", 
    "Cil":"Cil", 
    "Leak":"Leak"
    }

# Define links
mainLinks = {
    "DIM" : ["Phy"],
    "DOM_S" : ["Bac_FL", "Bac_PA"],
    "DOM_L" : ["Bac_FL", "TEP"], # not to "BAC_PA"??
    "TEP" : ["Det_L"],    # not to "Det_S"??
    "Det_S" : ["Det_L", "Bac_PA"],
    "Det_L" : ["Bac_PA", "Leak"],
    "Phy" : ["DOM_L", "DOM_S", "Det_S", "Det_L"],
    "Bac_FL" : ["DIM", "DOM_S", "DOM_L", "Det_S", "HF"],
    "Bac_PA" : ["DIM", "DOM_S", "DOM_L", "Det_S", "HF"],
    "HF" : ["DIM", "DOM_S", "DOM_L", "Det_S", "Cil"],
    "Cil" : ["DIM", "DOM_S", "DOM_L", "Det_S"],
    "Leak" : [],
    }

# Weak links (dotted in original scheme) are ignored, so far
weakLinks = {
    "Det_S" : ["HF", "Cil"],
    "Bac_FL" : ["Cil"],
    "Bac_PA" : ["Cil"],
    }

# Define link strengths (TODO: extract values from simulation)
linkWeights = {
    "DIM" : {"Phy":10.0},
    "DOM_S" : {"Bac_FL":1.0, "Bac_PA":0.5},
    "DOM_L" : {"Bac_FL":2.0, "TEP":1.0}, # not to "BAC_PA"??
    "TEP" : {"Det_L":1.0},    # not to "Det_S"??
    "Det_S" : {"Det_L":1.0, "Bac_PA":3.0},
    "Det_L" : {"Bac_PA":2.0, "Leak":3.0},
    "Phy" : {"DOM_L":2.0, "DOM_S":3.0, "Det_S":1.0, "Det_L":1.0},
    "Bac_FL" : {"DIM":3.0, "DOM_S":0.5, "DOM_L":0.5, "Det_S":0.5, "HF":3.0},
    "Bac_PA" : {"DIM":3.0, "DOM_S":0.5, "DOM_L":2.0, "Det_S":0.5, "HF":1.0},
    "HF" : {"DIM":1.0, "DOM_S":0.5, "DOM_L":0.5, "Det_S":0.5, "Cil":3.0},
    "Cil" : {"DIM":5.0, "DOM_S":0.5, "DOM_L":0.5, "Det_S":1.0},
    "Leak" : {},
    }


# Define color palette
nodeColors = [categoryColors[nodeCategories[k]]+[1] for k in nodeLabels]
nodeColorsStr = ["rgba(%g,%g,%g,%g)"%tuple(col) for col in nodeColors]
linkColorsStr = ["rgba(%g,%g,%g,%g)"%tuple(col[:3]+[linkAlpha]) for col in nodeColors]

xs = [nodePositions[k][0] for k in nodeLabels]
ys = [nodePositions[k][1] for k in nodeLabels]

nodeIX2ID = dict(enumerate(nodeLabels))
nodeID2IX = dict([(v,k) for k,v in nodeIX2ID.items()])
nodes = {"label": nodeLabels, 
         "x":xs, 
         "y":np.ones_like(ys)*0.95-ys,
         "color":nodeColorsStr}
# nodes = {"x", "y"}
links = {"source": [], "target": [], "value": [], "color": []}

for source in nodeLabels:
    sourceIX = nodeID2IX[source]
    for target in mainLinks[source]:
        targetIX = nodeID2IX[target]
        links["source"].append(sourceIX)
        links["target"].append(targetIX)
        links["value"].append(linkWeights[source][target])
        links["color"].append(linkColorsStr[sourceIX])


def plotSankey(nodes, links):
    fig = go.Figure(go.Sankey(
    node = nodes,
    link = links))
    
    fig.update_layout(title_text="Sankey diagram of model scheme",
                      font_size=10,
                      width=1200,
                      height=800)
    fig.show()


if __name__ == '__main__':
    plotSankey(nodes, links)


