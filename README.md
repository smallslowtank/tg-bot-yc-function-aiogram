### Отличия от версии в ветке master

1. Добавлена таблица Users для хранения в ней идентификатора последней цитаты.
2. Реализована логика для исключения повторения подряд одной и той же цитаты.
3. Цитаты в таблицу загружаются автоматически, если их там нет.
4. Добавлены файлы для развёртывание бота через Terraform.

### Развёртывание бота через Terraform

Копировать файл с настройками .terraformrc в домашнюю папку.

Редактировать файл terraform.tfvars

OAuth-токен в сервисе Яндекс ID, для получения нужно перейти по ссылке и от туда его скопировать.
Ссылка https://oauth.yandex.ru/authorize?response_type=token&client_id=1a6990aa636648e9b2ef855fa7bec2fb

Команды для создания ресурсов:
```
terraform apply \
    -target=yandex_iam_service_account.sa-editor \
    -target=yandex_resourcemanager_folder_iam_binding.sa-editor \
    -target=yandex_iam_service_account_static_access_key.sa-editor-static-key
```
```
terraform apply \
    -target=yandex_storage_bucket.tg-bot-bucket \
    -target=yandex_ydb_database_serverless.tg-bot-ydb
```
```
terraform apply \
    -target=yandex_ydb_table.Quotes \
    -target=yandex_ydb_table.Users \
    -target=yandex_storage_object.tg-bot-banner
```
```
terraform apply
```
### Подключить webhook:
```
curl \
  --request POST \
  --url https://api.telegram.org/bot<токен_бота>/setWebhook \
  --header 'content-type: application/json' \
  --data '{"url": "<домен_API-шлюза>/tg-bot"}'
```
### Удаление сервисов через Terraform
```
terraform destroy \
    -target=yandex_storage_object.tg-bot-banner \
    -target=yandex_message_queue.tg-bot-message-queue \
    -target=yandex_ydb_table.Quotes \
    -target=yandex_ydb_table.Users
```
```
terraform destroy
```