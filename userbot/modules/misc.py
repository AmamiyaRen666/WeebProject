# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# You can find misc modules, which dont fit in anything xD
""" Userbot module for other small commands. """

import io
import sys
from os import execl
from random import randint
from time import sleep

from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP, bot
from userbot.events import register
from userbot.utils import time_formatter


@register(outgoing=True, pattern=r"^\.random")
async def randomise(items):
    """ For .random command, get a random item from the list of items. """
    itemo = (items.text[8:]).split()
    if len(itemo) < 2:
        return await items.edit(
            "`2 item atau lebih diperlukan! Periksa .help random untuk info lebih lanjut.`"
        )
    index = randint(1, len(itemo) - 1)
    await items.edit(
        "**Kueri : **\n`" + items.text[8:] + "`\n**Keluaran : **\n`" + itemo[index] + "`"
    )


@register(outgoing=True, pattern=r"^\.sleep ([0-9]+)$")
async def sleepybot(time):
    """ For .sleep command, let the userbot snooze for a few second. """
    counter = int(time.pattern_match.group(1))
    await time.edit("`Saya merajuk dan tertidur...`")
    if BOTLOG:
        str_counter = time_formatter(counter)
        await time.client.send_message(
            BOTLOG_CHATID,
            f"You put the bot to sleep for {str_counter}.",
        )
    sleep(counter)
    await time.edit("`Oke, saya sudah bangun sekarang.`")


@register(outgoing=True, pattern=r"^\.shutdown$")
async def killthebot(event):
    """ For .shutdown command, shut the bot down."""
    await event.edit("`Selamat tinggal...`")
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, "#SHUTDOWN \n" "Bot shut down")
    await bot.disconnect()


@register(outgoing=True, pattern=r"^\.restart$")
async def killdabot(event):
    await event.edit("`Saya akan kembali sebentar lagi`")
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, "#RESTART \n" "Bot Restarted")
    await bot.disconnect()
    # Spin a new instance of bot
    execl(sys.executable, sys.executable, *sys.argv)
    # Shut the existing one down
    exit()


@register(outgoing=True, pattern=r"^\.readme$")
async def reedme(e):
    await e.edit(
        "Di sini sesuatu untuk Anda baca:\n"
        "\n[WeebProject's README.md file](https://github.com/BianSepang/WeebProject/blob/master/README.md)"
        "\n[Setup Guide - Basic](https://telegra.ph/How-to-host-a-Telegram-Userbot-11-02)"
        "\n[Setup Guide - Google Drive](https://telegra.ph/How-To-Setup-Google-Drive-04-03)"
        "\n[Setup Guide - LastFM Module](https://telegra.ph/How-to-set-up-LastFM-module-for-Paperplane-userbot-11-02)"
        "\n[Setup Guide - How to get Deezer ARL TOKEN](https://notabug.org/RemixDevs/DeezloaderRemix/wiki/Login+via+userToken)"
        "\n[Special - Note](https://telegra.ph/Special-Note-11-02)"
    )


# Copyright (c) Gegham Zakaryan | 2019
@register(outgoing=True, pattern=r"^\.repeat (.*)")
async def repeat(rep):
    cnt, txt = rep.pattern_match.group(1).split(" ", 1)
    replyCount = int(cnt)
    toBeRepeated = txt

    replyText = toBeRepeated + "\n"

    for i in range(0, replyCount - 1):
        replyText += toBeRepeated + "\n"

    await rep.edit(replyText)


@register(outgoing=True, pattern=r"^\.repo$")
async def repo_is_here(wannasee):
    """ For .repo command, just returns the repo URL. """
    await wannasee.edit("[Klik disini](https://github.com/BianSepang/WeebProject) untuk melihat base Repo yang saya gunakan.")


@register(outgoing=True, pattern=r"^\.myrepo$")
async def myrepo(wannasee):
    """ For .myrepo command, just returns to the URL. """
    await wannasee.edit("[Klik disini](https://github.com/AmamiyaRen666/WeebProject) untuk melihat Repo saya.")


@register(outgoing=True, pattern=r"^\.raw$")
async def raw(event):
    the_real_message = None
    reply_to_id = None
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        the_real_message = previous_message.stringify()
        reply_to_id = event.reply_to_msg_id
    else:
        the_real_message = event.stringify()
        reply_to_id = event.message.id
    with io.BytesIO(str.encode(the_real_message)) as out_file:
        out_file.name = "raw_message_data.txt"
        await event.edit("`Periksa log userbot untuk data pesan yang diterjemahkan!`")
        await event.client.send_file(
            BOTLOG_CHATID,
            out_file,
            force_document=True,
            allow_cache=False,
            reply_to=reply_to_id,
            caption="`Here's the decoded message data !!`",
        )


CMD_HELP.update(
    {
        "random": ">`.random <item1> <item2> ... <itemN>`"
        "\nUntuk: Dapatkan item acak dari daftar item.",
        "sleep": ">`.sleep <detik>`" "\nUntuk: Biarkan bot Anda tidur selama beberapa detik.",
        "shutdown": ">`.shutdown`" "\nUntuk: Matikan bot.",
        "repo": ">`.repo`" "\nUntuk: Github Repo asli dari bot ini.",
        "myrepo": ">`.myrepo`" "\nUntuk: Github Repo saya.",
        "readme": ">`.readme`"
        "\nUntuk: Berikan tautan untuk menyiapkan userbot dan modulnya.",
        "repeat": ">`.repeat <no> <teks>`"
        "\nUntuk: Ulangi teks tersebut beberapa kali. Jangan bingung ini dengan spam.",
        "restart": ">`.restart`" "\nUntuk: Mulai ulang bot.",
        "raw": ">`.raw`"
        "\nUntuk: Dapatkan data berformat seperti JSON mendetail tentang pesan yang dibalas.",
    }
)