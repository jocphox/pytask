from datetime import datetime
from sub_setting import dvset


def addtime():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def dvlog(content="", end= "\n"):
    testmode = True if dvset('testmode') == 'yes' else False
    try:
        if testmode:
            print("log ", end=" >\t ")
            if content.__class__ == [].__class__:
                print('list is in print...')
                for _ in content:
                    print(_)
            elif content == '':
                print("--------------------------------")
            else:
                print(content, end=end)
        else:

            with open('log.txt','a') as f:
                f.write("\nlog[" + addtime() + '] >\t')
                if content.__class__ == [].__class__:
                    f.write('list is in print...')
                    for _ in content:
                        f.write(_)
                else:
                    f.write(content)
                f.write("\n--------------------------------")

    except:
        pass

if __name__ == '__main__':
    # generate_settings()
    for i in range(10):
        dvlog(str(i))



