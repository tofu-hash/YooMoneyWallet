from handlers.callback_query import *
from handlers.messages import *
from handlers.init import *

dp.register_message_handler(wallet_cmd_handler, commands=['wallet'], state='*')
dp.register_message_handler(start_cmd_handler, commands=['start'], state='*')
dp.register_message_handler(replenish_handler, state=Replenish.set_amount_state)

dp.register_callback_query_handler(check_payment_handler,
                                   lambda msg: 'check_payment' in msg.data,
                                   state='*')
dp.register_callback_query_handler(replenish_cmd_handler,
                                   lambda msg: msg.data == 'replenish',
                                   state='*')


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            BotCommand('start', 'Перезапуск бота'),
            BotCommand('wallet', 'Кошелёк')
        ]
    )


async def start(dispatcher) -> None:
    bot_name = dict(await dispatcher.bot.get_me()).get('username')
    await set_default_commands(dispatcher)
    print(f'#    start on @{bot_name}')


async def end(dispatcher) -> None:
    bot_name = dict(await dispatcher.bot.get_me()).get('username')
    print(f'#    end on @{bot_name}')


if __name__ == '__main__':
    executor.start_polling(dispatcher=dp,
                           on_startup=start,
                           on_shutdown=end)
