# Задание на курсовой проект «Резервное копирование» первого блока «Основы языка программирования Python».

# озможна такая ситуация, что мы хотим показать друзьям фотографии из социальных сетей, но соц. сети могут быть
# недоступны по каким-либо причинам. Давайте защитимся от такого.
# Нужно написать программу для резервного копирования фотографий с профиля(аватарок) пользователя vk в облачное
# хранилище Яндекс.Диск.
# Для названий фотографий использовать количество лайков, если количество лайков одинаково, то добавить дату загрузки.
# Информацию по сохраненным фотографиям сохранить в json-файл.
# Нужно написать программу, которая будет:
#
# Получать фотографии с профиля. Для этого нужно использовать метод photos.get.
# Сохранять фотографии максимального размера(ширина/высота в пикселях) на Я.Диске.
# Для имени фотографий использовать количество лайков.
# Сохранять информацию по фотографиям в json-файл с результатами.
#
# Пользователь вводит:
#
# id пользователя vk;
# токен с Полигона Яндекс.Диска. Важно: Токен публиковать в github не нужно!
# Выходные данные:
# json-файл с информацией по файлу:
#     [{
#     "file_name": "34.jpg",
#     "size": "z"
#     }]
# Измененный Я.диск, куда добавились фотографии.​​
# Обязательные требования к программе:
# Использовать REST API Я.Диска и ключ, полученный с полигона.
# Для загруженных фотографий нужно создать свою папку.
# Сохранять указанное количество фотографий(по умолчанию 5) наибольшего размера (ширина/высота в пикселях) на Я.Диске
# Сделать прогресс-бар или логирование для отслеживания процесса программы.
# Код программы должен удовлетворять PEP8.
# У программы должен быть свой отдельный репозиторий.
# Все зависимости должны быть указаны в файле requiremеnts.txt.​
# Необязательные требования к программе:
# Сохранять фотографии и из других альбомов.
# Сохранять фотографии на Google.Drive.

import requests
import time
# import tqdm
import json

with open('token.txt', 'r') as f:
    vk_token = f.read().strip()

def main():
    class VkDownloader:

        def __init__(self, token):
            self.token = token

        def get_photos(self, offset=0, count=5):

            url = 'https://api.vk.com/method/photos.get'
            params = {'owner_id': user_id,
                      'album_id': 'wall',
                      'access_token': vk_token,
                      'v': '5.131',
                      'extended': '1',
                      'photo_sizes': '1',
                      'count': count,
                      'offset': offset
                      }
            res = requests.get(url=url, params=params)
            return res.json()

        def get_all_photos(self):
            data = self.get_photos()
            all_photo_count = data['response']['count']
            i = 0
            count = 5
            photos = []
            global max_size_photo_var
            max_size_photo = {}
            max_size_photo_var = max_size_photo
            while i <= all_photo_count:
                if i != 0:
                    data = self.get_photos(offset=i, count=count)
                for photo in data['response']['items']:
                    max_size = 0
                    photos_info = {}
                    for size in photo['sizes']:
                        if size['height'] >= max_size:
                            max_size = size['height']
                    if photo['likes']['count'] not in max_size_photo.keys():
                        max_size_photo[photo['likes']['count']] = size['url']
                        photos_info['file_name'] = f"{photo['likes']['count']}.jpg"
                    else:
                        max_size_photo[f"{photo['likes']['count']} + {time.ctime(photo['date'])}"] = size['url']
                        photos_info['file_name'] = f"{photo['likes']['count']}+{time.ctime(photo['date'])}.jpg"
                    photos_info['size'] = size['type']
                    photos.append(photos_info)
                i += count
            with open("photos.json", "w") as f:
                json.dump(photos, f, indent=4)
            return max_size_photo_var

    user_id = ''
    downloader = VkDownloader(vk_token)
    downloader.get_all_photos()

    class YaUploader:
        def __init__(self, token: str):
            self.token = token

        def folder_creation(self):
            url = f'https://cloud-api.yandex.net/v1/disk/resources/'
            headers = {'Content-Type': 'application/json',
                       'Authorization': f'OAuth {ya_token}'}
            params = {'path': f'{folder_name}',
                      'overwrite': 'false'}
            response = requests.put(url=url, headers=headers, params=params)
            return response

        def upload(self):
            file_name = ''
            url = f'https://cloud-api.yandex.net/v1/disk/resources/upload'
            headers = {'Content-Type': 'application/json',
                       'Authorization': f'OAuth {ya_token}'}
            params = {'path': f'{folder_name}/{file_name}',
                      'overwrite': 'true'}
            response = requests.get(url=url, headers=headers, params=params)
            href = response.json().get('href')
            print(max_size_photo_var)
            print(href)
            for file_name, files_path in max_size_photo_var.items():
                file_from_url = requests.get(files_path)
                requests.put(href, file_from_url)

    ya_token = ''
    folder_name = 'images_vk'
    uploader = YaUploader(ya_token)
    uploader.folder_creation()
    uploader.upload()

if __name__ == '__main__':
    main()
