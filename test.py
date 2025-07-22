import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def check_url(start_url, max_depth, current_depth=0, visited=None, found_original=False):
    if visited is None:
        visited = set()

    if current_depth > max_depth or start_url in visited:
        return visited, found_original

    try:
        response = requests.get(start_url, timeout=5)
        response.raise_for_status()
        html_content = response.text
    except Exception as e:
        print("Ошибка")
        return visited, found_original

    soup = BeautifulSoup(html_content, 'html.parser')
    links = soup.find_all('a')

    visited.add(start_url)

    for link in links:
        href = link.get('href')
        if not href:
            continue

        absolute_url = urljoin(start_url, href)

        if absolute_url == start_url and current_depth > 0:
            return visited, True

    for link in links:
        href = link.get('href')
        if not href:
            continue

        absolute_url = urljoin(start_url, href)

        if absolute_url not in visited and current_depth < max_depth:
            visited, found = check_url(
                absolute_url, max_depth, current_depth + 1, visited, found_original
            )
            if found:
                return visited, True

    return visited, False

start_url = input('Введите изначальную ссылку: ').strip()
max_depth = int(input('Введите количество обходов (1-5): '))

if max_depth > 5 or max_depth < 1:
    print('Неверное количество (должно быть от 1 до 5)')
else:
    visited, found = check_url(start_url, max_depth)
    print(found)
    ## перед началом введите в консоль: pip install -r requirements.txt
