# curl "http://commute.datashine.org.uk/getflows.php?msoa=E02000120&direction=both&mode=allflows" -H 'Content-Type:application/json'
import json_util
import csv_util
import bcolors
import sys
import urllib2
import json, csv
import requests

r_headers = {'Content-Type': 'application/json'}
mosa_file = 'mosa_pop_weighted_centroid.csv'
output_file = 'all_commutes.csv'

headers = ['d_id', 'o_id', 'allflows']

def get_mosa_data(mosas):
	rows = []
	count = 1
	total = len(mosas)
	with open(output_file, 'wb') as csvout:
		spamwriter = csv.writer(csvout, dialect = 'excel')
		spamwriter.writerow(headers)

		for mosa in mosas:
			id = mosa['msoa11cd']
			print '\r', bcolors.OKBLUE + 'requesting {0}/{1} ...'.format(count, total) + bcolors.ENDC

			url = 'http://commute.datashine.org.uk/getflows.php?msoa={0}&direction=both&mode=allflows'.format(id)
			raw_result = requests.get(url, headers=r_headers)

			if raw_result:
				results = raw_result.json()
					
				for result in results:
					spamwriter.writerow(map(lambda x: result[x], headers))

			count += 1

	csvout.close()
	
def main():
	mosas = csv_util.load_csv(mosa_file)

	get_mosa_data(mosas)

if __name__ == "__main__":
	main()