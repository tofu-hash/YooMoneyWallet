from handlers.init import *
from yoomoney import Client


async def replenish_cmd_handler(msg: CallbackQuery, state: FSMContext):
    await Replenish.set_amount_state.set()

    answer = '💸 Укажи сумму для пополнения\n( до `15.000 rub.` ):'
    await msg.message.edit_text(text=answer, parse_mode='markdown')


async def check_payment_handler(msg: CallbackQuery, state: FSMContext):
    label = msg.data.split('check_payment ')[1]

    client = Client(config.YOOMONEY_TOKEN)
    history = client.operation_history(label=label)

    if history.operations:
        await msg.answer()

        answer = ('💸 Платёж зачислен (`+%s rub.`)\n\n'
                  '/wallet - ваш кошелёк') % history.operations[0].amount
        await msg.message.edit_text(text=answer, parse_mode='markdown')
        execute(
            ('UPDATE users SET balance=balance+%s '
             'WHERE user_id=%s') %
            (history.operations[0].amount,
             msg.from_user.id)
        )
    else:
        await msg.answer(text='❗ Вы не оплатили счёт')
    # print("List of operations:")
    # print("Next page starts with: ", history.next_record)
    # for operation in history.operations:
    #     print()
    #     print("Operation:", operation.operation_id)
    #     print("\tStatus     -->", operation.status)
    #     print("\tDatetime   -->", operation.datetime)
    #     print("\tTitle      -->", operation.title)
    #     print("\tPattern id -->", operation.pattern_id)
    #     print("\tDirection  -->", operation.direction)
    #     print("\tAmount     -->", operation.amount)
    #     print("\tLabel      -->", operation.label)
    #     print("\tType       -->", operation.type)
