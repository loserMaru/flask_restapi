import requests
from flask import request


def upload_image_to_imgur(image_path, client_id):
    print(request.url)
    headers = {'Authorization': f'Client-ID {client_id}'}
    url = 'https://api.imgur.com/3/image'

    with open(image_path, 'rb') as image_file:
        files = {'image': image_file}
        print(files)
        response = requests.post(url, headers=headers, files=files)

    if response.status_code == 200:
        data = response.json()
        image_url = data['data']['link']
        return image_url
    else:
        print('Image upload failed. Error:', response.status_code)
        return None
