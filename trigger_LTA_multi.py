# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 09:13:34 2019

@author: Nejc Coz
@copyright: ZRC SAZU (Novi trg 2, 1000 Ljubljana, Slovenia)

Call multiple triggers in parallel.
"""

from trigger_LTA import main

if __name__ == "__main__":
    # TODO: import cocncurent futures (check how sentinel api does it)
    # Each request on individual thread

    # Path to CSV file with a list of products to be triggered
    csv_pth = ".\\userfiles\\SLC_all.csv"

    # Path to log file
    log_pth = ".\\userfiles\\LOG_trigg_0.log"

    # Path to file with SciHub credentials
    api_pth = ".\\userfiles\\apihub.txt"

    # For splitting between multiple accounts
    sequence = (1, 9)  # tuple = (seq. nr, total sequences)

    main(csv_pth, log_pth, api_pth, sequence)