import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import *
import matplotlib.pyplot as plt
import numpy as np
import matplotlib

matplotlib.use('TkAgg')

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)

class StockCalculator(tk.Tk):
	def __init__(self):
		super().__init__()
		
		# init window size and grid size
		self.title("StockCalculator")
		self.geometry("1280x720")
		self.resizable(True,True)
		
		### define 4 frames which build GUI 
		# menu left
		self.menu_left = tk.Frame(self, width=500, bg="#ababab")
		self.menu_left_upper = tk.Frame(self.menu_left, width=500, height=500, bg="red") # sliders 
		self.menu_left_lower = tk.Frame(self.menu_left, width=500, bg="blue") # buttons 

		self.menu_left_upper.pack(side="top", fill="both", expand=True)
		self.menu_left_lower.pack(side="top", fill="both", expand=True)

        # menu right
		self.menu_right = tk.Frame(self, width=600, bg="#dfdfdf")
		self.menu_right_upper = tk.Frame(self.menu_right,width=600, height=400)
		self.menu_right_lower = tk.Frame(self.menu_right,width=600, height=250, bg="blue")

		self.menu_right_upper.pack(side="top", fill="both", expand=True)
		self.menu_right_lower.pack(side="top", fill="both", expand=True)
		
        # define frame positions on grid	
		self.menu_left.grid(row=0, column=0, rowspan=2, sticky="nsew")
		self.menu_right.grid(row=0,column=1, rowspan=2, sticky="nsew")
		
        # define grid 
		self.grid_rowconfigure(1, weight=1)
		self.grid_columnconfigure(1, weight=1)
		
		###
		
		# configure grid rows (12 rows: 0 - 11)
		# for i in range(12):
			# self.rowconfigure(i, weight=1)
		
		# configure column rows (10 columns: 0 - 9)
		# self.columnconfigure(0,weight=1)
		# self.columnconfigure(1,weight=1)
		# self.columnconfigure(2,weight=1)
		# self.columnconfigure(3,weight=1)
		# self.columnconfigure(4,weight=5)
	
		
		#self.columnconfigure(10, minsize=1000, weight=1)
		
		# define text fields and placement
		self.txt_results = tk.Text(self.menu_right_lower, borderwidth=2, relief="solid")
		self.txt_results.insert('1.0', 'Results: ')
		self.txt_results['state'] = 'disabled'
		self.txt_results.pack(side="top", fill="both", expand=True,pady=5,padx=5)
		
		self.txt_status = tk.Text(self.menu_left_lower, borderwidth=2, relief="solid")
		self.txt_status.insert('1.0', 'Status: ')
		self.txt_status['state'] = 'disabled'
		self.txt_status.grid(row=1,column=0,columnspan=4, rowspan=1,ipady=5,ipadx=5)
				
		# define sliders + label 
		self.deposit_slider_base = tk.Scale(self.menu_left_upper, from_=0, to=1000, resolution=0.5 , tickinterval=100, orient=HORIZONTAL)
		self.deposit_slider_base_description = tk.Label(self.menu_left_upper, text="Deposit value [base]: ")
		self.deposit_slider_exponent = tk.Scale(self.menu_left_upper, from_=1, to=6, resolution=1, tickinterval=1,orient=HORIZONTAL)
		self.deposit_slider_exponent_description = tk.Label(self.menu_left_upper, text="Deposit value [exponent]: ")
		self.tax_slider = tk.Scale(self.menu_left_upper, from_=0, to=20, resolution=0.01, tickinterval=5,orient=HORIZONTAL)
		self.tax_slider_description = tk.Label(self.menu_left_upper, text="Tax [%]:")
		self.custody_fee_slider = tk.Scale(self.menu_left_upper, from_=0, to=20, resolution=0.01, tickinterval=5,orient=HORIZONTAL)
		self.custody_fee_slider_description = tk.Label(self.menu_left_upper, text="Custody fee [%]: ")
		self.interest_slider = tk.Scale(self.menu_left_upper, from_=0, to=50, resolution=0.01, tickinterval=5,orient=HORIZONTAL)
		self.interest_slider_description = tk.Label(self.menu_left_upper, text="Interest [%]: ")
		self.running_costs_slider = tk.Scale(self.menu_left_upper, from_=0, to=20, resolution=0.01, tickinterval=2,orient=HORIZONTAL)
		self.running_costs_slider_description = tk.Label(self.menu_left_upper, text="Running costs [%]: ")
		self.nbr_years_slider = tk.Scale(self.menu_left_upper, from_=0, to=100, resolution=1, tickinterval=10,orient=HORIZONTAL)
		self.nbr_years_slider_description = tk.Label(self.menu_left_upper, text="Number of years [years]: ")
		
		# define slider placement in GUI
		self.deposit_slider_base.grid(row=0,column=1,sticky="we",padx=5,pady=5)
		self.deposit_slider_base_description.grid(row=0,column=0,sticky="we",padx=5,pady=5)
		self.deposit_slider_exponent.grid(row=1,column=1,sticky="we",padx=5,pady=5)
		self.deposit_slider_exponent_description.grid(row=1,column=0,sticky="we",padx=5,pady=5)
		self.tax_slider.grid(row=2,column=1,sticky="we",padx=5,pady=5)
		self.tax_slider_description.grid(row=2,column=0,sticky="we",padx=5,pady=5)
		self.custody_fee_slider.grid(row=3,column=1,sticky="we",padx=5,pady=5)
		self.custody_fee_slider_description.grid(row=3,column=0,sticky="we",padx=5,pady=5)
		self.interest_slider.grid(row=4,column=1,sticky="we",padx=5,pady=5)
		self.interest_slider_description.grid(row=4,column=0,sticky="we",padx=5,pady=5)
		self.running_costs_slider.grid(row=5,column=1,sticky="we",padx=5,pady=5)
		self.running_costs_slider_description.grid(row=5,column=0,sticky="we",padx=5,pady=5)
		self.nbr_years_slider.grid(row=6,column=1,sticky="we",padx=5,pady=5)
		self.nbr_years_slider_description.grid(row=6,column=0,sticky="we",padx=5,pady=5)
		
		# slider 3 times size of label
		self.menu_left_upper.columnconfigure(1,weight=3)
		

		# define dropdown elements and placement
		market_list = ["Euronext Brussels","Euronext Paris","Euronext Amsterdam","Euronext Lisboa","Euronext Dublin","Euronext Expert Market","NYSE","NYSE Amex","NYSE MKT","Nasdaq",
        "OTC BB","Toronto","Germany","Czechia","Hungary","Poland","Sweden","Switserland","UK","Spain","Denmark","Italy","Norway","Finland","Austria","Luxembourg","Greece","Ireland",
            "South-Africa","Australia","Hong Kong","Japan"]
		frequency_list = ["Monthly","Bi-Monthly","Trimester","Four-Monthly","Semester","Yearly"]

		self.market_dropdown = ttk.Combobox(self.menu_left_upper,values=market_list,state="readonly")
		self.market_dropdown_description = tk.Label(self.menu_left_upper, text="Market: ")
		self.frequency_dropdown = ttk.Combobox(self.menu_left_upper,values=frequency_list,state="readonly")
		self.frequency_dropdown_description = tk.Label(self.menu_left_upper, text="Frequency: ")

		self.market_dropdown_description.grid(row=7,column=0,sticky="we",padx=5,pady=5)
		self.market_dropdown.grid(row=7,column=1,sticky="we",padx=5,pady=5)
		self.frequency_dropdown_description.grid(row=8,column=0,sticky="we",padx=5,pady=5)
		self.frequency_dropdown.grid(row=8,column=1,sticky="we",padx=5,pady=5)

		# define buttons and placement
		self.btn_calculate = tk.Button(self.menu_left_lower,text="Calculate")
		self.btn_plot = tk.Button(self.menu_left_lower, text="Plot graph") # ,command=plot_graph)
		self.btn_reset = tk.Button(self.menu_left_lower, text="Reset") #,command=reset_interface)

		self.btn_calculate.grid(row=0,column=0, pady=5, padx=5,sticky="we")
		self.btn_plot.grid(row=0,column=1, pady=5, padx=5,sticky="we")
		self.btn_reset.grid(row=0,column=2, pady=5, padx=5,sticky="we")
		
		# define plot area and placement
		self.fig = Figure(figsize=(5,5),dpi=100)
		self.plt_graph = self.fig.add_subplot(111)
		
		self.plt_canvas = FigureCanvasTkAgg(self.fig,self.menu_right_upper)
		self.plt_canvas.draw()
		self.plt_canvas.get_tk_widget().pack(side="top",fill="both",expand=True)

		self.plt_toolbar = NavigationToolbar2Tk(self.plt_canvas,self.menu_right_upper)
		self.plt_toolbar.update()
		self.plt_canvas._tkcanvas.pack(side="top",fill="both",expand=True)

	# calculate brokerage fee 
	def calculate_brokerage_fee(value, market):
			
		if market in ["Euronext Brussels","Euronext Paris","Euronext Amsterdam","Euronext Lisboa","Euronext Dublin"]:
			if (value <= 2500):
				fee = 7.5
				
			elif (value <= 70000):
				fee = 15*(value//10000) + 7.5
				fee = fee if fee <= 50 else 50
			else:
				fee = 50 + 15*(value//10000)
			
		elif market in ["Euronext Expert Market"]:
			fee = value*0.01 if value >=30 else 30
		
		elif market in ["NYSE","NYSE Amex","NYSE MKT","Nasdaq","OTC BB"]:                                   
			if (value <=2500):
				fee = 15
			elif (value <=70000):
				fee = 20*(value//10000) + 15
				fee = fee if fee <=50 else 50
			else:
				fee = 50 + 20*(value//10000)
		
		elif market in ["Toronto"]:
			if (value <= 2500):
				fee = 15
			else:
				fee = value*0.005
				fee = fee if fee >=20 else 20
			
		elif market in ["Germany"]:
			if (value <= 2500):
				fee = 15
			elif (value <= 70000):
				fee = 30*(value//10000) + 15
				fee = fee if fee <= 60 else 60
			else:
				fee = value*0.0015
						
		elif market in ["Czechia","Hungary","Poland"]:
			if (value <= 2500):
				fee = 7.5
			elif (value <= 70000):
				fee = 15*(value//10000) + 7.5
				fee = fee if fee <= 50 else 50
			else: 
				fee = 50 + 15*(value//10000)
						
		elif market in ["Sweden","Switserland","UK","Spain","Denmark","Italy","Norway","Finland","Austria","Luxembourg"]:
			fee = 15 
			if (value <=2500):
				fee = 15
			else:
				fee = value*0.0050
				fee = fee if fee >= 30 else 30
									
		elif market in ["Greece","Ireland","South-Africa","Australia","Hong Kong","Japan"]:                     
			fee = value*0.01 if value >= 75 else 75
		else:
			print("Error calculating Brokerage fee")
			fee = -1
		return fee

	# calculate how many deposits per year from slider value
	def calculate_deposit_frequency(value):
		if (value == "Monthly"):
			return 12
		elif (value == "Bi-Monthly"):
			return 6
		elif (value == "Trimester"):
			return 4
		elif (value == "Four-Monthly"):
			return 3
		elif (value == "Semester"):
			return 2        
		elif (value == "Yearly"):
			return 1
		else:
			return 0

	# calculate accumulated value 
	def calculate_accumulated_value(deposit,frequency, interest, running_cost, custody_fee, time):
		# interest per deposit (time dependent)
		interests = np.linspace(0,12,num=frequency,endpoint=False)
		
		accumulated_sum = 0 
		accumulated_sum_list = []
		
		accumulated_deposits = 0
		accumulated_deposits_list = []
		
		for year in range(0,time):
			yearly_sum = 0
			deposits = 0
			for i in interests:
				yearly_sum += deposit*((1+interest)**((12-i)/12))
				deposits += deposit

			accumulated_sum += yearly_sum*(1+interest)**(year)
			accumulated_sum -= accumulated_sum*running_cost # running costs subtracted at the end of financial year        
			accumulated_sum -= accumulated_sum*custody_fee  # custody_fee calculated after running cost subtraction
			accumulated_sum_list.append(accumulated_sum)
			
			accumulated_deposits += deposits
			accumulated_deposits_list.append(accumulated_deposits)
		
		#plot graph
		if (graph_checkbox.value == True):
			plot_accumulated_value(accumulated_sum_list,accumulated_deposits_list,time,interest)
		
		return accumulated_sum
	
	# plot graph
	def plot_accumulated_value(accumulated_sum,accumulated_deposits,years,interest):
		# config graph
		#clear_output(wait=True)
		plt.clf()
		plt.rcParams.update({
			"font.size":12.0
			})
		plt.rcParams['figure.figsize'] = [10, 10] # size in cm
		
		plt.grid(which='minor', alpha=0.2)
		plt.grid(which='major', alpha=0.2)

		plt.ylabel(r'Stock value [€]')
		plt.xlabel(r'Number of years [years]')
		
		# plot graph
		years_list = np.linspace(0,years,num=years)
			
		#adjust accumulated sum for taxes and fee (not done in accumulated sum calculation)
		fee = calculate_brokerage_fee(int(value_slider.value),market_dropdown.value)
		freq = calculate_deposit_frequency(deposit_slider.value)
		fee_overhead = fee * freq
		buyers_tax = tax_slider.value*int(value_slider.value)/100
		taxes_per_year = buyers_tax * freq
		
		for i in range(1,(len(years_list)+1)):
			accumulated_sum[(i-1)] -= (fee_overhead*i)
			accumulated_sum[(i-1)] -= (taxes_per_year*i)
			#print("Corrected acc sum: " + str(accumulated_sum[(i-1)]))
		
		breakeven_text.value = "Break even time estimate [years]: not reached with current configuration!"
		for i in range(len(accumulated_sum)):
			if accumulated_sum[i] > accumulated_deposits[i]:
				breakeven_text.value = "Break even time estimate [years]: " + str(i)
				break
		
			
		plt.plot(years_list,accumulated_sum, label=r'Accumulated sum', linewidth=2, color='blue')
		plt.plot(years_list,accumulated_deposits, label=r'Accumulated deposits', linewidth=1, color='black')
		plt.fill_between(years_list,accumulated_sum,accumulated_deposits,where=np.array(accumulated_sum)>np.array(accumulated_deposits),interpolate=True,color='green',alpha=0.2,label=r'Profit')
		plt.fill_between(years_list,accumulated_sum,accumulated_deposits,where=np.array(accumulated_sum)<np.array(accumulated_deposits),interpolate=True,color='red',alpha=0.2,label=r'Loss')
		plt.legend(loc='best')
		plt.show()

	def interface_change(change):
		# calculations TODO clean
		fee = calculate_brokerage_fee(int(value_slider.value),market_dropdown.value)
		fee_pct = (fee/int(value_slider.value))*100    
		freq = calculate_deposit_frequency(deposit_slider.value)
		fee_overhead = fee * freq
		nbr_years = nbr_years_slider.value
		total_deposit = int(value_slider.value)*freq*nbr_years
		buyers_tax = tax_slider.value*int(value_slider.value)/100
		taxes_per_year = buyers_tax * freq
		custody_fee_pct = custody_fee_slider.value/100
		custody_fee = total_deposit * custody_fee_pct
		interest_pct = interest_slider.value/100
		running_costs_pct = (running_costs_slider.value/100)
		accumulated_sum = calculate_accumulated_value(int(value_slider.value),freq, interest_pct, running_costs_pct, custody_fee_pct, nbr_years)
		running_costs = accumulated_sum * running_costs_pct
		total_taxes = taxes_per_year * nbr_years
		total_fees = fee_overhead * nbr_years
		profit = accumulated_sum - total_deposit - total_fees - total_taxes
		profit_pct = profit/total_deposit
			
		
		# display
		fee_text.value = "Fee per deposit of € {deposit}: € {fee}".format(deposit=int(value_slider.value), fee=fee)
		fee_percentage_text.value = "Fee overhead per deposit: {fee} / {deposit} = {p:.2f} %".format(fee=fee, deposit=int(value_slider.value), p = fee_pct) 
		buyers_tax_text.value = "Taxes per deposit: € {tax:.2f} [{tax_pct:.2f} %]".format(tax=buyers_tax,tax_pct=tax_slider.value)
		
		total_deposit_text.value = "Total deposited value: ({freq} x € {deposit}) x {years} = € {total}".format(freq=freq, deposit=int(value_slider.value), total=total_deposit, years=nbr_years)
		fee_overhead_text.value = "Fee per year: {fee} x {freq} = € {fee_overhead} ".format(fee=fee,freq=freq ,fee_overhead=fee_overhead)
		total_tax_text.value = "Taxes per year: {tax:.2f} x {freq} = € {taxes_year:.2f}".format(tax=buyers_tax,freq=freq,taxes_year=taxes_per_year)
		custody_fee_text.value = "Custody fee per year: € {fee:.2f}".format(fee=custody_fee)
		running_costs_text.value = "Current running costs: {running_costs_pct:.2f} x {total_profit:.2f} = € {running_costs:.2f}".format(running_costs_pct=running_costs_slider.value, total_profit=accumulated_sum, running_costs=running_costs)
		profit_text.value = "Profit after {years} years: accumulated_sum - taxes - deposit_fees = {accumulated_sum:.2f} - {taxes:.2f} - {deposit_fees:.2f} = {profit:.2f} [{profit_pct:.2f} %]".format(years=nbr_years, accumulated_sum=accumulated_sum, taxes=total_taxes, deposit_fees=total_fees,profit=profit, profit_pct=profit_pct*100)

	# connect components to callback: interface_change
	#value_slider.observe(interface_change, names='value')
	#deposit_slider.observe(interface_change,names='value')
	#market_dropdown.observe(interface_change,names='value')
	#tax_slider.observe(interface_change,names='value')
	#custody_fee_slider.observe(interface_change,names='value')
	#running_costs_slider.observe(interface_change,names='value')
	#interest_slider.observe(interface_change,names='value')
	#nbr_years_slider.observe(interface_change,names='value')
	#graph_checkbox.observe(interface_change,names='value')

	### reset interface ###
	def resetInterface(_):
		# reset sliders
		value_slider.value = 10
		tax_slider.value = 1
		custody_fee_slider.value = 1
		running_costs_slider.value = 1
		interest_slider.value = 1
		nbr_years_slider.value = 5
		
		market_dropdown.value = "Euronext Brussels"
		market_dropdown.selected_label = "Euronext Brussels"
		graph_checkbox.value = False
		
		# reset texts
		fee_text.value = ""
		fee_percentage_text.value = ""
		fee_overhead_text.value = ""
		total_deposit_text.value = ""
		deposit_slider.value = 'Trimester'
		buyers_tax_text.value = ""
		total_tax_text.value  = ""
		custody_fee_text.value = ""
		running_costs_text.value = ""
		profit_text.value = ""
		breakeven_text.value = ""
		plt.clf()


if __name__ == "__main__":
    app = StockCalculator()
    app.mainloop()

