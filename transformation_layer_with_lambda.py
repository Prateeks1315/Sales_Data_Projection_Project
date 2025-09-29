import base64
import json
from datetime import datetime

def lambda_handler(event, context):
    output_records = []

    for record in event['records']:
        try:
            payload = base64.b64decode(record['data'])
            payload_json = json.loads(payload)

            event_name = payload_json['eventName']
            approx_creation_datetime = payload_json['dynamodb']['ApproximateCreationDateTime']

            # Handle both timestamp and string
            if isinstance(approx_creation_datetime, (int, float)):
                creation_datetime = datetime.utcfromtimestamp(approx_creation_datetime).isoformat() + 'Z'
            else:
                creation_datetime = str(approx_creation_datetime)

            dynamodb_data = payload_json['dynamodb']
            new_image = dynamodb_data.get('NewImage', {})

            if not new_image:
                raise ValueError("No NewImage present in record")

            transformed_data = {
                'orderid': new_image['orderid']['S'],
                'product_name': new_image['product_name']['S'],
                'quantity': int(new_image['quantity']['N']),
                'price': float(new_image['price']['N']),
                'cdc_event_type': event_name,
                'creation_datetime': creation_datetime
            }

            transformed_data_str = json.dumps(transformed_data) + '\n'
            transformed_data_encoded = base64.b64encode(
                transformed_data_str.encode('utf-8')
            ).decode('utf-8')

            output_records.append({
                'recordId': record['recordId'],
                'result': 'Ok',
                'data': transformed_data_encoded
            })

        except Exception as e:
            print(f"Error processing record {record['recordId']}: {e}")
            output_records.append({
                'recordId': record['recordId'],
                'result': 'ProcessingFailed',
                'data': record['data']
            })

    return {'records': output_records}
