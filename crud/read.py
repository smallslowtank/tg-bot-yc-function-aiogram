import os
import ydb.aio
import ydb.iam
from random import randint


async def random_quote():
    """
    Случайная цитата и автор
    """

    async def callee(pool: ydb.aio.QuerySessionPool, quote_id):
        result = await pool.execute_with_retries(
            """
            DECLARE $parameter1 AS Int64;

            SELECT quote_id, author, quote
            FROM Quotes
            WHERE quote_id=$parameter1;
            """,
            {
                "$parameter1": quote_id
            },
        )

        return result

    async with ydb.aio.Driver(
            connection_string=os.getenv('YDB_CS'),
            credentials=ydb.iam.MetadataUrlCredentials(),
    ) as driver:
        await driver.wait(timeout=5, fail_fast=True)

        async with ydb.aio.QuerySessionPool(driver) as pool:
            r = randint(1, 10)
            result = await callee(pool, r)

        data = result[0].rows[0]
        quote_id = data.quote_id
        quote = data.quote
        author = data.author
        return quote_id, quote, author


async def last_quote(user_id):
    """
    Получить идентификатор последней цитаты для пользователя
    """

    async def callee(pool: ydb.aio.QuerySessionPool, user_id):
        result = await pool.execute_with_retries(
            """
            DECLARE $parameter1 AS Int64;

            SELECT quote_id FROM Users
            WHERE user_id = $parameter1;
            """,
            {
                "$parameter1": user_id
            },
        )

        return result

    async with ydb.aio.Driver(
            connection_string=os.getenv('YDB_CS'),
            credentials=ydb.iam.MetadataUrlCredentials(),
    ) as driver:
        await driver.wait(timeout=5, fail_fast=True)

        async with ydb.aio.QuerySessionPool(driver) as pool:
            result = await callee(pool, user_id)

        # Если нет пользователя в базе, то идентификатор 0
        if not result[0].rows:
            data = 0
        else:
            data = result[0].rows[0].quote_id

        return data
