import glob
import os
import shlex
import time
import subprocess

# 切换当前目录下的所有项目的git分支
rootPath = 'D:/javaWorkSpace/framework/'


def walf_file(path):
    for root, dirs, files in os.walk (path):
        # root 表示当前正在访问的文件夹路径
        # dirs 表示该文件夹下的子目录名list
        # files 表示该文件夹下的文件list

        # 遍历所有的文件夹(包括子目录)
        for d in dirs:
            print (os.path.join (root, d))
        # 只遍历当前目录，不查找子目录
        break


def globDir_FirstDir(path):
    if os.path.exists (path):
        # 获取该目录下的所有文件或文件夹目录路径
        files = glob.glob (path + "*")
        for fileName in files:
            if os.path.exists (fileName):
                switch_brand (fileName)
                break


# 定义一个函数，path为你的路径, 会查找两级
def traversalDir_FirstDir(filePath):
    # 判断路径是否存在
    if os.path.exists (filePath):
        # 获取该目录下的所有文件或文件夹目录(只找一级的）
        firstFiles = os.listdir (filePath)
        for firstFile in firstFiles:
            # 得到该文件下所有目录的路径
            m = os.path.join (filePath, firstFile)
            # 判断该路径下是否是文件夹
            if os.path.isdir (m):
                # 获取该目录下的所有文件或文件夹目录(只找一级的）
                secondFiles = os.listdir (m)
                for secondFile in secondFiles:
                    three = os.path.join(m, secondFile)
                    gitPath = m + '/.git'
                    if os.path.isdir(three) and os.path.exists (gitPath):
                        switch_brand (m)


def switch_brand(dirPath):
    try:
        os.chdir (dirPath)
         # 创建并合并分支
        command = shlex.split ('git checkout -b develop origin/develop')
        resultCode = subprocess.Popen (command)
        #print (dirPath + ':::' + resultCode)
        time.sleep (1)
    except Exception as e:
        print ("Error on %s: %s" % (dirPath, e.strerror))
    return


def main():
    # walf_file (rootPath)
    # globDir_FirstDir (rootPath)
    # 二级形式，查找当前目录下的文件夹，再遍历每个文件夹，找到所有项目，切换分支
     traversalDir_FirstDir (rootPath)


if __name__ == '__main__':
    main ()
