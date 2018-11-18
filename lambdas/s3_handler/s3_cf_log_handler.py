import boto3
import json
import os
from base64 import b64encode

s3 = boto3.resource('s3')
firehose = boto3.client('firehose')

delivery_stream_name = os.environ['DELIVERY_STREAM_NAME']

def process_line(line: str):
    record = line.strip('\n').split('\t')
    return {
        'date': record[0],
        'time': record[1],
        'x-edge-location': record[2],
        'sc-bytes': record[3],
        'c-ip': record[4],
        'cs-method': record[5],
        'cs-host': record[6],
        'cs-uri-stem': record[7],
        'sc-status': record[8],
        'cs-referer': record[9],
        'cs-user-agent': record[10],
        'cs-uri-query': record[11],
        'cs-cookie': record[12],
        'x-edge-result-type': record[13],
        'x-edge-request-id': record[14],
        'x-host-header': record[15],
        'cs-protocol': record[16],
        'cs-bytes': record[17],
        'time-taken': record[18],
        'x-forwarded-for': record[19],
        'ssl-protocol': record[20],
        'ssl-cipher': record[21],
        'x-edge-response-result-type': record[22],
        'cs-protocol-version': record[23],
        'fle-status': record[24],
        'fle-encrypted-fields': record[25]
    }

def filter_lines(lines: [str]) -> [str]:
    return list(filter(lambda line: not line.startswith('#'), lines))

def publish(batch: [dict]) -> None:
    assert len(batch) <= 500
    data = []
    for log in batch:
        encoded = bytes(json.dumps(log), 'utf-8')
        data.append({'Data': encoded})

    print(f'Publishing to {delivery_stream_name} data: {data}')
    firehose.put_record_batch(DeliveryStreamName=delivery_stream_name, Records=data)

def handler(event, ctx):
    counter = 0
    batch: [dict] = []
    bucket_event = event['Records'][0]
    if bucket_event['eventName'] == 'ObjectCreated:Put':
        bucket = bucket_event['s3']['bucket']['name']
        key = bucket_event['s3']['object']['key']
        obj = s3.Object(bucket, key)
        for line in obj.get()['Body'].read().splitlines():
            text: str = line.decode('utf-8')
            if not text.startswith('#'):
                if counter < 500:
                    batch.append(process_line(text))
                    counter += 1
                else:
                    publish(batch)
                    batch = []
                    counter = 0

        if counter is not 0:
            publish(batch)


