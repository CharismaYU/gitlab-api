import json
import os
import shlex
import subprocess
import time
from urllib.request import urlopen

gitlabToken = 'xxx'  # 自己gitlab上的tokne
gitlabAddr = 'xxx'  # gitlab地址名 注意：去掉http
groupName = 'xxx'  # 项目分组名 ， 为空则下载整个gitlab代码，慎用！
projectPath = 'F:/xxx/'
page = 1
per_page = 100


# 获取某个组下的所有项目，默认一页20条数据
def gen_next_url(target_id):
    return "http://%s/api/v4/groups/%s/projects?private_token=%s&per_page=%s" % (
        gitlabAddr, target_id, gitlabToken, per_page)


def gen_subgroups_url(target_id):
    return "http://%s/api/v4/groups/%s/subgroups?private_token=%s&per_page=%s" % (
        gitlabAddr, target_id, gitlabToken, per_page)


# 获取gitlab上所有的项目，默认一页20条数据
def gen_global_url():
    # http://XXX/api/v4/projects?private_token=XXX&page=1&per_page=100
    # page 当前页码
    # per_page 每页显示条数
    return "http://%s/api/v4/projects?private_token=%s&per_page=%s" % (gitlabAddr, gitlabToken, per_page)


# 获取所有的组
def gen_groups_url():
    return "http://%s/api/v4/groups?private_token=%s&per_page=%s" % (gitlabAddr, gitlabToken, per_page)


def pull_code(url):
    """
    调用url，获取ssh_url_to_repo和path_with_namespace，再通过git来pull代码到本地
    :param url: 接口地址
    :return:
    """

    # 发送用户请求
    allProjects = urlopen (url)
    allProjectsDict = json.loads (allProjects.read ().decode ())
    if len (allProjectsDict) == 0:
        return
    for thisProject in allProjectsDict:
        try:
            thisProjectURL = thisProject['ssh_url_to_repo']
            thisProjectPath = thisProject['path_with_namespace']
            print (thisProjectURL + ' ' + thisProjectPath)
            thisProjectPath = projectPath + thisProjectPath
            if os.path.exists (thisProjectPath):
                command = shlex.split ('git -C "%s" pull' % (thisProjectPath))
            else:
                command = shlex.split ('git clone %s %s' % (thisProjectURL, thisProjectPath))
            resultCode = subprocess.Popen (command)
            print (resultCode)
            time.sleep (5)
        except Exception as e:
            print ("Error on %s: %s" % (thisProjectURL, e.strerror))
    return resultCode


def get_next(group_id):
    """
    :param group_id:
    :return:
    """
    url = gen_next_url (group_id)
    return pull_code (url)


def get_sub_groups(parent_id):
    url = gen_subgroups_url (parent_id)
    allProjects = urlopen (url)
    allProjectsDict = json.loads (allProjects.read ().decode ())
    sub_ids = []
    if len (allProjectsDict) == 0:
        return sub_ids
    for thisProject in allProjectsDict:
        try:
            id = thisProject['id']
            sub_ids.append (id)
        except Exception as e:
            print ("Error on %s: %s" % (id, e.strerror))
    return sub_ids


def cal_next_sub_groupIds(parent_id):
    parent = parent_id
    parent_list = []
    sub_ids = get_sub_groups (parent_id)
    url = gen_next_url (parent_id)
    ok = url_exist (url)
    if len (sub_ids) != 0 and ok == False:
        for i in range (len (sub_ids)):
            print (sub_ids[i])
            a = cal_next_sub_groupIds (sub_ids[i])
            return a
    if len (sub_ids) != 0 and ok == True:
        for i in range (len (sub_ids)):
            parent = sub_ids[i]
            parent_list.append (sub_ids[i])
            a = cal_next_sub_groupIds (sub_ids[i])
            parent_list.extend (a)
    if len (sub_ids) == 0 and ok == True:
        parent_list.append (parent)
        return parent_list
    if len (sub_ids) == 0 and ok == False:
        return parent_list
    return parent_list


# url是否有数据
def url_exist(url):
    allProjects = urlopen (url)
    allProjectsDict = json.loads (allProjects.read ().decode ())
    if len (allProjectsDict) == 0:
        return False
    return True


def download_code(parent_id):
    data = cal_next_sub_groupIds (parent_id)
    for group_id in data:
        get_next (group_id)
    return


def main():
    if groupName == '':
        url = gen_global_url ()
        pull_code (url)
    else:
        # 获取所有的组
        url = gen_groups_url ()
        allProjects = urlopen (url)
        allProjectsDict = json.loads (allProjects.read ().decode ())
        if len (allProjectsDict) == 0:
            return
        groupId = ''
        for thisProject in allProjectsDict:
            try:
                # 获取组名
                thisName = thisProject['name']
                if groupName == thisName:
                    groupId = thisProject['id']
                    break
            except Exception as e:
                print ("Error on %s: %s" % (thisName, e.strerror))
        download_code (groupId)
        return


if __name__ == '__main__':
    main ()
