from grequests import get as gget, map as gmap
from requests import get
from bs4 import BeautifulSoup
from json import dumps, loads


def if_int(string: str):
    return all([s.isdigit() for s in string.split()])


def check_response(response):
    response.encoding = "UTF-8"

    if response.status_code != 200:
        raise Exception("Parsing failed.")


def get_page(page=1):
    url = "https://www.21vek.by/notebooks/page:{page}/?order%5Bpopularity%5D=desc&filter%5Bsa%5D=".format(page=page)
    response = get(url)
    check_response(response)

    return response


def check_for_redirects(response):
    if len(response.history) > 0:
        return True

    return False


def select_notebooks(page_content):
    soup = BeautifulSoup(page_content, "lxml")
    notebooks = soup.select("li.result__item")

    if not len(notebooks):
        return None

    return notebooks


def get_notebook_specs(response, url):
    specs_page_content = response.content
    specs_html = BeautifulSoup(specs_page_content, "lxml")
    specs_info = specs_html.select_one("#j-tabs-attrs > div.tabs__content > div.b-info.cr-info-attrs").text.split()

    try:
        diagonal_start = specs_info.index("Диагональ")
        diagonal = float(specs_info[diagonal_start + 2])
    except:
        diagonal = 0

    try:
        ram_amount_index = specs_info.index("Объем")
        if specs_info[ram_amount_index + 1] == "оперативной":
            ram_amount = float(specs_info[ram_amount_index + 3])
        else:
            ram_amount = 0
    except:
        ram_amount = 0

    try:
        ram_type = specs_html.select_one("div.b-attrs:nth-child(4) > div:nth-child(2) > span:nth-child(2)").text
        if "ddr" not in ram_type.lower():
            ram_type = "Неизвестна"
    except:
        ram_type = "Неизвестна"

    try:
        drive_configuration_index = specs_info.index("Конфигурация")
        interfaces_and_communications_index = specs_info.index("Интерфейсы")

        storage_specs = specs_info[drive_configuration_index + 2:interfaces_and_communications_index]
    except:
        storage_specs = tuple()

    summary_storage = []
    for index, data in enumerate(storage_specs):
        if data == "Гб":
            summary_storage.append(float(storage_specs[index - 1]))
        elif data == "Тб":
            summary_storage.append(float(storage_specs[index - 1]) * 1024)

    model_and_manufacturer = specs_html.select_one("#content > div.b-content > div > div.content__header > h1").text
    model_and_manufacturer_split = model_and_manufacturer.split()

    if model_and_manufacturer_split[0] == "Ноутбук":
        manufacturer = model_and_manufacturer_split[1]
        model = " ".join(model_and_manufacturer_split[2:])
    else:
        manufacturer = model_and_manufacturer_split[2]
        model = " ".join(model_and_manufacturer_split[3:])

    price = specs_html.select_one("span.g-item-data.j-item-data").text.replace(" ", "").replace(",", ".")

    if price.replace(".", "").isdigit():
        price = float(price)

    return {""
            "diagonal": diagonal,
            "summary_ram": ram_amount,
            "ram_type": ram_type,
            "storage": sum(summary_storage),
            "model": model,
            "price": price,
            "url": url,
            "manufacturer": manufacturer,
            }


def parse(save=True, start_page=1):
    with open("parsed_notebooks.txt", "a+", encoding="UTF-8") as fl:
        page = start_page
        end = False
        while not end:
            page_response = get_page(page)
            notebooks = select_notebooks(page_response.content)

            if check_for_redirects(page_response) or notebooks is None:
                break

            requests = (gget(notebook.select_one("a").attrs.get("href")) for notebook in notebooks)
            responses = gmap(requests)
            # print(responses)

            for response in responses:
                data = get_notebook_specs(response, response.url)

                price = data.get("price")

                if price in ("нетнаскладе", "толькоуценка"):
                    end = True
                    break

                if save:
                    fl.write(dumps(data, ensure_ascii=False) + "\n")

                model = data.get('model')
                manufacturer = data.get("manufacturer")
                model = model[:51] + "..." if len(model) > 50 else model
                print(f"{f'{page} стр.':<5} {manufacturer:<15} {model:<60} {f'{price}р':<15} {data.get('url')}")
                # print(data)

            page += 1


# TODO: rewrite this ...
def are_filters_true(notebook, filters):
    print(filters)
    print(notebook)
    if (not (filters.get("from_price") <= notebook.get("price") < filters.get("to_price"))
            and filters.get("to_price") != -1.0):
        return False
    elif (not (filters.get("manufacturer").lower() == notebook.get("manufacturer").lower().strip())
          and filters.get("manufacturer").strip() != "-1"):
        return False
    elif not (filters.get("diagonal") <= notebook.get("diagonal")) and filters.get("diagonal") != -1.0:
        return False
    elif not (filters.get("summary_ram") <= notebook.get("summary_ram")) and filters.get("summary_ram") != -1.0:
        return False
    if not (filters.get("summary_storage") <= notebook.get("storage")) and filters.get("summary_storage") != -1.0:
        return False
    if (not (filters.get("ram_type").strip().lower() == notebook.get("ram_type").lower())
            and filters.get("ram_type").strip() != "-1"):
        return False

    return True


def search_by_filters(notebooks, filters):
    filtered_notebooks = []
    for notebook in notebooks:
        if are_filters_true(notebook, filters):
            filtered_notebooks.append(notebook)

    return filtered_notebooks


def main(ask_parse=True):
    if ask_parse and input("Хотите ли заново стырить информацию с сайта? Д/н или Y/n > ").lower() in ("y", "д"):
        with open("parsed_notebooks.txt", "w+", encoding="UTF-8") as fl:
            fl.write("")

        parse(start_page=1)
        main(ask_parse=False)
    else:
        with open("parsed_notebooks.txt", "r", encoding="UTF-8") as fl:
            # Т.к. файл не слишком большой будем использовать fl.read()
            data = fl.read().splitlines()

        data = [loads(notebook_data) for notebook_data in data]

        show_all_of_filter = input("Введите Д, если хотите посмотреть все ноутбуки, иначе мы запросим фильтры > ")
        if show_all_of_filter.lower().strip() == "д":
            print("Вывожу все ноутбуки")

            for notebook_data in data:
                price = notebook_data.get("price")
                model = notebook_data.get("model")
                model = model[:51] + "..." if len(model) > 50 else model
                manufacturer = notebook_data.get("manufacturer")
                print(f"{manufacturer:<15} {model:<60} {f'{price}р':<15} {notebook_data.get('url')}")
        else:
            print("Вводите -1, если хотите пропустить фильтр")

            filters = {
                "manufacturer": input("Введите производителя ноутбуков > ").lower().strip(),
                "from_price": float(input("Введите от какой цены выводить ноутбуки > ")),
                "to_price": float(input("Введите до какой цены выводить ноутбуки > ")),
                "summary_ram": float(input("Введите минимиальный суммарный объём оперативной памяти > ")),
                "summary_storage": float(input("Введите минимальный суммарный объём дисков > ")),
                "diagonal": float(input("Введите минимальную диагональ экрана > ")),
                "ram_type": input("Введите тип оперативной памяти > ").lower().strip()
            }

            print(f"Марка: {filters.get('manufacturer')}, Цена от: {filters.get('from_price')} до: "
                  f"{filters.get('to_price')}, Диагональ от: {filters.get('diagonal')}, Суммарный объём оперативной "
                  f"памяти от {filters.get('summary_ram')} Гб, Суммарный объём дисков от "
                  f"{filters.get('summary_storage')} Гб, Тип памяти: {filters.get('ram_type')}")

            filtered_notebooks = search_by_filters(data, filters)

            for notebook in filtered_notebooks:
                model = notebook.get("model")
                diagonal = f"{notebook.get('diagonal')}\""

                model = model[:51] + "..." if len(model) > 50 else model
                manufacturer = notebook.get("manufacturer")

                print(f"{manufacturer:<15} {model:<60} {diagonal:<7} {str(notebook.get('price')) + 'р':<10} "
                      f"{str(notebook.get('summary_ram')) + ' Гб ОП.П.':<15}"
                      f" {notebook.get('ram_type'):<15} {str(notebook.get('storage')) + ' Гб памяти!':<30} {notebook.get('url')}")

        main(ask_parse=False)


if __name__ == "__main__":
    main()
