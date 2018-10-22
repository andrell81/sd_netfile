import os
import pandas as pd
import logging
import requests
import json
import math
from datetime import datetime

forms = {'460A':'0','460B1':'12','460C':'1','460D':'5','497P1':'20','496':'19'}
payload = {'format':'json'}
prod_columns = ['form',
                'schedule',
                'schedule_description',
                'recipient_id',
                'recipient_name',
                'report_period_from',
                'report_period_to',
                'contributor_code',
                'contributor_last',
                'contributor_first',
                'contributor_city',
                'contributor_state',
                'contributor_zip',
                'contributor_emp',
                'contributor_occ',
                'contribution_date',
                'contribution_amount',
                'contribution_annual',
                'contribution_desc',
                'contributor_id',
                'intermediary_last',
                'intermediary_first',
                'intermediary_city',
                'intermediary_state',
                'intermediary_zip',
                'intermediary_emp',
                'intermediary_occ',
                'filing_id',
                'report_year']
cur_yr = datetime.now().strftime("%Y")
prod_file = 'sd_netfile_'+str(cur_yr)+'.csv'

def get_transactions_a():
    """ Requesting transactions for schedule 460A """

    # Getting transactions for Form 460, Schedule A
    # Which contain semi-annual and pre-election reporting

    save_path = 'schedule_460a.csv'
    req_url = "https://netfile.com:443/" \
                + "Connect2/api/public/" \
                + "campaign/export/cal201/" \
                + "transaction/year"
    print("Requesting number of transactions")
    
    # First, we have to hit the API to get the total number
    # of records for this form type. This is because
    # of a 1,000 record limit that requires us to loop

    countRequest = requests.post(req_url,
                                params=payload,
                                data = {'Aid':'CSD',
                                        'Year':cur_yr,
                                        'CurrentPageIndex':0,
                                        'PageSize':'1',
                                        'TransactionType':forms['460A'],
                                        'ShowSuperceded':'false'})
    if countRequest.status_code == 200:
        formTransactions = countRequest.json()['totalMatchingCount']
        if formTransactions < 1000:
            requestLoops = 1
        else:
            requestLoops = math.ceil(formTransactions/1000)
        transactionsList = []

        # Not that we know how many loops to run, we can
        # loop to request records

        for i in range(requestLoops):
            print("Requesting transactions " + str(i))
            page = str(i)
            transactRequest = requests.post(req_url,
                                            params=payload,
                                            data={'Aid':'CSD',
                                                  'Year':cur_yr,
                                                  'CurrentPageIndex':page,
                                                  'PageSize':'1000',
                                                  'TransactionType':forms['460A'],
                                                  'ShowSuperceded':'false'})
            if transactRequest.status_code != 200:
                return "Transaction request " + str(i) + " failed " + str(transactRequest.status_code)
            else:
                print("Transaction request " + str(i) + " success")
                transactions_json = transactRequest.json()['results']
                
                # For each record, we are plugging fields into 
                # the appropriate columns for the final dataset.

                for t in transactions_json:
                    transactionsList.append(['460', #form
                                       t['form_Type'], #schedule
                                       'Monetary contributions', #schedule_description
                                       t['filerStateId'], #recipient_id
                                       t['filerName'], #recipient_name
                                       t['filingStartDate'], #'report_period_from'
                                       t['filingEndDate'], #'report_period_to'
                                       t['entity_Cd'], #'contributor_code'
                                       t['tran_NamL'], #'contributor_last'
                                       t['tran_NamF'], #'contributor_first'
                                       t['tran_City'], #'contributor_city'
                                       t['tran_ST'], #'contributor_state'
                                       t['tran_Zip4'], #'contributor_zip'
                                       t['tran_Emp'], #'contributor_emp'
                                       t['tran_Occ'], #'contributor_occ'
                                       t['tran_Date'], #'contribution_date'
                                       t['tran_Amt1'], #'contribution_amount'
                                       t['tran_Amt2'], #'contribution_annual'
                                       t['tran_Dscr'], #'contribution_desc'
                                       t['cmte_Id'], #'contributor_id'
                                       t['intr_NamL'], #'intermediary_last'
                                       t['intr_NamF'], #'intermediary_first'
                                       t['intr_City'], #'intermediary_city'
                                       t['intr_ST'], #'intermediary_state'
                                       t['intr_Zip4'], #'intermediary_zip'
                                       t['intr_Emp'], #'intermediary_emp'
                                       t['intr_Occ'], #'intermediary_occ'
                                       t['filingId'],
                                         cur_yr])

        campaignTransactions = pd.DataFrame(transactionsList,columns=prod_columns)
        print("Writing 460A transactions to temp")
        campaignTransactions.to_csv(save_path,index=False)

        # Process max dates for later use
        print("Calculate max filing dates")
        date_checks = campaignTransactions[['recipient_id','report_period_to']]
        date_checks = date_checks.drop_duplicates()
        date_checks_max = date_checks.groupby(['recipient_id'])['report_period_to'].max()
        date_checks_max = date_checks_max.to_frame()
        date_checks_max.reset_index(inplace=True)
        
        print("Writing max filing dates to temp")
        date_checks_max.to_csv('date_checks_max.csv',index=False)

    else:
        return "Count request failed " + str(countRequest.status_code)
        
    return "Created 460A transactions " + str(formTransactions)

def get_transactions_b():
    """ Requesting transactions for schedule 460B1 """

    # Getting transactions for Form 460, Schedule B1
    # Which contain semi-annual and pre-election reporting

    save_path = 'schedule_460b1.csv'
    req_url = "https://netfile.com:443/" \
                + "Connect2/api/public/" \
                + "campaign/export/cal201/" \
                + "transaction/year"
    print("Requesting number of transactions")
    countRequest = requests.post(req_url,
                                params=payload,
                                data = {'Aid':'CSD',
                                        'Year':cur_yr,
                                        'CurrentPageIndex':0,
                                        'PageSize':'1',
                                        'TransactionType':forms['460B1'],
                                        'ShowSuperceded':'false'})
    if countRequest.status_code == 200:
        formTransactions = countRequest.json()['totalMatchingCount']
        if formTransactions < 1000:
            requestLoops = 1
        else:
            requestLoops = math.ceil(formTransactions/1000)
        transactionsList = []
        for i in range(requestLoops):
            print("Requesting transactions " + str(i))
            page = str(i)
            transactRequest = requests.post(req_url,
                                            params=payload,
                                            data={'Aid':'CSD',
                                                  'Year':cur_yr,
                                                  'CurrentPageIndex':page,
                                                  'PageSize':'1000',
                                                  'TransactionType':forms['460B1'],
                                                  'ShowSuperceded':'false'})
            if transactRequest.status_code != 200:
                return "Transaction request " + str(i) + " failed " + str(transactRequest.status_code)
            else:
                print("Transaction request " + str(i) + " success")
                transactions_json = transactRequest.json()['results']
                for t in transactions_json:
                    transactionsList.append(['460', #form
                                       t['form_Type'], #schedule
                                       'Loans', #schedule_description
                                       t['filerStateId'], #recipient_id
                                       t['filerName'], #recipient_name
                                       t['filingStartDate'], #'report_period_from'
                                       t['filingEndDate'], #'report_period_to'
                                       t['entity_Cd'], #'contributor_code'
                                       t['tran_NamL'], #'contributor_last'
                                       t['tran_NamF'], #'contributor_first'
                                       t['tran_City'], #'contributor_city'
                                       t['tran_ST'], #'contributor_state'
                                       t['tran_Zip4'], #'contributor_zip'
                                       t['tran_Emp'], #'contributor_emp'
                                       t['tran_Occ'], #'contributor_occ'
                                       t['loan_Date1'], #'contribution_date'-CHANGED
                                       t['loan_Amt1'], #'contribution_amount'
                                       t['loan_Amt3'], #'contribution_annual'
                                       t['tran_Dscr'], #'contribution_desc'
                                       t['cmte_Id'], #'contributor_id'
                                       t['intr_NamL'], #'intermediary_last'
                                       t['intr_NamF'], #'intermediary_first'
                                       t['intr_City'], #'intermediary_city'
                                       t['intr_ST'], #'intermediary_state'
                                       t['intr_Zip4'], #'intermediary_zip'
                                       t['intr_Emp'], #'intermediary_emp'
                                       t['intr_Occ'], #'intermediary_occ'
                                       t['filingId'],
                                         cur_yr])

        campaignTransactions = pd.DataFrame(transactionsList,columns=prod_columns)
        print("Writing 460B1 transactions to temp")
        campaignTransactions.to_csv(save_path,index=False)
    else:
        return "Count request failed " + str(countRequest.status_code)
        
    return "Created 460B1 transactions " + str(formTransactions)

def get_transactions_c():
    """ Requesting transactions for schedule 460C """

    # Getting transactions for Form 460, Schedule C
    # Which contain semi-annual and pre-election reporting

    save_path = 'schedule_460c.csv'
    req_url = "https://netfile.com:443/" \
                + "Connect2/api/public/" \
                + "campaign/export/cal201/" \
                + "transaction/year"
    print("Requesting number of transactions")
    countRequest = requests.post(req_url,
                                params=payload,
                                data = {'Aid':'CSD',
                                        'Year':cur_yr,
                                        'CurrentPageIndex':0,
                                        'PageSize':'1',
                                        'TransactionType':forms['460C'],
                                        'ShowSuperceded':'false'})
    if countRequest.status_code == 200:
        formTransactions = countRequest.json()['totalMatchingCount']
        if formTransactions < 1000:
            requestLoops = 1
        else:
            requestLoops = math.ceil(formTransactions/1000)
        transactionsList = []
        for i in range(requestLoops):
            print("Requesting transactions " + str(i))
            page = str(i)
            transactRequest = requests.post(req_url,
                                            params=payload,
                                            data={'Aid':'CSD',
                                                  'Year':cur_yr,
                                                  'CurrentPageIndex':page,
                                                  'PageSize':'1000',
                                                  'TransactionType':forms['460C'],
                                                  'ShowSuperceded':'false'})
            if transactRequest.status_code != 200:
                return "Transaction request " + str(i) + " failed " + str(transactRequest.status_code)
            else:
                print("Transaction request " + str(i) + " success")
                transactions_json = transactRequest.json()['results']
                for t in transactions_json:
                    transactionsList.append(['460', #form
                                       t['form_Type'], #schedule
                                       'Non monetary contributions', #schedule_description
                                       t['filerStateId'], #recipient_id
                                       t['filerName'], #recipient_name
                                       t['filingStartDate'], #'report_period_from'
                                       t['filingEndDate'], #'report_period_to'
                                       t['entity_Cd'], #'contributor_code'
                                       t['tran_NamL'], #'contributor_last'
                                       t['tran_NamF'], #'contributor_first'
                                       t['tran_City'], #'contributor_city'
                                       t['tran_ST'], #'contributor_state'
                                       t['tran_Zip4'], #'contributor_zip'
                                       t['tran_Emp'], #'contributor_emp'
                                       t['tran_Occ'], #'contributor_occ'
                                       t['tran_Date'], #'contribution_date'
                                       t['tran_Amt1'], #'contribution_amount'
                                       t['tran_Amt2'], #'contribution_annual'
                                       t['tran_Dscr'], #'contribution_desc'
                                       t['cmte_Id'], #'contributor_id'
                                       t['intr_NamL'], #'intermediary_last'
                                       t['intr_NamF'], #'intermediary_first'
                                       t['intr_City'], #'intermediary_city'
                                       t['intr_ST'], #'intermediary_state'
                                       t['intr_Zip4'], #'intermediary_zip'
                                       t['intr_Emp'], #'intermediary_emp'
                                       t['intr_Occ'], #'intermediary_occ'
                                       t['filingId'],
                                         cur_yr])

        campaignTransactions = pd.DataFrame(transactionsList,columns=prod_columns)
        print("Writing 460C transactions to temp")
        campaignTransactions.to_csv(save_path,index=False)
    else:
        return "Count request failed " + str(countRequest.status_code)
        
    return "Created 460C transactions " + str(formTransactions)

def get_transactions_d():
    """ Requesting transactions for schedule 460D """

    # Getting transactions for Form 460, Schedule D
    # Which contain semi-annual and pre-election reporting

    save_path = 'schedule_460d.csv'
    req_url = "https://netfile.com:443/" \
                + "Connect2/api/public/" \
                + "campaign/export/cal201/" \
                + "transaction/year"
    print("Requesting number of transactions")
    countRequest = requests.post(req_url,
                                params=payload,
                                data = {'Aid':'CSD',
                                        'Year':cur_yr,
                                        'CurrentPageIndex':0,
                                        'PageSize':'1',
                                        'TransactionType':forms['460D'],
                                        'ShowSuperceded':'false'})
    if countRequest.status_code == 200:
        formTransactions = countRequest.json()['totalMatchingCount']
        if formTransactions < 1000:
            requestLoops = 1
        else:
            requestLoops = math.ceil(formTransactions/1000)
        transactionsList = []
        for i in range(requestLoops):
            print("Requesting transactions " + str(i))
            page = str(i)
            transactRequest = requests.post(req_url,
                                            params=payload,
                                            data={'Aid':'CSD',
                                                  'Year':cur_yr,
                                                  'CurrentPageIndex':page,
                                                  'PageSize':'1000',
                                                  'TransactionType':forms['460D'],
                                                  'ShowSuperceded':'false'})
            if transactRequest.status_code != 200:
                return "Transaction request " + str(i) + " failed " + str(transactRequest.status_code)
            else:
                print("Transaction request " + str(i) + " success")
                transactions_json = transactRequest.json()['results']
                for t in transactions_json:
                    if t['sup_Opp_Cd'] == 'S':
                        candName = t['cand_NamF']+' '+t['cand_NamL']
                        balName = t['bal_Name']
                        otherNameF = t['tran_NamF']
                        otherNameL = t['tran_NamL']
                        if balName != '':
                            fullName = balName
                        elif candName != ' ':
                            fullName = candName.strip()
                        else:
                            fullName = otherNameL
                    transactionsList.append(['460', #form
                                       t['form_Type'], #schedule
                                       'Independent expenditures in support', #schedule_description
                                       t['cmte_Id'], #recipient_id
                                       fullName, #recipient_name
                                       t['filingStartDate'], #'report_period_from'
                                       t['filingEndDate'], #'report_period_to'
                                       ' ', #'contributor_code'
                                       t['filerName'], #'contributor_last'
                                       ' ', #'contributor_first'
                                       ' ', #'contributor_city'
                                       ' ', #'contributor_state'
                                       ' ', #'contributor_zip'
                                       ' ', #'contributor_emp'
                                       ' ', #'contributor_occ'
                                       t['tran_Date'], #'contribution_date'
                                       t['tran_Amt1'], #'contribution_amount'
                                       t['tran_Amt2'], #'contribution_annual'
                                       t['tran_Dscr'], #'contribution_desc'
                                       t['filerStateId'], #'contributor_id'
                                       t['intr_NamL'], #'intermediary_last'
                                       t['intr_NamF'], #'intermediary_first'
                                       t['intr_City'], #'intermediary_city'
                                       t['intr_ST'], #'intermediary_state'
                                       t['intr_Zip4'], #'intermediary_zip'
                                       t['intr_Emp'], #'intermediary_emp'
                                       t['intr_Occ'], #'intermediary_occ'
                                       t['filingId'],
                                         cur_yr])

        campaignTransactions = pd.DataFrame(transactionsList,columns=prod_columns)
        print("Writing 460D transactions to temp")
        campaignTransactions.to_csv(save_path,index=False)
    else:
        return "Count request failed " + str(countRequest.status_code)
        
    return "Created 460D transactions " + str(formTransactions)

def get_transactions_summary():
    """ Requesting transactions for schedule 460, summary page """

    # Getting transactions for Form 460 summary page
    # Which contain semi-annual and pre-election reporting
    # Summary page includes unitemized contribs

    save_path = 'schedule_460sum.csv'
    req_url = "https://netfile.com:443/" \
                + "Connect2/api/public/" \
                + "campaign/export/cal201/" \
                + "summary/year"
    print("Requesting number of transactions")
    countRequest = requests.post(req_url,
                                params=payload,
                                data = {'Aid':'CSD',
                                        'Year':cur_yr,
                                        'CurrentPageIndex':0,
                                        'PageSize':'1',
                                        'ShowSuperceded':'false'})
    if countRequest.status_code == 200:
        formTransactions = countRequest.json()['totalMatchingCount']
        if formTransactions < 1000:
            requestLoops = 1
        else:
            requestLoops = math.ceil(formTransactions/1000)
        transactionsList = []
        for i in range(requestLoops):
            print("Requesting transactions " + str(i))
            page = str(i)
            transactRequest = requests.post(req_url,
                                            params=payload,
                                            data={'Aid':'CSD',
                                                  'Year':cur_yr,
                                                  'CurrentPageIndex':page,
                                                  'PageSize':'1000',
                                                  'ShowSuperceded':'false'})
            if transactRequest.status_code != 200:
                return "Transaction request " + str(i) + " failed " + str(transactRequest.status_code)
            else:
                print("Transaction request " + str(i) + " success")
                transactions_json = transactRequest.json()['results']
                num_transactions = 0
                for t in transactions_json:
                    if t['form_Type'] == 'A' or t['form_Type'] == 'C':
                        if t['line_Item'] == '2':
                            num_transactions += 1
                            if t['form_Type'] == 'A':
                                description = 'Unitemized monetary contributions less than $100'
                                schedule = 'SMRY A'
                            elif t['form_Type'] == 'C':
                                description = 'Unitemized nonmonetary contributions less than $100'
                                schedule = 'SMRY C'
                            transactionsList.append(['460', #form
                                           schedule, #schedule
                                           description, #schedule_description
                                           t['filerStateId'], #recipient_id
                                           t['filerName'], #recipient_name
                                           t['filingStartDate'], #'report_period_from'
                                           t['filingEndDate'], #'report_period_to'
                                           ' ', #'contributor_code'
                                           ' ', #'contributor_last'
                                           ' ', #'contributor_first'
                                           ' ', #'contributor_city'
                                           ' ', #'contributor_state'
                                           ' ', #'contributor_zip'
                                           ' ', #'contributor_emp'
                                           ' ', #'contributor_occ'
                                           ' ', #'contribution_date'
                                           t['amount_A'], #'contribution_amount'
                                           t['amount_B'], #'contribution_annual'
                                           ' ', #'contribution_desc'
                                           ' ', #'contributor_id'
                                           ' ', #'intermediary_last'
                                           ' ', #'intermediary_first'
                                           ' ', #'intermediary_city'
                                           ' ', #'intermediary_state'
                                           ' ', #'intermediary_zip'
                                           ' ', #'intermediary_emp'
                                           ' ', #'intermediary_occ'
                                           t['filingId'],
                                             cur_yr])

        campaignTransactions = pd.DataFrame(transactionsList,columns=prod_columns)

        print("Writing 460 summary transactions to temp")
        campaignTransactions.to_csv(save_path,index=False)
    else:
        return "Count request failed " + str(countRequest.status_code)
        
    return "Created 460 summary transactions " + str(num_transactions)

def get_transactions_497():
    """ Requesting transactions for 497 """

    # Getting transactions for 24-hr 497 reports
    # Which contain transactions in between semi-annual,
    # pre-election reports

    date_checks_max = pd.read_csv('date_checks_max.csv')
    save_path = 'schedule_497.csv'
    req_url = "https://netfile.com:443/" \
                + "Connect2/api/public/" \
                + "campaign/export/cal201/" \
                + "transaction/year"
    print("Requesting number of transactions")
    countRequest = requests.post(req_url,
                                params=payload,
                                data = {'Aid':'CSD',
                                        'Year':cur_yr,
                                        'CurrentPageIndex':0,
                                        'PageSize':'1',
                                        'TransactionType':forms['497P1'],
                                        'ShowSuperceded':'false'})
    if countRequest.status_code == 200:
        formTransactions = countRequest.json()['totalMatchingCount']
        if formTransactions < 1000:
            requestLoops = 1
        else:
            requestLoops = math.ceil(formTransactions/1000)
        transactionsList = []
        for i in range(requestLoops):
            print("Requesting transactions " + str(i))
            page = str(i)
            transactRequest = requests.post(req_url,
                                            params=payload,
                                            data={'Aid':'CSD',
                                                  'Year':cur_yr,
                                                  'CurrentPageIndex':page,
                                                  'PageSize':'1000',
                                                  'TransactionType':forms['497P1'],
                                                  'ShowSuperceded':'false'})
            if transactRequest.status_code != 200:
                return "Transaction request " + str(i) + " failed " + str(transactRequest.status_code)
            else:
                print("Transaction request " + str(i) + " success")
                transactions_json = transactRequest.json()['results']
                num_transactions = 0
                for t in transactions_json:
                    transaction_date = pd.to_datetime(t['tran_Date'])
                    for i, row in date_checks_max.iterrows():
                        if row[0] == t['filerStateId'] and row[0] != "Pending":
                            if transaction_date > pd.to_datetime(row[1]):
                                num_transactions += 1
                                transactionsList.append(['497', #form
                                       t['form_Type'], #schedule
                                       '24-hr contribution report', #schedule_description
                                       t['filerStateId'], #recipient_id
                                       t['filerName'], #recipient_name
                                       t['filingStartDate'], #'report_period_from'
                                       t['filingEndDate'], #'report_period_to'
                                       t['entity_Cd'], #'contributor_code'
                                       t['tran_NamL'], #'contributor_last'
                                       t['tran_NamF'], #'contributor_first'
                                       t['tran_City'], #'contributor_city'
                                       t['tran_ST'], #'contributor_state'
                                       t['tran_Zip4'], #'contributor_zip'
                                       t['tran_Emp'], #'contributor_emp'
                                       t['tran_Occ'], #'contributor_occ'
                                       t['tran_Date'], #'contribution_date'
                                       t['tran_Amt1'], #'contribution_amount'
                                       t['tran_Amt2'], #'contribution_annual'
                                       t['tran_Dscr'], #'contribution_desc'
                                       t['cmte_Id'], #'contributor_id'
                                       t['intr_NamL'], #'intermediary_last'
                                       t['intr_NamF'], #'intermediary_first'
                                       t['intr_City'], #'intermediary_city'
                                       t['intr_ST'], #'intermediary_state'
                                       t['intr_Zip4'], #'intermediary_zip'
                                       t['intr_Emp'], #'intermediary_emp'
                                       t['intr_Occ'], #'intermediary_occ'
                                       t['filingId'],
                                         cur_yr])

        campaignTransactions = pd.DataFrame(transactionsList,columns=prod_columns)
        print("Writing 497 24-hr transactions to temp")
        campaignTransactions.to_csv(save_path,index=False)
    else:
        return "Count request failed " + str(countRequest.status_code)
        
    return "Created 497 24-hr transactions " + str(num_transactions)

def get_transactions_496():
    """ Requesting transactions for 496 """

    # Getting transactions for 24-hr 496 reports
    # Which contain transactions in between semi-annual,
    # pre-election reports

    date_checks_max = pd.read_csv('date_checks_max.csv')
    save_path = 'schedule_496.csv'
    req_url = "https://netfile.com:443/" \
                + "Connect2/api/public/" \
                + "campaign/export/cal201/" \
                + "transaction/year"
    print("Requesting number of transactions")
    countRequest = requests.post(req_url,
                                params=payload,
                                data = {'Aid':'CSD',
                                        'Year':cur_yr,
                                        'CurrentPageIndex':0,
                                        'PageSize':'1',
                                        'TransactionType':forms['496'],
                                        'ShowSuperceded':'false'})
    if countRequest.status_code == 200:
        formTransactions = countRequest.json()['totalMatchingCount']
        if formTransactions < 1000:
            requestLoops = 1
        else:
            requestLoops = math.ceil(formTransactions/1000)
        transactionsList = []
        for i in range(requestLoops):
            print("Requesting transactions " + str(i))
            page = str(i)
            transactRequest = requests.post(req_url,
                                            params=payload,
                                            data={'Aid':'CSD',
                                                  'Year':cur_yr,
                                                  'CurrentPageIndex':page,
                                                  'PageSize':'1000',
                                                  'TransactionType':forms['496'],
                                                  'ShowSuperceded':'false'})
            if transactRequest.status_code != 200:
                return "Transaction request " + str(i) + " failed " + str(transactRequest.status_code)
            else:
                print("Transaction request " + str(i) + " success")
                transactions_json = transactRequest.json()['results']
                num_transactions = 0
                for t in transactions_json:
                    if t['sup_Opp_Cd'] == 'S':
                        candName = t['cand_NamF']+' '+t['cand_NamL']
                        balName = t['bal_Name']
                        otherNameF = t['tran_NamF']
                        otherNameL = t['tran_NamL']
                        if balName != '':
                            fullName = balName
                        elif candName != ' ':
                            fullName = candName.strip()
                        else:
                            fullName = otherNameL

                    # Create row
                    transaction_date = pd.to_datetime(t['tran_Date'])
                    for i, row in date_checks_max.iterrows():
                        if row[0] == t['filerStateId'] and row[0] != "Pending":
                            if transaction_date > pd.to_datetime(row[1]):
                                num_transactions += 1
                                transactionsList.append(['496', #form
                                       t['form_Type'], #schedule
                                       'Independent expenditures in support', #schedule_description
                                       t['cmte_Id'], #recipient_id
                                       fullName, #recipient_name
                                       t['filingStartDate'], #'report_period_from'
                                       t['filingEndDate'], #'report_period_to'
                                       ' ', #'contributor_code'
                                       t['filerName'], #'contributor_last'
                                       ' ', #'contributor_first'
                                       ' ', #'contributor_city'
                                       ' ', #'contributor_state'
                                       ' ', #'contributor_zip'
                                       ' ', #'contributor_emp'
                                       ' ', #'contributor_occ'
                                       t['tran_Date'], #'contribution_date'
                                       t['tran_Amt1'], #'contribution_amount'
                                       t['tran_Amt2'], #'contribution_annual'
                                       t['tran_Dscr'], #'contribution_desc'
                                       t['filerStateId'], #'contributor_id'
                                       t['intr_NamL'], #'intermediary_last'
                                       t['intr_NamF'], #'intermediary_first'
                                       t['intr_City'], #'intermediary_city'
                                       t['intr_ST'], #'intermediary_state'
                                       t['intr_Zip4'], #'intermediary_zip'
                                       t['intr_Emp'], #'intermediary_emp'
                                       t['intr_Occ'], #'intermediary_occ'
                                       t['filingId'],
                                         cur_yr])

        campaignTransactions = pd.DataFrame(transactionsList,columns=prod_columns)
        print("Writing 496 24-hr transactions to temp")
        campaignTransactions.to_csv(save_path,index=False)
        
    else:
        return "Count request failed " + str(countRequest.status_code)
        
    return "Created 496 24-hr transactions " + str(num_transactions)

def combine_all_schedules():
  """ Transactions combined into one file for year-to-date """

  schedule_460a = pd.read_csv('schedule_460a.csv')
  schedule_460b1 = pd.read_csv('schedule_460b1.csv')
  schedule_460c = pd.read_csv('schedule_460c.csv')
  schedule_460d = pd.read_csv('schedule_460d.csv')
  schedule_460sum = pd.read_csv('schedule_460sum.csv')
  form_497 = pd.read_csv('schedule_497.csv')
  form_496 = pd.read_csv('schedule_496.csv')

  outputDF = pd.concat([schedule_460a, 
    schedule_460b1,
    schedule_460c,
    schedule_460d,
    schedule_460sum,
    form_497,form_496], ignore_index=True)

  outputDF.to_csv(prod_file,index=False)


  return "Created prod file"

get_transactions_a()
get_transactions_b()
get_transactions_c()
get_transactions_d()
get_transactions_summary()
get_transactions_496()
get_transactions_497()
combine_all_schedules()

