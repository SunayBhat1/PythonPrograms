'''
SimAssets.py
Descrition: Run Simulations on Market Assets
By: Sunay Bhat
'''

# Import Libs
import xlrd
import numpy
import matplotlib.pyplot as plt
import datetime
import math
import getpass
from fpdf import FPDF
from tqdm import tqdm
import os

plt.style.use('seaborn')

# Top level Vars, Make Function Inputs Eventually
muReturn = .066 # Assumed Yearly Marlet Return... Default 6.6%
distributiion = 'Normal' # Assume Normal Distribution, market is More laplace daily
Age = 65
Iters = 3000

# System parms
username = getpass.getuser()

# Figures
fig1, (ax1,ax2) = plt.subplots(2, 1, figsize=(8,9), facecolor='w', edgecolor='k')

# Read in Equity Excel
equityExcelLoc = '/Users/' + username + '/Dropbox/Finances/Equity.xlsx'
wb = xlrd.open_workbook(equityExcelLoc)
SummarySheet = wb.sheet_by_index(0)
MarketSheet = wb.sheet_by_index(1)
SavingsSheet = wb.sheet_by_index(2)

# Print out total equity
equity = str(round(SummarySheet.cell_value(7,2),2))
equity = equity[:equity.find('.')-3] + ',' + equity[equity.find('.')-3:]

# Polyfit STD for returns for time period
returnSTD = [0.709, 1.664, 2.959, 5.128]
years = [60, 30, 20, 10]
fitReturnSTD = numpy.polyfit(years,returnSTD,1)

# Find Total Market Assets
currentAssets = round(MarketSheet.cell_value(3,2),2)

# Determine current year and time window
now = datetime.datetime.now()
investWindow = (1996 + Age) - now.year

# Determine sigma of yearly return based on window
sigmaReturn = (fitReturnSTD[0] * investWindow + fitReturnSTD[1])/100

ModelReturns = numpy.empty((0,investWindow+1), float)

# Iterate through modeled returns
for iIter in tqdm(range(1,Iters + 1),ncols=100):
	modelAssets = [currentAssets]
	assets = currentAssets

	# Generate normal random distrbution of yearly returns for number of years
	normReturns = numpy.random.normal(muReturn,sigmaReturn,investWindow)

	# Apply return to every year to generate model return
	for iYr in range(0,investWindow):
		assets =  assets +  assets * normReturns[iYr]
		modelAssets.append(round(assets,2))

	# Append to final model matrix and add to line plot
	ModelReturns = numpy.vstack([ModelReturns, numpy.array(modelAssets)])
	ax1.plot(ModelReturns[iIter-1,:])
 

# Plot Meta
ticks = numpy.array(list(range(0,investWindow)))
ticksLabels = numpy.array(range(now.year,now.year+investWindow))
ax1.set_xticks(ticks[::4])
ax1.set_xticklabels(ticksLabels[::4], rotation = 45)
ax1.set_xlabel('Year',fontsize = 13)
ax1.set_ylabel('Dollar Value ($)',fontsize = 13)
ax1.set_title('Monte Carlo Analysis \n' + str(Iters) + ' Iterations',fontsize = 15,fontweight='bold')
ax1.grid(1)

# Get Final Dataset Statistics and histogram
finalValues = ModelReturns[:,-1]
ax2.hist(finalValues,bins='auto')
# ax2.set_xticks([finalValues.min(),numpy.percentile(finalValues,5),numpy.percentile(finalValues,25),numpy.percentile(finalValues,50),
	# numpy.percentile(finalValues,75),numpy.percentile(finalValues,95),finalValues.max()])
ax2.set_xlabel('Final Value ($ Millions)',fontsize = 13)
ax2.set_ylabel('Number of Iterations',fontsize = 13)
ax2.set_title('Distribution of Results',fontsize = 15,fontweight='bold')

print('\nCurrent Equity = $' + equity + '\n')
print('\nStarting Market Assets = ' + '${:,.2f}'.format(currentAssets) + '\n')
print('\nMinimum Final Value is: ' + '${:,.2f}'.format(finalValues.min()))
print('\n95% Confidence > ' + '${:,.2f}'.format(numpy.percentile(finalValues,5)))
print('\nMedian is $' + '{:,.2f}'.format(numpy.percentile(finalValues,50)))
print('\n5% Confidence > ' + '${:,.2f}'.format(numpy.percentile(finalValues,95)))
print('\nMaximum Final Value is: $' + '${:,.2f}'.format(finalValues.max()) + '\n')
print('\nStandard Error: ' + '${:,.2f}'.format(finalValues.std()/math.sqrt(Iters),2))

# # Save Model
# dfModel = pd.DataFrame(ModelReturns).T
# dfModel.to_excel(excel_writer = '/Users/' + username + '/Dropbox/Finances/MonteCarloReturns.xlsx')


# Show Plot
plt.tight_layout()
fig1.savefig('/Users/' + username + '/Dropbox/Finances/plot.png')

# Make Report PDF
pdf = FPDF(format='A4')
pdf.add_page()
pdf.set_font('Helvetica', 'B', 16)
pdf.set_xy(0,8)
pdf.cell(h=15, w=210, txt='Sunay Bhat 65 Yrs Old',align='C')
pdf.set_font('Helvetica', 'B', 14)
pdf.set_xy(0,15)
pdf.cell(h=15, w=210, txt='MonteCarlo Sim Finances',align='C')
pdf.set_font('Helvetica', '',11)
pdf.set_xy(15,30)
pdf.cell(h=10, w=210, txt='Starting Market Assets: ' + '${:,.2f}'.format(currentAssets))
pdf.set_font('Helvetica', 'B', 12)
pdf.set_xy(15,40)
pdf.cell(h=10, w=210, txt='Median Outcome is: ' + '${:,.2f}'.format(numpy.percentile(finalValues,50)))

pdf.set_font('Helvetica', '',9)
pdf.set_xy(15,50)
pdf.cell(h=5, w=210, txt='Current Equity: $' + equity,align='L')
pdf.set_xy(15,55)
pdf.cell(h=5, w=210, txt='Minimum Final Value is: ' + '${:,.2f}'.format(finalValues.min()))
pdf.set_xy(15,60)
pdf.cell(h=5, w=210, txt='95% Confidence > ' + '${:,.2f}'.format(numpy.percentile(finalValues,5)))
pdf.set_xy(15,65)
pdf.cell(h=5, w=210, txt='5% Confidence > ' + '${:,.2f}'.format(numpy.percentile(finalValues,95)))
pdf.set_xy(15,70)
pdf.cell(h=5, w=210, txt='Maximum Final Value is: $' + '${:,.2f}'.format(finalValues.max()))
pdf.set_xy(15,75)
pdf.cell(h=5, w=210, txt='Standard Error: ' + '${:,.2f}'.format(finalValues.std()/math.sqrt(Iters),2))
pdf.rect(5,5,200,287)
pdf.rect(8,8,194,282)
pdf.image('/Users/' + username + '/Dropbox/Finances/plot.png',x=35,y=95,w=700/5,h=450/3)
pdf.set_xy(15,260)
pdf.cell(h=5, w=210, txt='Market Mean Return: {:.2%}%'.format(muReturn))
pdf.set_xy(15,265)
pdf.cell(h=5, w=210, txt='Market Sigma Return: ({:.2f} * Yrs + {:.2f})/100'.format(returnSTD[0],returnSTD[1]))
pdf.set_xy(15,270)
pdf.cell(h=5, w=210, txt='Run on {}/{}/{}'.format(now.month,now.day,now.year))
os.remove('/Users/' + username + '/Dropbox/Finances/plot.png')
pdf.output('/Users/' + username + '/Dropbox/Finances/Monte Carlo Report.pdf', 'F')



