# Парсер официального сайта PEP (Python Enhancement Proposals) и
# официального сайта с документацией для Python 3

https://peps.python.org/
https://docs.python.org/3/

### Парсер позволяет

- собирать данные о документах PEP: проверять статусы PEP, считать количество документов в каждом статусе, а также общее количество PEP,
- собирать ссылки на статьи о нововведениях в Python, переходить по ним и забирать информацию об авторах и редакторах статей,
- собирать информацию о статусах версий Python,
- скачивать архив с актуальной документацией.

### Работа с парсером
Работа с парсером осуществляется через командную строку.

Находясь в директории src/ вы можете с помощью команды ```python main.py --help``` ознакомиться с возможностями парсера:

```
usage: main.py [-h] [-c] [-o {pretty,file}]
               {whats-new,latest-versions,download,pep}

Парсер документации Python

positional arguments:
  {whats-new,latest-versions,download,pep}
                        Режимы работы парсера

optional arguments:
  -h, --help            show this help message and exit
  -c, --clear-cache     Очистка кеша
  -o {pretty,file}, --output {pretty,file}
                        Дополнительные способы вывода данных
```

### Примеры команд
Выгрузка файла с нововведениями в последней версии Python (с предварительной очисткой кэша):
```python main.py whats-new -c --output file```

Вывод в терминал таблицы со статусами версий Python:
```python main.py latest-versions -o pretty```

Выгрузка архива с актуальной документацией Python:
```python main.py download```

Стандартный вывод в терминал таблицы с количеством PEP в каждом статусе:
```python main.py pep```

### Логирование
Проект оснащён логированием. Запись логов производится в файл, а также параллельно осуществляется их вывод в терминал.

### Авторство
Парсинг официального сайта с документацией для Python 3 реализован с большой помощью _Яндекс.Практикума_.
Парсинг сайта PEP описан мной.