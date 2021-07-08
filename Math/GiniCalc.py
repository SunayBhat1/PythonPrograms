'''
GiniCalc.py
Descrition: Generate Gini Coefficient for a two dimenional vector
By: Sunay Bhat
'''

# Import Libs
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Define Gini Coefficient Function
def giniCoeffCalc(dataVec):

	AMD = 0
	# Loop through and sum absolute differences of all elements
	for xi in dataVec:

		AMD = AMD + np.sum(abs(dataVec - xi))

	giniCoeff = AMD/(2 * dataVec.size ** 2 * dataVec.mean())

	return giniCoeff

# Define Lorenz Curve Plotter
def lorenz_curve(X,giniCoeff):
	X_lorenz = X.cumsum() / X.sum()
	X_lorenz = np.insert(X_lorenz, 0, 0)
	fig, ax = plt.subplots(figsize=[6,6])
	# scatter plot of Lorenz curve
	ax.plot(np.arange(X_lorenz.size)/(X_lorenz.size-1) * 100, X_lorenz * 100, color='darkgreen')
	# line plot of equality
	ax.plot([0,100], [0,100], color='k')
	plt.xlabel('% of Values',fontsize=18)
	plt.ylabel('% of Cumulative Sum',fontsize=18)
	plt.title('Lorenz Curve\n Gini Coeff = ' + str(round(giniCoeff * 100,1)) + '%',fontsize=24)
	plt.grid()
	plt.show()

# File to np vector
SPY_Data = pd.read_csv('/Users/sunaybhat/Documents/GitHub/PythonPrograms/Math/SPY.csv', delimiter=',')
SPY_Data['Day Range'] = SPY_Data['High'] - SPY_Data['Low']
SPY_Data['Percent Range'] = (SPY_Data['Day Range'] * 100) /SPY_Data['Open']
Percent_Change = SPY_Data['Percent Range'].to_numpy()

# Get Gini Coefficient of Vector
giniCoeff = giniCoeffCalc(Percent_Change)

print('Gini Coefficent is', str(round(giniCoeff * 100,1)), '%')

# Plot Lorenz Curve
lorenz_curve(np.sort(Percent_Change),giniCoeff)
