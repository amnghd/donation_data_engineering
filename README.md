# Data Engineering on Campaign Contributions

This is a short read me for clarifying the code written for the [donation analytic challenge](https://github.com/InsightDataScience/donation-analytics).

## Summary of the task:

The data engineer is asked to provide insights for cash-strapped political candidates.
We would like to explore the repeat donors (donors who have donated in previous records). We want to see how loyal are the repeat donors to each candidate (recipient).
We define a **reception** as the donation to a particular recipient in a particular year and a particular area (zip code).
We need to calculate for each reception the following: the number of donation received, the total amount of donations received, and the percentile given as an output.

## Data

The data can be found [here](https://classic.fec.gov/finance/disclosure/metadata/DataDictionaryContributionsbyIndividuals.shtml).
It is acquired by Federal Election Commission. It provides data for election cycles from 1980 to present. We are interested in the Individual Contributions that "contains each contribution from an individual to a federal committee". The provided files are quite large (in order of millions of records and GB of size).

## Understanding the Code:

In this section, I am going to briefly discuss the code structure, its variables, and functions.

### Structure of the code:
The code is written similar to a real-time-control program.
Such program contains an infinite loop that contains three basic parts:

1. Infinite loop:
Such loop receives input, performs calculations, and write out output. In our case since our data has the limited number of records, we do not require an infinite loop. 
In our code, the infinite loop is written using a context manager:

    ```css
    with open(input_data_path, "r") as f, open(output_path, "w") as o:
        for line in f:
    ```

2. Reading input:
The first step inside the loop is reading the input from IO (in our case the text file). This is done in our program using:
    
    ```
    line_list = (line.strip().split('|'))
    ```
3. Performing calculation:
This is the heart of a real-time code. All of the calculation is performed in this section.
In our case, we need to produce the following contents in this step: calculating total amount donated for each contribution, calculating the number of contributions, calculation percentile of the contribution.
Moreover, we need to prepare the line of string we need to write on output in this part.
    
4. Writing output:
The final step is to write the resultant of the computations on the IO (in our case the repeat_donor.txt). This is done using:

    ```
    o.write("|".join(out)+'\n')
    ```


### Functions:

One function is written in this code which is ``is_number(string)``.
This function is used for identifying whether the input value is a number and is used in checking whether data is in proper shape.

### Variables:
Several variables are declared in this code. More important ones are:

1. ``donor_id``: This is a unique identifier for the donors, combined from their name and zip_code.

2. ``reception_id``: This is a unique identifier for each reception which includes recipient id, zipcode of donation, year of donation.

3. ``all_individuals``: This is a set variable. It contains unique repeat donors.

4. ``repeat_recipient``: This is a set variable. It contains unique receptions.

5. ``list_of_outputs``: This is a dictionary. Its keys are the receptions and its values is a list. This list will contain the strings to be output in a pipe-separated manner.

### Data Quality Check:
The quality of the data is checked against the following conditions.
If it doesn't meet the requirements, that specific line is skipped and new input will be investigated.
1. The line of data consists of all of the columns (21 columns).

2. The ``OTHER_ID`` column is empty.

3. ``ZIP_CODE`` is numeric and its length is equal or more than 5.

4. The ``TRANSACTION_DT`` has the **mmddyyyy** format. 

5. The ``CMTD_ID`` follows the propoer pattern, regex = ``"^C{1}\d{8}$"``. 

6. The ``TRANSACTION_AMT`` is numerical.

### Run Summary:
Once running the program is finished, a brief summary of the results will be prompted. 
This is an example of such a prompt.
```
-------------------------------------
RUN SUMMARY:

Total number of records:   7
Total number of skipped records:   1
Percentage of healthy data:   85.7%
Total run time:   0.0 seconds
-------------------------------------
```