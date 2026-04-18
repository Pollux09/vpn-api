Нужно подготовить:

- Сервер с Ubuntu 22.04 или 24.04
- Доступ по SSH к серверу
- Уже работающую панель Remnawave
- `BASE_URL` панели Remnawave, например `https://panel.example.com`
- `API_TOKEN` от Remnawave
- `APP_TOKEN`, ключ приложения для доступа к этому API
- `API_KEY` только если Remnawave у вас закрыта дополнительной защитой

В папке app/.env.example есть пример.

В папке `app` нужно создать файл `.env`, заполнить его по образцу `.env.example` и подставить реальные значения.

## Что нужно установить на сервер

На сервере достаточно установить:

- `git`
- Docker Engine
- Docker Compose Plugin


## Команды для запуска на сервере

Подключиться к серверу:

```bash
ssh root@YOUR_SERVER_IP
```

Установить `git` и Docker:

```bash
sudo apt update
sudo apt install -y ca-certificates curl git
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
docker --version
docker compose version
```

Скачать проект:

```bash
cd /opt
git clone https://github.com/Pollux09/vpn-api.git vpn-api
cd /opt/vpn-api
```

Создать `.env`:

```bash
cp app/.env.example app/.env
nano app/.env
```

Заполнить `app/.env` так же, как `app/.env.example`, но с реальными значениями:

```env
BASE_URL=https://panel.example.com
CREATE_USER_PATH=/api/users
INTERNAL_SQUADS_PATH=/api/internal-squads
API_TOKEN=your_remnawave_api_token
API_KEY=
APP_TOKEN=your_app_token
```


Запустить проект:

```bash
cd /opt/vpn-api
docker compose up -d --build
```

Проверить, что контейнер поднялся:

```bash
docker compose ps
docker compose logs -f
```

## Как проверить работу API

Проверка с самого сервера:

```bash
curl -X POST "http://127.0.0.1:6767/create-user" \
  -H "Content-Type: application/json" \
  -H "App-token: your_long_random_secret_token" \
  -d '{
    "username": "test_user_01",
    "days": 30
  }'
```

Если все настроено правильно, вы получите ответ примерно такого вида:

```json
{
  "subscription_url": "https://..."
}
```

## Если получили 502 Bad Gateway

Минимальный запрос ниже нужно отправлять в это приложение, то есть на
`/create-user`:

```json
{
  "username": "user_001",
  "days": 30
}
```

Напрямую в Remnawave `/api/users` поле `days` отправлять нельзя.
Приложение само преобразует `days` в обязательное для Remnawave поле
`expireAt`.

Если 502 возвращает это приложение, в ответе будет JSON с `detail.status_code`,
`detail.url` и `detail.body`. Если тела ответа нет вообще, 502, скорее всего,
возвращает внешний reverse proxy перед приложением или контейнер с приложением
не доступен.

## Какие поля можно передавать в запросе

Минимальный рабочий запрос:

```json
{
  "username": "user_001",
  "days": 30
}
```

Расширенный вариант:

```json
{
  "username": "user_001",
  "days": 30,
  "status": "ACTIVE",
  "traffic_limit_bytes": 53687091200,
  "traffic_limit_strategy": "MONTH",
  "hardware_id_device_limit": 3
}
```

Пояснение:

- `username` - логин пользователя
- `days` - на сколько дней выдать доступ
- `status` - статус пользователя
- `traffic_limit_bytes` - лимит трафика в байтах
- `traffic_limit_strategy` - стратегия сброса лимита
- `hardware_id_device_limit` - лимит устройств по HWID для конкретного пользователя

Допустимые значения `traffic_limit_strategy`:

- `NO_RESET`
- `DAY`
- `WEEK`
- `MONTH`

Поле `hardware_id_device_limit` необязательное. Если его не передавать,
приложение не будет отправлять `hwidDeviceLimit` в Remnawave, и панель сможет
использовать свой fallback-лимит по умолчанию.


## Как открыть порт на Ubuntu

Если на сервере включен UFW, откройте порт:

```bash
sudo ufw allow 6767/tcp
sudo ufw reload
```

Проверить статус:

```bash
sudo ufw status
```
