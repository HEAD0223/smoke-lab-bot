from aiogram import Dispatcher


def register_all_filters(dp: Dispatcher):
    filters = ()
    for filter in filters:
        dp.bind_filter(filter)
    pass
