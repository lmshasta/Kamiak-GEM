import sys
import os
import json
import urllib2
import xmltodict

query = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=sra&term='
fetch = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=sra&id='

sra_file = open('SRA_IDs.txt', 'r')
for line in sra_file:

  # Get the current SRA ID.
  sra_id = line.strip()
  print('Retreiving ' + sra_id)
  
  # Make sure our sample directory exists.
  if not os.path.exists(sra_id):
    os.makedirs(sra_id)
  
  # First perform the entrez query with the SRA database.
  response_obj = urllib2.urlopen(query + sra_id + '[Accession]')
  response_xml = response_obj.read()
  response = xmltodict.parse(response_xml)
  query_id = response['eSearchResult']['IdList']['Id']
  
  # Next get the query results. We are only querying a single SRA
  # record at a time.
  response_obj = urllib2.urlopen(fetch + query_id)
  response_xml = response_obj.read()
  response = xmltodict.parse(response_xml)
  meta_file = open(sra_id + '/' + sra_id + '.sra.json', 'w')
  meta_file.write(json.dumps(response))
  meta_file.close()

  
sra_file.close()
