import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import asksaveasfilename
from tkinter import *
from tkinter import messagebox
from numpy import linspace, array
import matplotlib 

matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)

# Stolen from: https://stackoverflow.com/questions/20399243/display-message-when-hovering-over-something-with-mouse-cursor-in-python
# Display message when hovering mouse over object
###
class ToolTip(object):

    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 60
        y = y + cy + self.widget.winfo_rooty() + 30
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(tw, text=self.text, justify=LEFT,
                      background="#ffffe0", relief=SOLID, borderwidth=1,
                      font=("helvetica", "10", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

def CreateToolTip(widget, text):
    toolTip = ToolTip(widget)
    def enter(event):
        toolTip.showtip(text)
    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)
###

class StockCalculator(tk.Tk):
	def __init__(self):
		super().__init__()
		
		# init window size and grid size
		self.title("Stock Calculator")
		self.geometry("1280x720")
		#self.state("zoomed")
		self.resizable(True, True)
		
		# init layout 
		self.init_layout()
		
		# init text boxes 
		self.init_txt_elements()

		# init sliders 
		self.init_slider_elements()

		# init dropdowns
		self.init_dropdown_elements()
		
		# init buttons
		self.init_btn_elements()
		
		# init plot
		self.init_plot_area_elements()
		
		# init entries
		self.init_entry_elements()

		# add hover info
		self.init_hover_elements()

		# dict which stores all parameter values
		self.stock_parameters = {}
		
		# init parameters
		self.update_parameters()

	# define 4 frames which build GUI
	def init_layout(self):	 

		# menu left
		self.menu_left = tk.Frame(self, width=500)
		self.menu_left_upper = tk.Frame(self.menu_left, width=500, height=500) # menu with sliders 
		self.menu_left_lower = tk.Frame(self.menu_left, width=500, height=100) # menu with buttons 

		self.menu_left_upper.grid(row=0, column=0, sticky="nsew")
		self.menu_left_lower.grid(row=1, column=0, sticky="nsew")
		
		self.menu_left.rowconfigure(0, weight=1)
		self.menu_left.rowconfigure(1, weight=1)
		self.menu_left.grid_columnconfigure(0, weight=1)

        # menu right
		self.menu_right = tk.Frame(self, width=600)
		self.menu_right_upper = tk.Frame(self.menu_right, width=600, height=400) # plot area
		self.menu_right_lower = tk.Frame(self.menu_right, width=600, height=250) # result text area

		self.menu_right_upper.grid(row=0, column=0, sticky="nsew")
		self.menu_right_lower.grid(row=1, column=0, sticky="nsew")
		self.menu_right.grid_columnconfigure(0, weight=1)
		
        # define frame positions on grid	
		self.menu_left.grid(row=0, column=0, rowspan=2, sticky="nsew")
		self.menu_right.grid(row=0, column=1, rowspan=2, sticky="nsew")
		
        # define grid 
		self.grid_columnconfigure(0, weight=1)
		self.grid_columnconfigure(1, weight=1)
	

	# define text fields and placement
	def init_txt_elements(self):
				
		self.txt_results = tk.Text(self.menu_right_lower, borderwidth=2, relief="solid")
		self.txt_results.insert('1.0', 'Results: ')
		self.txt_results.pack(side="top", fill="both", expand=True, pady=5, padx=5)
		
		self.txt_status = tk.Text(self.menu_left_lower, borderwidth=2, relief="solid")
		self.txt_status.insert('1.0', 'Status: ')
		self.txt_status.grid(row=1, column=0, columnspan=4, rowspan=1, pady=5, padx=5)


	# define sliders and placement
	def init_slider_elements(self):

		# define sliders + label 
		self.tax_slider = tk.Scale(self.menu_left_upper, from_=0, to=10, resolution=0.01, tickinterval=1, orient=HORIZONTAL, command=self.update_parameters)
		self.tax_slider_description = tk.Label(self.menu_left_upper, text="Tax [%]:")
		self.custody_fee_slider = tk.Scale(self.menu_left_upper, from_=0, to=10, resolution=0.01, tickinterval=1,orient=HORIZONTAL, command=self.update_parameters)
		self.custody_fee_slider_description = tk.Label(self.menu_left_upper, text="Custody fee [%]: ")
		self.interest_slider = tk.Scale(self.menu_left_upper, from_=0, to=20, resolution=0.01, tickinterval=2,orient=HORIZONTAL, command=self.update_parameters)
		self.interest_slider_description = tk.Label(self.menu_left_upper, text="Interest [%]: ")
		self.running_costs_slider = tk.Scale(self.menu_left_upper, from_=0, to=10, resolution=0.01, tickinterval=1, orient=HORIZONTAL, command=self.update_parameters)
		self.running_costs_slider_description = tk.Label(self.menu_left_upper, text="Running costs [%]: ")
		self.nbr_years_slider = tk.Scale(self.menu_left_upper, from_=0, to=100, resolution=1, tickinterval=10, orient=HORIZONTAL, command=self.update_parameters)
		self.nbr_years_slider_description = tk.Label(self.menu_left_upper, text="Number of years [years]: ")
		
		# define slider placement in GUI
		self.tax_slider.grid(row=2, column=1, sticky="we", padx=5, pady=5)
		self.tax_slider_description.grid(row=2, column=0, sticky="we", padx=5, pady=5)
		self.custody_fee_slider.grid(row=3, column=1, sticky="we", padx=5, pady=5)
		self.custody_fee_slider_description.grid(row=3, column=0, sticky="we", padx=5, pady=5)
		self.interest_slider.grid(row=4, column=1, sticky="we", padx=5, pady=5)
		self.interest_slider_description.grid(row=4, column=0, sticky="we", padx=5, pady=5)
		self.running_costs_slider.grid(row=5, column=1, sticky="we", padx=5, pady=5)
		self.running_costs_slider_description.grid(row=5, column=0, sticky="we", padx=5, pady=5)
		self.nbr_years_slider.grid(row=6, column=1, sticky="we", padx=5, pady=5)
		self.nbr_years_slider_description.grid(row=6, column=0, sticky="we", padx=5, pady=5)
		
		# slider 3 times size of label
		self.menu_left_upper.columnconfigure(1, weight=3)
	

	# define dropdown elements and placement
	def init_dropdown_elements(self):
		market_list = ["Euronext Brussels","Euronext Paris","Euronext Amsterdam","Euronext Lisboa","Euronext Dublin","Euronext Expert Market","NYSE","NYSE Amex","NYSE MKT","Nasdaq",
        "OTC BB","Toronto","Germany","Czechia","Hungary","Poland","Sweden","Switserland","UK","Spain","Denmark","Italy","Norway","Finland","Austria","Luxembourg","Greece","Ireland",
            "South-Africa","Australia","Hong Kong","Japan"]
		frequency_list = ["Monthly","Bi-Monthly","Trimester","Four-Monthly","Semester","Yearly"]

		self.market_dropdown_var = StringVar()
		self.market_dropdown = ttk.Combobox(self.menu_left_upper, values=market_list, state="readonly", textvariable=self.market_dropdown_var, validate="focusout", validatecommand=self.update_parameters)
		self.market_dropdown.current(0)
		self.market_dropdown_description = tk.Label(self.menu_left_upper, text="Market: ")

		self.frequency_dropdown_var = StringVar()
		self.frequency_dropdown = ttk.Combobox(self.menu_left_upper, values=frequency_list, state="readonly", textvariable=self.frequency_dropdown_var, validate="focusout", validatecommand=self.update_parameters)
		self.frequency_dropdown.current(0)
		self.frequency_dropdown_description = tk.Label(self.menu_left_upper, text="Frequency: ")

		self.market_dropdown_description.grid(row=7, column=0, sticky="we", padx=5, pady=5)
		self.market_dropdown.grid(row=7, column=1, sticky="we", padx=5, pady=5)
		self.frequency_dropdown_description.grid(row=8, column=0, sticky="we", padx=5, pady=5)
		self.frequency_dropdown.grid(row=8, column=1, sticky="we", padx=5, pady=5)


	# define buttons and placement	
	def init_btn_elements(self):

		self.btn_calculate = tk.Button(self.menu_left_lower, text="Calculate", command=self.perform_calculations)
		self.btn_plot = tk.Button(self.menu_left_lower, text="Plot graph", command=self.plot_accumulated_value)
		self.btn_save = tk.Button(self.menu_left_lower, text="Save results", command=self.save_results)
		self.btn_reset = tk.Button(self.menu_left_lower, text="Reset", command=self.reset_interface)

		self.btn_calculate.grid(row=0, column=0, pady=5, padx=5, sticky="we")
		self.btn_plot.grid(row=0, column=1, pady=5, padx=5, sticky="we")
		self.btn_save.grid(row=0, column=2,padx=5, pady=5, sticky="we")
		self.btn_reset.grid(row=0, column=3, pady=5, padx=5, sticky="we")


	# define plot area and placement	
	def init_plot_area_elements(self):

		self.fig = Figure(figsize=(5,5), dpi=100)
		
		self.plt_graph = self.fig.add_subplot(111)
		self.plt_graph.title.set_text("Stock Calculator: results plot")
		self.plt_graph.grid(which='minor', alpha=0.4)
		self.plt_graph.grid(which='major', alpha=0.4)
		self.plt_graph.set_ylabel(r'Stock value [€]')
		self.plt_graph.set_xlabel(r'Number of years [years]')

		self.plt_canvas = FigureCanvasTkAgg(self.fig, self.menu_right_upper)
		self.plt_canvas.draw()
		self.plt_canvas.get_tk_widget().pack(side="top", fill="both", expand=True)

		self.plt_toolbar = NavigationToolbar2Tk(self.plt_canvas, self.menu_right_upper)
		self.plt_toolbar.update()
		self.plt_canvas._tkcanvas.pack(side="top", fill="both", expand=True)


	# define deposit entries and placement
	def init_entry_elements(self):
		
		self.regular_deposit_entry_var = StringVar()
		self.regular_deposit_entry = ttk.Entry(self.menu_left_upper, textvariable=self.regular_deposit_entry_var, validate="focusout", validatecommand=self.update_parameters)
		self.regular_deposit_entry.insert(INSERT, "150")
		self.regular_deposit_entry_description = tk.Label(self.menu_left_upper, text="Regular deposit: ")

		self.initial_deposit_entry_var = StringVar()
		self.initial_deposit_entry = ttk.Entry(self.menu_left_upper, textvariable=self.initial_deposit_entry_var, validate="focusout", validatecommand=self.update_parameters)
		self.initial_deposit_entry.insert(INSERT, "1000")
		self.initial_deposit_entry_description = tk.Label(self.menu_left_upper, text="Initial deposit: ")
		
		self.initial_deposit_entry.grid(row=0, column=1, sticky="we", padx=5, pady=5)
		self.initial_deposit_entry_description.grid(row=0, column=0, sticky="we", padx=5, pady=5)
		self.regular_deposit_entry.grid(row=1, column=1, sticky="we", padx=5, pady=5)
		self.regular_deposit_entry_description.grid(row=1, column=0, sticky="we", padx=5, pady=5)


	# define tooltip hover 
	def init_hover_elements(self):
		# entries
		CreateToolTip(self.initial_deposit_entry_description, "Initial deposit that is transferred to the brokerage account.")
		CreateToolTip(self.regular_deposit_entry_description, "Deposit that is transferred to the brokerage account on a regular basis.")

		# sliders 
		CreateToolTip(self.tax_slider_description, "Taxes to be payed during the acquisition of the stock(s).")
		CreateToolTip(self.custody_fee_slider_description, "Annual fee charged by broker for storing one your stocks.")
		CreateToolTip(self.interest_slider_description, "Average expected interest rate.")
		CreateToolTip(self.running_costs_slider_description, "Annual fee deducted from stock by expeditor of the stock (aka expense ratio).")
		CreateToolTip(self.nbr_years_slider_description, "Number of years invested in stock.")

		# dropdowns
		CreateToolTip(self.market_dropdown_description, "Stock market where stock is registered.")
		CreateToolTip(self.frequency_dropdown_description, "Frequency during which stocks are acquired via the regular deposit.")

		# buttons
		CreateToolTip(self.btn_calculate, "Perform calculations with selected parameters.")
		CreateToolTip(self.btn_plot, "Plot accumulated sum of stock value with selected parameters.")
		CreateToolTip(self.btn_save, "Save current parameters and results to a text file.")
		CreateToolTip(self.btn_reset, "Reset interface and parameters to default values.")


	# convert entry to float value
	def __parse_entry(self, entry_value):
		try:
			parsed_value = float(entry_value)
			return parsed_value
		except: # print error message if unsuccessful
			messagebox.showerror("Error", "[ERROR] Invalid entry input.")
			self.print_status_box("[ERROR] Invalid entry input.")
			return 


	# update dict which stores values per parameter
	def update_parameters(self, *args, **kwargs):
		self.stock_parameters['initial_deposit'] = self.__parse_entry(self.initial_deposit_entry.get())
		self.stock_parameters['regular_deposit'] = self.__parse_entry(self.regular_deposit_entry.get())
		self.stock_parameters['market'] = self.market_dropdown.get()
		self.stock_parameters['initial_fee'] = self.__calculate_brokerage_fee(self.stock_parameters['market'], self.stock_parameters['initial_deposit']) 
		self.stock_parameters['regular_fee'] = self.__calculate_brokerage_fee(self.stock_parameters['market'], self.stock_parameters['regular_deposit']) 
		self.stock_parameters['deposit_frequency'] = self.frequency_dropdown.get()
		self.stock_parameters['frequency'] = self.__calculate_deposit_frequency(self.stock_parameters['deposit_frequency'])
		self.stock_parameters['nbr_years'] = self.nbr_years_slider.get()
		self.stock_parameters['tax_pct'] = self.tax_slider.get()/100
		self.stock_parameters['custody_fee_pct'] = self.custody_fee_slider.get()/100
		self.stock_parameters['interest_pct'] = self.interest_slider.get()/100
		self.stock_parameters['running_costs_pct'] = self.running_costs_slider.get()/100
		self.stock_parameters['regular_fee_overhead'] = self.stock_parameters['regular_fee'] * self.stock_parameters['frequency']
		self.stock_parameters['regular_buyers_tax'] = self.stock_parameters['regular_deposit'] * self.stock_parameters['tax_pct']
		self.stock_parameters['initial_buyers_tax'] = self.stock_parameters['initial_deposit'] * self.stock_parameters['tax_pct']
		self.stock_parameters['taxes_per_year'] = self.stock_parameters['regular_buyers_tax'] * self.stock_parameters['frequency']
		self.stock_parameters['accumulated_sum_list'] = [self.stock_parameters['initial_deposit']]
		self.stock_parameters['accumulated_deposits_list'] = [self.stock_parameters['initial_deposit']]
		self.stock_parameters['breakeven'] = 0

		# flag indicating that parameters have changed
		self.stock_parameters['updated'] = True
		
		#print(self.stock_parameters)
		

	# get stock parameter dict	
	def get_parameters(self):
		return self.stock_parameters
		

	# calculate brokerage fee 
	def __calculate_brokerage_fee(self, market, value):
		fee = 0
		
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

		return fee


	# calculate how many deposits per year from slider value
	def __calculate_deposit_frequency(self, value):
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
			messagebox.showerror("ERROR","[ERROR] Unable to calculate deposit frequency.")
			self.print_status_box("[ERROR] Unable to calculate deposit frequency.")
			return 0


	# calculate accumulated value 
	def calculate_accumulated_value(self):
		parameter_dict = self.get_parameters()

		# interest per deposit (time dependent)
		interests = linspace(0,12,num=parameter_dict['frequency'], endpoint=False)
		
		accumulated_sum = parameter_dict['initial_deposit']
		accumulated_sum_list = []
				
		accumulated_deposits = parameter_dict['initial_deposit']
		accumulated_deposits_list = []
		
		# calculate sum after one year
		yearly_sum = 0
		deposits = 0
		for i in interests:
			yearly_sum += parameter_dict['regular_deposit']*(1 + parameter_dict['interest_pct']*((12-i)/12))
			deposits += parameter_dict['regular_deposit']
		
		if (parameter_dict['nbr_years'] == 0):
			accumulated_sum = parameter_dict['initial_deposit']
			breakeven_period = -1
			
		else:

			for _ in range(0, parameter_dict['nbr_years']):
				accumulated_sum *= (1 + parameter_dict['interest_pct'])
				accumulated_sum += yearly_sum
				accumulated_deposits += deposits
				accumulated_sum -= accumulated_sum * parameter_dict['running_costs_pct'] # running costs subtracted at the end of financial year        
				accumulated_sum -= accumulated_sum * parameter_dict['custody_fee_pct']   # custody_fee calculated after running cost subtraction
				accumulated_sum_list.append(accumulated_sum)
				accumulated_deposits_list.append(accumulated_deposits)

			#print(accumulated_sum_list)
			
			#adjust accumulated sum for taxes and fee		
			# accumulated_sum_list[0] -= parameter_dict['initial_fee']
			# accumulated_sum_list[0] -= parameter_dict['initial_buyers_tax']
			# for i in range(1, (parameter_dict['nbr_years']+1)):
			# 	accumulated_sum_list[(i-1)] -= (parameter_dict['regular_fee_overhead'] * i)
			# 	accumulated_sum_list[(i-1)] -= (parameter_dict['taxes_per_year'] * i)

			# break-even calculation 
			breakeven_period = -1
			for i in range(len(accumulated_sum_list)):
				if accumulated_sum_list[i] >= accumulated_deposits_list[i]:
					breakeven_period = i
					break
			
			self.stock_parameters['accumulated_sum_list'] = accumulated_sum_list
			self.stock_parameters['accumulated_deposits_list'] = accumulated_deposits_list
			self.stock_parameters['breakeven'] = breakeven_period

	# plot graph 
	def plot_accumulated_value(self):
		parameter_dict = self.get_parameters()

		if self.nbr_years_slider.get() < 2:
			messagebox.showwarning("WARNING","[WARNING] Unable to plot with given parameters (number of years < 2).")
			self.print_status_box("[WARNING] Unable to plot with given parameters (number of years < 2).")
			return

		elif parameter_dict['updated'] == True:
			self.perform_calculations()
			#messagebox.showwarning("WARNING","[WARNING] Plot only possible after re-performing calculations.")
			#self.print_status_box("[WARNING] Plot only possible after re-performing calculations.")
			#return

		# clear graph
		self.plt_graph.clear()
		self.plt_graph.title.set_text("Stock Calculator: results plot")
		self.plt_graph.grid(which='minor', alpha=0.4)
		self.plt_graph.grid(which='major', alpha=0.4)
		self.plt_graph.set_ylabel(r'Stock value [€]')
		self.plt_graph.set_xlabel(r'Number of years [years]')
		
		# plot graph
		years  = parameter_dict['nbr_years']
		years_list = linspace(0, years,num=years)
							
		self.plt_graph.plot(years_list, parameter_dict['accumulated_sum_list'], label=r'Accumulated sum', linewidth=2, color='blue')
		self.plt_graph.plot(years_list, parameter_dict['accumulated_deposits_list'], label=r'Accumulated deposits', linewidth=1, color='black')
		self.plt_graph.fill_between(years_list, parameter_dict['accumulated_sum_list'], parameter_dict['accumulated_deposits_list'], where=array(parameter_dict['accumulated_sum_list']) > array(parameter_dict['accumulated_deposits_list']), interpolate=True, color='green', alpha=0.2, label=r'Profit')
		self.plt_graph.fill_between(years_list, parameter_dict['accumulated_sum_list'], parameter_dict['accumulated_deposits_list'], where=array(parameter_dict['accumulated_sum_list']) < array(parameter_dict['accumulated_deposits_list']), interpolate=True, color='red', alpha=0.2, label=r'Loss')
		self.plt_graph.legend(loc='best')
		self.plt_canvas.draw()
		self.print_status_box("[INFO] Plot drawn succesfully.")


	# calculate results
	def perform_calculations(self):
		
		# get parameters
		self.update_parameters()
		parameter_dict = self.get_parameters()

		# fee calculations  
		initial_fee_pct = (parameter_dict['initial_fee']/parameter_dict['initial_deposit']) * 100 if parameter_dict['initial_deposit'] > 0 else 0
		regular_fee_pct = (parameter_dict['regular_fee']/parameter_dict['regular_deposit']) * 100 if parameter_dict['regular_deposit'] > 0 else 0
		total_fees = parameter_dict['regular_fee_overhead'] * parameter_dict['nbr_years']   + parameter_dict['initial_fee']
		
		# tax calculations 
		total_taxes = parameter_dict['taxes_per_year'] * parameter_dict['nbr_years'] + parameter_dict['initial_buyers_tax']
		
		# accumulated sum and current running costs 
		self.calculate_accumulated_value()
		accumulated_sum =  parameter_dict['accumulated_sum_list'][-1] 
		break_even_period = parameter_dict['breakeven']
		running_costs = accumulated_sum * parameter_dict['running_costs_pct']

		# total deposit value 
		total_deposit = parameter_dict['regular_deposit'] * parameter_dict['frequency'] * parameter_dict['nbr_years'] + parameter_dict['initial_deposit']

		# custody fee
		custody_fee = total_deposit * parameter_dict['custody_fee_pct']
		
		# profit calculations 
		profit = accumulated_sum - total_deposit - total_fees - total_taxes
		profit_pct = profit/total_deposit if total_deposit > 0 else 0 
			
		# display results in textbox 
		self.txt_results.delete(1.0, END) # clear contents 
		result_string = "Results: \n" 
		result_string += "Initial deposit fee per deposit of € {initial_deposit}: € {fee}\n".format(initial_deposit=parameter_dict['initial_deposit'], fee=parameter_dict['initial_fee'])
		result_string += "Initial deposit fee overhead: {fee} / {initial_deposit} = {p:.2f} %\n".format(fee=parameter_dict['initial_fee'], initial_deposit=parameter_dict['initial_deposit'], p = initial_fee_pct) 
		result_string += "Regular deposit fee per deposit of € {regular_deposit}: € {fee}\n".format(regular_deposit=parameter_dict['regular_deposit'], fee=parameter_dict['regular_fee'])
		result_string += "Regular deposit fee overhead: {fee} / {regular_deposit} = {p:.2f} %\n".format(fee=parameter_dict['regular_fee'], regular_deposit=parameter_dict['regular_deposit'], p = regular_fee_pct) 
		result_string += "Fee per year: {fee} x {freq} = € {fee_overhead} \n".format(fee=parameter_dict['regular_fee'], freq=parameter_dict['frequency'], fee_overhead=parameter_dict['regular_fee_overhead'])
		result_string += "Taxes on initial deposit: € {tax:.2f} \n".format(tax=parameter_dict['initial_buyers_tax'])
		result_string += "Taxes per regular deposit: € {tax:.2f} \n".format(tax=parameter_dict['regular_buyers_tax'])
		result_string += "Taxes per year: {tax:.2f} x {freq} = € {taxes_year:.2f}\n".format(tax=parameter_dict['regular_buyers_tax'], freq=parameter_dict['frequency'], taxes_year=parameter_dict['taxes_per_year'])
		result_string += "Custody fee current year: € {fee:.2f}\n".format(fee=custody_fee)
		result_string += "Current running costs: {running_costs_pct:.2f} x {total_profit:.2f} = € {running_costs:.2f}\n".format(running_costs_pct=parameter_dict['running_costs_pct'], total_profit=accumulated_sum, running_costs=running_costs)
		result_string += "Total deposited value: ({freq} x € {regular_deposit}) x {years} + {initial_deposit} = € {total}\n".format(freq=parameter_dict['frequency'], regular_deposit=parameter_dict['regular_deposit'],initial_deposit=parameter_dict['initial_deposit'], total=total_deposit, years=parameter_dict['nbr_years'])		
		result_string += "Total accumulated sum: {accumulated_sum:.2f}\n".format(accumulated_sum=parameter_dict['accumulated_sum_list'][-1])
		result_string += "Profit after {years} years: accumulated_sum - taxes - deposit_fees = {accumulated_sum:.2f} - {taxes:.2f} - {deposit_fees:.2f} = {profit:.2f} [{profit_pct:.2f} %]\n".format(years=parameter_dict['nbr_years'], accumulated_sum=accumulated_sum, taxes=total_taxes, deposit_fees=total_fees,profit=profit, profit_pct=profit_pct*100)
		result_string += "Estimated break even time: {breakeven} years\n".format(breakeven=break_even_period)
		self.txt_results.insert(INSERT, result_string)

		self.print_status_box("[INFO] Calculations performed succesfully.")
	
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
		self.initial_deposit_entry.delete(0, END)
		self.initial_deposit_entry.insert(0, "1000")
		self.regular_deposit_entry.delete(0, END)
		self.regular_deposit_entry.insert(0, "150")
		
		# reset dropdowns
		self.market_dropdown.set("Euronext Brussels")
		self.frequency_dropdown.set("Monthly")
				
		# reset texts
		self.txt_status.delete(1.0,END) # clear contents 
		self.txt_status.insert(INSERT, "Status: \n")
		self.txt_results.delete(1.0,END) # clear contents 
		self.txt_results.insert(INSERT, "Results: \n")

		#reset plot
		self.plt_graph.clear()
		self.plt_graph.title.set_text("Stock Calculator: results plot")
		self.plt_graph.grid(which='minor', alpha=0.4)
		self.plt_graph.grid(which='major', alpha=0.4)
		self.plt_graph.set_ylabel(r'Stock value [€]')
		self.plt_graph.set_xlabel(r'Number of years [years]')
		self.plt_canvas.draw()
		
	# debugging: print messages in status txt box
	def print_status_box(self, value):
		self.txt_status.delete(1.0, END)
		new_text = "Status: \n" + str(value) 
		self.txt_status.insert(INSERT, new_text)
	
	# save current config to a file
	def save_results(self):
		filepath = asksaveasfilename(
        	defaultextension=".txt",
        	filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
    	)
		if not filepath:
			#messagebox.showinfo("INFO","[INFO] operation aborted by user.")
			return
		with open(filepath, mode="a", encoding="utf-8") as output_file:
			self.print_status_box(f"[INFO] Adding results to file: {filepath}\n")
			output_file.write("##########\n")
			output_file.write(self.print_parameters())
			output_file.write("~~~~~~~~~~\n")
			output_file.write(self.txt_results.get('1.0','end'))
			output_file.close()
			return 
	
	# print parameters 
	def print_parameters(self):
		parameter_dict = self.get_parameters()
		result_txt = "Parameters: \n"
		result_txt += f"Initial deposit: {parameter_dict['initial_deposit']} \n"
		result_txt += f"Regular deposit: {parameter_dict['regular_deposit']} \n"
		result_txt += f"Market: {parameter_dict['market']}\n"
		result_txt += f"Deposit frequency: {parameter_dict['deposit_frequency']}\n"
		result_txt += f"Number of years: {parameter_dict['nbr_years']}\n"
		result_txt += f"Tax percentage: {parameter_dict['tax_pct']:.2f}\n"
		result_txt += f"Custody fee percentage: {parameter_dict['custody_fee_pct']:.2f}\n"
		result_txt += f"Interest percentage: {parameter_dict['interest_pct']:.2f}\n"
		result_txt += f"Running costs percentage: {parameter_dict['running_costs_pct']:.2f}\n"
		return result_txt		


if __name__ == "__main__":
    app = StockCalculator()
    app.mainloop()


