# 🖥️ Simple OPC-UA GUI Client

[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/FreeOpcUa/opcua-client-gui/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/FreeOpcUa/opcua-client-gui/?branch=master)
[![Build Status (Client GUI)](https://travis-ci.org/FreeOpcUa/opcua-client-gui.svg?branch=master)](https://travis-ci.org/FreeOpcUa/opcua-client-gui)
[![Build Status (Widgets)](https://travis-ci.org/FreeOpcUa/opcua-widgets.svg?branch=master)](https://travis-ci.org/FreeOpcUa/opcua-widgets)

## 📦 Описание

Простой графический OPC-UA клиент, написанный с использованием **FreeOpcUa Python API** и **PyQt5**. Реализует основные функции:

- Подписка на изменения данных и события
- Чтение и запись значений переменных
- Получение атрибутов и ссылок узлов
- Вызов методов

## 🖼️ Скриншоты программы

![Screenshot2](https://github.com/user-attachments/assets/d9b34101-aa3e-4bba-bcad-a0b091718641)
![Screenshot](/screenshot.png?raw=true "Main Window")


## 🔧 Установка

> ⚠️ Требуются зависимости: `opcua`, `pyqt5`, `pyqtgraph`, `cryptography`, `numpy`

### 🐧 Linux

1. Убедитесь, что установлены `python` и `pip`
2. Установите клиент и зависимости:

```bash
   pip3 install opcua pyqt5 pyqtgraph cryptography numpy
```

3. Запуск:

   ```bash
   opcua-client
   ```


### 🪟 Windows

1. Установите [WinPython](https://winpython.github.io/) с поддержкой PyQt5
2. Установите клиент и зависимости:

   ```bash
   pip install opcua pyqt5 pyqtgraph cryptography numpy
   ```
3. Запуск:

   ```
   YOUR_INSTALL_PATH\Python\Python35\Scripts\opcua-client.exe
   ```

---

### 🍏 macOS

1. Убедитесь, что установлены `python`, `pip` и `Homebrew`
2. Установите зависимости:

   ```bash
   brew install pyqt@5
   pip3 install opcua pyqtgraph cryptography numpy
   ```
3. Запуск:

   ```bash
   opcua-client
   ```

---

## 🔄 Обновление

Для обновления всех компонентов:

```bash
pip install --upgrade opcua pyqt5 pyqtgraph cryptography numpy
```



