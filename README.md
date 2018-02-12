# Data Engineering on Campaign Contributions

This is a short read me for clarifying the code written for the [donation analytic challenge](https://github.com/InsightDataScience/donation-analytics).

## Summary of the task:

The data engineer is asked to provide insights for cash-strapped political candidates.
We would like to explore the repeat donors (donors who have donated in previous records). We want to see how loyal are the repeat donors to each candidate (recepient) .
We define a **reception** as donation to a particular recepient in a particular year and a particular area (zip code).
We need to calculate for each reception the following: the number of donation receivied, the total amount of donations received, and the percentile given as an output.

## Data

The data can be found [here](https://classic.fec.gov/finance/disclosure/metadata/DataDictionaryContributionsbyIndividuals.shtml).
It is acquired by Fedetal Election Commission. It provides data for election cylces from 1980 to present. We are interested in the Individual Contributions that "containts each contributions from an individual to a fedetal committee". The provided files are quite large (in order of millions of records and GB of size).

## Understanding the Code:

In this section I am going to briefly discuss about the code structure, its variables, and functions.

### Structure of the code:
The code is written similar to a real-time-control program.
Such program containts an infinie loop that containts three basic parts:

1. Infinite loop:
Such loop receives input, performs calculations, and write out output. In our case since our data has limited number of records, we do not require an infinite loop. 
In our code, the infinite loop is written using a context manager:

	```css
	with open(input_data_path, "r") as f, open(output_path, "w") as o:
		for line in f:
	```

2. Reading input:
The first step inside the loop is reading the input from IO (in our case the text file). This is done in our program using:
	
	```css
	line_list = (line.strip().split('|'))
	```
3. Performing calculation:
This is the heart of a real-time code. All of the calculation is performed in this section.
In our case, we need to produce the following contents in this step: calculating total amount donated for each contribution, calculating number of contributions, calculation percentile of the contribution.
	
4. Writing output:
The final step is to write the resultan of the computations on the IO (in our case the repeat_donor.txt). This is done using:

	```css
	o.write("|".join(out)+'\n')
	```


### Functions:


### Variables:


### Loops:


