# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

filename = 'Job-4e-SS-Pulse'


"""
LOAD DATA FROM ABAQUS POSTPROCESSING
===============================================================================

nodeCoord has 4 columns:
    (1) node ID
    (2) x coordinate [m]
    (3) y coordinate [m]
    (4) z coordinate [m]
"""
results = np.load(filename + '.npz')
vonMisesMax = results['vonMisesMax'].transpose()
vonMisesMin = results['vonMisesMin'].transpose()
vonMisesStatic = results['vonMisesStatic'].transpose()
nodeCoord = results['nodeCoord']
# Sort nodeCoord on nodal values
nodeCoord = nodeCoord[nodeCoord[:,0].argsort()]


"""
CALCULATE MEAN and AMPLITUDE
===============================================================================
"""
vonMisesAmp = (vonMisesMax - vonMisesMin)/2
vonMisesMean = (vonMisesMax + vonMisesMin)/2

yerrVM = [abs(vonMisesStatic - vonMisesMin)/1.E6,
          abs(vonMisesMax - vonMisesStatic)/1.E6]

"""
PLOT SMITH DIAGRAM
===============================================================================
"""
fig1 = plt.figure(figsize=(6,6), dpi=200)
ax1 = fig1.add_axes([0,0,1,1])

ax1.set_xlabel('Quasi-Static Stress (von Mises) [MPa]')
ax1.set_ylabel('Beam Pulse Response Stress Range [MPa]')
ax1.set_title('Ta Pulse Response: No HIP Residual Stress & Irradiated W')

ax1.errorbar(vonMisesStatic/1.E6, 
             vonMisesStatic/1.E6, 
             yerr = yerrVM,
             fmt='.',
             markeredgecolor=('k'),
             color='green',
             label='Nodal Static Stress $\pm$ Stress Range')

plt.legend(loc='upper left')
plt.grid(which='major', axis='both')

fig1.savefig(filename+'_Smith.png', bbox_inches = "tight")



"""
PLOT GOODMAN DIAGRAM
===============================================================================
"""
fig2 = plt.figure(figsize=(6,6), dpi=200)
ax2 = fig2.add_axes([0,0,1,1])

ax2.set_xlabel('Mean Stress [MPa]')
ax2.set_ylabel('Stress Amplitude [MPa]')
ax2.set_title('Ta Pulse Response: No HIP Residual Stress & Irradiated W')

ax2.plot(vonMisesMean/1.E6, 
         vonMisesAmp/1.E6, 
         color='green',
         marker='.',
         lw=0,
         label="Nodal von Mises Stess")

plt.legend(loc='upper right')
plt.grid(which='major', axis='both')

fig2.savefig(filename+'_Goodman.png', bbox_inches = "tight")
