# -*- coding: utf-8
import requests, time, datetime, ast, os, re, random, bisect, argparse
from tkinter import *
sleepTime, waitTime = 0.34, 53
INFINITY, AU_OFFSET_CONSTANT, HI_OFFSET_CONSTANT, W_OFFSET_CONSTANT, L_OFFSET_CONSTANT, LF_OFFSET_CONSTANT, mnemofile, ignorefile, tokenfile, raspyafile, cachefile, headerfile, delayfile, looping, photosizes, printm, width, height, mnemonics, ignore, header, idscache, uidscache, lastNviewcache, prob, token_num, block, delayed, full_auth_line = 10000000, 300, 200, 100, 1000, 100, 'mnemo.txt', 'ignore.txt', 'tokens.txt', 'rasp.ya.txt', 'cache.txt', 'header.txt', 'delay.txt', False, [2560, 1280, 807, 604, 512, 352, 256, 130, 128, 100, 75, 64], '', 0, 0, {}, [], {}, [], {}, [], [], 0, [], [], 'https://oauth.vk.com/authorize?client_id=5015702&scope=notify,friends,photos,audio,video,docs,notes,pages,status,offers,questions,wall,groups,messages,notifications,stats,ads,offline&redirect_uri=https://oauth.vk.com/blank.html&display=page&response_type=token'
simple_smileys={128522: ':-)', 128515: ':-D', 128521: ';-)', 128518: 'xD', 128540: ';-P', 128523: ':-p', 128525: '8-)', 128526: 'B-)', 128530: ':-(', 128527: ';-]', 128532: '3(', 128546: ":'(", 128557: ':_(', 128553: ':((', 128552: ':o', 128528: ':|',128524: '3-)', 128519: 'O:)', 128560: ';o', 128562: '8o', 128563: '8|', 128567: ':X', 10084: '<3', 128538: ':-*', 128544: '>(', 128545: '>((', 9786: ':-]', 128520: '}:)', 128077: ':like:', 128078: ':dislike:', 9757: ':up:', 9996: ':v:', 128076: ':ok:'}
rev_simple_smileys={':-)': 'D83DDE0A.png', ':-D': 'D83DDE03.png', ';-)': 'D83DDE09.png', 'xD': 'D83DDE06.png', ';-P': 'D83DDE1C.png', ':-p': 'D83DDE0B.png', '8-)': 'D83DDE0D.png', 'B-)': 'D83DDE0E.png', ':-(': 'D83DDE12.png', ';-]': 'D83DDE0F.png', '3(': 'D83DDE14.png', ":'(": 'D83DDE22.png', ':_(': 'D83DDE2D.png', ':((': 'D83DDE29.png', ':o': 'D83DDE28.png', ':|': 'D83DDE10.png', '3-)': 'D83DDE0C.png', 'O:)': 'D83DDE07.png', ';o': 'D83DDE30.png', '8o': 'D83DDE32.png', '8|': 'D83DDE33.png', ':X': 'D83DDE37.png', '<3': '2764.png', ':-*': 'D83DDE1A.png', '>(': 'D83DDE20.png', '>((': 'D83DDE21.png', ':-]': '263A.png', '}:)': 'D83DDE08.png', ':like:': 'D83DDC4D.png', ':dislike:': 'D83DDC4E.png', ':up:': '261D.png', ':v:': '270C.png', ':ok:': 'D83DDC4C.png'}
smiley = re.compile('|'.join([re.escape(sm) for sm in rev_simple_smileys])+r'|\d+') #warning: all numbers are smileys!
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
                        if delaystr: print(delaystr+'\nWILL BE REMOVED FROM DELAY FILE!')
                        delayed = []
        if os.path.isdir('smileys'): smileys = os.listdir('smileys')
def call_api(method, params):
        #print(method, params, token_num)
        #time.sleep(sleepTime)
        print('.', end='') if not looping else print(',', end='')
        if method[:7]=='http://':
                q = method.find('?')
                url = method[:q]
                files = {'photo': ('file.png', open(params, 'rb'))}
                params = {} #dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(method[q+1:]).query))
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
                        try: result = requests.post(url, data=params, files=files)
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
                cache_file.write(str(idscache)+'\n')
                cache_file.write(str(lastNviewcache)+'\n')
                cache_file.write(str(prob)+'\n')
                cache_file.write(str(token_num)+'\n')
                cache_file.write(str(prevuserid)+'\n')
                cache_file.write(str(uidscache)+'\n')
def reset():
        global token_num, idscache, uidscache, lastNviewcache, prob, prevuserid, token_list
        idscache, uidscache, lastNviewcache, prob = [], {}, [], []
        if not token_list:
                print(full_auth_line+'\n\n\nauthorisation token needed\nplease insert that in your browser and do what it interdicts\ni strongly promiss not to steal your profile\nactually, i cannot :(\n')
                s = cin()
                if s is None:
                        print("c'mon, i AM really a good guy")
                        s = cin()
                        if s is None:
                                raise PermissionError ('Lack of trust error')
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
                prob=prob+[1, 1]
        token_num = 0
        prevuserid = idscache[token_num]
        saveinstance()
        print()
        return 0
def getcache():
        global token_num, idscache, lastNviewcache, prob, prevuserid, uidscache
        with open(cachefile, 'r', encoding='utf-8') as cache_file:
                try:
                        i, l, p, t, r, u = cache_file.readlines()
                        idscache, lastNviewcache, prob, token_num, prevuserid, uidscache = ast.literal_eval(i), ast.literal_eval(l), ast.literal_eval(p), int(t), ast.literal_eval(r), ast.literal_eval(u)
                except: reset()
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
        with open(headerfile, 'r') as header_file:
                for line in header_file.readlines():
                        colon = line.find(':')
                        header[line[:colon].strip()] = line[colon+1:].strip()
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
        wrong = wrong.lower().strip() 
        right = ''  #re.match("^[' 'A-Za-z0-9_-]*$", wrong)
        for wrong_letter in wrong:
                right_letter = wrong_letter if ord(wrong_letter)<128 else 'qwertyuiop[]asdfghjkl;\'zxcvbnm,.#_'['йцукенгшщзхъфывапролджэячсмитьбю№_'.find(wrong_letter)]
                right = right + right_letter
        return right
def mn(idstring):
        idstring = l(idstring)
        if idstring in mnemonics: return mnemonics[idstring]
        else:
                try: return int(idstring)
                except: return #api_call = call_api('users.get', {'user_ids': idstring}) #if api_call: return str(api_call[0].get('id')) #else: return '0'
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
        #print('{'+printm+'}')
        print(printm)
        printm = ''
def printsn(s):
        global printm
        printm += '\n'+s #print(s)
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
                elif atype=='video': adress = adress + '_' + str(stuff.get('access_key', '')) #call_api('video.get', {'videos': req})# api_call.get('items')[0].get('player'))
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
                printsn('     '*k + '[fwd_messages:]')
                for fwdm in fwd: print_message('     '*(k+1) + '['+name_from_id(fwdm.get('user_id'))+']', fwdm, k+1)
def getHistory(count, print_numbers, uid):
        if not isinstance(uid, int): uid = mn(uid)
        chat = uid>=2000000000
        unread = False
        history = get_long_list('messages.getHistory', {'peer_id': uid}, count, HI_OFFSET_CONSTANT)
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
        print()
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
def messaging():
        global token_num, printm, waitTime, prevuserid, block
        iam()
        m, s, attachments, forward_messages, userid, wall_flag, wall_edit_flag, subject, delay_time = '', '', '', '', None, False, False, None, None
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
                                        repeated = r("<")
                                        nowstamp = datetime.datetime.fromtimestamp(time.time())
                                        s = cin()
                                        if s is None: return(0)
                                        if r("?"):
                                                print('input a period of time in seconds (can be float)' if repeated else nowstamp.strftime('input time in format 18:00:00 %d.%m.%Y'))
                                                return(0)
                                        if repeated:
                                                delay_period = float(s)
                                                delay_time = time.time()+delay_period
                                        else: delay_time = time.mktime(datetime.datetime.strptime(s, "%H:%M:%S %d.%m.%Y").timetuple())
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
                                                print("command1\ncommand2\n...\n}")
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
                                                s = cin() #try: s = input()
                                                if s is None: #except KeyboardInterrupt:
                                                        temp_block = []
                                                        break
                                        block.extend(temp_block)
                                        if delay_time is not None: add_delayed(delay_time)
                                        return(0)
                                elif r("?"):
                                        print("all the commands are layout-insensitive and almost all are case-insensitive\n' - wait mode\n+ - attach (? for help)\n~ or ` - waittime for wait mode\nn - mark notifications as read\no - open a file from a direct link (see help there using ?-command)\np - set probabilities of checking (2N numbers in columnar form)\ne - rasp.ya.ru from the file with informer-links\nw - see wall or wall post\n: - any site in Internet in raw\ns - see smiley image from its number or :-] - form\nt - input raw api call\nl - likes\nv - find a video; V - find an hd-video\na - find an audio; A - find an audio of exact author, title or id. ? for help\nd - find a doc (? for help)\nx - raw link to photo/audio(linked to IP)/video/doc\nu - user/group info\nf - friend someone/join a group/see friends of\nb - posts to your wall - warning: makes you online!\nr - reset cache\n. - quick check\ni - see ignore list and add something to it\nm - see mnemolist and add something to it\nh - saving history to file\n- - delete messages or a wall post (or edit, or restore) (? for help)\nz - latinize the layout\ny - user IP and location\ng - google something\n> - delayed execution of a block of commands\n< - repeated execution\n{ - start a block of commands; (? for help) } - end the block\n? - this help info\nq - quit")
                                        return(0)
                                elif r("'"): return(-1)
                                elif r("+"):
                                        s = cin()
                                        if s is None: return(0)
                                        if r("?"):
                                                print('forward messages ids (e.g. 1232,1233,1237) |\nattachments (e.g. photo123123_123223,audio-34232_23123) |\ns Subject of the message |\nu - upload photo to a message (input file adress or nothing for Безымянный.png) |\nw - upload photo to a wallpost (same here)')
                                                return(0)
                                        if r("u"): uploades = ['photos.getMessagesUploadServer', 'photos.saveMessagesPhoto']
                                        elif r("w"): uploades = ['photos.getWallUploadServer', 'photos.saveWallPhoto']
                                        else: uploades = None
                                        if uploades:
                                                s = cin()
                                                if s is None: return(0)
                                                if s.strip()=='': s='Безымянный.png'
                                                upload_url = call_api(uploades[0], {})
                                                if upload_url: upload_stuff = call_api(upload_url.get('upload_url'), s)
                                                else: return(0)
                                                if upload_stuff: uploaded_photo = call_api(uploades[1], upload_stuff)      
                                                else: return(0)
                                                if uploaded_photo: s = 'photo'+str(uploaded_photo[0].get('owner_id'))+'_'+str(uploaded_photo[0].get('id'))
                                                print('\n'+s)
                                        if s[0].isdigit(): forward_messages += ','+s
                                        elif l(s[0])=='s': subject = s[2:] #s_The subject of my message
                                        else: attachments += ','+s
                                        continue
                                if r("~") or r("`"):
                                        s = cin()
                                        if s is None: return(0)
                                        try: waitTime = int(s)
                                        except: return(0)
                                        return(0)
                                elif r("n"):
                                        call_api('notifications.markAsViewed', {})
                                        lastNviewcache[token_num] = int(time.time())
                                        saveinstance()
                                        print()
                                        return(0)
                                elif r("p"):
                                        print('Set probabilities of message check and notifies check fot every token_nums while checkbox')
                                        global prob
                                        print(prob)
                                        try: prob = [float(input()) for i in range(2*len(token_list))]
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
                                        wall_owner = mn(s)
                                        if wall_owner is None:
                                                findwall = s.find('wall')
                                                if findwall+1: s = s[findwall:]
                                                s = s.replace('wall','')
                                                wall = call_api('wall.getById',{'posts':s})
                                                if wall is None: return(0)
                                        else:
                                                print('Now you have to input the number of posts')
                                                s = cin()
                                                if s is None: return(0)
                                                try: postsN = int(s)
                                                except: return(0)
                                                api_call = call_api('wall.get', {'owner_id': wall_owner, 'count': postsN})
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
                                                printsn('\nSUGGEST\n____' if post.get('post_type')=='suggest' else '\n'+str(post.get('likes').get('count'))+' likes, '+str(post.get('comments').get('count'))+' comments\n____')
                                        if len(wall)==1:
                                                printsn('COMMENTS:')
                                                wallcomments = get_long_list('wall.getComments', {'owner_id': wowner, 'post_id': wid, 'need_likes': 1},INFINITY,W_OFFSET_CONSTANT)
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
                                        s = cin()
                                        if s is None: return(0)
                                        if r("?"):
                                                print("'api_method', {'param1': 'value1', 'param2': 'value2', ...}")
                                                return(0)
                                        lit = ast.literal_eval(s)
                                        g = call_api(*lit)
                                        print(charfilter(str(g)))
                                        return(0)
                                elif r("l"):
                                        print('syntax: type owner_id (e.g. audio 26522309_422813886 or post -69528510_158)\ntypes: post, comment, photo, audio, video, note, photo_comment, video_comment, topic_comment, sitepage')
                                        s = cin()
                                        if s is None: return(0)
                                        lobjecttype, what = s.split()
                                        lowner, lid = what.split('_') #ifLiked - likes.delete
                                        print("now type\n+ to like\n- to unlike\n? to get to know whether you or someone has already liked that\nc - to get the list of who reposted\nf - to get the list of friends who liked\ncf or fc - friends who reposted\nand anything else (e.g. empty string) to get the full list of who liked that")
                                        s = cin()
                                        if s is None: return(0)
                                        like_list = None
                                        if r("+"): print(call_api('likes.add', {'type': lobjecttype, 'owner_id': lowner, 'item_id': lid}))
                                        elif r("-"): print(call_api('likes.delete', {'type': lobjecttype, 'owner_id': lowner, 'item_id': lid}))
                                        elif r("?"):
                                                print('Whos likes interest you? As always, youself is an empty string, just press Enter.')
                                                s = cin()
                                                if s is None: return(0)
                                                luserid = mn(s)
                                                print(call_api('likes.isLiked', {'user_id': luserid, 'type': lobjecttype, 'owner_id': lowner, 'item_id': lid}))
                                        elif r("c"): like_list = get_long_list('likes.getList', {'filter': 'copies', 'type': lobjecttype, 'owner_id': lowner, 'item_id': lid}, INFINITY, L_OFFSET_CONSTANT)
                                        elif r("f"): like_list = get_long_list('likes.getList', {'friends_only': 1, 'type': lobjecttype, 'owner_id': lowner, 'item_id': lid}, INFINITY, LF_OFFSET_CONSTANT)
                                        elif r("cf") or r("fc"): like_list = get_long_list('likes.getList', {'filter': 'copies', 'friends_only': 1, 'type': lobjecttype, 'owner_id': lowner, 'item_id': lid}, INFINITY, LF_OFFSET_CONSTANT)
                                        else: like_list = get_long_list('likes.getList', {'type': lobjecttype, 'owner_id': lowner, 'item_id': lid}, INFINITY, L_OFFSET_CONSTANT)
                                        if like_list is not None: print_id_list(like_list)
                                        return(0)
                                elif r("d"):
                                        s = cin()
                                        if s is None: return(0)
                                        dtype = None
                                        if r("?"):
                                                print("[T\ntype]\nsearch string")
                                                return(0)
                                        elif r("t"):
                                                s = cin()
                                                if s is None: return(0)
                                                dtype = s.lower()
                                                s = cin()
                                                if s is None: return(0)
                                        docdata = {'act': 'search_docs', 'al': '1', 'offset': '0', 'oid': idscache[token_num], 'q': s}
                                        if not header:
                                                print("Please open your browser, open vk.com/docs, Ctrl+Shift+J, click Network tab, search something in docs search field, choose a request for docs.php, copy all Request Headers (it's Accept:*/*, Accept-Encoding:gzip, deflate, etc.), and paste here.")
                                                h = ''
                                                for i in range(12):
                                                        s = cin()
                                                        if s is None: return(0)
                                                        h += s+'\n'
                                                with open(headerfile, 'w') as header_file: header_file.write(h)
                                                read_header()
                                        r = requests.request(method="POST", url="https://vk.com/docs.php", headers=header, data=docdata) #docheader["Referer"] = "https://vk.com/docs"
                                        v = r.text[r.text.find('[['):r.text.rfind(']]')+2]
                                        if not v:
                                                print('Something gone wrong, try update headers')
                                                return(0)
                                        lit = ast.literal_eval(v)
                                        if dtype: lit = [doc for doc in lit if doc[1]==dtype]
                                        for doc in lit: print(doc[2], 'doc'+str(doc[4])+'_'+str(doc[0])) #doc[3] - size and date
                                        return(0)
                                elif r("o"):
                                        s = cin()
                                        if s is None: return(0)
                                        if r("?"):
                                                print('[wget - to download using wget] opens a file from a direct link. Or opens tokenfile, mnemofile, ignorefile, raspyafile - using T,M,I,R commands')
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
                                                ofname = 'file'+s[s.rfind('.'):]
                                                if owget:
                                                        wget_filename = 'opwget.bat'
                                                        with open(wget_filename, 'w', encoding='utf-8') as wget_file: wget_file.write('chcp 65001\nwget -nc ' + s + ' -O "' + ofname + '"\nDel %0 /q\n')
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
                                        s = cin() #get the video from a "player"-link or "player"-link from video id
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
                                                                if v.get('is_private'): print('ADULT_CONTENT')
                                                                s = v.get('player')
                                                                print(s)
                                        else:
                                                print("photo123123_123123 or audio1231231_12213 or video2123_123123 or http://vk.com/video_ext.php?oid=...")
                                                return(0)
                                        if 'video_ext' not in s: return(0)
                                        x = requests.get('https://vk.com/'+s).text
                                        if 'Видеозапись была помечена модераторами сайта как «Материал для взрослых». Такие видеозаписи запрещено встраивать на внешние сайты.' in x:
                                                print('Adult content error')
                                                return(0)
                                        xd = x.find('video_max_hd = ')
                                        try: video_max_hd = int(x[xd+16:xd+17])
                                        except: video_max_hd = 0
                                        hds = ['240', '360', '480', '720', '1080']
                                        video_url = x[x.find('url'+hds[video_max_hd])+7:]
                                        video_url = video_url[:video_url.find('&amp;')]
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
                                        s = cin()
                                        if s is None: return(0)
                                        if r("?"):
                                                print('[HERE]\n[WGET][start num]\n[Number]\n[Author | ID]\n[Title | id/mnemonic]') if big_audio_flag else print('[HERE]\n[wget][start num]\n[Number]\n[Search string]')
                                                return(0)
                                        if r("here"):
                                                m3u_flag = False
                                                s = cin()
                                                if s is None: return(0)
                                        if l(s[:4])=='wget':
                                                wget_flag = True
                                                try: wget_start_num = int(s[4:])
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
                                        suserid = mn(s)
                                        if not suserid: suserid = l(s)
                                        info = call_api('users.get', {'user_ids': suserid})
                                        if info:
                                                for user in info:
                                                        deactif = user.get('deactivated')
                                                        if deactif is None: deactif = ''
                                                        print(user.get('first_name'),user.get('last_name'),user.get('id'),deactif)
                                                if len(info)==1:
                                                        actif = call_api('messages.getLastActivity', {'user_id': info[0].get('id')})
                                                        if actif:
                                                                onstatus = 'online' if actif.get('online') else 'offline'
                                                                print(onstatus, printtime(actif.get('time')))
                                        else:
                                                info = call_api('utils.resolveScreenName', {'screen_name': suserid})
                                                if info: print(info.get('type'), info.get('object_id'))
                                        print("now it's " + printtime(time.time())+"\nhttps://vk.com/albums"+str(suserid))
                                        return(0)
                                elif r("f"):
                                        s = cin()
                                        if s is None: return(0)
                                        if r("?"):
                                                print("Enter empty line for getting your friends list\n> - for list of your subscribers\n< - list of whom you are a subscriber of\nF - enter - userid or a mnemonic to get someone's friends of members of a group")
                                                return(0)
                                        friend_id_list = None
                                        if s=='': friend_id_list = call_api('friends.getRecent', {'count': 1000})
                                        elif l(s)=='<' or l(s)==',': friend_id_list = call_api('friends.getRequests', {'count': 1000, 'out': 1})
                                        elif l(s)=='>' or l(s)=='.': friend_id_list = call_api('friends.getRequests', {'count': 1000, 'out': 0})
                                        elif l(s)=='f':
                                                s = cin()
                                                if s is None: return(0)
                                                t = mn(s)
                                                friend_id_list = call_api('groups.getMembers', {'group_id': -t, 'count': 1000, 'sort': 'time_desc'}) if t<0 else call_api('friends.get', {'user_id': t, 'count': 1000})
                                        if friend_id_list is not None: print_id_list(friend_id_list)
                                        else:
                                                suserid = mn(s)
                                                print(call_api('groups.join', {'group_id': -suserid}) if suserid<0 else call_api('friends.add', {'user_id': suserid})) #domain unavailable
                                        return(0)
                                elif r("b"): #makes you online!
                                        wall_flag = True
                                        userid = 0
                                        s = cin()
                                        if s is None: return(0)
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
                                        print("Now add something to ignore list or temporarily remove something from it (to cancel - CTRL+C).")
                                        s = cin()
                                        if s is None: return(0)
                                        s = l(s.strip())
                                        if s=='': return(0)
                                        iuid = mn(s)
                                        if iuid in ignore:
                                                ignore.remove(iuid)
                                                print('temporarily seen')
                                        else:
                                                ignore.append(iuid)
                                                if os.path.exists(ignorefile):
                                                        with open(ignorefile, 'a') as f: f.write('\n'+s)
                                                else:
                                                        print('ignore file was deleted!')
                                                        with open(ignorefile, 'w') as f: f.write('\n'+s)
                                        return(0)
                                elif r("m"):
                                        print(mnemonics)
                                        print("Now add something to mnemo list (to cancel - CTRL+C).")
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
                                                print('mnemo file was deleted!')
                                                with open(mnemofile, 'w') as f: f.write('\n'+s+' '+muserids)
                                        return(0)
                                elif r("h"):
                                        print("saving history to file. if you need HELP - type '?'")
                                        huid = cin()
                                        if huid is None: return(0)
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
                                                print("deleting messages (e.g. 5123,5124,5653)\nor a wall post (e.g. [[https://vk.com/]wall]-2424_2123).\ntype anything instead 'Y' for the confirmation request and edit the wall post\ntry to delete non-existing post to make an attempt to restore it")
                                                return(0)
                                        dwall = '_' in s
                                        if dwall:
                                                wcrop = s.find('wall')
                                                if wcrop+1: s = s[wcrop+4:]
                                                print(s)
                                                wowner, wid = s.split('_')
                                                wall = call_api('wall.getById',{'posts':s})
                                                if not wall:
                                                        print('not found, trying to restore')
                                                        print(call_api('wall.restore', {'owner_id': wowner, 'post_id': wid}))
                                                        return(0)
                                                post = wall[0]
                                                printsn('\n'+charfilter(post.get('text')))              
                                                print_attachments(post.get('attachments', []))
                                        else:
                                                api_call = call_api('messages.getById', {'message_ids': s})
                                                if api_call: delete_list = api_call.get('items')
                                                else: return(0)
                                                printm = ''
                                                for mes in delete_list:                                                        
                                                        del_uid = str(mes.get('user_id'))
                                                        printsn('>'+del_uid if (mes.get('out')==0) else '<'+del_uid)
                                                        print_message('', mes, 0)                                        
                                        printms()
                                        print('DELETE THAT?\nY\\N')
                                        delete_confirmation = cin()
                                        if delete_confirmation is None: return(0)
                                        if l(delete_confirmation)=='y':
                                                print(call_api('wall.delete', {'owner_id': wowner, 'post_id': wid}) if dwall else call_api('messages.delete', {'message_ids': s}))
                                                return(0)
                                        elif dwall:
                                                print('Edit post:')
                                                s = ''
                                                wall_edit_flag = True
                                        continue
                                elif r("z"):
                                        s = cin()
                                        if s is None: return(0)
                                        print(l(s))
                                        return(0)
                                elif r("y"):
                                        site = 'https://yandex.ru/internet' #'http://jsonip.com' ip = r.json()['ip']
                                        r = requests.get(site)
                                        r.encoding = 'UTF-8'
                                        x = r.text
                                        p = x.find('Поздравляем') #region = re.findall(r'Регион.*?\<\/li\>', x)
                                        inf = x[p:p+200] #if region is not None: print(region[0][:-12].replace('</div><span class="data__item-content">',' '))
                                        inf = inf.replace('strong','').replace('/', '').replace('<>', '')
                                        print(inf[:inf.find('Браузер')])
                                        return(0)
                                elif r("g"):
                                        s = cin()
                                        if s is None: return(0)
                                        gooreq = requests.get("https://www.google.ru/search?q="+s)#, data={'q':s})
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
                        if len(m)>348:
                                print("C'mon, do I really interested in that? Better ask me how am I.\n[or all is well?]")
                                confirmation = cin()
                                if confirmation is None or l(confirmation)!="all is well":
                                        print("resend it to youself, yeah? hah")
                                        confirmation = cin()
                                        if confirmation is None: return(0)
                                        userid = idscache[token_num]
                        getHistory(10, False, userid)
                        if not printm:
                                print('The history is empty!\nall is well?')
                                confirmation = cin()
                                if confirmation is None or l(confirmation)!="all is well":
                                        print('Input another token_num')
                                        s = cin()
                                        if not s: return(0)
                                        if s.isdigit(): token_num = int(s)
                                        else: return(0)
                        while len(m)>4096:
                                lastn = m[:4096].rfind('\n')
                                if lastn==-1: lastn=4095
                                call_api('messages.send', {'peer_id': userid, 'message': m[:lastn], 'attachment': attachments, 'forward_messages': forward_messages, 'title': subject})
                                m = m[lastn:]
                        call_api('messages.send', {'peer_id': userid, 'message': m, 'attachment': attachments, 'forward_messages': forward_messages, 'title': subject})
                        print(printm+m+'\n'+printtime(time.time()))
                        printm = ''
                        if out_flag: return(-1)
        return(0)
def check_inbox():
        A=0
        global token_num, printm
        index = 0
        prev_token_num = token_num
        for token_num in range(len(token_list)): #if random.random() > prob[token_num]: continue
                myname = name_from_id(idscache[token_num])
                viewed_time = lastNviewcache[token_num]# - 2000000
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
        return(A) #messages+notifies of all tokens
def main():
        global printm, waitTime, looping, lastNviewcache
        start(), read_mnemonics(), read_ignore(), read_header(), getcache()
        parser = argparse.ArgumentParser()
        parser.add_argument('-L', action='store_true', required=False)
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
if __name__ == '__main__': main()
