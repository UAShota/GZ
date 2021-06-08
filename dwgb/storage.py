from classes import bot_engine
from classes import bot_consts

tmpEngine = bot_engine('.', '', 111111111, {
                            
    2000000005: [bot_consts.COMMAND_GETBAF, bot_consts.COMMAND_BALANCE, bot_consts.COMMAND_STORAGE, bot_consts.COMMAND_TRANSFERGOLD, bot_consts.COMMAND_TRANSFERITEM, bot_consts.COMMAND_GETITEM, bot_consts.COMMAND_SAVEPROFILE, bot_consts.COMMAND_CONVERT]
#     2000000001: [bot_consts.COMMAND_SAVEPROFILE, bot_consts.COMMAND_CONVERT]
})
tmpEngine.listen()