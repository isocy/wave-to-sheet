import glob

instrument = 'drum'
train_or_test = 'Test'
argvs = glob.glob('./datasets/{}/{}/*.wav'.format(train_or_test, instrument))
print(argvs)


path = 'D:\PyCharm\wave-to-sheet'

for argv in argvs:
    arg = ''
    argv = argv.replace('/','\\')
    arg += path + argv[1:]
    with open('./{}_{}.txt'.format(instrument,train_or_test),'a') as f:
        f.write(arg+'\n')

