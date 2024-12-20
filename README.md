# MoreTech2024NFT

Этот проект представляет собой систему для выпуска soulbound NFT на сети Arbitrum, включающую backend на Python и смарт-контракты на Solidity. Он состоит из нескольких компонентов, включая backend для взаимодействия с пользователями и смарт-контрактами, а также интеграцию с блокчейном.

## Структура проекта

```
project_root/
│
├── backend/                    # Backend на Python
│   ├── app.py                  # Основной файл приложения Flask
│   ├── backend_1.py            # Второй backend для взаимодействия с блокчейном
│   ├── requirements.txt        # Зависимости для Python
│   └── uploads/                # Папка для сохранения файлов
│
├── smart_contracts/            # Контракты на Solidity
│   ├── contracts/              # Папка со смарт-контрактами
│   ├── hardhat.config.js       # Конфигурация Hardhat
│   ├── scripts/                # Скрипты для развертывания контрактов
│   ├── package.json            # Зависимости Node.js
│   └── .env                    # Переменные окружения для сети Arbitrum
│
├── frontend/                   # Frontend приложения
│   ├── package.json            # Зависимости Node.js для frontend
│   ├── public/                 # Публичные файлы
│   ├── src/                    # Исходный код фронтенда
│   └── .env                    # Переменные окружения для frontend
│
├── .env                        # Основной файл конфигурации окружения
├── README.md                   # Документация
└── .gitignore                  # Игнорируемые файлы
```

## Установка и настройка

### 1. Клонирование проекта

Сначала клонируйте репозиторий:

```bash
git clone https://github.com/your_username/your_repository.git
```

### 2. Установка зависимостей для Python

Перейдите в папку backend и создайте виртуальное окружение:

```bash
cd backend
python -m venv venv
```

Активируйте виртуальное окружение:

- Для Windows: 
  ```bash
  venv\Scripts\activate
  ```
- Для Linux/macOS:
  ```bash
  source venv/bin/activate
  ```

Установите зависимости:
Возможны ошибки при загрузке библиотек на UNIX-подобные системы. 
Тогда нужно отрыть requirements.txt и удалить незагружающиеся библиотеки
```bash
pip install -r requirements.txt
```

### 3. Установка зависимостей для Node.js

Перейдите в папку со смарт-контрактами и установите зависимости:

```bash
cd ../smart_contracts
npm install
```

Если при установке возникнут ошибки, попробуйте использовать опцию `--legacy-peer-deps`:

```bash
npm install --legacy-peer-deps
```

### 4. Установка зависимостей для Frontend

Перейдите в папку `frontend` и установите зависимости:

```bash
cd ../frontend
npm install
```

Запустите локальный сервер для разработки:

```bash
npm run dev
```

### 5. Настройка переменных окружения

Создайте файл `.env` в корне проекта и добавьте нужные переменные окружения. Пример:

```env
# https://www.infura.io/faucet/sepolia
ARBITRUM_RPC_URL="https://arbitrum-sepolia.infura.io/v3/YOUR_INFURA_PROJECT_ID"
CONTRACT_ADDRESS="0xeDEF0d73424d8623EF8adcB0E5807365e7F560a7"

# https://www.alchemy.com/faucets/arbitrum-sepolia
ADDRESS_KEY_FOR_PAY_COMISSIONS="PRIVATE_KEY_FOR_PAYMENTS"
BACKEND_1_URL="http://localhost:5000"
```

Добавьте `.env` в `.gitignore`, чтобы не загружать конфиденциальные данные в репозиторий.

### 6. Запуск проекта

#### Запуск Backend


Перейдите в папку `backend` и запустите `backend_1`:

```bash
python backend_1.py
```
Также запустите приложение Flask:

```bash
cd backend
python app.py
```

#### Запуск В тестовой сети Arbitrum (опционально)

#### Компиляция и развертывание смарт-контрактов

Перейдите в папку `smart_contracts` и выполните команды:

```bash
npm install --save-dev hardhat @nomiclabs/hardhat-ethers @nomiclabs/hardhat-waffle ethers dotenv

npx hardhat compile
npx hardhat run scripts/deploy.js --network arbitrumSepolia
```

### 7. Использование проекта

После успешного развёртывания backend и смарт-контрактов, вы сможете использовать различные API-эндпоинты для взаимодействия с NFT и загрузки файлов. Backend обеспечивает функции регистрации и аутентификации пользователей, загрузку и получение файлов, а также взаимодействие с блокчейном.

### 8. Основные команды

- **Клонирование проекта**:
  ```bash
  git clone https://github.com/your_username/your_repository.git
  ```
- **Установка зависимостей Python**:
  ```bash
  pip install -r requirements.txt
  ```
- **Установка зависимостей Node.js**:
  ```bash
  npm install --legacy-peer-deps
  ```
- **Запуск Flask Backend**:
  ```bash
  python app.py
  ```
- **Компиляция смарт-контрактов**:
  ```bash
  npx hardhat compile
  ```
- **Запуск Frontend**:
  ```bash
  npm run dev
  ```

## Отладка

- Убедитесь, что все зависимости установлены правильно. Если возникают ошибки при установке, попробуйте использовать флаг `--legacy-peer-deps` для Node.js.
- Используйте `ganache-cli` для тестирования смарт-контрактов на локальной сети.
- Если возникают ошибки при подключении к сети Arbitrum, убедитесь, что URL и ключи в `.env` файле правильные.

## Возможные проблемы

1. **Ошибка компиляции Hardhat**: Проверьте, что все зависимости установлены, и добавьте недостающие с флагом `--save-dev`.
2. **Ошибка с backend**: Убедитесь, что оба backend запущены и что вы используете правильные переменные окружения.

---

Если потребуется больше деталей или дополнительная помощь, дайте знать.
