# Telegram Basic CLI

This project is not intended to be a fully-featured Telegram client. The goal of this project is to be interfaced with an Alfred workflow to send links to contacts.

The python script still needs to manage the authentication of the user before being able to send messages.

## Installation

This script needs some python modules to be able to run. They are listed in the "requirements.txt" file.

If you use pip to manage your modules, you can use the following command to install all the required packages.

```
pip install -r requirements.txt
```

The script needs to be registered on the Telegram network using an API ID and an API hash.
These can be obtained on the Telegram website: https://my.telegram.org/ under the category "API development tools".

The "settings.py" file contains global variables where you can put the needed information obtained on the Telegram webiste.

## Usage

The script works with arguments of the main.py script.

Valid arguments script_name [args]:

* login

    This parameter will start the client and will ask questions to authorize the user on the Telegram network.
    The credentials are saved in ~/.tbc/credentials
    
    If an account already exists, an error message appears to the user to warn him/her that an account is already connected.
    
* send_message
    
    This parameter allows the connected user to send a text message to a contact/group
    
    If the script outputs 0 in the standard output, the message has successfully been sent.
    
    Other numbers indicate an error and are described in the file "errors.py".
    
* get_contacts
    
    This parameters allows the connected user to retrieve all the contacts/groups to which a message can be sent.
    
    If the script outputs 0 on the first line of the standard output, the contact/group list has successfully been retrieved.
    The names of the contacts are displayed on each line separated by a "\n" character.
    
    If the first line is another number, it indicates that there is another error. The meaning of the error is described in the file "errors.py".
    