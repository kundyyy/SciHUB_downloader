# -*- coding: utf-8 -*-
"""
Created on Thu Aug 22 10:12:00 2019

@author: Nejc Coz
@copyright: ZRC SAZU (Novi trg 2, 1000 Ljubljana, Slovenia)

IMPORTANT: Set your SciHUB account credentials in apihub.txt!

The script creates CSV file containing the list of files to be downloaded from
SciHUB API. The list includes file ID, title, and downloaded status.
"""

import os
import sys

from shapely.geometry import box
from sentinelsat import SentinelAPI
# from sentinelsat import read_geojson, geojson_to_wkt


def main(csvpath, apipath, qp):
    # Read password file
    # ==================
    try:
        with open(apipath) as f:
            (usrnam, psswrd) = f.readline().split(" ")
            if psswrd.endswith("\n"):
                psswrd = psswrd[:-1]
    except IOError:
        sys.exit("Error reading the password file!")

    # Connect to API using <username> and <password>
    # ===============================================
    print("Connecting to SciHub API...")
    api = SentinelAPI(usrnam, psswrd, "https://scihub.copernicus.eu/dhus")

    # Search by SciHub query keywords
    # ===============================
    products = api.query(qp['footprint'],
                         beginposition=(qp['strtime'], qp['endtime']),
                         endposition=(qp['strtime'], qp['endtime']),
                         platformname=qp['platformname'],
                         producttype=qp['producttype'])

    # Convert to Pandas DataFrame and sort by date ascending
    # ======================================================
    products_df = api.to_dataframe(products)
    products_df_sorted = products_df.sort_values('beginposition', ascending=True)

    # Save to CSV file
    # ================
    print(f"Saving list to {os.path.basename(csvpath)}")
    prep_csv = products_df_sorted[['uuid', 'title']]
    prep_csv.insert(2, "downloaded", False, allow_duplicates=True)
    prep_csv.to_csv(csvpath, index=False)

    print('Finished!')


if __name__ == "__main__":
    # Path to CSV file with a list of products to be triggered
    csv_pth = ".\\userfiles\\DK_isl.csv"

    # Path to file with SciHub credentials
    api_pth = ".\\userfiles\\apihub.txt"

    # Set query parameters
    ############################################################################
    #   * (Date-type query parameter 'beginposition' expects a two-element tuple
    #     of str or datetime objects.)
    #   * Search for last 24 hrs: date=('NOW-8HOURS', 'NOW') or NOW-<n>DAY(S) or
    #     datetime(2017, 1, 5, 23, 59, 59, 999999) + import datetime or string
    #     '2017-12-31T23:59:59.999Z'
    strtime = '2017-01-01T00:00:00.000Z'  # 'NOW-14DAYS'
    endtime = '2019-12-31T23:59:59.999Z'  # '2019-07-31T23:59:59.999Z'

    # Platform name:
    platformname = 'Sentinel-1'

    # Product type:
    producttype = 'SLC'

    # # Geographical extents (minx, miny, maxx, maxy)
    # footprint = box(13.278422963870495, 45.33663869316604,
    #                 16.687265418304985, 46.96845660190081)

    # # DK
    # footprint = "POLYGON ((8.1033117000000008 54.5929266999999996," \
    #             " 8.1033117000000008 56.9700600651396343," \
    #             " 9.6849787446935096 57.5727969000000002," \
    #             " 11.3985439642586321 57.5727969000000002," \
    #             " 11.3178000533890710 57.2122917977483141," \
    #             " 10.9051089533890941 56.6470844216613898," \
    #             " 11.2549992338238578 56.3510234151396645," \
    #             " 12.6372213363646999 56.2561073303223012," \
    #             " 12.6814749925194299 54.5929266999999996," \
    #             " 12.6814749925194299 54.5929266999999996," \
    #             " 8.1033117000000008 54.5929266999999996))"

    # DK small
    footprint = "POLYGON((14.6540499750765516 54.9727815065246190," \
                " 14.6540499750765516 55.3212713285623821," \
                " 15.1624632085973996 55.3212713285623821," \
                " 15.1624632085973996 54.9727815065246190," \
                " 14.6540499750765516 54.9727815065246190))"

    # # NL
    # footprint = "POLYGON((7.2374317000000001 53.4855396000000027," \
    #             " 7.2374317000000001 51.8134772943518342," \
    #             " 6.2301860398024003 51.7716100813083600," \
    #             " 6.2436433582806607 50.7342656000000005," \
    #             " 5.5692821767589598 50.7342656000000005," \
    #             " 5.5704036199654787 51.1127621974768829," \
    #             " 3.3850240999999999 51.1391161128301519," \
    #             " 3.3850240999999999 51.7441347227485977," \
    #             " 4.3872810370851072 52.3766286912268342," \
    #             " 4.8044579099111706 53.4855396000000027," \
    #             " 7.2374317000000001 53.4855396000000027))"

    # nam_aoi = 'polygon.geojson'
    # pth_aoi = join(wrkdir, nam_aoi)
    # footprint = geojson_to_wkt(read_geojson(pth_aoi))

    query_params = {
        'strtime': strtime,
        'endtime': endtime,
        'platformname': platformname,
        'producttype': producttype,
        'footprint': footprint
    }

    main(csv_pth, api_pth, query_params)
