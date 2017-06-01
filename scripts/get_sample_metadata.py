import sys
import os
import json
import urllib2
import xmltodict


# Get the list of JSON files
json_files = [os.path.join(root, name)
  for root, dirs, files in os.walk('.')
    for name in files
      if name.endswith((".json"))]

print ("Sample\tTreatment\tTime\tTissue")
for json_file in json_files:
  json_data = open(json_file).read()
  data = json.loads(json_data)
  sample = data['EXPERIMENT_PACKAGE_SET']['EXPERIMENT_PACKAGE']['SAMPLE']
  run_set = data['EXPERIMENT_PACKAGE_SET']['EXPERIMENT_PACKAGE']['RUN_SET']['RUN']
  accession = run_set['@accession']
  attributes = sample['SAMPLE_ATTRIBUTES']['SAMPLE_ATTRIBUTE']
  treatment = ''
  time = ''
  tissue = ''
  for attribute in attributes:
    if attribute['TAG'] == 'treatment':
      treatment = attribute['VALUE']
    if attribute['TAG'] == 'time':
      time = attribute['VALUE']
    if attribute['TAG'] == 'tissue':
      tissue = attribute['VALUE']
  print (accession + "\t" + treatment + "\t" + time + "\t" + tissue)
