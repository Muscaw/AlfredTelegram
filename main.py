import argparse
import sys


def login(args):
    
    print "Login"
    pass

def send_message(args):
    print "Send message"

def get_contacts(args):
    print "Get contacts"

def setup_argparse():
    parser = argparse.ArgumentParser()
    sp = parser.add_subparsers()

    sp.add_parser("login").set_defaults(func=login)
    send_msg_parser = sp.add_parser("send_message")
    send_msg_parser.set_defaults(func=send_message)
    send_msg_parser.add_argument("contact", help="Contact/group name")
    send_msg_parser.add_argument("msg", help="message to send")
    sp.add_parser("get_contacts").set_defaults(func=get_contacts)
    return parser.parse_args()

if __name__ == "__main__":
    args = setup_argparse()
    args.func(args)