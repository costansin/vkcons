# -*- coding: utf-8
import requests, time, datetime, ast, os, re, random, bisect, argparse
from tkinter import *
sleepTime, INFINITY, AU_OFFSET_CONSTANT, HI_OFFSET_CONSTANT, W_OFFSET_CONSTANT, L_OFFSET_CONSTANT, LF_OFFSET_CONSTANT, mnemofile, ignorefile, tokenfile, raspyafile, cachefile, headerfile, delayfile, looping, wfilters, photosizes, printm, width, height, mnemonics, ignore, header, idscache, uidscache, lastNviewcache, prob, token_num, block, delayed, default, full_auth_line = 0.34, 10000000, 300, 200, 100, 1000, 100, 'mnemo.txt', 'ignore.txt', 'tokens.txt', 'rasp.ya.txt', 'cache.txt', 'header.txt', 'delay.txt', False, {'<<': "postponed", '>>': "suggests", '>': "others", '<': "owner"}, [2560, 1280, 807, 604, 512, 352, 256, 130, 128, 100, 75, 64], '', 0, 0, {}, [], '', [], {}, [], [], 0, [], [], (0, 0, 53, 500, 1, False, "all is well"), 'https://oauth.vk.com/authorize?client_id=5193865&scope=notify,friends,photos,audio,video,docs,notes,pages,status,offers,questions,wall,groups,messages,notifications,stats,ads,offline&redirect_uri=https://oauth.vk.com/blank.html&display=page&response_type=token'
simple_smileys={128522: ':-)', 128515: ':-D', 128521: ';-)', 128518: 'xD', 128540: ';-P', 128523: ':-p', 128525: '8-)', 128526: 'B-)', 128530: ':-(', 128527: ';-]', 128532: '3(', 128546: ":'(", 128557: ':_(', 128553: ':((', 128552: ':o', 128528: ':|',128524: '3-)', 128519: 'O:)', 128560: ';o', 128562: '8o', 128563: '8|', 128567: ':X', 10084: '<3', 128538: ':-*', 128544: '>(', 128545: '>((', 9786: ':-]', 128520: '}:)', 128077: ':like:', 128078: ':dislike:', 9757: ':up:', 9996: ':v:', 128076: ':ok:'}
rev_simple_smileys={':-)': 'D83DDE0A.png', ':-D': 'D83DDE03.png', ';-)': 'D83DDE09.png', 'xD': 'D83DDE06.png', ';-P': 'D83DDE1C.png', ':-p': 'D83DDE0B.png', '8-)': 'D83DDE0D.png', 'B-)': 'D83DDE0E.png', ':-(': 'D83DDE12.png', ';-]': 'D83DDE0F.png', '3(': 'D83DDE14.png', ":'(": 'D83DDE22.png', ':_(': 'D83DDE2D.png', ':((': 'D83DDE29.png', ':o': 'D83DDE28.png', ':|': 'D83DDE10.png', '3-)': 'D83DDE0C.png', 'O:)': 'D83DDE07.png', ';o': 'D83DDE30.png', '8o': 'D83DDE32.png', '8|': 'D83DDE33.png', ':X': 'D83DDE37.png', '<3': '2764.png', ':-*': 'D83DDE1A.png', '>(': 'D83DDE20.png', '>((': 'D83DDE21.png', ':-]': '263A.png', '}:)': 'D83DDE08.png', ':like:': 'D83DDC4D.png', ':dislike:': 'D83DDC4E.png', ':up:': '261D.png', ':v:': '270C.png', ':ok:': 'D83DDC4C.png'}
smiley = re.compile('|'.join([re.escape(sm) for sm in rev_simple_smileys])+r'|\d+') #warning: all numbers are smileys!
helpinfo = {'?': ['% - эээ, а можно по-русски?\nto get user/group id use "u" command with his page address (you always can omit "https:/vk.com/"). Then assign him/her a mnemonic ("m"-command) and forget the id.\nall the commands are layout-insensitive and almost all are case-insensitive\nin a command syntax [something in brackets] means an optional parameter\nmessage syntax: [userid/mnemonic#]multi-line message [Ctrl+C to cancel]#[id/mnemonic#]# - mark as read\n[id/mnemonic#]## - 200 last messages (not marking as read!)\n[id/mnemonic#]###... - 200, 400, 600... last messages with their  numbers [for resend or deleting] and dates\n  - check messages and notifies (just press Enter)\n^ - hide tips\n! - set "too long" constant (? for help)\n\' - wait mode (autocheck once in a while; crtl+C to stop, execute the script with -L for non-console wait mode)\n+ - attach (? for help)\n~ - set waittime for wait mode\n` - history attachments filter (? for help)\nn - mark notifications as read\no - open a file from a direct link (? for help)\np - set probabilities of checking messages and notifies (? for help)\ne - info from your rasp.ya.ru file with informer-links\nw - see a wall or a wall post (? for help)\n: - open any site in the Internet in raw\ns - see the images of all the smileys from inserted text (? for help)\nt - input a raw call to vk API(? for help)\nl - likes (? for help)\nv - find a video; V - find a long HD-video\na - find an audio; A - of exact author, title or audios of a vk-user (? for help)\nd - find a doc (? for help)\nx - raw link to photo/audio(linked to IP)/video/doc\nu - user(s)/group info (? for help)\nf - friend someone/join a group/see someone\'s friends/subscribers (? for help)\nb - posts to your wall - warning: makes you online!\nr - reset the cache\n. - quick messages check\ni - see ignore list and add something to it\nm - see mnemo list and add something to it (? for help)\nh - saving history to a file\n- - deleting messages or a wall post (or edit, or restore) (? for help)\nz - latinize the layout (ПроLZLZрпр -> ghjlzlzhgh)\ny - user IP and location\ng - google something\n> - delayed execution of a single-line command or a block of commands (? for help with syntax)\n< - repeated execution (? for help with syntax)\n{ - start a block of commands; (? for help) } - end the block\n? - this help info\nq - quit', '% - Um, English, please\nчтоб заполучить чей-либо id, используйте команду "u" на адрес его страницы (всегда можно опустить "https:/vk.com/"). Затем назначьте ему мнемонику (команда "m") и забудьте про id.\nвсе команды не чувствительны к раскладке и почти все - к регистру\nв синтаксисе команды [в скобках] указаны необязательные параметры\nсинтаксис сообщения: [id/мнемоника#]многострочное сообщение [Ctrl+C для отмены ввода]#\n[id/мнемоника#]# - пометить прочтённым\n[id/мнемоника#]## - двести последних сообщений (не помечая прочтённым)\n[id/мнемоника#]###... - загрузить 200, 400, 600... последних сообщений с номерами [для пересылки или удаления] и датами\n  - проверка входящих сообщений и ответов (просто нажмите Enter)\n^ - спрятать подсказки\n! - установить константу "слишком длинно" (? для справки)\n\' - режим ожидания (автоматическая проверка входящих; ctrl+C чтобы прервать; запустите программу с ключом -L для режима ожидания без консоли)\n+ - прикрепить (? для справки)\n~ - установить время ожидания для режима ожидания\n` - фильтр на историю сообщений по вложениям\nn - отметить Ответы прочитанными\no - открыть файл по ссылке (? для справки)\np - установить вероятности проверки для сообщений и ответов (? для справки)\ne - информация по информерам rasp.ya.ru, ссылки на которые сохранены в вашем файле rasp.ya.txt\nw - просмотр стены или постов со стен (? для справки)\n: - открыть вообще любой сайт в Интернете в HTML\ns - посмотреть на картинки смайликов из вставленного куска текста (? для справки)\nt - отдать прямой запрос к vk API (? for help)\nl - лайки (? для справки)\nv - найти видео; V - найти длинное HD-видео\na - найти аудио; A - по точному имени исполнителя, названия или аудиозаписи пользователя vk (? для справки)\nd - найти документ (? для справки)\nx - прямая ссылка на фото/аудио (привязана к IP)/видео/документ (? для справки)\nu - информация о пользователе(-ях)/группе (? для справки)\nf - добавить кого-либо в друзья/добавиться в группу/посмотреть чьих-то друзей/подписчиков (? для справки)\nb - запостить себе на стену - внимание: делает онлайн!\nr - удалить кэш\n. - быстрая проверка входящих\ni - просмотреть игнор и занести туда кого-нибудь\nm - список мнемоник и добавить ещё (? для справки)\nh - сохранить историю сообщений в файл\n- - удаление/восстановление сообщений, постов со стены, редактирование постов (? для справки)\nz - латинизация раскладки (ПроLZLZрпр -> ghjlzlzhgh)\ny - IP и местоположение по яндексу\ng - погуглить\n> - отложенное выполнение однострочной команды или блока команд (? для справки)\n< - повторяющееся выполнение (? для справки)\n{ - начать блок команд; (? для справки) } - закончить блок\n? - эта справка\nq - выход'], '%': ['The language is changed. Sorry for my poor English. MGIMO finished, yeah.', 'Язык изменён, угадайте на какой.'], 'delay_warning': ['This will be REMOVED from the delay file!', 'Сие будет УДАЛЕНО из отложки!'], 'auth1': ['authorisation token needed\nplease insert that in your browser, press Allow and do what it strongly prohibits: copypaste the address line in here\nif you suspect me or something, just check the code you are using.', 'нужен токен авторизации\nпожалуйста, вставьте сие в свой браузер, нажмите Разрешить и сделайте то, что он запрещает: скопируйте то, что образуется в адресной строке, и вставьте мне сюда.\nесли вы мне не доверяете, просто покопайтесь в коде.'], 'auth2': ['c\'mon, dont you believe me? if i had made some backdoors, someone would have found them!', 'далааадно, не доверяете-с? если бы там были бэкдоры, их бы кто-нибудь уже нашёл!'], '<': ['input a period of time in hours (can be float),', 'введите период времени в часах (можно десятичной дробью через точку),'], '>': ['input time in format', 'введите время в формате'], '{}': [['command1\ncommand2\n...\n}', 'then input your single-line command or a block of commands in {brackets}'], ['команда1\nкоманда2\n...\n}', 'потом введите однострочную команду или блок команд в {скобках}']], '+': ['to the next message that will be attached:\nforward messages ids (e.g. 1232, 1233, 1237 or [1232], [1233], [1237] - find in ###-history a number line, press Enter, comma) |\nattachments (e.g. photo123123_123223,audio-34232_23123) |\ns Subject of the message |\nu - upload photo to a message (input file adress or nothing for Безымянный.png) |\nw - upload photo to a wallpost (same here) |\ndu - upload a document to send in via message |\ndw - upload a document to attach it to a wallpost\nif after attached audio\photo input a\p, nothing is attached, but the audio\photo is in your audios\saved photos', 'к следующему сообщению будут прикреплены:\nномера пересылаемых сообщений (e.g. 1232, 1233, 1237 или даже [1232], [1233], [1237] - находим в ###-истории строку с номером, Enter, запятая) |\nвложения (e.g. photo123123_123223,audio-34232_23123) |\ns Тема сообщения |\nu - загрузить фото в сообщение (ввести полный или относительный адрес файла или ничего для Безымянный.png, прикрепляется автоматически) |\nw - загрузить фото для прикрепления к посту на стену (пустое имя файла => Безымянный.png) |\ndu - загрузить документ для отправки в сообщение |\ndw - загрузить документ для отправки на стену\nесли после прикреплённой аудиозаписи/фото ввести a/p, ничего никуда прикреплено не будет, зато аудиозапись/фото добавится в ваши аудиозаписи/сохранённые картинки'], 'subj1': ['The subject is ', 'Тема сообщения: '], 'subj2': ['\nThe subject is not seen in history output of the script, but seen in bold in dialogs in a browser', '\nТема сообщения не видна в истории сообщений, которую выдаёт этот скрипт, но вполне видна жирненьким в диалогах в браузере.'], '~': ['waitTime = ', 'время ожидания = '], '~~': ['\nnew waitTime = ', '\nновое время ожидания = '], 'p': ['Set probabilities of message check and notifies check for every token while checkbox', 'Установить вероятности проверки сообщений и ответов для каждого токена'], 'p2': [['messages of ', 'notifies of '], ['сообщения пользователя ', 'ответы пользователя ']], 'w': ['Now you have to input the number of posts', 'А теперь введите-с кол-во постов, иже жаждете просмотреть'], '^': ['Yeah! All my stupid jokes enabled. I mean, tips.', 'Урра! Мои тупые шутки включены. В смысле, подсказки.'], 'comments': [['\nComments?', '\nDownload ', ' comments? Y / N / S - to last one will sort them in like-order'], ['\nКомментарии?', '\nПодгрузить ', ' комментариев? Y / N / S - последняя опция отсортирует их по лайкам']], 's': ['Input a text with smileys. Numbers and default graphic representation - ":-)", not ":)" - will be recognized and opened every smiley in a new window, lol', 'Введите текст со смайликами. Числа и стандартные графические репрезентации - т.е. ":-)", а не ":)" - будут распознаны и открыты: каждый смайлик в новом окне, лол.'], 't': [["'API method', {'param1': 'value1', 'param2': 'value2', ...}", 'input any API method from vk.com/dev/methods\nSyntax:\n'], ["'метод API', {'параметр1': 'значение1', 'параметр2': 'значение2', ...}", 'введите любой метод API из списка vk.com/dev/methods\nСинтаксис:\n']], 'l': [['syntax: type owner_id (e.g. audio 26522309_422813886 or post -69528510_158)\ntypes: post, comment, photo, audio, video, note, photo_comment, video_comment, topic_comment, sitepage', 'now type\n+ to like\n- to unlike\n? to get to know whether you or someone has already liked that\nc - to get the list of who reposted\nf - to get the list of friends who liked\ncf or fc - friends who reposted\nand anything else (e.g. empty string) to get the full list of who liked that', 'whos likes interest you? as usual, youself is an empty string, just press Enter.'], ['синтаксис: тип владелец_id (e.g. audio 26522309_422813886 или post -69528510_158)\nтипы: post, comment, photo, audio, video, note, photo_comment, video_comment, topic_comment, sitepage', 'теперь введите\n+ чтобы лайнуть сие\n - разлайнуть\n? - чтоб узнать, ужели ль лайнули ль сие вы или кто-то ещё\nс - получить список всех, кто репостнул\nf - получить список лайкнувших друзей\ncf - получить список репостнувших друзей\nчто угодно ещё (e.g. пустую строку) - чтоб получить полный список тех, кто это лайкнул', 'чьи лайки вас интересуют? как обычно, вы - просто пустая строка, тыкайте в Enter']], 'd': ['[T\ntype, e.g. fb2 or txt]\nsearch string', '[T\nтип, e.g. fb2 или txt]\nпоисковая строка'], 'header': ['Docs search function is not available in API. That\'s why please open your browser, open vk, Ctrl+Shift+J, click Network tab, choose any POST-request, find there your Cookie, remixsid is needed, paste it here', 'Поиск по документам не реализован в API. Посему, пожалуйста, откройте в браузере вконтактик, Ctrl+Shift+J, вкладка Сеть, выберите любой POST-запрос, найдите там Cookie, там найдите remixsid, скопируйте и вставьте его сюда.'], 'badheader': ['Something gone wrong, try update remixsid. (? for help)', 'Всё плохо, нужен новый remixsid. (? для справки)'], 'o': ['[wget - to download using wget]\nopens a file from a direct link. Or opens tokenfile, mnemofile, ignorefile, raspyafile - using T,M,I,R commands', '[wget - загрузить с помощью wget]\nоткрывает файл по прямой ссылке. Или открывает токен-файл, мнемо-файл, игнор-файл, rasp.ya-файл - через T,M,I,R команды соответственно'], 'x': [['get a direct link for a vk-object', 'photo123123_123123 or audio1231231_12213 or doc12412_34234 or video2123_123123 or http://vk.com/video_ext.php?oid=...'], ['прямая ссылка на vk-объект по его адресу вида', 'photo123123_123123 или audio1231231_12213 или doc12412_34234 или video2123_123123 или http://vk.com/video_ext.php?oid=...']], 'adult': [['ADULT CONTENT ERROR', '"This video was marked as adult.\nEmbedding adult videos on external sites is prohibited."\nThat\'s why i cannot get the link.', ' (? for help)'], ['ОШИБКА: КОНТЕНТ "ДЛЯ ВЗРОСЛЫХ"', '"Видеозапись была помечена модераторами сайта как «Материал для взрослых». Такие видеозаписи запрещено встраивать на внешние сайты."\nПосему я не могу получить ссылку.', ' (? для справки)']], 'damaged_cache' :['cache is damaged. reset? y\n', 'кэш повреждён. удалить? y\n'], '!': [['Set "too long" constant: if you exceed this number of symbols in a message you are trying to send, confirmation is inquired.', 'integer number is expected'], ['Установить константу "слишком длинно": если вы превышаете это кол-во символов в сообщении, что пытаетесь отослать, будет запрошено подтверждение.', 'это так-то целое число, вообще говоря']], 'u': ['user(s - separated with commas)/group info by id, address or a mnemonic\n[+\na string with parameters from vk.com/dev/fields separated with commas]', 'информация о пользователе(-ях через запятую)/группе по id, адресу или мнемонике\n[+\nстрока с параметрами с vk.com/dev/fields через запятую]'], 'f': ['Enter a userid or a mnemonic to friend someone/join a group.\nEnter empty line for getting your friends list\n> - for list of your subscribers\n< - list of whom you are a subscriber of\nF - enter - userid or a mnemonic to get someone\'s friends of members of a group','Введите id пользователя или мнемонику, чтоб зафрендить кого-нибудь/добавиться в группу.\nПустая строка, чтоб получить список своих друзей по дате последнего взаимного добавления.\n> - список ваших подписчиков\n< - список тех, на кого вы подписаны\nF - Enter - id пользователя или мнемонику, чтоб получить список чьих-либо друзей или членов группы.'], 'a': [['[Search string / nothing for your own audio]', '[Author / ID]\n[Title | id/mnemonic]', '[HERE]\n[WGET][start num]\n[Number]\n', '[HERE - to get output in here, (m3u.m3u is default output)]\n[WGET - to download using wget (on Win add it to PATH)][start number: incrementing number-prefix for files to save the order]\n[Number - the quantity of audios (may be SO big [e.g. group audio], but the search engine wont get more than 1000)]\n', '[Author - the exact name of the author (still case insensitive) or the word "ID", which means the next line is a userid/mnemonic]\n[Nothing for search by the author/your own audio or the exact title / userid/mnemonic]'], ['[Строка поиска / ничего для собственных аудио]', '[Автор / ID]\n[Название / id/мнемоника]', '[HERE]\n[WGET][стартовый номер]\n[Кол-во]\n', 'HERE - вывод в консоль (по умолчанию вывод в m3u.m3u)\n[WGET - загрузить с помощью wget (на винде добавьте его в PATH)]\n][старовый номер: возрастающий числовой префикс в названия файлов чтоб порядок аудиозаписей сохранился]\nКол-во аудиозаписей (может быть Очень большим [аудио группы, скажем], но если API-шный поиск выдаст не больше тысячи)\n', '[Автор - точное имя автора (не чувствительно к регистру) или слово "ID", означающее, в следующей строке будет id/мнемоника]\n[Ничего, чтоб искать по автору/вашим собственным аудио или точное название / id/мнемоника]']], 'b': ['just write a message, ending with #, it will be posted on your wall. You will become online.', 'просто наберите сообщение, заканчивающееся на #, оно отправится вам на стену. Вы станете онлайн.'], 'i': [['Now add something to ignore list! Chats are 2000000000 + chat_id. Or temporarily remove someone from it. No? Ctrl+C.', 'temporarily seen, to remove from ignore at all use "o" then "i"', 'ignore file was deleted!'], ['А теперь добавьте кого-нибудь в игнор! Чатики - это 2000000000 + id чата. Или временно удалите кого-нибудь оттуда. Не хотите? Ctrl+C', 'временно виден, чтоб удалить из игнора совсем - команда "o" потом "i"', 'Ой, кто-то удалил игнор-файл, а я и не заметил!']], 'm': [['Now add something to mnemo list (to cancel - CTRL+C). (? for help)', 'Mnemonics are freaking essential in this script. Type "ma" - Enter - and then user id of your mom. Now "ma" will always be your mom, always when your really mean it.', 'mnemo file was deleted!'], ['Теперь добавьте юзера/группу в мнемоники (? для справки)', 'Без мнемоник в этом скрипте хоть вешайся. Введите "mm" - Enter - и добавьте id пользователя своей мамы. И теперь "mm" (а также ьь, Ьm и проч.) будет всегда вам матерью, вот реально всегда, когда вы действительно имеете это в виду.', 'невероятно! пока я отвернулся, кто-то удалил мнемо-файл.']], 'h': [['This command saves a history to a file. If you wanted help, help command is "?"', 'simply input userid/mnemonic, history with whom you wanna save'], ['Эта команда сохраняет историю сообщений в файл. Если вы хотели справку, это команда "?".', 'Просто введите id или мнемонику того, переписку с кем вы жаждете сохранить для будущих поколений на случай краха серверов вконташи.']], '-': [['deleting/restoring messages (e.g. 5123,5124,5653)\nor a wall post (e.g. [[https://vk.com/]wall]-2424_2123).\ntype anything instead "Y" for the confirmation request and edit the wall post\ntry to delete non-existing post to make an attempt to restore it', 'not found, trying to restore', 'DELETE THAT?\nY/N', 'Edit post:'], ['удаление/восстановление сообщений (e.g. 5123,5124,5653']], '-': [['deleting/restoring messages (e.g. 5123, [5124],5653)\nor a wall post (e.g. [[https://vk.com/]wall]-2424_2123).\ntype anything instead "Y" for the confirmation request and edit the wall post\nif you try delete deleted messages, they are restored (for not deleting them again - Ctrl+C)\ntry to delete non-existing post to make an attempt to restore it', 'not found, trying to restore', 'DELETE THAT?\nY/N', 'Edit post:'], ['удаление/восстановление сообщений (e.g. 5123, [5124],5653)\nили пост со стены (e.g. [[https://vk.com/]wall]-2424_2123).\nЕсли на запрос подтверждения удаления ввести что угодно, кроме Y=y=Н=н (да, "н" это "да"), включается режим редактироваия стены.\nЕсли попытаться удалить удалённые сообщения, они сначала будут восстановлены (Чтоб не удалять их обратно - ctrl+C)\nудалить удалённый пост = попытаться его восстановить', 'не найдено, пытаемся восстановить', 'УДАЛИТЬ?\nY/N', 'Редактировать пост:']], 'toolong': [["C'mon, do I really interested in that? Better ask me how am I. (?fh)", 'too long', 'resend it to youself, yeah? hah. (only Ctrl+C to cancel)', 'to self?'], ['Далаадно, думаешь, ей реально интересно читать всю эту писанину? (?спр)', 'длинно.', 'переслать это себе, чтоб не потерять? (ctrl+C отмена)', 'себе?']], 'mixup': [['The history is empty! Have you mixed up your tokens? (?fh)', 'empty history', 'input another token number', 'token_num:'], ['История пуста! Кто-то запутался в фейках? (?спр)', 'история пуста', 'введите другой номер токена', 'token_num:']], 'confirmation': [['for confirmation just type in that mantra: "', '". To change mantra print it in here:'], ['для подтверждения введи мантру: "', '". Cменить мантру можно прямо здесь:']], 'fwd': [['[forward_messages:]', '[fwd]'], ['[пересланные сообщения:]', '[>>]']], 'wfilters': ['wall34124_14124,22424_2424,wall2124_224\n|\nuserid/mnemonic\n[filter]\nnumber of posts\n\nwall filters are: >> for suggests, << for postponed, > for others\' posts, < for only own posts', 'wall34124_14124,22424_2424,wall2124_224\n|\nid/мнемоника\n[фильтр]\nкол-во постов\n\nфильтры стены: >> - предложка, << - отложка, > - посты других, < - собственные посты'], '`': ['temporary filter on message history by attachments: substring in type name:  e.g. p, h or ph for photo ot d for auDio, viDeo and Docs ', 'Временный фильтр на историю сообщений по вложениям: подстрока в имении типа вложения, e.g. p, h или ph для photo или d для auDio, viDeo и Docs']}
def help(index): return helpinfo[index][lang]
def start():
        for x in mnemofile, ignorefile, tokenfile, raspyafile, cachefile, headerfile, delayfile:
                if not os.path.exists(x):
                        with open(x, 'w') as f: pass
        global token_list, raspyadress, smileys, delayed
        with open(tokenfile, 'r') as token_file: token_list = [token.strip() for token in token_file.readlines() if token[0]!='#'] #start line with # to make it comment
        with open(raspyafile, 'r') as raspya_file: raspyadress = [a for a in raspya_file.readlines() if a[0]!='#'] #start line with # to make it comment
        with open(delayfile, 'r') as delay_file:
                delaystr = delay_file.read()
                try: delayed = ast.literal_eval(delaystr)
                except:
                        if delaystr: print(delaystr+'\n'+help("delay_warning"))
                        delayed = []
        if os.path.isdir('smileys'): smileys = os.listdir('smileys')
def call_api(method, params):
        #print(method, params, token_num)
        #time.sleep(sleepTime)
        print('.', end='') if not looping else print(',', end='')
        if method[:7]=='http://':
                q = method.find('?')
                url = method[:q]
                if 'act=add_doc' in method: files = {'file': ('file'+params[params.rfind('.'):], open(params, 'rb'))}
                else: files = {'photo': ('file.png', open(params, 'rb'))}
                params = {}
                for query in method[q+1:].split('&'):
                        v = query.split('=')
                        params[v[0]]=v[1]
        else:
                params['access_token'] = token_list[token_num]
                params['v'] = '5.40'
                url = 'https://api.vk.com/method/' + method
                files = None
        E = False
        while True:
                try:
                        E = False
                        timeout = 0.5 if 'messages' in url or 'notifications' in url else None #if files or else len(str(params))/266                        
                        try: result = requests.post(url, data=params, files=files, timeout=timeout)
                        except KeyboardInterrupt: return
                        result = result.json()
                        if 'error' not in result: return result['response'] if 'response' in result else result
                        else:
                                err = result.get('error')
                                msg = err.get('error_msg')
                                print(msg)
                                if 'Validation' in msg: print(err.get('redirect_uri'))
                                if 'authorization' in msg: print(full_auth_line)
                                return
                except:
                        if not E:
                                print('E', end='')
                                E = True
                        time.sleep(sleepTime)
def saveinstance():
        with open(cachefile, 'w', encoding='utf-8') as cache_file:
                cache_file.write('\n'.join([str(idscache), str(lastNviewcache), str(prob), str((token_num, prevuserid, waitTime, TOO_LONG_CONSTANT, lang, hide, confirmation_word)), str(uidscache)]))
def reset():
        global token_num, idscache, uidscache, lastNviewcache, prob, prevuserid, token_list, sleepTime, waitTime, TOO_LONG_CONSTANT, lang, hide, confirmation_word
        lastNviewcache, idscache, uidscache, prob, token_num, prevuserid, waitTime, TOO_LONG_CONSTANT, lang, hide, confirmation_word = [], [], {}, [], *default
        if not token_list:
                print(full_auth_line+'\n\n\n'+help("auth1"))
                s = cin()
                if s is None:
                        print(help("auth2"))
                        s = cin()
                        if s is None: raise PermissionError ('Lack of trust error')
                refull = re.findall('access_token=.*?&', s)
                if refull: s = refull[0][13:-1]
                token_list = [s]
                with open(tokenfile, 'w') as token_file: token_file.write(s+'\n')
        for token_num in range(len(token_list)):
                api_call = call_api('users.get', {})
                if api_call:
                        me = api_call[0]
                        idscache = idscache + [me.get('id')]
                        uidscache[me.get('id')] = me
                else: idscache = idscache + [0]
                api_call = call_api('notifications.get',{'count': '0'})
                lastNviewcache = lastNviewcache + [api_call.get('last_viewed')] if api_call else lastNviewcache + [int(time.time())]
                prob.extend([1,1])
        token_num = 0
        prevuserid = idscache[token_num]
        saveinstance()
        print()
        return 0
def getcache():
        global idscache, lastNviewcache, prob, token_num, prevuserid, waitTime, TOO_LONG_CONSTANT, lang, hide, confirmation_word, uidscache
        with open(cachefile, 'r', encoding='utf-8') as cache_file:
                try:
                        i, l, p, cort, u = cache_file.readlines()
                        idscache, lastNviewcache, prob, token_num, prevuserid, waitTime, TOO_LONG_CONSTANT, lang, hide, confirmation_word, uidscache = ast.literal_eval(i), ast.literal_eval(l), ast.literal_eval(p), *ast.literal_eval(cort), *default[cort.count(',')+1:], ast.literal_eval(u)
                except:
                        print(help("damaged_cache"))
                        s = cin()
                        if l(s)=='y': reset()
def getcached(uid):
        global uidscache
        result = uidscache.get(uid)
        if result is None:
                api_call = (call_api('users.get', {'user_ids': uid}) if uid>=0 else call_api('groups.getById', {'group_ids': -uid}))
                if api_call: result = api_call[0]
                if result: uidscache[uid] = result
                saveinstance()
        return result
def get_long_list(method, params, l_count, OFFSET_CONSTANT):
        l_offset = 0
        long_list = []
        long_list_step = []
        while l_count>0:
                params.update({'count': min(l_count, OFFSET_CONSTANT),'offset': l_offset})
                api_call = call_api(method, params)
                long_list_step = api_call.get('items') if api_call else None
                if not long_list_step: break
                long_list = long_list + long_list_step
                l_offset = l_offset + OFFSET_CONSTANT
                l_count = l_count - OFFSET_CONSTANT
                print(len(long_list), end='')
        return long_list
def cin():
        if block: return block.pop(0)
        else:
                if looping: exit()
                try: return(input())
                except KeyboardInterrupt: exit
def read_header():
        global header
        with open(headerfile, 'r') as header_file: header = header_file.read().strip()
def read_mnemonics():
        global mnemonics
        with open(mnemofile, 'r') as f:
                for line in f:
                        key, value = line.split()
                        mnemonics[key] = int(value)
def read_ignore():
        global ignore
        with open(ignorefile, 'r') as f:
                for line in f: ignore.append(mn(line.strip()))
def l(wrong):
        wrong = wrong.strip() 
        right = ''
        for wrong_letter in wrong:
                right_letter = wrong_letter if ord(wrong_letter)<128 else '#`qwertyuiop[]asdfghjkl;\'zxcvbnm,.~QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>_'['№ёйцукенгшщзхъфывапролджэячсмитьбюЁЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ_'.find(wrong_letter)]
                right = right + right_letter
        return right.lower()
def mn(idstring):
        idstring = l(idstring)
        if idstring in mnemonics: return mnemonics[idstring]
        else:
                try: return int(idstring)
                except: return
def smiley_hex(c, sh): return hex(c+sh).upper()[2:]+'.png'
def charfilter(s):
        r=''
        for c in s:
                ch = ord(c)
                if ch<8617: r+=c
                elif ch in simple_smileys: r+=simple_smileys[ch]+' '
                else: r+='&#'+str(ch)+';'
        return r
def printms():
        global printm
        print(printm) #print('{'+printm+'}')
        printm = ''
def printsn(s):
        global printm
        printm += '\n'+s
def printtime(date): return('['+datetime.datetime.fromtimestamp(date).strftime('%d %b %Y (%a) %H:%M:%S')+']')
def name_from_id(uid):
        cachedid = getcached(uid)
        if cachedid:
                name = cachedid.get('first_name', '') + ' '
                if uid>=0: name += cachedid.get('last_name', '')+' '
                else: name = cachedid.get('name', '')+' '
                if name.strip()=='DELETED': name=''
                return name + '('+'-'*(uid<0)+str(cachedid.get('id', ''))+')'
        else: return '0'
def iam():
        if idscache: print('\n'+name_from_id(idscache[token_num])+' to '+name_from_id(prevuserid)+':')
def photolink(photo):
        for size in photosizes:
                link=photo.get('photo_'+str(size))
                if link is not None: return link
        return None
def print_attachments(attache):
        for attached in attache:
                atype = attached.get('type', '')
                cropf = atype.find('_')
                croptype = atype[:cropf] if cropf>=0 else atype
                stuff = attached.get(atype)
                owner = stuff.get('owner_id')
                if owner is None: owner = stuff.get('to_id')
                if owner is None:
                        try: owner = -stuff.get('group_id')
                        except: owner = None
                cropadress = str(owner)+'_'+str(stuff.get('id'))
                adress = croptype + cropadress
                if (atype=='photo')or(atype=='sticker'): printsn(photolink(stuff))
                elif atype=='video': adress = adress + '_' + str(stuff.get('access_key', ''))
                elif atype=='link':
                        printsn('['+stuff.get('title', '')+']\n['+stuff.get('description', '')+']\n'+stuff.get('url', ''))
                        return
                else:
                        url = stuff.get('url', '')
                        if url is None: url = stuff.get('view_url', '')
                        if url is not None:
                                urlf = url.find('?extra')        
                                if (urlf!=-1):
                                        printsn(stuff.get('artist', '')+' - '+stuff.get('title', ''))
                                        printsn(url[:urlf]+' ')
                                else: printsn(url+' ')
                printsn(adress+' ')
def print_message(prefix, message, k):
        body = prefix + message.get('body')
        if body: printsn(charfilter(body)) if message.get('emoji') else printsn(body)
        print_attachments(message.get('attachments', []))
        fwd = message.get('fwd_messages')
        if fwd is not None:
                printsn('     '*k + help("fwd")[int(hide)])
                for fwdm in fwd: print_message('     '*(k+1) + '['+name_from_id(fwdm.get('user_id'))+']', fwdm, k+1)
def getHistory(count, print_numbers, uid):
        if not isinstance(uid, int): uid = mn(uid)
        chat = uid>=2000000000
        unread = False
        history = get_long_list('messages.getHistory', {'peer_id': uid}, count, HI_OFFSET_CONSTANT)
        if history_filter: history = [message for message in history if any(history_filter in atmt.get('type', '') for atmt in message.get('attachments', []))]
        inoutchar = ''
        if not history: return
        for message in reversed(history):
                if not unread and (message.get('read_state')==0):
                        unread = True
                        printsn('_._')
                if (message.get('out')==0):
                        if (inoutchar!='>'):
                                inoutchar='>'
                                printsn(inoutchar)
                else:
                        if (inoutchar!='<'):
                                inoutchar='<'
                                printsn(inoutchar)
                if print_numbers:
                        printsn('['+str(message.get('id'))+']')
                print_message('['+name_from_id(message.get('user_id'))+']' if chat else '', message, 0)
                if print_numbers: printsn(printtime(message.get('date')))
        if not print_numbers: printsn(printtime(message.get('date')))
def print_id_list(id_list):
        print_list = call_api('users.get', {'user_ids': str(id_list)[1:-1]})
        print('\n'+str(len(print_list)))
        if print_list:
                for pus in print_list:
                        try:
                                print(pus.get('first_name'), pus.get('last_name'), pus.get('id'))
                                uidscache[pus.get('id')] = pus
                        except KeyboardInterrupt: break
        saveinstance()
def showprintm():
        master=Tk()
        master.wm_attributes("-topmost", 1)
        master.wm_state('normal')
        w = Canvas(master, width=width, height=height)
        w = Message(master, text=printm)
        w.pack()
        master.mainloop()
def check_delayed():
        while delayed and time.time() > delayed[0][0]: block.extend(delayed.pop(0)[1])
        if block:
                with open(delayfile, 'w') as delay_file: delay_file.write(str(delayed))
        return (len(block))
def add_delayed(delay_time):
        global delayed, block
        bisect.insort(delayed, (delay_time, block))
        with open(delayfile, 'w') as delay_file: delay_file.write(str(delayed))
        block = []
confirmation_word = "all is well"
def ask_confirmation(helpindex):
    global confirmation_word
    print(help(helpindex)[int(hide)])
    confirmation = cin()
    if confirmation is None or l(confirmation)!=l(confirmation_word):
        if confirmation=='?':
            print(help("confirmation")[0] + confirmation_word + help("confirmation")[1])
            confirmation = cin()
            if confirmation is not None:
                if l(confirmation)==l(confirmation_word): return(-1)
                confirmation_word = confirmation
                saveinstance()
                return(-1)
        print(help(helpindex)[2+int(hide)])
        return(cin())
    else: return(-1)
def messaging():
        global token_num, printm, waitTime, prevuserid, block, lang, TOO_LONG_CONSTANT, hide, header, history_filter
        iam()
        m, s, attachments, forward_messages, userid, wall_flag, wall_edit_flag, subject, delay_time, history_filter = '', '', '', '', None, False, False, None, None, None
        check_delayed()
        while (s=='')or(l(s[-1])!='#'):
                s = cin()
                if s is None: return(0)
                if (m==''):
                        if (s==''): return(-2)
                        if (len(s)==1):
                                if s.isdigit():
                                        n = int(s)
                                        if n<len(token_list):
                                                token_num = n
                                                prevuserid = idscache[n]
                                                saveinstance()
                                        return(0)
                                def r(c): return l(s)==c
                                if r(">") or r("<"):
                                        fs = '\n'+s
                                        repeated = r("<")
                                        nowstamp = datetime.datetime.fromtimestamp(time.time())
                                        s = cin()
                                        if s is None: return(0)
                                        if r("?"):
                                                print(help("<") if repeated else nowstamp.strftime(help(">")+' 18:00:00 %d.%m.%Y,'), help("{}")[1], sep='\n')
                                                return(0)
                                        if repeated:
                                                try: delay_period = float(s)/3600
                                                except: m = fs
                                                else: delay_time = time.time()+delay_period
                                        else:
                                                try: delay_time = time.mktime(datetime.datetime.strptime(s, "%H:%M:%S %d.%m.%Y").timetuple())
                                                except: m = fs
                                        if not m:
                                                s = cin()
                                                if s is None: return(0)
                                                if not r("{"):
                                                        block.append(s)
                                                        if repeated: block.extend(['<', str(delay_period), s])
                                                        add_delayed(delay_time)
                                                        return(0)
                                if r("{"):
                                        bracket_counter = 1
                                        s = cin()
                                        if s is None: return(0)
                                        if r("?"):
                                                print(help("{}")[0])
                                                return(0)
                                        temp_block = []
                                        while True:
                                                bracket_counter += int(r("{")) - int(r("}"))
                                                if not bracket_counter:
                                                        if repeated:
                                                                block.extend(temp_block + ['<', str(delay_period), '{'])
                                                                temp_block.append('}') #block += [temp, <, delay_period, {, temp, }]
                                                        break
                                                temp_block.append(s)
                                                s = cin()
                                                if s is None:
                                                        temp_block = []
                                                        break
                                        block.extend(temp_block)
                                        if delay_time is not None: add_delayed(delay_time)
                                        return(0)
                                elif r("?"):
                                        print(help("?"))
                                        return(0)
                                elif r("%"):
                                        lang = 1-lang
                                        if not hide: print(help("%"))
                                        saveinstance()
                                        return(0)
                                elif r("^"):
                                        if hide: print(help("^"))
                                        hide = not hide
                                        saveinstance()
                                        return(0)
                                elif r("!"):
                                        s = cin()
                                        if s is None: return(0)
                                        if r("?"):
                                                print(help("!")[0])
                                                return(0)
                                        else:
                                                while True:
                                                        try: TOO_LONG_CONSTANT = int(s)
                                                        except:
                                                                print(help("!")[1])
                                                                s = cin()
                                                                if s is None: return(0)
                                                        else: return(0)
                                elif r("'"): return(-1)
                                elif r("+"):
                                        s = cin()
                                        if s is None: return(0)
                                        if r("?"):
                                                print(help("+"))
                                                return(0)
                                        if r("u"): uploades = ['photos.getMessagesUploadServer', 'photos.saveMessagesPhoto']
                                        elif r("w"): uploades = ['photos.getWallUploadServer', 'photos.saveWallPhoto']
                                        elif r("du"): uploades = ['docs.getUploadServer', 'docs.save']
                                        elif r("dw"): uploades = ['docs.getWallUploadServer', 'docs.save']
                                        else: uploades = None
                                        if uploades:
                                                up_doc = int(s[0]=='d')
                                                s = cin()
                                                if s is None: return(0)
                                                if s.strip()=='': s='Безымянный.png'
                                                upload_url = call_api(uploades[0], {})
                                                if upload_url: upload_stuff = call_api(upload_url.get('upload_url'), s)
                                                else: return(0)
                                                if upload_stuff: uploaded = call_api(uploades[1], upload_stuff)      
                                                else: return(0)
                                                if uploaded: s = ['photo','doc'][up_doc]+str(uploaded[0].get('owner_id'))+'_'+str(uploaded[0].get('id'))
                                                print('\n'+s)
                                        if s.strip(' \n\t[]')[0].isdigit(): forward_messages += ',' + re.sub('\[(.*?)\]', r'\1', s)
                                        elif l(s[0])=='s': 
                                                subject = s[1:].strip() #s The subject of my message
                                                if not hide: print(help("subj1") + subject + help("subj2"))
                                        else: attachments += ',' + s.replace(' ','')
                                        continue
                                if r("~"):
                                        print(help("~"), waitTime, help("~~"), end='')
                                        s = cin()
                                        if s is None: return(0)
                                        try: waitTime = int(s)
                                        except: return(0)
                                        saveinstance()
                                        return(0)
                                elif r("`"):
                                        s = cin()
                                        if s is None: return(0)
                                        if r("?"):
                                                print(help("`"))
                                                s = cin()
                                                if s is None: return(0)
                                        history_filter = s
                                        continue
                                elif r("n"):
                                        call_api('notifications.markAsViewed', {})
                                        lastNviewcache[token_num] = int(time.time())
                                        saveinstance()
                                        print()
                                        return(0)
                                elif r("p"):
                                        if attachments:
                                                add_owner_id, add_photo_id = attachments.split('_')
                                                print('photo'+str(idscache[token_num])+'_'+str(call_api('photos.copy', {'owner_id': int(add_owner_id[6:]), 'photo_id': int(add_photo_id)})))
                                                return(0)
                                        print(help("p"))
                                        global prob
                                        print(prob)
                                        try: prob = [float(input(help("p2")[i&1]+name_from_id(idscache[i>>1])+': ')) for i in range(len(token_list)<<1)]
                                        except: return(0)
                                        return(0)
                                elif r("e"): #rasp.yandex.ru/search/suburban/? #https://rasp.yandex.ru/informers/search/?fromId=s0000000&amp;toId=s0000000&amp;
                                        for rasp in raspyadress:
                                                r = requests.get(rasp)
                                                r.encoding = 'UTF-8'
                                                x = r.text
                                                print(x[x.find('<title>')+7:x.find('</title>')])
                                                l2 = [x[m.start()-5:m.start()] for m in re.finditer(':00&', x)]
                                                stations = [st[st.find('>')+1:st.find('<')].replace('\xa0',' ') for st in re.findall(r'overflow-inner.*?div',x)]
                                                l3 = list(map(lambda z, x, y: x+' - '+y+' - '+z, stations[::], l2[::2], l2[1::2]))
                                                for r in l3: print(r)
                                        return(0)
                                elif r("w"):
                                        s = cin()
                                        if s is None: return(0)
                                        if r("?"):
                                                print(help("wfilters"))
                                                s = cin()
                                                if s is None: return(0)
                                        s = l(s)
                                        if s in wfilters.keys():
                                                wall_filter = wfilters[s]
                                                s = cin()
                                                if s is None: return(0)
                                        else: wall_filter = "all"
                                        wall_owner = mn(s)
                                        print(wall_owner)
                                        if wall_owner is None:
                                                findwall = s.find('wall')
                                                if findwall+1: s = s[findwall:]
                                                s = s.replace('wall','')
                                                wall = call_api('wall.getById',{'posts':s})
                                                if wall is None: return(0)
                                        else:
                                                if not hide: print(help("w"))
                                                s = cin()
                                                if s is None: return(0)
                                                try: postsN = int(s)
                                                except: return(0)
                                                api_call = call_api('wall.get', {'owner_id': wall_owner, 'count': postsN, 'filter': wall_filter})
                                                if api_call: wall = api_call.get('items')
                                                else: return(0)
                                        printm='\n'
                                        for post in wall:
                                                wowner, wid = str(post.get('owner_id')), str(post.get('id'))
                                                printsn('wall'+wowner+'_'+wid+'\n'+name_from_id(post.get('from_id'))+'\n\n'+charfilter(post.get('text')))
                                                reposted = post.get('copy_history')
                                                if reposted:
                                                        for reposts in reposted:
                                                                printsn('\t[REPOSTED]\n\t'+charfilter(reposts.get('text')))
                                                                print_attachments(reposts.get('attachments', []))
                                                print_attachments(post.get('attachments', []))
                                                posttype = post.get('post_type')
                                                sugpone = posttype=='suggest' or posttype=='postpone'
                                                printsn('\n'+posttype.upper()+'\n____' if sugpone else '\n'+str(post.get('likes').get('count'))+' likes, '+str(post.get('comments').get('count'))+' comments\n____')
                                        if len(wall)==1:
                                                print(printm)
                                                com_num = post.get('comments').get('count')
                                                if com_num>10:                                        
                                                        print(help("comments")[0] if hide else help("comments")[1] + str(com_num) + help("comments")[2])
                                                        s = cin()
                                                        if s is None: return(0)
                                                else: s="y"
                                                if not sugpone and (r("y") or r("s")):
                                                        printsn('COMMENTS:')
                                                        wallcomments = get_long_list('wall.getComments', {'owner_id': wowner, 'post_id': wid, 'need_likes': 1},INFINITY,W_OFFSET_CONSTANT)
                                                        if r("s"): wallcomments.sort(key=lambda comment: comment.get('likes').get('count'))
                                                        for comment in wallcomments:
                                                                printsn('wall'+wowner+'_'+wid+'?reply='+str(comment.get('id'))+'\n'+name_from_id(comment.get('from_id'))+'\n\n'+charfilter(comment.get('text')))
                                                                print_attachments(comment.get('attachments', []))
                                                                printsn('\n'+str(comment.get('likes').get('count'))+' likes')
                                                                printsn('____')
                                        printms()
                                        return(0)
                                elif r(":"):
                                        s = cin()
                                        if s is None: return(0)
                                        if not s.startswith('http'): s='http://'+s
                                        x = requests.get(s)
                                        print(x.text)
                                        return(0)
                                elif r("s"):
                                        s = cin()
                                        if s is None: return(0)
                                        if r("?"):
                                                print(help("s"))
                                                return(0)
                                        y = smiley.findall(s)
                                        for s in y:
                                                if s in rev_simple_smileys:
                                                        os.system('smileys\\'+rev_simple_smileys[s])
                                                        return(0)
                                                try: c = int(s)
                                                except:
                                                        while (s!='')and not (s[0].isdigit()): s=s[1:]
                                                        while (s!='')and not (s[-1].isdigit()): s=s[:-1]
                                                        try: c=int(s)
                                                        except: return(0)
                                                h72 = smiley_hex(c,3627804672)
                                                h60 = smiley_hex(c,3627740160)
                                                h0 = smiley_hex(c,0)
                                                if h72 in smileys: os.system('smileys\\'+h72)
                                                elif h60 in smileys: os.system('smileys\\'+h60)
                                                elif h0 in smileys: os.system('smileys\\'+h0)
                                        return(0)
                                elif r("t"):
                                        if not hide: print(help("t")[0])
                                        s = cin()
                                        if s is None: return(0)
                                        if r("?"):
                                                print(help("t")[1]+help("t")[0])
                                                return(0)
                                        lit = ast.literal_eval(s)
                                        g = call_api(*lit)
                                        print(charfilter(str(g)))
                                        return(0)
                                elif r("l"):
                                        globalhide = hide
                                        if not hide: print(help("l")[0])
                                        s = cin()
                                        if s is None: return(0)
                                        if r("?"):
                                                print(help("l")[0])
                                                hide = False
                                                s = cin()
                                                if s is None: return(0)
                                        try: lobjecttype, what = s.split()
                                        except:
                                                hide = globalhide
                                                return(0)
                                        lowner, lid = what.split('_')
                                        if not hide: print(help("l")[1])
                                        s = cin()
                                        if s is None:
                                                hide = globalhide
                                                return(0)
                                        like_list = None
                                        if r("+"): print(call_api('likes.add', {'type': lobjecttype, 'owner_id': lowner, 'item_id': lid}))
                                        elif r("-"): print(call_api('likes.delete', {'type': lobjecttype, 'owner_id': lowner, 'item_id': lid}))
                                        elif r("?"):
                                                if not hide: print(help("l")[2])
                                                s = cin()
                                                if s is None:
                                                        hide = globalhide
                                                        return(0)
                                                luserid = mn(s)
                                                print(call_api('likes.isLiked', {'user_id': luserid, 'type': lobjecttype, 'owner_id': lowner, 'item_id': lid}))
                                        elif r("c"): like_list = get_long_list('likes.getList', {'filter': 'copies', 'type': lobjecttype, 'owner_id': lowner, 'item_id': lid}, INFINITY, L_OFFSET_CONSTANT)
                                        elif r("f"): like_list = get_long_list('likes.getList', {'friends_only': 1, 'type': lobjecttype, 'owner_id': lowner, 'item_id': lid}, INFINITY, LF_OFFSET_CONSTANT)
                                        elif r("cf") or r("fc"): like_list = get_long_list('likes.getList', {'filter': 'copies', 'friends_only': 1, 'type': lobjecttype, 'owner_id': lowner, 'item_id': lid}, INFINITY, LF_OFFSET_CONSTANT)
                                        else: like_list = get_long_list('likes.getList', {'type': lobjecttype, 'owner_id': lowner, 'item_id': lid}, INFINITY, L_OFFSET_CONSTANT)
                                        if like_list is not None: print_id_list(like_list)
                                        hide = globalhide
                                        return(0)
                                elif r("d"):
                                        s = cin()
                                        if s is None: return(0)
                                        dtype = None
                                        if r("?"):
                                                print(help("d"))
                                                return(0)
                                        elif r("t"):
                                                s = cin()
                                                if s is None: return(0)
                                                dtype = s.lower()
                                                s = cin()
                                                if s is None: return(0)
                                        docdata = {'act': 'search_docs', 'al': '1', 'offset': '0', 'oid': idscache[token_num], 'q': s}
                                        while True:
                                                rq = requests.request(method="POST", url="https://vk.com/docs.php", headers={'Cookie': 'remixsid='+header}, data=docdata) #docheader["Referer"] = "https://vk.com/docs"
                                                v = rq.text[rq.text.find('[['):rq.text.rfind(']]')+2]
                                                if v: break
                                                print("remixsid:" if hide else help("badheader"))
                                                s = cin()
                                                if s is None: return(0)
                                                if r("?"):
                                                    print(help("header"))
                                                    s = cin()
                                                    if s is None: return(0)
                                                header = s
                                        with open(headerfile, 'w', encoding='utf-8') as header_file: header_file.write(header)
                                        lit = ast.literal_eval(v)
                                        if dtype: lit = [doc for doc in lit if doc[1]==dtype]
                                        for doc in lit: print(doc[2], 'doc'+str(doc[4])+'_'+str(doc[0])) #doc[3] - size and date
                                        return(0)
                                elif r("o"):
                                        s = cin()
                                        if s is None: return(0)
                                        if r("?"):
                                                print(help("o"))
                                                return(0)
                                        owget = r("wget")
                                        if owget:
                                                s = cin()
                                                if s is None: return(0)
                                        if r("t"): os.system(tokenfile)
                                        elif r("m"): os.system(mnemofile)
                                        elif r("i"): os.system(ignorefile)
                                        elif r("r"): os.system(raspyafile)
                                        else:
                                                ofname = 'file'+(s+'A')[s.rfind('.'):s.rfind('?')]
                                                if owget:
                                                        wget_filename = 'opwget.bat'
                                                        with open(wget_filename, 'w', encoding='utf-8') as wget_file: wget_file.write('chcp 65001\nwget ' + s + ' -O "' + ofname + '"\nDel %0 /q\n')
                                                        os.system(wget_filename)
                                                else:
                                                        with open(ofname, 'wb') as f: f.write(requests.get(s).content)
                                                os.system(ofname)
                                                return(0)
                                        start()
                                        return(0)
                                elif r("v"):
                                        vhd = int(s.isupper())
                                        s = cin()
                                        if s is None: return(0)
                                        v = call_api('video.search', {'q':s, 'sort': 2, 'hd': vhd, 'filters': 'long'*vhd, 'adult': '1'})
                                        if v is None: return(0)
                                        for vid in v.get('items'): print('video'+str(vid.get('owner_id'))+'_'+str(vid.get('id')), vid.get('title'), sep='\t') #print(vid.get('player')))
                                        return(0)
                                elif r("x"):
                                        s = cin()
                                        if s is None: return(0)
                                        if r("?"):
                                                print(help("x")[0], help("x")[1], sep='\n')
                                                s = cin()
                                                if s is None: return(0)
                                        vktrim = s.find('vk.com')
                                        if vktrim+1: s = s[vktrim+7:]
                                        if s.startswith('doc'):
                                                r = requests.get('https://vk.com/'+s)
                                                if not r: return(0)
                                                t = r.text
                                                print(t[t.find('src="')+5:t.find('" w')])
                                        elif s.startswith('photo'):
                                                api_call = call_api('photos.getById', {'photos': s[5:]})
                                                if api_call: print(photolink(api_call[0]))
                                                return(0)
                                        elif s.startswith('audio'):
                                                owner, aid = s[5:].split('_')
                                                api_call = call_api('audio.get', {'owner_id': owner, 'audio_ids': aid})
                                                if not api_call: return(0)
                                                auresplist = api_call.get('items')
                                                if not auresplist: return(0)
                                                aur = auresplist[0]
                                                for x in aur: print(x, aur[x], sep='\t\t')
                                                return(0)
                                        elif s.startswith('video'):
                                                s = s[s.find('video')+5:]
                                                api_call = call_api('video.get', {'videos': s})
                                                if api_call:
                                                        vid = api_call.get('items')
                                                        if vid:
                                                                v = vid[0]
                                                                if v.get('is_private'): print('ADULT_CONTENT') #or just private?
                                                                s = v.get('player')
                                                                print(s)
                                        else:
                                                print(help("x")[1])
                                                return(0)
                                        if 'video_ext' not in s: return(0)
                                        if 'http://vk.com/' not in s: s = 'http://vk.com/'+s
                                        x = requests.get(s).text
                                        if 'video_ext_msg' in x:
                                                print(help("adult")[0] + help("adult")[2]*int(not hide))
                                                s = cin()
                                                if r("?"): print(help("adult")[1])
                                                return(0)
                                        xd = x.find('video_max_hd = ')
                                        try: video_max_hd = int(x[xd+16])
                                        except: video_max_hd = 0
                                        hds = ['240', '360', '480', '720', '1080']
                                        vurlfind = x.find('url'+hds[video_max_hd])+7
                                        video_url = x[vurlfind:x.find('&amp;', vurlfind)]
                                        print(video_url)                        
                                        return(0)
                                elif r("a"):
                                        if attachments:
                                                add_owner_id, add_audio_id = attachments.split('_')
                                                print(call_api('audio.add', {'owner_id': int(add_owner_id[6:]), 'audio_id': int(add_audio_id)}))
                                                return(0)
                                        big_audio_flag = s.isupper()
                                        m3u_flag = True
                                        wget_flag = False
                                        wget_start_num = None
                                        if not hide: print(help("a")[2]+help("a")[int(big_audio_flag)])
                                        s = cin()
                                        if s is None: return(0)
                                        if r("?"):
                                                print(help("a")[3]+help("a")[int(big_audio_flag)<<2])
                                                return(0)
                                        if r("here"):
                                                m3u_flag = False
                                                s = cin()
                                                if s is None: return(0)
                                        if l(s[:4])=='wget':
                                                wget_flag = True
                                                try: wget_start_num = int(s[4:].strip())
                                                except: wget_start_num = None
                                                s = cin()
                                                if s is None: return(0)
                                        if s.isdigit():
                                                au_count = int(s)
                                                s = cin()
                                                if s is None: return(0)
                                        else:
                                                au_count = 3000 if m3u_flag else 10
                                        if big_audio_flag:
                                                autitle = cin()
                                                if autitle is None: return(0)
                                                autitle = autitle.strip()
                                        s = s.strip().lower()
                                        audio_list = []
                                        audioget = s=='id' 
                                        if not s:
                                                audioget = True
                                                t = idscache[token_num]
                                        elif audioget: t = mn(autitle)
                                        if audioget: big_audio_flag = False
                                        if audioget: audio_list = get_long_list('audio.get', {'owner_id': t}, au_count, AU_OFFSET_CONSTANT)
                                        elif big_audio_flag:
                                                if autitle=='': audio_list = get_long_list('audio.search', {'q': s, 'performer_only': 1}, au_count, AU_OFFSET_CONSTANT)
                                                else: audio_list = get_long_list('audio.search', {'q': s+' '+autitle}, au_count, AU_OFFSET_CONSTANT)
                                        else: audio_list = get_long_list('audio.search', {'q': s}, au_count, AU_OFFSET_CONSTANT)
                                        print()
                                        def au_adress(audio): return 'audio' + str(audio.get('owner_id')) + '_' + str(audio.get('id'))
                                        def au(audio): return audio.get('artist') + ' - ' + audio.get('title')
                                        if wget_flag:
                                                wget_filename = 'auwget.bat'
                                                with open(wget_filename, 'w', encoding='utf-8') as wget_file:
                                                        if not s: s = '~'
                                                        if wget_start_num is None: aunum = ''
                                                        else: wget_start_num -= len(audio_list)
                                                        wget_file.write('chcp 65001\nmkdir '+s+'\n')
                                                        for audio in audio_list:
                                                                url = audio.get('url')
                                                                aufname = re.sub('"(.*?)"', r'«\1»', au(audio)) # "" to «»
                                                                aufname = re.sub(r'[\\/:*?<>|+\n]','-',aufname) # replace bad characters with -
                                                                if wget_start_num is not None:
                                                                        wget_start_num += 1
                                                                        aunum = str(wget_start_num)+'_'
                                                                if url!='': wget_file.write('wget -nc '+url[:url.find('?extra')]+' -O "' + s+'\\'+aunum+aufname + '.mp3"\n')
                                                        wget_file.write('Del %0 /q\n')
                                                os.system(wget_filename)
                                        if m3u_flag:
                                                m3uname = str(token_num) if audioget and not s else 'm3u'
                                                with open(m3uname+'.m3u', 'w', encoding='utf-8') as m3u_file:
                                                        m3u_file.write('#EXTM3U\n')
                                                        for audio in audio_list:
                                                                if (not big_audio_flag) or ((audio.get('artist').lower()==s.lower())and((audio.get('title').lower()==autitle.lower())or(autitle==''))):
                                                                        url = audio.get('url')                
                                                                        m3u_file.write('#EXTINF:'+str(audio.get('duration'))+', '+au(audio)+'\n#'+au_adress(audio)+'\n'+url[:url.find('?extra')]+'\n')
                                        else:
                                                for audio in audio_list:
                                                        if (not big_audio_flag) or ((audio.get('artist').lower()==s.lower())and((audio.get('title').lower()==autitle.lower())or(autitle==''))):
                                                                url = audio.get('url')
                                                                if not big_audio_flag or (autitle==''): print(au(audio))
                                                                print(url[:url.find('?extra')], au_adress(audio))
                                        return(0)
                                elif r("u"):
                                        s = cin()
                                        if s is None: return(0)
                                        if r("?"):
                                                print(help("u"))
                                                s = cin()
                                                if s is None: return(0)
                                        if r("+"):
                                                fields = cin()
                                                if fields is None: return(0)
                                                s = cin()
                                                if s is None: return(0)
                                        else: fields = ''
                                        vktrim = s.find('vk.com')
                                        if vktrim+1: s = s[vktrim+7:]
                                        suserid = ','.join([str(mn(x)) for x in s.split(',')])
                                        if 'None' in suserid: suserid = l(s)
                                        print(suserid)
                                        info = call_api('users.get', {'user_ids': suserid, 'fields': fields})
                                        if info:
                                                for user in info:
                                                        deactif = user.get('deactivated')
                                                        if deactif is None: deactif = ''
                                                        fifo = ''
                                                        if not deactif:
                                                                for smth in fields.replace(' ','').split(','):
                                                                        if user.get(smth): fifo += str(user.get(smth))+' '
                                                        print(user.get('first_name'), user.get('last_name'), user.get('id'), deactif+fifo)
                                                if len(info)==1:
                                                        actif = call_api('messages.getLastActivity', {'user_id': info[0].get('id')})
                                                        if actif:
                                                                onstatus = 'online' if actif.get('online') else 'offline'
                                                                print(onstatus, printtime(actif.get('time')))
                                                        print("now it's " + printtime(time.time())+"\nhttps://vk.com/albums"+str(info[0].get('id')))
                                        else:
                                                info = call_api('utils.resolveScreenName', {'screen_name': suserid})
                                                if info:
                                                        utype = info.get('type')
                                                        suserid = (int(utype!='group')*2-1) * info.get('object_id')
                                                        print(utype, suserid)
                                        return(0)
                                elif r("f"):
                                        fs = '\n'+s
                                        s = cin()
                                        if s is None: return(0)
                                        if r("?"):
                                                print(help("f"))
                                                return(0)
                                        friend_id_list = None
                                        if s=='': friend_id_list = call_api('friends.getRecent', {'count': 1000})
                                        elif r("<") or r(","): friend_id_list = call_api('friends.getRequests', {'count': 1000, 'out': 1})
                                        elif r(">") or r("."): friend_id_list = call_api('friends.getRequests', {'count': 1000, 'out': 0})
                                        elif r("f"):
                                                s = cin()
                                                if s is None: return(0)
                                                t = mn(s)
                                                friend_id_list = call_api('groups.getMembers', {'group_id': -t, 'count': 1000, 'sort': 'time_desc'}) if t<0 else call_api('friends.get', {'user_id': t, 'count': 1000})
                                        if friend_id_list is not None:
                                                print_id_list(friend_id_list)
                                                return(0)
                                        else:
                                                suserid = mn(s)
                                                if suserid is None: m = fs
                                                else:
                                                        print(call_api('groups.join', {'group_id': -suserid}) if suserid<0 else call_api('friends.add', {'user_id': suserid})) #domain unavailable
                                                        return(0)
                                elif r("b"): #makes you online!
                                        wall_flag = True
                                        userid = 0
                                        s = cin()
                                        if s is None: return(0)
                                        if r("?"):
                                                print(help("b"))
                                                return(0)
                                elif r("r"): return(reset())
                                elif r("."):
                                        api_call = call_api('messages.getDialogs', {'unread': '1'})
                                        if api_call: resmes = api_call.get('items')
                                        else: return(0)
                                        if (resmes == []): print('-')
                                        else:
                                                for mes in resmes:
                                                        rm = mes.get('message')
                                                        print(rm.get('user_id'), mes.get('unread'), '#'+charfilter(rm.get('body')))
                                        return(0)
                                elif r("i"):
                                        print(ignore)
                                        if not hide: print(help("i")[0])
                                        s = cin()
                                        if s is None: return(0)
                                        s = l(s.strip())
                                        if s=='': return(0)
                                        iuid = mn(s)
                                        if iuid in ignore:
                                                ignore.remove(iuid)
                                                if not hide: print(help("i")[1])
                                        else:
                                                ignore.append(iuid)
                                                if os.path.exists(ignorefile):
                                                        with open(ignorefile, 'a') as f: f.write('\n'+s)
                                                else:
                                                        print(help("i")[2])
                                                        with open(ignorefile, 'w') as f: f.write('\n'+s)
                                        return(0)
                                elif r("m"):
                                        print(mnemonics)
                                        if not hide: print(help("m")[0])
                                        s = cin()
                                        if s is None: return(0)
                                        if r("?"):
                                                print(help("m")[1])
                                                s = cin()
                                                if s is None: return(0)
                                        s = s.strip()
                                        if s=='': return(0)
                                        muserids = cin()
                                        if muserids is None: return(0)
                                        try: muserid = int(muserids)
                                        except: return(0)
                                        muserids = str(muserid)
                                        mnemonics[s] = muserid
                                        if os.path.exists(mnemofile):
                                                with open(mnemofile, 'a') as f: f.write('\n'+s+' '+muserids)
                                        else:
                                                print(help("m")[2])
                                                with open(mnemofile, 'w') as f: f.write('\n'+s+' '+muserids)
                                        return(0)
                                elif r("h"):
                                        if not hide: print(help("h")[0])
                                        huid = cin()
                                        if huid is None: return(0)
                                        if l(huid)=="?":
                                                print(help("h")[1])
                                                return(0)
                                        huid = mn(huid)
                                        getHistory(INFINITY, True, huid)
                                        with open('history_' + str(idscache[token_num]) + '_to_' + name_from_id(huid) + '.txt', 'w', encoding='utf-8') as f: f.write(printm)
                                        printm=''
                                        print()
                                        return(0)
                                elif r("-"):
                                        s = cin()
                                        if s is None: return(0)
                                        if r("?"):
                                                print(help("-")[0])
                                                return(0)
                                        dwall = '_' in s
                                        if dwall:
                                                wcrop = s.find('wall')
                                                if wcrop+1: s = s[wcrop+4:]
                                                print(s)
                                                wowner, wid = s.split('_')
                                                wall = call_api('wall.getById',{'posts':s})
                                                if not wall:
                                                        print(help("-")[1])
                                                        print(call_api('wall.restore', {'owner_id': wowner, 'post_id': wid}))
                                                        return(0)
                                                post = wall[0]
                                                printsn('\n'+charfilter(post.get('text')))              
                                                print_attachments(post.get('attachments', []))
                                        else:
                                                s = re.sub('\[(.*?)\]', r'\1', s)
                                                api_call = call_api('messages.getById', {'message_ids': s})
                                                if api_call: delete_list = api_call.get('items')
                                                else: return(0)
                                                printm = ''
                                                for mes in delete_list:
                                                        deleted = bool(mes.get('deleted'))
                                                        printsn('<>'[int(mes.get('out')==0)]+'[is now restored]'*int(deleted)+' ' + name_from_id(mes.get('user_id')))
                                                        if deleted: call_api('messages.restore', {'message_id': mes.get('id')})
                                                        print_message('', mes, 0)                                        
                                        printms()
                                        print(help("-")[2])
                                        delete_confirmation = cin()
                                        if delete_confirmation is None: return(0)
                                        if l(delete_confirmation)=='y':
                                                print(call_api('wall.delete', {'owner_id': wowner, 'post_id': wid}) if dwall else call_api('messages.delete', {'message_ids': s}))
                                                return(0)
                                        elif dwall:
                                                print(help("-")[3])
                                                s = ''
                                                wall_edit_flag = True
                                        else: return(0)
                                        continue
                                elif r("z"):
                                        s = cin()
                                        if s is None: return(0)
                                        print(l(s))
                                        return(0)
                                elif r("y"):
                                        site = 'https://yandex.ru/internet'
                                        r = requests.get(site)
                                        r.encoding = 'UTF-8'
                                        x = r.text
                                        p = x.find('<strong>')
                                        inf = x[p:x.find('</span>', x.find('info__value_type_pinpoint-region', p))+1]
                                        print(''.join(re.split('<[\/\!]*?[^<>]*?>', inf))[:-1])
                                        return(0)
                                elif r("g"):
                                        s = cin()
                                        if s is None: return(0)
                                        gooreq = requests.get("https://www.google.com/search?q="+s)
                                        goolist = [x[x.find('?q=')+3:x.find('&amp')]+'\n'+x[x.find('_blank">')+8:x.rfind('</a>')]+'\n' for x in re.findall('"r".*?h3', gooreq.text)]
                                        for link in goolist: print(link.replace('%25', '%'))
                                        return(0)
                                elif r("q"):
                                        saveinstance()
                                        return(-3)
                sharp = s.find('#')
                Nsign = s.find('№')
                if (Nsign>=0)and((Nsign<sharp)or(sharp<0)): sharp = Nsign
                alls = s
                if userid is None:
                        userstr = s[:sharp]
                        s = s[sharp+1:]
                        userid = mn(userstr)
                if not userid:
                        userid = prevuserid
                        s = alls
                m+='\n'+s
                if m=='\n':
                        break
        prevuserid = userid
        saveinstance()
        m=m[:-1]
        if wall_edit_flag:
                print(call_api('wall.edit', {'owner_id': wowner, 'post_id': wid, 'message': m, 'attachments': attachments}))
                return(0)
        if wall_flag:
                print(call_api('wall.post', {'message': m, 'attachments': attachments}))
                return(0)
        if userid is None: return(0)
        if (m==''): return(0)
        if userid<0:
                print(call_api('wall.post', {'owner_id': userid, 'from_group': 1, 'message': m, 'attachments': attachments}))
                return(0)
        if (m=='\n')and not attachments and not forward_messages:
                call_api('messages.markAsRead', {'peer_id': userid})
                getHistory(10, False, userid)
                printms() #return(-1)
        elif (l(m)=='#'):
                getHistory(200, False, userid)
                printms()
        else:
                resh = re.match('\n[#|№]+', m)
                if resh:
                        getHistory((resh.endpos-2)*200, True, userid)
                        printms()
                else:
                        out_flag = l(m[-1])=='#'
                        if out_flag: m=m[:-1]
                        print(len(m))
                        if len(m)>TOO_LONG_CONSTANT:
                                s =  ask_confirmation("toolong")
                                if s!=-1 and s is not None: userid = idscache[token_num]
                        getHistory(10, False, userid)
                        if not printm:
                                s = ask_confirmation("mixup")
                                if s!=-1:
                                        if s.isdigit():
                                                token_num = int(s)
                                                saveinstance()
                                        else: return(0)
                        while len(m)>4096:
                                lastn = m[:4096].rfind('\n')
                                if lastn==-1: lastn=4095
                                call_api('messages.send', {'peer_id': userid, 'message': m[:lastn], 'attachment': attachments, 'forward_messages': forward_messages, 'title': subject})
                                m = m[lastn:]
                        call_api('messages.send', {'peer_id': userid, 'message': m, 'attachment': attachments, 'forward_messages': forward_messages, 'title': subject})
                        print(printm+int(subject is not None)*('\n['+str(subject)+']')+m+'\n'*(len(attachments)>1)+attachments[1:]+'\n'*(len(forward_messages)>1)+forward_messages[1:]+'\n'+printtime(time.time()))
                        printm = ''
                        if out_flag: return(-1)
        return(0)
def check_inbox():
        A=0
        global token_num, printm
        index = 0
        prev_token_num = token_num
        for token_num in range(len(token_list)):
                myname = name_from_id(idscache[token_num])
                viewed_time = lastNviewcache[token_num]# - 3600
                notif_resp, resp = None, None
                tn = token_num<<1
                if (prob[tn+1]==0 and prob[tn]==0): continue
                if random.random() < prob[tn+1]: notif_resp = call_api('notifications.get',{'start_time': viewed_time})
                if random.random() < prob[tn]: resp = call_api('messages.getDialogs', {'unread': '1'})
                if notif_resp:
                        r = notif_resp.get('count')
                        nitems = reversed(notif_resp.get('items'))
                else:
                        r = 0
                        nitems = []
                if resp:
                        t = resp.get('count')
                        items = resp.get('items')
                else:
                        t = 0
                        items = []
                a=r+t
                A+=a
                printsn(myname + ' - ' + str(t) + ' new dialogues' + ' - ' + str(r) + ' new responses')
                if r<0: A-=r
                if not looping:
                        if a: printms()
                        else: printm='' #print()
                for x in items:
                        N = x.get('unread')
                        mes = x.get('message')
                        chat_id = mes.get('chat_id')
                        chat = chat_id is not None
                        uid = 2000000000 + chat_id if chat else mes.get('user_id') #check dialogue is not a chat
                        if uid in ignore:
                                A-=1
                                t-=1
                                if chat: call_api('messages.markAsRead', {'peer_id': 2000000000+chat_id}) #autoread
                                continue
                        respname = getcached(uid)
                        if respname: printsn('\n'+respname.get('first_name')+' '+respname.get('last_name')+' '+str(uid)+' '+str(N)+' messages')
                        getHistory(N, False, uid)
                        if not looping: printms()
                for x in nitems:
                        xparent, xtype, xdate, xfeedback = x.get('parent'), x.get('type'), x.get('date'), x.get('feedback') #xreply for ur own replies on that
                        printsn('***\n'+xtype)
                        if xparent:
                                xparenttext = xparent.get('text')
                                prextype = xtype[xtype.rfind('_')+1:]
                                if 'comment' in prextype: prextype='post'
                                if 'reply_comment' in xtype or 'like_comment' in xtype:
                                        comment_id = '?reply='+str(xparent.get('id'))
                                        xparent = xparent.get(prextype)
                                else: comment_id=''
                                xowner = xparent.get('to_id')
                                if xowner is None: xowner = xparent.get('owner_id')
                                printsn(prextype.replace('post','wall')+str(xowner)+'_'+str(xparent.get('id'))+comment_id)
                                if xparenttext: printsn(charfilter(xparenttext[:140])+'<..>'*int(len(xparenttext)>140)+'\n')
                        if xfeedback:
                                xfeedlist = xfeedback.get('items')
                                if not xfeedlist: xfeedlist = [xfeedback]
                                for xid in xfeedlist: printsn(name_from_id(xid.get('from_id')))
                                xfeedbacktext = xfeedback.get('text')
                                if xfeedbacktext: printsn('»»\n' + charfilter(xfeedbacktext))
                                print_attachments(xfeedback.get('attachments',[]))
                        printsn(printtime(xdate))
                        if not looping: printms()
        token_num = prev_token_num
        return(A) #messages + notifies of all tokens
def main():
        global printm, waitTime, looping, lastNviewcache
        start(), read_mnemonics(), read_ignore(), read_header(), getcache()
        parser = argparse.ArgumentParser()
        parser.add_argument('-L', action='store_true', required=False, help='waiting mode')
        args = parser.parse_args()
        glooping = vars(args).get('L')
        mes = -int(glooping)
        while True:
                if mes<0:
                        if mes==-2: check_inbox()
                        elif mes==-1:
                                looping = True
                                while (check_inbox()==0):
                                        print('-', end='')
                                        if check_delayed():
                                                print()
                                                messaging()
                                        try:
                                                for timer in range(waitTime):
                                                        time.sleep(1)
                                        except KeyboardInterrupt:
                                                printm=''
                                                break
                                        printm=''
                                else:
                                        showprintm()
                                        printms()
                                        if glooping: lastNviewcache = [int(time.time())] * len(token_list)
                                looping = False
                        elif mes==-3: return
                if not glooping: mes=messaging()
__doc__ == helpinfo["?"][0]
if __name__ == '__main__': main()
