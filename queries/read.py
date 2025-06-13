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
            DECLARE $r AS Int64;

            select author, quote from Quotes where quote_id=$r;
            """,
            {
                "$r": quote_id
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
        quote = data.quote
        author = data.author
        return quote, author
