# importing required packages
import re # to perform regex matching
import math # to perform mathematical operations
import time # to time the program
import os # to get the
start_time = time.time()

# utility function
def is_number(s):  # checking if the input is numeric
    try:
        float(s)
        return True
    except ValueError:
        pass
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False


# defining path to IO files
scriptpath = os.path.dirname(__file__)
input_data_path = os.path.join(scriptpath, r'..\input\itcont.txt')  # path to the donor data
percetile_path = os.path.join(scriptpath, '..\input\percentile.txt')  # path to percentile input
output_path = os.path.join(scriptpath, r'..\output\repeat_donors.txt')  # path to the output

# regex patterns to be used in data engineering
punctuation = "[\s.,]"  # for cleaning the name columns
cmtid_pattern = "^C{1}\d{8}$"  # for recipient (CMTD_ID) matching
date_pattern = "[0-1][0-9][0-3][0-9][0-9]{4}"  # for datatime matching

# defining sets and dictionary to hold data inside the loop
all_individuals = set()  # a set that contains all the unique repeat donors and will updated with new repeat donors
repeat_recipient = set()  # a set that contains all the unique donation receptions = recipient/year/zip_code
list_of_outputs = dict()  # its keys are the unique donation receptions and values are list to output to txt file


# reading text files
with open(percetile_path, "r") as perc:
    percentile = int(perc.readlines()[0])  # reads the first string of the text file as the integer value of percentile


def do_it():
    ctr = 0  # sets a counter to save the number of records
    ctr_skipped = 0  # sets a counter to save the number of records skipped because not met data requirement
    with open(input_data_path, "r") as f, open(output_path, "w") as o: # opens a read/input and write/output connection
        for line in f:  # streaming the the input file
            ctr += 1  # increasing the counter
            line_list = (line.strip().split('|'))  # getting the pipe-separated lines into list of string
            if (len(line_list)) != 21:  # if the line does not contain enough entries, skip
                #  uncomment the following line if want to receive detail information on skipped lines
                #  print("row # {} skipped: incomplete record!".format(ctr))
                ctr_skipped += 1  # increasing the skipped-line counter
                continue  # move to the next entry without any more operation

            # getting variables from the list of strings
            cmte_id = line_list[0]  # recipient identifier
            name = re.sub(punctuation, "",line_list[7])  # gets the name of recipient as a long connected string
            zip_code = line_list[10][0:5]  # gets first 5 digits of the zip-code
            transaction_dt = line_list[13]  # gets transaction date
            transaction_amt = line_list[14]  # gets transaction amount
            other_id = line_list[15]  # gets transaction amount

            if len(other_id) != 0:  # if the OTHER_ID is not empty skip the line
                #  uncomment the following line if want to receive detail information on skipped lines
                # print("row # {} skipped: other_id column is not empty!".format(ctr))
                ctr_skipped += 1  # increasing the skipped-line counter
                continue  # move to the next entry without any more operation

            if len(zip_code) < 5 or not is_number(zip_code):  # if the zip-code is malformed skip it
                #  uncomment the following line if want to receive detail information on skipped lines
                # print("row # {} skipped: zip_code is malformed!".format(ctr))
                ctr_skipped += 1  # increasing the skipped-line counter
                continue  # move to the next entry without any more operation

            if not re.match(date_pattern, transaction_dt):  # date time pattern is in mmddyyyy
                #  uncomment the following line if want to receive detail information on skipped lines
                # print("row # {} skipped: transaction_dt is malformed!".format(ctr))
                ctr_skipped += 1  # increasing the skipped-line counter
                continue  # move to the next entry without any more operation

            if not re.match(cmtid_pattern, cmte_id):  # recipient id has acceptable format
                #  uncomment the following line if want to receive detail information on skipped lines
                #  print("row # {} skipped: cmte_id is malformed!".format(ctr))
                ctr_skipped += 1  # increasing the skipped-line counter
                continue  # move to the next entry without any more operation

            if not is_number(transaction_amt):  # checking if the transaction amount is numeric
                #  uncomment the following line if want to receive detail information on skipped lines
                # print("row # {} skipped: transaction_amt is malformed!".format(ctr))
                ctr_skipped += 1  # increasing the skipped-line counter
                continue  # move to the next entry without any more operation

            transaction_amt = float(transaction_amt)  # case the transaction amount to float for calculation
            donor_id = name + zip_code  # generates a unique id for donors based on name and zip_code
            reception_id = cmte_id + zip_code + transaction_dt[4:]  # generates a unique id for each reception

            if donor_id in all_individuals:  # checks if a donor is repeated, if repeated to calculate output

                if reception_id not in repeat_recipient:  # if such a reception has happened first time
                    #  If it is the first time a reception (recipient/zip_code/year) occurs, we generate a new key in
                    #  the list_of_outputs and update its values by variables derived from input, no calculation is
                    #  performed.
                    rcpt = cmte_id
                    zip = zip_code
                    yr = transaction_dt[4:]  # only year
                    pctl = transaction_amt
                    n = 1  # this is the first time this reception has occurred.
                    ttl = transaction_amt
                    all_dons = [transaction_amt]  # this list will later be used to hold transaction amoutn that will
                    #  consequently calculate the running percentile.
                    list_of_outputs[reception_id] = [rcpt, zip, yr, pctl, ttl, n, all_dons]  # fill  the output list
                    repeat_recipient.update([reception_id])  # update the recipient list with this new reception

                elif reception_id in repeat_recipient:  # Now, if this reception has been performed before, we will
                    #  calculate the running percentile, total amount, and number of transactions
                    list_of_outputs[reception_id][4] += transaction_amt  # adds the transaction amount to existing total
                    list_of_outputs[reception_id][5] += 1  # increases the number of transactions
                    m = math.ceil(percentile/100*len(list_of_outputs[reception_id][6]))-1  # calculates percentile index
                    list_of_outputs[reception_id][6].append(transaction_amt)  # add amount to the list of amounts
                    transaction_list = sorted(list_of_outputs[reception_id][6])  # sorting to select the percentile
                    list_of_outputs[reception_id][3] = transaction_list[m]  # sets the percentile

                # The following line drops out the last value of the list (the list of amount) and bring the data in
                # the format acceptable for output (integers for amount and percentile, string for the rest)
                out = [str(int(x))if isinstance(x, float) else str(x) for x in list_of_outputs[reception_id][:-1]]
                o.write("|".join(out)+'\n')  # makes a pipe-separated line to output
            all_individuals.update([donor_id])  # updates the set of donor ids

        # makes a run summary for the output
        print("-" * 37)
        print("RUN SUMMARY:\n")
        print("Total number of records:   {}".format(ctr))
        print("Total number of skipped records:   {}".format(ctr_skipped))
        print("Percentage of healthy data:   {0:.1f}%".format((ctr-ctr_skipped)/ctr*100))
        end_time = time.time()
        print("Total run time:   {0:.1f} seconds".format(end_time - start_time))
        print("-" * 37)

        
do_it()