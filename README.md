
# Stock Calculator: contents
GUI application to calculate the accumulated value of stocks.
- [Overview](#overview)
- [Tkinter GUI Usage](#tkinter-gui-usage-recommended)
- [IPython GUI Usage](#ipython-gui-usage-legacy)
- [How it works](#how-it-works)
- [Known limitations](#known-limitations)
- [Dependencies](#dependencies)

## Overview
Investing a fixed amount of money every month over a prolonged period of time allows money to accumulate exponentially.
This principle is known as compound interest (read more: [Compound interest Wikipedia](https://en.wikipedia.org/wiki/Compound_interest)).

The aim of this basic GUI is to calculate the accumulated sum given an initial deposit value, regular deposit value and multiple relevant parameters.
Most online calculators provide only a very rough estimate of the accumulated value but mostly fail to factor in (hidden) costs. 

## Tkinter GUI usage (Recommended)
To start the Tkinter GUI:
>`cd < place where python script is stored > `
>`python StockCalculator.pyw `

<img src="img/default_view.png" title="Default Stock Calculator GUI."  alt="Default Stock Calculator GUI." width="600" />

Example usage: 
1. Set the parameters of choice. 
<img src="img/default_view_1.png" title="StockCalculator set parameters."  alt="StockCalculator set parameters." width="600" />

2. Calculate the results via the calculate button. <br> Results will appear in the results textbox.
<img src="img/default_view_2.png" title="StockCalculator example results."  alt="Stockcalculator example results." width="600" />

3. Make a plot via the plot button.
<img src="img/default_view_3.png" title="StockCalculator plot generation."  alt="StockCalculator plot generation." width="600" />

4. Save your current configuration and their results to a file via the save button.
<img src="img/default_view_4.png" title="StockCalculator save results."  alt="StockCalculator save results." width="600" />

5. Reset the interface to default values via the reset button.
<img src="img/default_view_5.png" title="StockCalculator reset interface."  alt="StockCalculator reset interface." width="600" />

If anything were to go wrong during execution, an appropriate message will pop up and this message will remain in the status textbox.
<img src="img/default_view_6.png" title="StockCalculator error message."  alt="StockCalculator error message." width="600" />


## IPython GUI usage (Legacy)
To start the IPython GUI:
> `cd < place where notebook is stored >` 
> `jupyter notebook StockCalculator.ipynb`

Your default browser should open the jupyter notebook interface. 
If the interface does not appear open your browser and go to:
> localhost:8888/notebooks/StockCalculator.ipynb

Example usage:
1. Execute all code cells until GUI appears.
<img src="img/jupyter_gui_1.png" title="Execute Jupyter notebook code cells." alt="Execute Jupyter notebook code cells." width="600" />

2. Fill in parameters
<img src="img/jupyter_gui_2.png" title="StockCalculator notebook parameters." alt="StockCalculator notebook parameters." width="600" />
<img src="img/jupyter_gui_3.png" title="StockCalculator notebook example usage." alt="StockCalculator notebook example usage." width="600" />

3. Example output
<img src="img/jupyter_gui_4.png" title="StockCalculator example output." alt="StockCalculator example output." width="600" />

4. Plot generation
<img src="img/jupyter_gui_5.png" title="StockCalculator plot generation." alt="StockCalculator plot generation." width="600" />


## How it works
### Maths
#### Basics: 
Compound interest is expressed as: 
$$ A = P (1 + \frac{r}{n})^{nt}$$ 
Where: 
	- total amount $A$
	- initial amount $P$
	- interest rate $r$
	- compounds per year $n$
	- time $t$
(Example [compound interest](https://www.thecalculatorsite.com/articles/finance/compound-interest-formula.php))

Since the interest rate is regarded as constant and average during one year, the compouding formula can be simplified to the form: 
$$ A = P (1 + r)^{t} $$.
Meaning that over the span of one year only one interest compound takes place.

Furthermore, the formula can be rewritten into a form using the multiplicative sum:
$$ A = P \prod_{t=1}^{t} (1 + r) $$

#### Accumulation: 
The basic compound interest formula is only valid if only one initial deposit ($P_{0}$) is made.
By expanding upon the compound interest formula in multiplicative form, additional deposits can be taken into account. <br>

The regular deposits ($P_{r}$) accumulated during one year and their respective interests ([Known limitations](#known-limitations)).
$$ P_{year} =  \sum_{i=0}^{i} P_{r} (1 + r (\frac{12-i}{12})) $$

The intial accumulated sum equals the initial deposit:
$$ sum_{0} = P_{0} $$

The acummulated sum for the next year is calculated according to:
$$ sum_{n} = sum_{n-1} * (1 + r) + P_{year} $$ 


#### Added complexity:
Our compounding formula does not yet include running costs and custody fee.
Both are important due to the exponential behaviour of our equation.
Excluding them might grant significant differences whenever a large amount of compounding takes place. <br>

Running costs percentage ($C_{r}$) is extracted from the accumulated sum by the expeditor of the stock on yearly basis ([Known limitations](#known-limitations)).
Incorporated into the formula:

$$ sum_{n} = \{ sum_{n-1} * (1 + r) + P_{year} \} * (1 - C_{r})  $$ 

Banks sometimes also issue a custody fee percentage ($C_{f}$), the price for storing your brokerage account.
These costs are also on a yearly basis and calculated on the remaining accumulated sum (after running costs).

$$ sum_{n} = [ \{ sum_{n-1} * (1 + r) + P_{year} \} * (1 - C_{r}) ] (1- C_{f}) $$ 

#### Profit:
The profit of our investment is defined as the value that is gained when compared to the deposits made and one-time costs (taxes and brokerage fees).
[$f$ is number of regular deposits per year]

Total deposits: 
$$ P_{total} = P_{0} + n f P_{r} $$

Total taxes:
$$ T_{total} = T_{P_{0}} + n f T_{P_{r}} $$

Total brokerage fees:
$$ B_{total} = B_{P_{0}} + n f B_{P_{r}} $$

Profit:
$$ profit = sum_{n} - P_{total} - T_{total} - B_{total} $$

### Example
If: <br>
- Initial deposit $P_{0}$ = 1000
- Regular deposit $P_{r}$ = 500
- Number of years invested $n$ = 2
- Interest $r$ = 5%
- Running costs $C_{r}$ = 1% 
- Custody fee $C_{f}$ = 2% 
- Frequency $f$ = 2 deposits per year (January and July )

<b> First year: </b>
$$ P_{0} = 1000 $$
$$ P_{r_{1}} = 500 * (1 + 0.05*( \frac{12-0}{12} )) = 525 $$
$$ P_{r_{2}} = 500 * (1 + 0.05*(\frac{12-6}{12})) = 512.5 $$
$$ P_{year} = P_{r_{1}}  + P_{r_{2}}  = 1037.5 $$
$$ sum_{1}^*  = 1000 *  (1 + 0.05) + 525 + 512.5 = 2087.5 $$
$$ sum_{1} = [2087.5 (1 - C_{r}) ](1 - C_{f})  = 2025.2925 $$
$$ C_{r} = 20.875 $$
$$ C_{f} = 41.3325 $$
<br>
<b> Second year:</b>
$$ sum_{2} = [sum_{1} * (1 + 0.05) + P_{year} ](1 - C_{r})(1 - C_{f}) = (2126.40 + 1037.5)(1 - 0.01)(1 - 0.02)  = 3069.77 $$
$$ C_{r} = 31.64 $$
$$ C_{f} = 62.64 $$
$$ P_{total} = P_{0} + n f P_{r}= 1000 + 2 * (2 * 500) = 3000 $$
$$ profit = sum_{n} - P_{total} - T_{total} - B_{total} = 3069.77 - 3000 - T_{total}^* - B_{total}^* $$
Taxes depending on chosen market and stock type.
Brokerage fee depending on chosen market.

## Known limitations
### Exactness
The proposed formulas are more accurate than most similar calculators found online.
But there are still some limitations to this program.
- Interest rate:
The interest rate given as a paramater to the program is considered as a year average constant.
This constant value is subsequently used to calculate the interest for different deposits using a linear approach.
E.g. a deposit in the first month will have interest rate $r$, a second deposit will have an interest rate $r/2$.
In real-life stock markets this is never the case since markets fluctuate day by day.

- Cost calculation and frequency:
Most stock expeditors and banks calculate their respective running costs and custody on a yearly basis. 
However, this is not set in stone and can vary.

### Brokerage fee 
Depending on the stock market platform and residing country the brokerage fees might differ from the brokerage fee from the calculator.
This calculator uses the pricings as presented in the document: [Bolero fees:](https://www.bolero.be/uploads/media/61f801717277e/info-tarieven-nl-220131-ex-ante.pdf)

### Tkinter
The GUI of the stockcalculator is written using TKinter library which is a default library of Python.
This is by no means the greatest GUI toolkit and the look is a bit outdated.

## Dependencies
### TKinter
The Tkinter program mostly uses the Python standard library, only the matplotlib and numpy packages are necessary.

To check if the packages are installed on your system:
> `pip list` 

To install dependencies if the required packages are not present:
> `pip install matplotlib && pip install numpy` 

### Jupyter notebook
Jupyter notebook can be installed via
> `pip install notebook`


