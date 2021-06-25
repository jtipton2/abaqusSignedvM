# abaqusSignedvM
Create a signed von Mises equivalent stress in Abaqus and use for fatigue analysis


## Language:
PYTHON scripting for Abaqus/Viewer Release 2020.HF4


## File Run:
C:\temp>abaqus python <filename>.py
(Console messages are redirected to abaqus.rpy)


## Summary:

### abqPython_SvM_1_PostProc
This script opens an Abaqus|Explicit solution.  It operates on averaged nodal stresses and calculates a signed von Mises equivalent stress.  At each timestep, it runs through each node and keeps track of the initial (static), dynamic minimum, and dynamic maximum stresses.  These are saved as python binary files. 

### abqPython_SvM_2_Goodman
This script opens the python binary file. For each node of the FEA, it calculates the mean stress and stress amplitude using the peak minimum and maximum stresses over time.  Results are plotted on a Smith diagram and also a Goodman diagram.

### abqPython_SvM_3_SaveODB
This script opens the original Abaqus ODB results database.  At the final timestep, it saves the various signed von Mises stress calculations.  Abaqus CAE can then be used to plot contour maps.


## Source Examples:

### Python

Notes regarding bulkDataBlock:
* https://stackoverflow.com/questions/46573959/accelerate-a-slow-loop-in-abaqus-python-code-for-extracting-strain-data-from-od

Explanations of field output options:
* https://abaqus-docs.mit.edu/2017/English/SIMACAEKERRefMap/simaker-c-fieldoutputcpp.htm

Solution on how to average nodal values:
* https://stackoverflow.com/questions/42783385/max-stress-node/
* https://stackoverflow.com/questions/54350924/find-stresses-at-unique-nodal-on-abaqus-with-python-script

Solution on how to take largest, unaveraged nodal value:
* https://python-forum.io/Thread-Get-max-values-based-on-unique-values-in-another-list-python

Vectorizing conditional loops in Python:
* https://towardsdatascience.com/data-science-with-python-turn-your-conditional-loops-to-numpy-vectors-9484ff9c622e
