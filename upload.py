import os
import ydb.aio
import ydb.iam


async def upload_quotes():
    """
    Загрузка данных в таблицу Quotes
    """

    async def callee(pool: ydb.aio.QuerySessionPool):
        await pool.execute_with_retries(
            """
            UPSERT INTO `Quotes` (`quote_id`, `quote`, `author`) VALUES (1, 'Пока любишь — надеешься.', 'Элен Бронтэ');
            UPSERT INTO `Quotes` (`quote_id`, `quote`, `author`) VALUES (2, 'Цезарю многое непозволительно потому, что ему дозволено все.', 'Луций Анней Сенека');
            UPSERT INTO `Quotes` (`quote_id`, `quote`, `author`) VALUES (3, 'Если вы не можете увидеть себя богатым, то никогда не сможете этого добиться.', 'Роберт Кийосаки');
            UPSERT INTO `Quotes` (`quote_id`, `quote`, `author`) VALUES (4, 'Справедливость без мудрости значит много, мудрость без справедливости не значит ничего.', 'Марк Туллий Цицерон');
            UPSERT INTO `Quotes` (`quote_id`, `quote`, `author`) VALUES (5, 'Мир несовершенен, поскольку мы несовершенны.', 'Далай-лама XIV');
            UPSERT INTO `Quotes` (`quote_id`, `quote`, `author`) VALUES (6, 'Если не предъявлять к жизни особых претензий, то всё, что ни получаешь, будет прекрасным даром.', 'Эрих Мария Ремарк');
            UPSERT INTO `Quotes` (`quote_id`, `quote`, `author`) VALUES (7, 'Воистину, на свете есть и травы, не дающие цветов, и цветы, не дающие плодов!', 'Конфуций');
            UPSERT INTO `Quotes` (`quote_id`, `quote`, `author`) VALUES (8, 'Правильная постановка вопроса свидетельствует о некотором знакомстве с делом.', 'Фрэнсис Бэкон');
            UPSERT INTO `Quotes` (`quote_id`, `quote`, `author`) VALUES (9, 'Как много мы знаем и как мало мы понимаем.', 'Альберт Эйнштейн');
            UPSERT INTO `Quotes` (`quote_id`, `quote`, `author`) VALUES (10, 'Никогда не спешите, и вы прибудете вовремя.', 'Шарль Морис де Талейран-Перигор');
            """
        )

    async with ydb.aio.Driver(
            connection_string=os.getenv('YDB_CS'),
            credentials=ydb.iam.MetadataUrlCredentials(),
    ) as driver:
        await driver.wait(timeout=5, fail_fast=True)

        async with ydb.aio.QuerySessionPool(driver) as pool:
            await callee(pool)


async def check_quotes():
    """
    Проверка таблицы Quotes на наличие в ней данных
    """

    async def callee(pool: ydb.aio.QuerySessionPool):
        result = await pool.execute_with_retries(
            """
            SELECT quote_id
            FROM Quotes
            WHERE quote_id=1;
            """
        )

        return result

    async with ydb.aio.Driver(
            connection_string=os.getenv('YDB_CS'),
            credentials=ydb.iam.MetadataUrlCredentials(),
    ) as driver:
        await driver.wait(timeout=5, fail_fast=True)

        async with ydb.aio.QuerySessionPool(driver) as pool:
            result = await callee(pool)

        # Если нет пользователя в базе, то идентификатор 0
        if not result[0].rows:
            data = False
        else:
            data = True

        return data
