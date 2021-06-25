# -*- coding: utf-8 -*-

import numpy as np
from odbAccess import *
from abaqusConstants import *

filename = 'Job-4e-SS-Pulse'


"""
LOAD DATA
===============================================================================
"""
results = np.load(filename + '.npz')
vonMisesMax = results['vonMisesMax'].transpose()
vonMisesMin = results['vonMisesMin'].transpose()
vonMisesStatic = results['vonMisesStatic'].transpose()
nodeNum = results['nodeNum'].transpose()
nodeCoord = results['nodeCoord']

# Sort nodeCoord on nodal values
nodeCoord = nodeCoord[nodeCoord[:,0].argsort()]

# Calculate Mean and Amplitude
vonMisesAmp = (vonMisesMax - vonMisesMin)/2
vonMisesMean = (vonMisesMax + vonMisesMin)/2


"""
LOAD ODB
===============================================================================
"""

odb = openOdb(filename+'.odb',readOnly=False)

# Get Instance
allInstances = (odb.rootAssembly.instances.keys())
odbInstance = odb.rootAssembly.instances[allInstances[-1]]


"""
FORMAT AND SAVE DATA TO ODB
===============================================================================
"""

vMNodes  = np.ascontiguousarray(nodeNum, dtype=np.int32)
vMMax    = np.ascontiguousarray(np.reshape(vonMisesMax,(-1,1)), dtype=np.float32)
vMMin    = np.ascontiguousarray(np.reshape(vonMisesMin,(-1,1)), dtype=np.float32)
vMStatic = np.ascontiguousarray(np.reshape(vonMisesStatic,(-1,1)), dtype=np.float32)
vMMean   = np.ascontiguousarray(np.reshape(vonMisesMean,(-1,1)), dtype=np.float32)
vMAmp    = np.ascontiguousarray(np.reshape(vonMisesAmp,(-1,1)), dtype=np.float32)


newFieldOutputMax = odb.steps['Step-6-Response'].frames[-1].FieldOutput(name = 'vMMax', description = 'Max Signed von Mises', type = SCALAR)
newFieldOutputMax.addData(position=NODAL, instance = odbInstance, labels = vMNodes, data = vMMax.tolist())

newFieldOutputMin = odb.steps['Step-6-Response'].frames[-1].FieldOutput(name = 'vMMin', description = 'Min Signed von Mises', type = SCALAR)
newFieldOutputMin.addData(position=NODAL, instance = odbInstance, labels = vMNodes, data = vMMin.tolist())

newFieldOutputMStatic = odb.steps['Step-6-Response'].frames[-1].FieldOutput(name = 'vMStatic', description = 'Static Signed von Mises', type = SCALAR)
newFieldOutputMStatic.addData(position=NODAL, instance = odbInstance, labels = vMNodes, data = vMStatic.tolist())

newFieldOutputMean = odb.steps['Step-6-Response'].frames[-1].FieldOutput(name = 'vMMean', description = 'Signed von Mises Mean', type = SCALAR)
newFieldOutputMean.addData(position=NODAL, instance = odbInstance, labels = vMNodes, data = vMMean.tolist())

newFieldOutputAmp = odb.steps['Step-6-Response'].frames[-1].FieldOutput(name = 'vMAmp', description = 'Signed von Mises Amplitude', type = SCALAR)
newFieldOutputAmp.addData(position=NODAL, instance = odbInstance, labels = vMNodes, data = vMAmp.tolist())



"""
SAVE AND CLOSE
===============================================================================
"""

odb.save()
odb.close()
