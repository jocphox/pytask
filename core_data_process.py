import os
import sqlite3
import operator
from collections import OrderedDict
import time
from datetime import datetime, timedelta
import getpass
from sub_setting import dvset
from sub_log import dvlog
import re

def datetime_standard(pywindate):
    return datetime(pywindate.year, pywindate.month, pywindate.day, hour=pywindate.hour, minute=pywindate.minute, microsecond=pywindate.microsecond)

def getdate(pdatetime):
    return pdatetime.strftime("%Y-%m-%d")

def read_outlook_tasks(task_recorded_list):
    from win32com.client.gencache import EnsureDispatch as Dispatch  # 读取邮件模块
    """连接Outlook邮箱，读取收件箱内的邮件内容"""
    #  使用MAPI协议连接Outlook
    account = Dispatch('Outlook.Application').GetNamespace('MAPI')
    #  获取收件箱所在位置
    folder = account.GetDefaultFolder(13)
    #  获取收件箱下的所有邮件
    items = folder.Items
    #  items.Sort('[StartDate]', True)  # 邮件按时间排序
    itemcount=len(items)
    # print(itemcount)
    mailinfos=[]
    record_added_in_this_refresh = 0
    for index in range(itemcount):
        # print(index)
        mail = items.Item(index+1)
        try:
            if mail.EntryID not in task_recorded_list:
                mailinfos.append((mail.EntryID, mail.Subject, mail.DueDate,
                                  'unallocated', 'outlook', "unset", "yes",
                                  mail.Complete, mail.Status, mail.Body[:300],
                                  mail.StartDate,  "08:00", 30,
                                  "", "", 30))
                task_recorded_list.append(mail.EntryID)
                record_added_in_this_refresh += 1
        except:
            pass

    return mailinfos


def cleanerror2():
    try:
        from win32com import client
        xl = client.gencache.EnsureDispatch('Excel.Application')
    except AttributeError:
        # Corner case dependencies.
        import os
        import re
        import sys
        import shutil
        # Remove cache and try again.
        MODULE_LIST = [m.__name__ for m in sys.modules.values()]
        for module in MODULE_LIST:
            if re.match(r'win32com\.gen_py\..+', module):
                del sys.modules[module]
        shutil.rmtree(os.path.join(os.environ.get('LOCALAPPDATA'), 'Temp', 'gen_py'))
        from win32com import client
        xl = client.gencache.EnsureDispatch('Excel.Application')

if __name__ == '__main__':
    # from datetime import datetime, timedelta
    # t0 = datetime.now()
    # for i  in range(5):
    #     print(len(geteverythingresult(i,i-1)),end="\t")
    #     print(len(get_history_data(i, i-1)),end="\t")
    #     print(len(read_outlook_mailbox(i, i-1, "inbox")),end="\t")
    #     print(len(read_outlook_mailbox(i, i-1, "outbox")),end="\n")
    # print( datetime.now() - t0 )
    print(len(read_outlook_tasks([])))
    # cleanerror2()
    # print(os.path.join(os.environ.get('LOCALAPPDATA'), 'Temp', 'gen_py'))