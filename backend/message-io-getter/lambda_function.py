import json
import boto3

BUCKET = 'message-io-bucket'
DATA_FILE = 'data.json'

s3_client = boto3.client('s3')

def load_data():
    response = s3_client.get_object(Bucket=BUCKET, Key=DATA_FILE)
    body = response['Body'].read()
    data_dict = json.loads(body.decode('utf-8'))
    return data_dict

def type_check(event):
    if not 'channel_id' in event:
        return 'key: "channel_id" is not contained.'
    elif not 'next_message_id' in event:
        return 'key: "next_message_id" is not contained.'
    elif not 'limit' in event:
        return 'key: "limit" is not contained.'
    elif event['channel_id'] != None and not isinstance(event['channel_id'], (int, str)):
        return f'"channel_id" must be an string or integer or null, not {type(event['channel_id'])}.'
    elif event['next_message_id'] != None and not isinstance(event['next_message_id'], (int ,str)):
        return f'"next_message_id" must be an string or integer or null, not {type(event['next_message_id'])}.'
    elif event['limit'] != None and not isinstance(event['limit'], int):
        return f'"limit" must be an integer or null, not {type(event['limit'])}.'
    if event['channel_id']:
        try:
            event['channel_id'] = int(event['channel_id'])
        except:
            return '"channel_id" can not be converted to integer.'
    if event['next_message_id']:
        try:
            event['next_message_id'] = int(event['next_message_id'])
        except:
            return '"next_message_id" can not be converted to integer.'
    return None

def binary_search_message(messages, id, limit):
    left, right = 0, len(messages)-1
    while left <= right:
        mid = (left + right) // 2
        if messages[mid]['id'] == id:
            if limit:
                return messages[mid+1:mid+limit+1]
            else:
                return messages[mid+1:]
        elif messages[mid]['id'] < id:
            left = mid + 1
        else:
            right = mid - 1
    return None

def lambda_handler(event, context):
    print('deployment is successful!')
    event = json.loads(event['body'])
    diff_type = type_check(event)
    if diff_type:
        return {
            'statusCode': 405,
            'body': json.dumps(diff_type)
        }
    data_dict: list[dict] = load_data()
    if event['channel_id']:
        for channel in data_dict:
            if channel['id'] == event['channel_id']:
                target_channel = channel
                break
        if target_channel:
            if not 'name' in target_channel:
                return {
                    'statusCode': 200,
                    'body': json.dumps([target_channel])
                }
            if event['next_message_id']:
                messages = binary_search_message(target_channel['messages'], event['next_message_id'], event['limit'])
                if messages == None:
                    return {
                        'statusCode': 405,
                        'body': json.dumps(f'"next_message_id": {event['next_message_id']} is not existed.')
                    }
            else:
                messages = target_channel['messages'][:event['limit']]

            target_channel['messages'] = messages
            return {
                'statusCode': 200,
                'body': json.dumps([target_channel])
            }
        else:
            return {
                'statusCode': 405,
                'body': json.dumps(f'"channel_id": {event['channel_id']} is not existed.')
            }
    else:
        channels = []
        for channel in data_dict:
            if 'name' in channel:
                channel['messages'] = channel['messages'][:event['limit']]
                channels.append(channel)
            else:
                channels.append(channel)

        return {
            'statusCode': 200,
            'body': json.dumps(channels)
        }
