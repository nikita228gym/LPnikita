from lib.vkmini import VkApi
from utils import parse, log
from .prefixes import add_prefix, remove_prefix, prefix_list
from .ignore import ignore_add, ignore_list, ignore_remove
from .binds import bind_add, binds_list, bind_remove
from .ping import pings, ping
from .updating import update
from .info import info


commands = {
    '+преф': add_prefix,
    '-преф': remove_prefix,
    'префы': prefix_list,
    '+игнор': ignore_add,
    '-игнор': ignore_remove,
    'игнор': ignore_list,
    'игнорлист': ignore_list,
    'связать': bind_add,
    'отвязать': bind_remove,
    'бинды': binds_list,
    'связки': binds_list,
    'инфо': info,
    'обновить': update
}

commands.update({name: ping for name in pings})


async def passer(*_):
    return "Неизвестная команда"


async def handle(update: list, vk: VkApi):
    command, args, payload = parse(update[5].replace('<br>', '\n'))
    log(f'Обрабатываю локальную команду "{command}"...')
    update[5] = command
    response = await commands.get(command, passer)(args, payload, vk, update)
    if response is not None:
        await vk.msg_op(2, update[3], response, update[1])
