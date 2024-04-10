import requests


def get_api_login():
    try:
        with open('api_login', 'r') as file:
            api_login = file.read().strip()
            return api_login
    except FileNotFoundError:
        print("Файл 'api_login' не найден")
        return None


def get_token(api_login):
    url = 'https://api-ru.iiko.services/api/1/access_token'

    payload = {
        'apiLogin': api_login
    }

    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        token = response.json().get('token')
        return token
    else:
        print("Error:", response.status_code)
        return None


def get_organisation_id(api_login):
    token = get_token(api_login)
    if not token:
        return None

    url = 'https://api-ru.iiko.services/api/1/organizations'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        organizations = response.json().get('organizations')
        if organizations:
            return organizations[0]['id']
        else:
            print("No organizations found")
            return None
    else:
        print("Error:", response.status_code)
        return None


def get_menu():
    api_login = get_api_login()
    if not api_login:
        return None

    organization_id = get_organisation_id(api_login)
    if not organization_id:
        return None

    url = 'https://api-ru.iiko.services/api/1/nomenclature'
    headers = {
        'Authorization': f'Bearer {get_token(api_login)}',
        'Content-Type': 'application/json'
    }

    payload = {
        "organizationId": organization_id,
        "startRevision": 0
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        products = response.json().get('products')
        if products:
            menu = {product['name']: product['id'] for product in products}
            return menu
        else:
            print("No products found")
            return None
    else:
        print("Error:", response.status_code)
        return None


def get_terminal_group():
    api_login = get_api_login()
    if not api_login:
        return None

    organization_id = get_organisation_id(api_login)
    if not organization_id:
        return None

    url = 'https://api-ru.iiko.services/api/1/terminal_groups'
    headers = {
        'Authorization': f'Bearer {get_token(api_login)}',
        'Content-Type': 'application/json'
    }

    payload = {
        "organizationIds": [organization_id]
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        terminal_groups = response.json().get('terminalGroups')
        if terminal_groups:
            first_terminal_group_id = terminal_groups[0]['items'][0]['id']
            return first_terminal_group_id
        else:
            print("No terminal groups found")
            return None
    else:
        print("Error:", response.status_code)
        return None


def create_order(order_items):
    api_login = get_api_login()
    if not api_login:
        return None

    organization_id = get_organisation_id(api_login)
    if not organization_id:
        return None

    terminal_group_id = get_terminal_group()
    if not terminal_group_id:
        return None

    url = 'https://api-ru.iiko.services/api/1/order/create'
    headers = {
        'Authorization': f'Bearer {get_token(api_login)}',
        'Content-Type': 'application/json'
    }

    items = []
    for product_id, amount in order_items.items():
        item = {
            "productId": product_id,
            "type": "Product",
            "amount": amount,
            "comment": "Тестовый заказ. Не делать!"
        }
        items.append(item)

    payload = {
        "organizationId": organization_id,
        "terminalGroupId": terminal_group_id,
        "order": {
            "items": items
        }
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        print("Заказ успешно создан")
    else:
        print("Ошибка при создании заказа:", response.status_code)


def do_test_order():
    menu = get_menu()
    if not menu:
        print("Не удалось получить меню")
        return

    order_items = {}
    for product_id in list(menu.values())[:3]:
        order_items[product_id] = 0
    print(order_items)

    create_order(order_items)


if __name__ == "__main__":
    # do_test_order()
    pass