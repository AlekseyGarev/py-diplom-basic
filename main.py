import requests
import json
from datetime import datetime
from tqdm import tqdm
from tokens import vk_token 


result_data = []

id_vk = input('Введите айди пользователя:')
 
n_photo = input('Введите кол-во фото для скачивания(По умолчанию 5шт):')

if n_photo.isdigit():
    n_photo = int(n_photo)
else:
    print('Вы ввели не число! По умолчанию ставим - 5')
    n_photo = 5   


ya_token = input('Введите токен с Полигона Яндекс.Диска:')

down_photo_url = 'https://api.vk.com/method'
params = {
    'access_token': vk_token,
    'owner_id': id_vk,
    'count': n_photo,
    'album_id': 'profile',
    'v': '5.199',
    'extended': 1
}

response = requests.get(f'{down_photo_url}/photos.get', params=params)

data = response.json()
total_photos = data['response']['count']
print(f'Найдено:{total_photos} фото!')

if n_photo > total_photos:
    download_photo = total_photos
else:
    download_photo = n_photo    

yd_url = 'https://cloud-api.yandex.net/v1/disk/resources'
params = {'path': 'Photo'}
headers = {'Authorization': ya_token}
response = requests.put(yd_url, params=params, headers=headers)

with tqdm(total=download_photo, desc="Процесс выполнения", unit="фото") as pbar:
    name_list = []
    
    for item in data['response']['items']:
        img_url = item['sizes'][-1]['url']
        img_name = item['likes']['count']
        if img_name in name_list:
            current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
            img_name = f"{item['likes']['count']}_{current_time}"
        else:
            name_list.append(img_name)


        result_data.append({
            "file_name": f"{img_name}.jpg",
            "size": item['sizes'][-1]['type']
        })

        upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        params = {
        'path': f'Photo/{img_name}',
        'url': {img_url}
        }

        response = requests.post(upload_url, params=params, headers=headers)
    
        pbar.set_postfix(file=f"{img_name}.jpg")
        pbar.update(1)

with open('result.json', 'w', encoding='utf-8') as f:
    json.dump(result_data, f, ensure_ascii=False, indent=4)