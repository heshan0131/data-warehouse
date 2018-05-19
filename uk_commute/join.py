# -*- coding: utf-8 -*-
import json_util
import csv_util
import bcolors
import sys

mosa_file = 'mosa_pop_weighted_centroid.csv'
commute_file = 'all_commutes.csv'
output_file = 'all_commutes_uk.csv'

# longitude,latitude,objectid,msoa11cd,msoa11nm
min_flow = 10
decimal = 6

def round_to(str, num):
	return round(float(str), num)

def add_geo(commute, mosa):
	final = []
	missing = []
	for cm in commute:
		resid_id = cm['o_id']
		work_id = cm['d_id']

		if not resid_id in mosa:
			if not resid_id in missing:
				missing.append(resid_id)
		elif not work_id in mosa:
			if not work_id in missing:
				missing.append(work_id)
		elif int(cm['allflows']) >= min_flow:
			loc_res = mosa[resid_id]
			loc_work = mosa[work_id]
	
			row = {
				'residence_lat': round_to(loc_res['latitude'], decimal),
				'residence_lng': round_to(loc_res['longitude'],  decimal),
				#'residentc_name': loc_res['msoa11nm'],
				'workplace_lat': round_to(loc_work['latitude'],  decimal),
				'workplace_lng': round_to(loc_work['longitude'],  decimal),
				#'workplace_name': loc_work['msoa11nm'],
				'all_flows': cm['allflows']
			}
			final.append(row)

	bcolors.log_fail('missing {0}'.format(missing))
	return final

def csv_dict_to_row(csv_dict):
	rows = []
	headers = csv_dict[0].keys()

	for row in csv_dict:
		data = map(lambda x: row[x], headers)

		rows.append(data)
	return [headers, rows]

def main():
	mosa = csv_util.load_csv(mosa_file)
	commute = csv_util.load_csv(commute_file)
	
	mosa_dict = {}

	# biuld mosa dict
	for area in mosa:
		id = area['msoa11cd']
		mosa_dict[id] = area

	final_commute = add_geo(commute, mosa_dict)
	csv_rows = csv_dict_to_row(final_commute)

	csv_util.save_to_csv(csv_rows[0], csv_rows[1], output_file)


if __name__ == "__main__":

	main()