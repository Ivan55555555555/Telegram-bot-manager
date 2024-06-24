from .dispatcher_bot import dispatcher
from aiogram.types import CallbackQuery
from .keyboards_bot import user_inline_keyboard
import sqlite3 
from .buttons_bot import button_delete_user


@dispatcher.callback_query()
async def callback_handler(callback: CallbackQuery):
    # 
    data_base = sqlite3.connect(database= 'instance/data.db')
    cursor = data_base.cursor()
    # 
    if callback.data == "user":
        cursor.execute("SELECT * FROM user")
        list_users = cursor.fetchall()
        for user in list_users:
            button_delete_user.callback_data= f"delete_user_{user[0]}"
            await callback.message.answer(
                text= f"ID: {user[0]} \nName: {user[1]} \nPassword: {user[2]} \nIs_admin: {user[3]}",
                reply_markup= user_inline_keyboard
            )
    #
    elif "delete_user" in callback.data:
        id_user = int(callback.data.split("_")[-1]) # id_user = ['delete', 'user', '1'] => id_user = 1
        cursor.execute("DELETE FROM user WHERE id = ?", (id_user,)) 
        await callback.message.delete()

    #
    data_base.commit()
    data_base.close()
