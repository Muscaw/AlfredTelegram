import argparse
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.contacts import GetContactsRequest
from telethon.tl.functions.messages import GetAllChatsRequest, GetChatsRequest
from telethon.tl.functions.channels import GetChannelsRequest
from telethon.tl.types import InputUser, InputChannel, PeerChannel, PeerUser, PeerChat
from telethon.tl.functions.users import GetUsersRequest
import settings
import time
from getpass import getpass
import errors
import sys
import os
import io
import pickle

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')

ALFRED_MODE = True

BASE_SESSION_NAME="TBC"

class PicklableContact:
    def __init__(self):
        self.id = 0
        self.name = 0
        self.mode = ""

def get_client():
    client = TelegramClient(BASE_SESSION_NAME, settings.API_ID, settings.API_HASH)
    while not client.connect():
        time.sleep(1)
    return client

def login(args):
    client = get_client()
    if not client.is_user_authorized():
        phone = input("Enter your phone number associated with your Telegram account: ")
        client.sign_in(phone)

        current_user = None
        while current_user is None:
            code = input("Enter the code received on Telegram: ")

            try:
                current_user = client.sign_in(code=code)

            except SessionPasswordNeededError:
                pw = getpass("Please enter your telegram password: ")
                current_user = client.sign_in(password=pw)
    else:
        print("User is already connected. Call \"" + sys.argv[0] + " disconnect\"")

def send_message(args):
    client = get_client()
    if not client.is_user_authorized():
        print(str(errors.ERROR_NOT_CONNECTED))
        return
    id = int(args.contact)
    receiver = None
    if args.mode == "user":
        receiver = client.get_entity(PeerUser(id))
    else:
        try:
            receiver = client.get_entity(PeerChannel(id))
        except:
            receiver = client.get_entity(PeerChat(id))

    if receiver is None:
        print(str(errors.ERROR_RECEIVER_NOT_FOUND))
        return



    client.send_message(receiver, ' '.join(args.msg))
    print(0)

def get_contacts(args):
    client = get_client()
    if not client.is_user_authorized():
        print(str(errors.ERROR_NOT_CONNECTED))
        return

    renew = False
    if os.path.exists("contacts") and time.time() - 30 > float(os.path.getmtime("contacts")):
        contacts = pickle.load(open("contacts", "rb"))
    else:
        contacts = []

        users = client.invoke(GetContactsRequest(0)).users
        for u in users:
            c = PicklableContact()
            c.id = u.id
            c.mode = "user"
            d = ""
            if u.first_name is not None:
                d += str(u.first_name) + " "
            if u.last_name is not None:
                d += str(u.last_name)
            c.name = d
            contacts.append(c)

        chats = client.invoke(GetAllChatsRequest([])).chats
        for c in chats:
            cc = PicklableContact()
            cc.id = c.id
            cc.mode = "group"
            cc.name = c.title
            contacts.append(cc)
        renew = True

    """if os.path.exists("chats") and time.time() - 30 > float(os.path.getmtime("chats")):
        
    else:
        
        renew = True"""

    if ALFRED_MODE:
        contact_name = args.name
        s = "<?xml version=\"1.0\"?>"
        s+= "<items>"
        for u in contacts:

            if not (contact_name.lower() in u.name.lower() or contact_name.lower().startswith(u.name.lower())):
                continue

            msg = ""
            if contact_name.lower() not in u.name.lower() and u.name.lower() in contact_name.lower():
                msg = contact_name[len(u.name):]

            s += "<item uid=\"" + str(u.id) + "\" arg=\"" + u.mode + " " + str(u.id) + " " + msg + "\" autocomplete=\"" + u.name + " \">"
            s += "<title>"
            s += u.name
            s += "</title>"
            s += "<subtitle>"
            s += msg
            s+= "</subtitle>"
            s += "</item>"
        s+= "</items>"
        #s = s.encode("utf-8")
        #s = s.encode("ascii", "backslashreplace")

        #print(s.decode("ascii", "ignore"))
        if renew:
            pickle.dump(contacts, open("contacts", "wb"))
        print(s)
    else:
        cc = [(x.first_name, x.last_name, x.id) for x in users]
        contacts = []
        for f, l, i in cc:
            if i is not None:
                s = "U" + str(i) + ":"
            else:
                continue
            if f is not None:
                s += f + " "
            if l is not None:
                s += l

            contacts.append(s.strip())

        contacts.extend(["C" + str(x.id) + ":" + x.title for x in chats])
        print(0)
        for c in contacts:
            print(c)

def disconnect(args):
    os.remove(BASE_SESSION_NAME + ".session")

def setup_argparse(args=None):
    parser = argparse.ArgumentParser()
    sp = parser.add_subparsers()

    sp.add_parser("login").set_defaults(func=login)
    send_msg_parser = sp.add_parser("send_message")
    send_msg_parser.set_defaults(func=send_message)
    send_msg_parser.add_argument("mode", choices=("user", "group"), help="Is username, phone or group")
    send_msg_parser.add_argument("contact", help="Contact/group name")
    send_msg_parser.add_argument("msg", nargs="+", help="message to send")
    gc = sp.add_parser("get_contacts")
    gc.set_defaults(func=get_contacts)
    gc.add_argument("name", help="Contact/chat name")
    sp.add_parser("disconnect").set_defaults(func=disconnect)
    return parser.parse_args(args)

def from_alfred(query):
    args = query.split(" ")
    setup_argparse(args)
    h = """
        <?xml version="1.0"?>
<items>
  <item uid="desktop" arg="~/Desktop" valid="YES" autocomplete="Desktop" type="file">
    <title>Desktop</title>
    <subtitle>~/Desktop</subtitle>
    <icon type="fileicon">~/Desktop</icon>
  </item>
</items>
    """
    print(h)
    pass

if __name__ == "__main__":
    args = setup_argparse()
    args.func(args)