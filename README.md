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
* Maths
* Example

### Known limitations
* Tkinter
* Exactness
* Brokerage fee

### Dependencies
The program mostly uses the Python standard library, only the matplotlib and numpy packages are necessary.

To check if the packages are installed on your system:
> `pip list` 

To install dependencies if the required packages are not present:
> `pip install matplotlib && pip install numpy` 
