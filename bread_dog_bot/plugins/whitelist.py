from nonebot import on_command, logger
from nonebot.adapters.onebot.v11 import Bot, Event, MessageSegment, Message
from nonebot.permission import SUPERUSER
import models.server
import utils.server
import utils.admin
import utils.whitelist
import config

add_whitelist = on_command("添加白名单")


@add_whitelist.handle()
async def add_whitelist_handle(bot: Bot, event: Event):
    logger.info(f"「{event.get_user_id()}」执行了 「添加白名单」")
    text = event.get_plaintext().split(" ")
    if len(text) == 2:
        if config.Whitelist.method == "normal":  # 普通模式
            player_name = text[1]
            if not player_name.isalnum():
                await add_whitelist.finish("添加失败！\n不合法的名称\n名称只能包含中文字母数字")
            result, server_info_list = utils.server.GetInfo.all()
            msg = []
            if result:
                if server_info_list:
                    for i in server_info_list:
                        conn = models.server.Connect(i[2], i[3], i[4])
                        result, reason = conn.add_whitelist(event.get_user_id(), player_name)
                        if result:
                            msg.append(f"๑{i[0]}๑{MessageSegment.face(190)}{i[1]}\n"
                                       f"添加成功！")
                        else:
                            msg.append(f"๑{i[0]}๑{MessageSegment.face(190)}{i[1]}\n"
                                       f"添加失败！\n"
                                       f"{reason}")
                    await add_whitelist.finish(Message("\n".join(msg)))
                else:
                    await add_whitelist.finish(Message("添加失败！\n没有添加服务器！"))
            else:
                await add_whitelist.finish(Message("添加失败！\n无法连接至数据库"))
        elif config.Whitelist.method == "cluster":  # 集群模式
            main_server_id = config.Whitelist.main_server
            player_name = text[1]
            result, server_info = utils.server.GetInfo.by_id(main_server_id)
            if result:
                conn = models.server.Connect(server_info[2], server_info[3], server_info[4])
                result, reason = conn.add_whitelist(event.get_user_id(), player_name)
                if result:
                    await add_whitelist.finish("添加成功！")
                else:
                    await add_whitelist.finish("添加失败！\n" + reason)
            else:
                await add_whitelist.finish(Message("添加失败！\n无法连接至数据库"))
        else:
            await add_whitelist.finish(Message("添加失败！\n未知的模式\n请在config.py中重新配置"))
    else:
        await add_whitelist.finish("添加失败！\n用法错误！\n请输入【帮助 添加白名单】获取该功能更多信息")


bind_whitelist = on_command("绑定白名单")


@bind_whitelist.handle()
async def bind_whitelist_handle(bot: Bot, event: Event):
    logger.info(f"「{event.get_user_id()}」执行了 「添加白名单」")
    text = event.get_plaintext().split(" ")
    if len(text) == 2:
        player_name = text[1]
        if not player_name.isalnum():
            await add_whitelist.finish("添加失败！\n不合法的名称\n名称只能包含中文字母数字")
        result, reason = utils.whitelist.GetInfo.by_qq(event.get_user_id())
        if result:
            await bind_whitelist.finish("添加失败！\n你已经添加过白名单了")
        else:
            if reason == "不存在此玩家":
                result, reason = utils.whitelist.add_to_db(event.get_user_id(), player_name)
                if result:
                    await bind_whitelist.finish("添加成功！")
                else:
                    await bind_whitelist.finish(f"添加失败！\n{reason}")
            else:
                await bind_whitelist.finish(f"添加失败！\n无法连接到数据库\n{reason}")
    else:
        await bind_whitelist.finish("添加失败！\n用法错误！\n请输入【帮助 绑定白名单】获取该功能更多信息")


rebind_whitelist = on_command("改绑白名单")


@rebind_whitelist.handle()
async def rebind_whitelist_handle(bot: Bot, event: Event):
    logger.info(f"「{event.get_user_id()}」执行了 「改绑白名单」")
    text = event.get_plaintext().split(" ")
    if len(text) == 2:
        player_name = text[1]
        if not player_name.isalnum():
            await add_whitelist.finish("改绑失败！\n不合法的名称\n名称只能包含中文字母数字")
        result, reason = utils.whitelist.rebind_db(event.get_user_id(), player_name)
        if result:
            await bind_whitelist.finish("改绑成功")
        else:
            if reason == "不存在此玩家":
                await bind_whitelist.finish(f"改绑失败！\n你还没有添加白名单")
            else:
                await bind_whitelist.finish(f"改绑失败！\n无法连接到数据库\n{reason}")
    else:
        await bind_whitelist.finish("改绑失败！\n用法错误！\n请输入【帮助 改绑白名单】获取该功能更多信息")


delete_whitelist = on_command("删除白名单")


@delete_whitelist.handle()
async def delete_whitelist_handle(bot: Bot, event: Event):
    logger.info(f"「{event.get_user_id()}」执行了 「删除白名单」")
    admin_list = utils.admin.get()
    if event.get_user_id() in admin_list:
        text = event.get_plaintext().split(" ")
        if len(text) == 2:
            if config.Whitelist.method == "normal":  # 普通模式
                qq = text[1]
                result, server_info_list = utils.server.GetInfo.all()
                msg = []
                if result:
                    if server_info_list:
                        for i in server_info_list:
                            conn = models.server.Connect(i[2], i[3], i[4])
                            result, reason = conn.delete_whitelist(qq)
                            if result:
                                msg.append(f"๑{i[0]}๑{MessageSegment.face(190)}{i[1]}\n"
                                           f"删除成功！")
                            else:
                                msg.append(f"๑{i[0]}๑{MessageSegment.face(190)}{i[1]}\n"
                                           f"删除失败！\n"
                                           f"{reason}")
                        await delete_whitelist.finish(Message("\n".join(msg)))
                    else:
                        await delete_whitelist.finish(Message("删除失败！\n没有可用的服务器！"))
                else:
                    await delete_whitelist.finish(Message("删除失败！\n无法连接至数据库"))
            elif config.Whitelist.method == "cluster":  # 集群模式
                main_server_id = config.Whitelist.main_server
                qq = text[1]
                result, server_info = utils.server.GetInfo.by_id(main_server_id)
                if result:
                    conn = models.server.Connect(server_info[2], server_info[3], server_info[4])
                    result, reason = conn.delete_whitelist(qq)
                    if result:
                        await delete_whitelist.finish("删除成功！")
                    else:
                        await delete_whitelist.finish("删除失败！\n" + reason)
                else:
                    await delete_whitelist.finish(Message("删除失败！\n无法连接至数据库"))
            else:
                await delete_whitelist.finish(Message("删除失败！\n未知的模式\n请在config.py中重新配置"))
        else:
            await delete_whitelist.finish("删除失败！\n用法错误！\n请输入【帮助 删除白名单】获取该功能更多信息")

    else:
        await delete_whitelist.finish("删除失败！\n权限不足！\n请输入【帮助 删除白名单】获取该功能更多信息")


self_delete = on_command("自删白名单")


@self_delete.handle()
async def self_delete_handle(bot: Bot, event: Event):
    logger.info(f"「{event.get_user_id()}」执行了 「自删白名单」")
    if config.Whitelist.method == "normal":  # 普通模式
        qq = event.get_user_id()
        result, server_info_list = utils.server.GetInfo.all()
        msg = []
        if result:
            if server_info_list:
                for i in server_info_list:
                    conn = models.server.Connect(i[2], i[3], i[4])
                    result, reason = conn.delete_whitelist(qq)
                    if result:
                        msg.append(f"๑{i[0]}๑{MessageSegment.face(190)}{i[1]}\n"
                                   f"删除成功！")
                    else:
                        msg.append(f"๑{i[0]}๑{MessageSegment.face(190)}{i[1]}\n"
                                   f"删除失败！\n"
                                   f"{reason}")
                await self_delete.finish(Message("\n".join(msg)))
            else:
                await self_delete.finish(Message("删除失败！\n没有可用的服务器！"))
        else:
            await self_delete.finish(Message("删除失败！\n无法连接至数据库"))
    elif config.Whitelist.method == "cluster":  # 集群模式
        main_server_id = config.Whitelist.main_server
        qq = event.get_user_id()
        result, server_info = utils.server.GetInfo.by_id(main_server_id)
        if result:
            conn = models.server.Connect(server_info[2], server_info[3], server_info[4])
            result, reason = conn.delete_whitelist(qq)
            if result:
                await delete_whitelist.finish("删除成功！")
            else:
                await delete_whitelist.finish("删除失败！\n" + reason)
        else:
            await self_delete.finish(Message("删除失败！\n无法连接至数据库"))
    else:
        await self_delete.finish(Message("删除失败！\n未知的模式\n请在config.py中重新配置"))


reset = on_command("重置白名单", permission=SUPERUSER)


@reset.handle()
async def reset_handle(bot: Bot, event: Event):
    logger.info(f"「{event.get_user_id()}」执行了 「重置白名单」")
    result, reason = utils.whitelist.reset()
    if result:
        await reset.finish("重置成功！\n已重置数据库中的白名单")
    else:
        await reset.finish("重置失败！\n" + reason)
