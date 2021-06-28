#==============================================================================
# IMPORT NECESSARY MODULES
#==============================================================================
# C:\temp>abaqus viewer -noGUI  (this requires a CAE license)
# C:\temp>abaqus python         (this does not require a license)

import numpy as np
from odbAccess import openOdb
from abaqusConstants import *


#==============================================================================
# DEFINE FUNCTIONS
#==============================================================================
def nodalAveraged(odbInstance,Frame,StressType,timestep):
    """
    For a given solution step, timestep, and stress type
    this function will return 100% nodal averaged results
    sorted by node number.  (Note that the element set is
    hardcoded.)
    """
    
    # Get number of nodes
    Field = Frame[timestep].fieldOutputs['S'].getSubset(region = odbInstance.elementSets['TA_ELEM']).getSubset(position = ELEMENT_NODAL).getScalarField(invariant = StressType)
    NumValues = len(Field.values)
    
    # Create vector of element nodes and stresses
    # (for some reason, ababqus breaks into blocks of data
    #  need to join the various data blocks into an array)
    Values = Field.bulkDataBlocks[0].data
    NodeLabels = Field.bulkDataBlocks[0].nodeLabels
    for i in range(len(Field.bulkDataBlocks)-1):
        Values = np.vstack((Values,Field.bulkDataBlocks[i+1].data))
        NodeLabels = np.hstack((NodeLabels,Field.bulkDataBlocks[i+1].nodeLabels))
    
    # Nodes are shared across multiple elements.  Get unique node labels.
    NodeLabels_unique, unq_idx = np.unique(NodeLabels, return_inverse=True)
    NumNodes = len(NodeLabels_unique)
    
    # Calculate nodal averaged stresses at timestep
    Values_Averaged=np.zeros((NodeLabels_unique.size,Values.shape[1]))
    unq_counts = np.bincount(unq_idx)
    for i in xrange(0,Values.shape[1]):
       ValuesTemp = [item[i] for item in Values]
       unq_sum = np.bincount(unq_idx, weights=ValuesTemp)
       Values_Averaged[:,i] = unq_sum / unq_counts
       
    return NodeLabels_unique, Values_Averaged



#==============================================================================
# RUN THE PROGRAM
#==============================================================================
filename = 'Job-4e-SS-Pulse'

#
# LOAD ABAQUS SOLUTION DATA
#-------------------------------------------------------------------
odb = openOdb(filename+'.odb',readOnly=True)

# Get Instance
allInstances = (odb.rootAssembly.instances.keys())
odbInstance = odb.rootAssembly.instances[allInstances[-1]]

#
# PROCESS RESULTS
#-------------------------------------------------------------------

# Retrieve nodal averaged stresses at steady-state solution
timestep = 0
Frame = odb.steps['Step-3-Pulse'].frames
nodeNum, pressure = nodalAveraged(odbInstance,Frame,PRESS,timestep)
nodeNum, vonMises = nodalAveraged(odbInstance,Frame,MISES,timestep)

# Create a signed von Mises stress
vonMisesSigned = np.sign(-1.*pressure)*vonMises

# Save static stress and also initialize dynamic stress vectors
stressStatic = vonMisesSigned.copy()
stressDynamicMin = vonMisesSigned.copy()
stressDynamicMax = vonMisesSigned.copy()

# Get nodal coordinates
nodeList = Frame[0].fieldOutputs['S'].values[0].instance.nodes
nodeCoord = np.zeros((len(nodeList),4))

for item in range(len(nodeList)):
    nodeCoord[item,0] = nodeList[item].label
    nodeCoord[item,1] = nodeList[item].coordinates[0]
    nodeCoord[item,2] = nodeList[item].coordinates[1]
    nodeCoord[item,3] = nodeList[item].coordinates[2]

# Find max and min stress values at each node during pulse response
Frame = odb.steps['Step-4-Response'].frames
for timestep in range(len(Frame)):
    nodeNum, pressure = nodalAveraged(odbInstance,Frame,PRESS,timestep)
    nodeNum, vonMises = nodalAveraged(odbInstance,Frame,MISES,timestep)
    
    vonMisesSigned = np.sign(-1.*pressure)*vonMises
    
    stressDynamicMax = np.maximum(stressDynamicMax, vonMisesSigned)
    stressDynamicMin = np.minimum(stressDynamicMin, vonMisesSigned)

Frame = odb.steps['Step-6-Response'].frames
for timestep in range(len(Frame)):
    nodeNum, pressure = nodalAveraged(odbInstance,Frame,PRESS,timestep)
    nodeNum, vonMises = nodalAveraged(odbInstance,Frame,MISES,timestep)
    
    vonMisesSigned = np.sign(-1.*pressure)*vonMises
    
    stressDynamicMax = np.maximum(stressDynamicMax, vonMisesSigned)
    stressDynamicMin = np.minimum(stressDynamicMin, vonMisesSigned)

#
# SAVE DATA TO NUMPY COMPRESSED BINARY FILE FOR LATER USE
#-------------------------------------------------------------------
np.savez_compressed(filename, 
                    nodeNum=nodeNum.flatten(),
                    vonMisesMax=stressDynamicMax.flatten(), 
                    vonMisesMin=stressDynamicMin.flatten(), 
                    vonMisesStatic=stressStatic.flatten(),
                    nodeCoord=nodeCoord)

#
# TERMINATE PROGRAM
#-------------------------------------------------------------------

#odb.save()
odb.close()

