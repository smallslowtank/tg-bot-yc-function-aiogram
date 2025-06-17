//
// Подтянуть переменные из файла
//
variable "token" { type = string }
variable "cloud_id" { type = string }
variable "folder_id" { type = string }
variable "zone" { type = string }
variable "bot_token" { type = string }

//
// Настройка провайдера
//
terraform {
  required_providers {
    yandex = {
      source = "yandex-cloud/yandex"
    }
  }
}
provider "yandex" {
  token     = var.token
  cloud_id  = var.cloud_id
  folder_id = var.folder_id
  zone      = var.zone
}

//
// Создать сервисный аккаунт "sa-editor"
//
resource "yandex_iam_service_account" "sa-editor" {
  name      = "sa-editor"
  folder_id = var.folder_id
  description = "сервисный аккаунт для телеграм-бота"
}

//
// Выдать сервисному аккаунту "sa-editor" роль editor на каталог
//
resource "yandex_resourcemanager_folder_iam_binding" "sa-editor" {
  for_each = toset([
    "editor",
  ])
  role      = each.value
  folder_id = var.folder_id
  members = [
    "serviceAccount:${yandex_iam_service_account.sa-editor.id}",
  ]
  sleep_after = 5
}

//
// Создать статический ключ для сервисного аккаунта "sa-editor" (для работы с очередью)
//
resource "yandex_iam_service_account_static_access_key" "sa-editor-static-key" {
  service_account_id = yandex_iam_service_account.sa-editor.id
  description        = "static access key"
}

//
// Создать бакет в объектном хранилище (Object Storage)
//
resource "yandex_storage_bucket" "tg-bot-bucket" {
  bucket                = "tg-bot-bucket-${var.folder_id}"
  folder_id             = var.folder_id
  max_size              = 1073741824
  default_storage_class = "STANDARD"

  anonymous_access_flags {
    read        = true
    list        = false
    config_read = false
  }
}

//
// Загрузить в хранилище файл IMG.jpg для баннера
//
resource "yandex_storage_object" "tg-bot-banner" {
  bucket = "tg-bot-bucket-${var.folder_id}"
  key    = "IMG.jpg"
  source = "IMG.jpg"
}

//
// Создать лог-группу "default"
//
resource "yandex_logging_group" "default" {
  name      = "default"
  folder_id = var.folder_id
}

//
// Создать базу данных
//
resource "yandex_ydb_database_serverless" "tg-bot-ydb" {
  name                = "tg-bot-ydb"
  folder_id           = var.folder_id
  location_id         = "ru-central1"
  deletion_protection = false
  description = "база данных для телеграм-бота"
  sleep_after = 30
}

//
// Создать таблицу Quotes
//
resource "yandex_ydb_table" "Quotes" {
  path              = "Quotes"
  connection_string = yandex_ydb_database_serverless.tg-bot-ydb.ydb_full_endpoint

  column {
    name     = "quote_id"
    type     = "Int64"
    not_null = true
  }
  column {
    name     = "quote"
    type     = "Utf8"
    not_null = true
  }
  column {
    name     = "author"
    type     = "Utf8"
    not_null = true
  }

  primary_key = ["quote_id"]

}


//
// Создать таблицу Users
//
resource "yandex_ydb_table" "Users" {
  path              = "Users"
  connection_string = yandex_ydb_database_serverless.tg-bot-ydb.ydb_full_endpoint

  column {
    name     = "quote_id"
    type     = "Int64"
    not_null = true
  }
  column {
    name     = "user_id"
    type     = "Int64"
    not_null = true
  }

  primary_key = ["user_id"]

}

//
// Создать очередь
//
resource "yandex_message_queue" "tg-bot-message-queue" {
  name                      = "tg-bot-message-queue"
  message_retention_seconds = 3600
  access_key                = yandex_iam_service_account_static_access_key.sa-editor-static-key.access_key
  secret_key                = yandex_iam_service_account_static_access_key.sa-editor-static-key.secret_key
}

//
// Создать шлюз
//
resource "yandex_api_gateway" "tg-bot-api-gateway" {
  name        = "tg-bot-api-gateway"
  description = "шлюз для телеграм-бота"
  spec        = <<-EOT
openapi: 3.0.0
info:
  title: Sample API
  version: 1.0.0
paths:
  /tg-bot:
    post:
      x-yc-apigateway-integration:
        queue_url: ${yandex_message_queue.tg-bot-message-queue.id}
        action: SendMessage
        type: cloud_ymq
        payload_format_type: body
        folder_id: ${var.folder_id}
        service_account_id: ${yandex_iam_service_account.sa-editor.id}
EOT
}

//
// Создать функцию
//
resource "yandex_function" "tg-bot-function" {
  name               = "tg-bot-function"
  user_hash          = "v1"
  runtime            = "python312"
  entrypoint         = "index.handler"
  memory             = "128"
  execution_timeout  = "10"
  service_account_id = yandex_iam_service_account.sa-editor.id
  description        = "телеграм-бот"
  content {
    zip_filename = "tg-bot.zip"
  }
  environment = {
    "BOT_TOKEN" = var.bot_token
    "URL_IMG"   = "https://storage.yandexcloud.net/tg-bot-bucket-${var.folder_id}/${yandex_storage_object.tg-bot-banner.source}"
    "YDB_CS"    = "${yandex_ydb_database_serverless.tg-bot-ydb.ydb_full_endpoint}"
  }
}

//
// Создать триггер
//
resource "yandex_function_trigger" "tg-bot-trigger" {
  name        = "tg-bot-trigger"
  description = "триггер для телеграм-бота"
  folder_id   = var.folder_id
  message_queue {
    service_account_id = yandex_iam_service_account.sa-editor.id
    queue_id           = yandex_message_queue.tg-bot-message-queue.arn
    batch_cutoff       = 0
    batch_size         = 1
  }
  function {
    id                 = yandex_function.tg-bot-function.id
    tag                = "$latest"
    service_account_id = yandex_iam_service_account.sa-editor.id
  }
}
