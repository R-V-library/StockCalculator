import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import *
from tkinter import messagebox
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

		self.menu_left_upper.grid(row=0,column=0,sticky="nsew")
		self.menu_left_lower.grid(row=1,column=0,sticky="nsew")

        # menu right
		self.menu_right = tk.Frame(self, width=600, bg="#dfdfdf")
		self.menu_right_upper = tk.Frame(self.menu_right,width=600, height=400)
		self.menu_right_lower = tk.Frame(self.menu_right,width=600, height=250, bg="blue")

		self.menu_right_upper.grid(row=0,column=0,sticky="ew")
		self.menu_right_lower.grid(row=1,column=0,sticky="ew")
		self.menu_right.grid_columnconfigure(0,weight=1)
		
        # define frame positions on grid	
		self.menu_left.grid(row=0, column=0, rowspan=2, sticky="nsew")
		self.menu_right.grid(row=0,column=1, rowspan=2, sticky="nsew")
		
        # define grid 
		self.grid_rowconfigure(1, weight=1)
		self.grid_columnconfigure(1, weight=1)
		
		# define text fields and placement
		self.txt_results = tk.Text(self.menu_right_lower, borderwidth=2, relief="solid")
		self.txt_results.insert('1.0', 'Results: ')
		#self.txt_results['state'] = 'disabled'
		self.txt_results.pack(side="top", fill="both", expand=True,pady=5,padx=5)
		
		self.txt_status = tk.Text(self.menu_left_lower, borderwidth=2, relief="solid")
		self.txt_status.insert('1.0', 'Status: ')
		#self.txt_status['state'] = 'disabled'
		self.txt_status.grid(row=1,column=0,columnspan=4, rowspan=1,ipady=5,ipadx=5)
				
		# define sliders + label 
		self.tax_slider = tk.Scale(self.menu_left_upper, from_=0, to=10, resolution=0.01, tickinterval=5,orient=HORIZONTAL)
		self.tax_slider_description = tk.Label(self.menu_left_upper, text="Tax [%]:")
		self.custody_fee_slider = tk.Scale(self.menu_left_upper, from_=0, to=10, resolution=0.01, tickinterval=5,orient=HORIZONTAL)
		self.custody_fee_slider_description = tk.Label(self.menu_left_upper, text="Custody fee [%]: ")
		self.interest_slider = tk.Scale(self.menu_left_upper, from_=0, to=20, resolution=0.01, tickinterval=5,orient=HORIZONTAL)
		self.interest_slider_description = tk.Label(self.menu_left_upper, text="Interest [%]: ")
		self.running_costs_slider = tk.Scale(self.menu_left_upper, from_=0, to=10, resolution=0.01, tickinterval=2,orient=HORIZONTAL)
		self.running_costs_slider_description = tk.Label(self.menu_left_upper, text="Running costs [%]: ")
		self.nbr_years_slider = tk.Scale(self.menu_left_upper, from_=0, to=100, resolution=1, tickinterval=10,orient=HORIZONTAL)
		self.nbr_years_slider_description = tk.Label(self.menu_left_upper, text="Number of years [years]: ")
		
		# define slider placement in GUI
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

		self.market_dropdown_var = StringVar()
		self.market_dropdown = ttk.Combobox(self.menu_left_upper,values=market_list,state="readonly",textvariable=self.market_dropdown_var)
		self.market_dropdown.current(0)
		self.market_dropdown_description = tk.Label(self.menu_left_upper, text="Market: ")

		self.frequency_dropdown_var = StringVar()
		self.frequency_dropdown = ttk.Combobox(self.menu_left_upper,values=frequency_list,state="readonly",textvariable=self.frequency_dropdown_var)
		self.frequency_dropdown.current(0)
		self.frequency_dropdown_description = tk.Label(self.menu_left_upper, text="Frequency: ")

		self.market_dropdown_description.grid(row=7,column=0,sticky="we",padx=5,pady=5)
		self.market_dropdown.grid(row=7,column=1,sticky="we",padx=5,pady=5)
		self.frequency_dropdown_description.grid(row=8,column=0,sticky="we",padx=5,pady=5)
		self.frequency_dropdown.grid(row=8,column=1,sticky="we",padx=5,pady=5)

		# define buttons and placement
		self.btn_calculate = tk.Button(self.menu_left_lower,text="Calculate",command=self.perform_calculations)
		self.btn_plot = tk.Button(self.menu_left_lower, text="Plot graph",command=self.plot_accumulated_value) # ,command=plot_graph)
		self.btn_save = tk.Button(self.menu_left_lower, text="Save results")
		self.btn_reset = tk.Button(self.menu_left_lower, text="Reset",command=self.reset_interface)


		self.btn_calculate.grid(row=0,column=0, pady=5, padx=5,sticky="we")
		self.btn_plot.grid(row=0,column=1, pady=5, padx=5,sticky="we")
		self.btn_save.grid(row=0,column=2,padx=5,pady=5,sticky="we")
		self.btn_reset.grid(row=0,column=3, pady=5, padx=5,sticky="we")
		
		# define plot area and placement
		self.fig = Figure(figsize=(5,5),dpi=100)
		#matplotlib.rcParams.update({
		#	"font.size":12.0
		#})
		self.plt_graph = self.fig.add_subplot(111)
		self.plt_canvas = FigureCanvasTkAgg(self.fig,self.menu_right_upper)
		self.plt_canvas.draw()
		self.plt_canvas.get_tk_widget().pack(side="top",fill="both",expand=True)
		self.plt_toolbar = NavigationToolbar2Tk(self.plt_canvas,self.menu_right_upper)
		self.plt_toolbar.update()
		self.plt_canvas._tkcanvas.pack(side="top",fill="both",expand=True)

		# define deposit entries and placement
		self.regular_deposit_entry = ttk.Entry(self.menu_left_upper)
		self.regular_deposit_entry.insert(INSERT,"150")
		self.regular_deposit_entry_description = tk.Label(self.menu_left_upper, text="Regular deposit: ")
		self.initial_deposit_entry = ttk.Entry(self.menu_left_upper)
		self.initial_deposit_entry.insert(INSERT,"1000")
		self.initial_deposit_entry_description = tk.Label(self.menu_left_upper, text="Initial deposit: ")
		
		self.initial_deposit_entry.grid(row=0,column=1,sticky="we",padx=5,pady=5)
		self.initial_deposit_entry_description.grid(row=0,column=0,sticky="we",padx=5,pady=5)
		self.regular_deposit_entry.grid(row=1,column=1,sticky="we",padx=5,pady=5)
		self.regular_deposit_entry_description.grid(row=1,column=0,sticky="we",padx=5,pady=5)

	
	# convert entry to float
	def parse_entry(self,entry_value):
		try:
			parsed_value = float(entry_value)
			return parsed_value
		except:
			#TODO throw error message
			messagebox.showerror("Error", "Invalid entry input")
			return -1

	# calculate brokerage fee 
	def calculate_brokerage_fee(self, value, market):
		#print(f"Value: {value}, market: {market}")
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
	def calculate_deposit_frequency(self, value):
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
	def calculate_accumulated_value(self, initial_deposit, regular_deposit, frequency, interest, running_cost, custody_fee, time):
		
		# interest per deposit (time dependent)
		interests = np.linspace(0,12,num=frequency,endpoint=False)
		
		accumulated_sum = 0
		accumulated_sum_list = []
				
		accumulated_deposits = initial_deposit
		accumulated_deposits_list = []

		breakeven_period = -1
		

		for year in range(0,time):
			yearly_sum = 0
			deposits = 0
			for i in interests:
				yearly_sum += regular_deposit*((1+interest)**((12-i)/12))
				deposits += regular_deposit

			accumulated_sum += yearly_sum*(1+interest)**(year)
			accumulated_sum += initial_deposit*(1+interest)**year
			accumulated_sum -= accumulated_sum*running_cost # running costs subtracted at the end of financial year        
			accumulated_sum -= accumulated_sum*custody_fee  # custody_fee calculated after running cost subtraction
			accumulated_sum_list.append(accumulated_sum)
			
			accumulated_deposits += deposits
			accumulated_deposits_list.append(accumulated_deposits)
		#print(accumulated_deposits_list)
		#adjust accumulated sum for taxes and fee
		market = self.market_dropdown.get()
		initial_fee = self.calculate_brokerage_fee(initial_deposit, market) if initial_deposit > 0 else 0
		regular_fee = self.calculate_brokerage_fee(regular_deposit, market) if regular_deposit > 0 else 0 
		freq = self.calculate_deposit_frequency(frequency)
		fee_overhead = regular_fee * freq 
		tax_pct = self.tax_slider.get()
		regular_buyers_tax = tax_pct*regular_deposit/100
		initial_buyers_tax = tax_pct*initial_deposit/100
		taxes_per_year = regular_buyers_tax * freq
		
		accumulated_sum_list[0] -= initial_fee
		accumulated_sum_list[0] -= initial_buyers_tax
		for i in range(1,(time+1)):
			accumulated_sum_list[(i-1)] -= (fee_overhead*i)
			accumulated_sum_list[(i-1)] -= (taxes_per_year*i)


		# TODO: add break-even calculation + return 
		for i in range(len(accumulated_sum_list)):
			if accumulated_sum_list[i] >= accumulated_deposits_list[i]:
				breakeven_period = i
				break
		
		self.accumulated_sum_list = accumulated_sum_list
		self.accumulated_deposits_list = accumulated_deposits_list

		return accumulated_sum, breakeven_period
	
	# plot graph 
	def plot_accumulated_value(self):
		
		if self.nbr_years_slider.get() < 2:
			messagebox.showwarning("WARNING","[WARNING] Unable to plot with given parameters (number of years < 2).")
			return

		elif self.nbr_years_slider.get() != len(self.accumulated_sum_list):
			messagebox.showwarning("WARNING","[WARNING] Plot only possible after re-performing calculations.")
			return

		# config graph
		#clear_output(wait=True)
		self.plt_graph.clear() #change 
		#plt.rcParams['figure.figsize'] = [10, 10] # size in cm
		
		self.plt_graph.grid(which='minor', alpha=0.4)
		self.plt_graph.grid(which='major', alpha=0.4)

		self.plt_graph.set_ylabel(r'Stock value [€]')
		self.plt_graph.set_xlabel(r'Number of years [years]')
		
		# plot graph
		years  = self.nbr_years_slider.get()
		years_list = np.linspace(0,years,num=years)
							
		self.plt_graph.plot(years_list,self.accumulated_sum_list, label=r'Accumulated sum', linewidth=2, color='blue')
		self.plt_graph.plot(years_list,self.accumulated_deposits_list, label=r'Accumulated deposits', linewidth=1, color='black')
		self.plt_graph.fill_between(years_list,self.accumulated_sum_list,self.accumulated_deposits_list,where=np.array(self.accumulated_sum_list)>np.array(self.accumulated_deposits_list),interpolate=True,color='green',alpha=0.2,label=r'Profit')
		self.plt_graph.fill_between(years_list,self.accumulated_sum_list,self.accumulated_deposits_list,where=np.array(self.accumulated_sum_list)<np.array(self.accumulated_deposits_list),interpolate=True,color='red',alpha=0.2,label=r'Loss')
		self.plt_graph.legend(loc='best')
		self.plt_canvas.draw()

	# TODO rewrite 
	def perform_calculations(self):
		# calculations TODO clean

		# read input values 
		initial_deposit = self.parse_entry(self.initial_deposit_entry.get())
		regular_deposit = self.parse_entry(self.regular_deposit_entry.get()) 
		market = self.market_dropdown.get()
		deposit_frequency = self.frequency_dropdown.get()
		if self.nbr_years_slider.get() > 0:
			nbr_years = self.nbr_years_slider.get()
		else:
			nbr_years = 1
		#nbr_years = self.nbr_years_slider.get()  if (self.nbr_years_slider.get() > 0) else 1 
		tax_pct = self.tax_slider.get()/100
		custody_fee_pct = self.custody_fee_slider.get()/100
		interest_pct = self.interest_slider.get()/100
		running_costs_pct = self.running_costs_slider.get()/100

		# fee calculations 
		initial_fee = self.calculate_brokerage_fee(initial_deposit, market) if initial_deposit > 0 else 0
		regular_fee = self.calculate_brokerage_fee(regular_deposit, market) if regular_deposit > 0 else 0 
		initial_fee_pct = (initial_fee/initial_deposit)*100 if initial_deposit > 0 else 0
		regular_fee_pct = (regular_fee/regular_deposit)*100 if regular_deposit > 0 else 0
		freq = self.calculate_deposit_frequency(deposit_frequency)
		regular_fee_overhead = regular_fee * freq
		initial_fee_overhead = initial_fee
		total_fees = regular_fee_overhead * nbr_years + initial_fee_overhead
		
		# tax calculations 
		regular_buyers_tax = tax_pct * regular_deposit
		initial_buyers_tax = tax_pct * initial_deposit
		taxes_per_year = regular_buyers_tax * freq  
		total_taxes = taxes_per_year * nbr_years + initial_buyers_tax
		
		# accumulated sum and running costs 
		accumulated_sum, break_even_period = self.calculate_accumulated_value(initial_deposit,regular_deposit,freq, interest_pct, running_costs_pct, custody_fee_pct, nbr_years)
		running_costs = accumulated_sum * running_costs_pct

		# total deposit value 
		total_deposit = regular_deposit * freq * nbr_years + initial_deposit

		# custody fee
		custody_fee = total_deposit * custody_fee_pct
		
		# profit calculations 
		profit = accumulated_sum - total_deposit - total_fees - total_taxes
		profit_pct = profit/total_deposit if total_deposit > 0 else 0 
			
		# display #TODO add all texts to main textbox
		# display results in textbox 
		self.txt_results.delete(1.0,END) # clear contents 
		result_string = "Results: \n" 
		result_string += "Initial deposit fee per deposit of € {initial_deposit}: € {fee}\n".format(initial_deposit=initial_deposit, fee=initial_fee)
		result_string += "Initial deposit fee overhead: {fee} / {initial_deposit} = {p:.4f} %\n".format(fee=initial_fee, initial_deposit=initial_deposit, p = initial_fee_pct) 
		result_string += "Regular deposit fee per deposit of € {regular_deposit}: € {fee}\n".format(regular_deposit=regular_deposit, fee=regular_fee)
		result_string += "Regular deposit fee overhead: {fee} / {regular_deposit} = {p:.4f} %\n".format(fee=regular_fee, regular_deposit=regular_deposit, p = regular_fee_pct) 
		result_string += "Fee per year: {fee} x {freq} = € {fee_overhead} \n".format(fee=regular_fee, freq=freq, fee_overhead=regular_fee_overhead)
		result_string += "Taxes on initial deposit: € {tax:.4f} [{tax_pct:.4f} %]\n".format(tax=initial_buyers_tax, tax_pct=tax_pct)
		result_string += "Taxes per regular deposit: € {tax:.4f} [{tax_pct:.4f} %]\n".format(tax=regular_buyers_tax, tax_pct=tax_pct)
		result_string += "Taxes per year: {tax:.4f} x {freq} = € {taxes_year:.4f}\n".format(tax=regular_buyers_tax, freq=freq, taxes_year=taxes_per_year)
		result_string += "Custody fee current year: € {fee:.4f}\n".format(fee=custody_fee)
		result_string += "Current running costs: {running_costs_pct:.4f} x {total_profit:.4f} = € {running_costs:.4f}\n".format(running_costs_pct=running_costs_pct, total_profit=accumulated_sum, running_costs=running_costs)
		result_string += "Total deposited value: ({freq} x € {regular_deposit}) x {years} + {initial_deposit} = € {total}\n".format(freq=freq, regular_deposit=regular_deposit,initial_deposit=initial_deposit, total=total_deposit, years=nbr_years)		
		result_string += "Profit after {years} years: accumulated_sum - taxes - deposit_fees = {accumulated_sum:.4f} - {taxes:.4f} - {deposit_fees:.4f} = {profit:.4f} [{profit_pct:.4f} %]\n".format(years=nbr_years, accumulated_sum=accumulated_sum, taxes=total_taxes, deposit_fees=total_fees,profit=profit, profit_pct=profit_pct*100)
		result_string += "Estimated break even time: {breakeven} years\n".format(breakeven=break_even_period)
		self.txt_results.insert(INSERT,result_string)
	
	### reset interface ###
	# TODO rewrites
	def reset_interface(self):
		# reset sliders
		self.custody_fee_slider.set(0)
		self.interest_slider.set(0)
		self.nbr_years_slider.set(0)
		self.running_costs_slider.set(0)
		self.tax_slider.set(0)
		
		# reset entries
		self.initial_deposit_entry.delete(0,END)
		self.initial_deposit_entry.insert(0,"1000")
		self.regular_deposit_entry.delete(0,END)
		self.regular_deposit_entry.insert(0,"150")
		
		# reset dropdowns
		self.market_dropdown.set("Euronext Brussels")
		self.frequency_dropdown.set("Monthly")
				
		# reset texts
		self.txt_status.delete(1.0,END) # clear contents 
		self.txt_status.insert(INSERT,"Status: \n")
		self.txt_results.delete(1.0,END) # clear contents 
		self.txt_results.insert(INSERT,"Results: \n")

		#reset plot
		self.plt_graph.clear()
		self.plt_canvas.draw()
		

	# debugging 
	def print_status_box(self,value):
		print(self.txt_status.get())
		new_text = "Value: " + str(value) 
		self.txt_status.insert(tk.END,new_text)



if __name__ == "__main__":
    app = StockCalculator()
    app.mainloop()

