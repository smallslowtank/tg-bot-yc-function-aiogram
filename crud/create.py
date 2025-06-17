import os
import ydb.aio
import ydb.iam


async def add_user(user_id, quote_id):
    """
    Добавить пользователя в таблицу Users
    """

    async def callee(pool: ydb.aio.QuerySessionPool, user_id, quote_id):
        await pool.execute_with_retries(
            """
            DECLARE $parameter1 AS Int64;
            DECLARE $parameter2 AS Int64;

            INSERT INTO Users (user_id, quote_id)
            VALUES ($parameter1, $parameter2);
            """,
            {
                "$parameter1": user_id,
                "$parameter2": quote_id,
            },
        )

        return

    async with ydb.aio.Driver(
            connection_string=os.getenv('YDB_CS'),
            credentials=ydb.iam.MetadataUrlCredentials(),
    ) as driver:
        await driver.wait(timeout=5, fail_fast=True)

        async with ydb.aio.QuerySessionPool(driver) as pool:
            await callee(pool, user_id, quote_id)

        return
