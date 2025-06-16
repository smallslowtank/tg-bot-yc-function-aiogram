-- создать в базе таблицу Quotes
CREATE TABLE `Quotes`
(
    `quote_id` Int64,
    `quote` Utf8,
    `author` Utf8,
    PRIMARY KEY (`quote_id`)
);
-- наполнить таблицу Quotes данными
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
-- создать в базе таблицу Users
CREATE TABLE `Users`
(
    `quote_id` Int64,
    `user_id` Int64,
    PRIMARY KEY (`user_id`)
);