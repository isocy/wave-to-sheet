import glob

argvs = glob.glob('./datasets/Train/piano/*.wav')
print(argvs)


path = 'D:\PyCharm\wave-to-sheet'

for argv in argvs:
    arg = ''
    argv = argv.replace('/','\\')
    arg += path + argv[1:]+' '
    with open('./args.txt','a') as f:
        f.write(arg+'\n')

