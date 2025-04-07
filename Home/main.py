import requests
import os
import json
from datetime import datetime
from tqdm import tqdm
from tokens import vk_token
from pprint import pprint 

gl_count = 0
id_vk = input('Введите айди пользователя:')
n_photo = int(input('Введите кол-во фото для скачивания(По умолчанию 5шт):'))
if n_photo == '':
    n_photo = 5

ya_token = input('Введите токен с Полигона Яндекс.Диска:')
result_data = []

down_photo_url = 'https://api.vk.com/method'
params = {
    'access_token': vk_token,
    'owner_id': id_vk,
    'album_id': 'profile',
    'v': '5.199',
    'extended': 'True'
}

response = requests.get(f'{down_photo_url}/photos.get', params=params)

data = response.json()
total_photos = data['response']['count']
print(f'Найдено:{total_photos} фото!')
with tqdm(total=n_photo, desc="Процесс выполнения", unit="фото") as pbar:
    
    for item in data['response']['items']:
        img_url = item['sizes'][-1]['url']
        img_name = item['likes']['count']
        if os.path.exists(f'{img_name}.jpg'):
            current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
            img_name = f"{item['likes']['count']}_{current_time}"


        photo_response = requests.get(img_url)
        with open(f'{img_name}.jpg', 'wb') as f:
            f.write(photo_response.content)        
        # print(img_url, img_name)

        yd_url = 'https://cloud-api.yandex.net/v1/disk/resources'
        params = {'path': 'Photo'}
        headers = {'Authorization': ya_token}
        responce = requests.put(yd_url, params=params, headers=headers)

        upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        params = {'path': f'Photo/{img_name}.jpg'}

        response = requests.get(upload_url, params=params, headers=headers)
        url_for_upload = response.json()['href']
        with open(f'{img_name}.jpg', 'rb') as f:
            requests.put(url_for_upload, files={'file': f})
            result_data.append({
            "file_name": f"{img_name}.jpg",
            "size": item['sizes'][-1]['type']
        })
            pbar.set_postfix(file=f"{img_name}.jpg")
            pbar.update(1)
            gl_count += 1
            if gl_count == n_photo:
                break


with open('result.json', 'w', encoding='utf-8') as f:
    json.dump(result_data, f, ensure_ascii=False, indent=4)






# for item in data['response']['items']:
#     id_photo = item['id']
#     owner_id_photo = item['owner_id']
#     url_photo = item['orig_photo']['url']
#     print(url_photo)
#     response2 = requests.get(f'{down_photo_url}/photos.getById?photos={owner_id_photo}_{id_photo}', params=params)
#     likes = response2.json()['response'][0]['likes']['count']
#     print(likes)
#     photo_response = requests.get(url_photo)
#     with open(f'{likes}.jpg', 'wb') as f:
#         f.write(photo_response.content)



# # Создание папки на Яндекс Диске
# yd_url = 'https://cloud-api.yandex.net/v1/disk/resources'
# params = {'path': 'Photo'}
# headers = {'Authorization': ya_token}
# responce = requests.put(yd_url, params=params, headers=headers)
# print(responce.status_code)

# # Загрузка файла на Яндекс Диск
# upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
# params = {'path': 'Photo/{name_photo}'}
# headers = {'Authorization': ya_token}
# responce = requests.get(upload_url, params=params, headers=headers)
# url_for_upload = responce.json()['href']
# with open(f'', 'rb') as f:
#     requests.put(url_for_upload, files={'file': f})



# Получаем кол-во фоток у профиля
# pprint(response.json()['response']['count'])

# Получаем фото
# pprint(response.json()['response']['items'][0]['orig_photo']['url'])