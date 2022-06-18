# Stock Calculator: contents
GUI application to calculate the accumulated value of stocks.
- [Overview](#overview)
- [Usage](#usage)
- [How it works](#how-it-works)
- [Known limitations](#known-limitations)
- [Dependencies](#dependencies)

## Overview
Investing a fixed amount of money every month over a prolonged period of time allows money to accumulate exponentially.
This principle is known as compound interest (read more: [Compound interest Wikipedia](https://en.wikipedia.org/wiki/Compound_interest)).

The aim of this basic GUI is to calculate the accumulated sum given an initial deposit value, regular deposit value and multiple relevant parameters.
Most online calculators provide only a very rough estimate of the accumulated value but mostly fail to factor in (hidden) costs. 

## Usage 
To start the GUI:
>`cd < place where python script is stored > `
>`python StockCalculator.pyw `

<img src="img/default_view.png" title="Default Stock Calculator GUI."  alt="Default Stock Calculator GUI." width="600" />

Example usage: 
1. Set the parameters of choice. 
<img src="img/default_view_1.png" title="Default Stock Calculator GUI."  alt="Default Stock Calculator GUI." width="600" />

2. Calculate the results via the calculate button. <br> Results will appear in the results textbox.
<img src="img/default_view_2.png" title="Default Stock Calculator GUI."  alt="Default Stock Calculator GUI." width="600" />

3. Make a plot via the plot button.
<img src="img/default_view_3.png" title="Default Stock Calculator GUI."  alt="Default Stock Calculator GUI." width="600" />

4. Save your current configuration and their results to a file via the save button.
<img src="img/default_view_4.png" title="Default Stock Calculator GUI."  alt="Default Stock Calculator GUI." width="600" />

5. Reset the interface to default values via the reset button.
<img src="img/default_view_5.png" title="Default Stock Calculator GUI."  alt="Default Stock Calculator GUI." width="600" />

If anything were to go wrong during execution, an appropriate message will pop up and this message will remain in the status textbox.
<img src="img/default_view_6.png" title="Default Stock Calculator GUI."  alt="Default Stock Calculator GUI." width="600" />



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
- Initial deposit = 1000
- Regular deposit = 500
- Number of years invested = 2
- Interest = 5%
- Running costs = 1% 
- Custody fee = 2% 
- Frequency = 2 deposits per year (January and July )

<b> First year: </b>
$$ deposit_{initial} = 1000 * (1 + 0.05) = 1050 $$
$$ deposit_1 = 500 * (1 + 0.05*((12-0)/12)) = 525 $$
$$ deposit_2 = 500 * (1 + 0.05*((12-6)/12)) = 512.5 $$
$$ sum  = 525 + 512.5 + 1050 = 2087.5 $$
$$ runningcosts = 2087.3475 * 0.01 = 20.875 $$
$$ custodyfee = (sum - runningcosts) * 0.02 = 41.3325 $$
$$ sum_{1 year} = 2025.2925 $$
<br>
<b> Second year:</b>
$$ sum = sum_{1_year} * (1 + 0.05) + 1037.5 = 2126.40 + 1037.5  = 3164.06 $$
$$ runningcosts = 31.64 $$
$$ custodyfee = (sum - runningcosts) * 0.02 = 62.64 $$
$$ sum_{2 year} = 3069.77 $$ 
$$ sum_{deposits} = 1000 + 2 * 500 + 2 * 500 = 3000 $$
$$ profit = 3069.77 - 3000 - taxes^ - brokeragefee^* $$
Taxes depending on chosen market and stock type.
Brokerage fee depending on chosen market.

### Known limitations
#### Exactness
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

#### Brokerage fee 
Depending on the stock market platform and residing country the brokerage fees might differ from the brokerage fee from the calculator.
This calculator uses the pricings as presented in the document: [Bolero fees:](https://www.bolero.be/uploads/media/61f801717277e/info-tarieven-nl-220131-ex-ante.pdf)

#### Tkinter
The GUI of the stockcalculator is written using TKinter library which is a default library of Python.
This is by no means the greatest GUI toolkit and the look is a bit outdated.

### Dependencies
The program mostly uses the Python standard library, only the matplotlib and numpy packages are necessary.

To check if the packages are installed on your system:
> `pip list` 

To install dependencies if the required packages are not present:
> `pip install matplotlib && pip install numpy` 
