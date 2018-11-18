from base64 import b64encode, b64decode
import json

def handler(event, context):
	records = event['records']
	for record in records:
		record.pop('approximateArrivalTimestamp', None)
		print(f"decoded: '{b64decode(record['data']).decode('utf8')}'")
		record.update({'result': 'Ok'}) # Ok, Dropped, ProcessingFailed
	print(json.dumps(records))
	return {'records': records}
