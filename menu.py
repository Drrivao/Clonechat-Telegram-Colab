from subprocess import run

def main():

    run('clear || cls',shell=True)
    print(
        'Tip: for optional configurations\n'+
        'you can press enter to use default.\n\n'+
        'Options:\n\n'+
        '1- Start client\n2- Clone\n3- Exit'
    )
    inp=int(input('\nChoose one: '))

    if inp == 1:
        api_id=input('\napi id: ')
        api_hash=input('api hash: ')
        bot_token=input('bot token: ')
        if bot_token is None:bot_token='blank'
        run([
            'python','configs.py','-i',api_id,'-s',api_hash,
            '-b',bot_token
        ])

    elif inp == 2:
        orig=input('\nOrigin chat title: ')
        dest=input('Destination chat title (optional): ')
        type=input('Type (optional): ')
        mode=input('Mode (optional): ')
        new=input('New (optional): ')
        query=input('Query (optional): ')
        limit=input('Limit (optional): ')

        if dest == '':dest='auto'
        if type == '': type='0'
        if mode == '': mode='user'
        if new == '': new='1'
        if query == '':query='all'
        if limit == '': limit='0'

        run([
            'python','clonechat.py','--orig',orig,'--dest',dest,
            '-t',type,'-m',mode,'-n',new,'-q',query,'-l',limit
        ])
    elif inp == 3:
        exit()
    else:
        print('Invalid option. Try again.\n')

while True:
    main()