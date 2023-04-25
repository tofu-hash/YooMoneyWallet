import aiogram.utils.exceptions

from handlers.init import *

from yoomoney import Quickpay, Client


async def delete_last_messages(msg: Message, count: int = 3):
    """Удаляет последние N сообщений до команды."""

    for i in range(0, count):
        try:
            await bot.delete_message(chat_id=msg.from_user.id,
                                     message_id=msg.message_id - i)
        except aiogram.utils.exceptions.MessageToDeleteNotFound:
            pass


async def start_cmd_handler(msg: Message, state: FSMContext):
    await state.finish()

    # Create user
    execute(
        ('INSERT OR IGNORE INTO users '
         '(user_id, created) '
         'VALUES (%s, %s);') %
        (msg.from_user.id, now_unix_time())
    )

    if msg.get_args():
        payment = get_absolute_value(execute(
            ('SELECT paid FROM payments '
             'WHERE id="%s" AND user_id=%s') %
            (msg.get_args(), msg.from_user.id),
            fetchone=True
        ))

        if payment and payment == 1:
            client = Client(config.YOOMONEY_TOKEN)
            history = client.operation_history(label=msg.get_args())

            if history.operations:
                answer = ('💸 Платёж зачислен (`+%s rub.`)\n\n'
                          '/wallet - ваш кошелёк') % history.operations[0].amount
                await msg.answer(text=answer, parse_mode='markdown')
                execute(
                    ('UPDATE users SET balance=balance+%s '
                     'WHERE user_id=%s') %
                    (history.operations[0].amount,
                     msg.from_user.id)
                )
            else:
                await msg.answer(text='❗ Счёт не оплачен')
        else:
            await msg.answer(text='❗ Счёта не существует, или он уже оплачен')
    else:
        balance = execute(
            ('SELECT balance FROM users '
             'WHERE user_id=%s') % msg.from_user.id,
            fetchone=True
        )[0]

        answer = '💸 Баланс: `%s rub.`' % balance
        await msg.answer(text=answer, parse_mode='markdown', reply_markup=wallet_reply_markup)


async def wallet_cmd_handler(msg: Message, state: FSMContext):
    await state.finish()

    balance = execute(
        ('SELECT balance FROM users '
         'WHERE user_id=%s') % msg.from_user.id,
        fetchone=True
    )[0]

    answer = '💸 Баланс: `%s rub.`' % balance
    await msg.answer(text=answer, parse_mode='markdown', reply_markup=wallet_reply_markup)


async def replenish_handler(msg: Message, state: FSMContext):
    if msg.text.isdigit():
        amount = int(msg.text)
        if amount <= 15000:
            label = key()
            execute(
                ('INSERT INTO payments (id, amount, user_id, created) '
                 'VALUES ("%s", %s, %s, %s);') %
                (label, amount, msg.from_user.id, now_unix_time())
            )

            bot_data = await dp.bot.get_me()
            bot_username = bot_data.username

            success_url = 'https://t.me/%s?start=%s' % (bot_username, label)
            targets = "Пополнение баланса"

            pay = Quickpay(
                receiver=config.WALLET,
                quickpay_form='shop',
                targets=targets,
                paymentType="SB",
                sum=amount,
                successURL=success_url,
                label=label
            )

            reply_markup = InlineKeyboardMarkup()
            reply_markup.add(InlineKeyboardButton(text='Оплатить 💸',
                                                  url=pay.redirected_url))
            reply_markup.add(InlineKeyboardButton(text='Проверить оплату 🔒',
                                                  callback_data='check_payment %s' % label))

            await msg.answer(text='💸 Счёт на `%s rub`' % amount, parse_mode='markdown',
                             reply_markup=reply_markup)

            await state.finish()
        else:
            await msg.answer(text='Максимальная сумма - `15.000 rub.`',
                             parse_mode='markdown')
    else:
        await msg.answer(text='Укажите число до `15.000 rub.`',
                         parse_mode='markdown')
