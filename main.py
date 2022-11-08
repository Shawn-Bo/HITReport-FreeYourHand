import datetime
import json

import requests
import logging

FORMAT = '%(asctime)s %(clientip)-15s %(user)-8s %(message)s'
logging.basicConfig(format=FORMAT)


class Agent(object):
    def __init__(self, cookie: str):
        self.url_for_unpost_students = "https://xg.hit.edu.cn/zhxy-xgzs/xg_yqgl/yqxxqrnew/getXsxx"
        self.url_for_student_info = "https://xg.hit.edu.cn/zhxy-xgzs//xg_yqgl/mrsbNew/getMrsb"
        self.url_for_posting_student = "https://xg.hit.edu.cn/zhxy-xgzs/xg_yqgl/mrsbNew/save"
        self.cookie = cookie
        # 通过信息发送模板自动填充应有的字段，从而实现对应
        self.student_post_dict = {"XH": "1170800202", "RQ": "2022-10-17", "JZDZ": "", "KZL1": "1", "KZL2": "",
                                  "KZL3": "", "KZL4": "", "KZL5": "", "KZL6": "230000", "KZL7": "230100",
                                  "KZL8": "230103", "KZL9": "繁荣街153号", "KZL10": "黑龙江省哈尔滨市南岗区繁荣街153号",
                                  "KZL11": "", "KZL12": "", "KZL13": "3", "KZL14": "", "KZL15": "0", "KZL16": "",
                                  "KZL17": "1", "KZL18": "0;", "KZL19": "", "KZL20": "", "KZL21": "", "KZL22": "",
                                  "KZL23": "0", "KZL24": "0", "KZL25": "", "KZL26": "", "KZL27": "", "KZL28": "0",
                                  "KZL29": "", "KZL30": "", "KZL31": "", "KZL32": "2", "KZL33": {}, "KZL34": "",
                                  "KZL38": "黑龙江省", "KZL39": "哈尔滨市", "KZL40": "南岗区", "KZL41": "0"}

    def run_to_post_all_students(self, begin_date, end_date):
        for i in range((end_date - begin_date).days + 1):
            post_day = begin_date + datetime.timedelta(days=i)
            date = {"year": str(post_day.year), "month": str(post_day.month).zfill(2),
                    "day": str(post_day.day).zfill(2)}
            unpost_students_ids = self.get_unpost_students_by_date(date)
            for unpost_students_id in unpost_students_ids:
                self.post_student_with_date_and_id(date, unpost_students_id)
            print(f"完成了{date}的学生上报工作")

    def get_unpost_students_by_date(self, date: dict):
        body = 'info={"xhxm":"","rq":"'+date["year"]+'-'+str(date["month"]).zfill(2)+'-'+str(date["day"]).zfill(2)+'","page":1,"pageSize":500,"take":500,"skip":0} '
        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie": self.cookie,
            "Host": "xg.hit.edu.cn",
            "Origin": "https://xg.hit.edu.cn",
            "sec-ch-ua": '"Chromium";v="106", "Microsoft Edge";v="106", "Not;A=Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Windows",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.42",
            "X-Requested-With": "XMLHttpRequest"
        }
        res = requests.post(
            url=self.url_for_unpost_students,
            data=body,
            headers=headers,
        ).json()
        if res["isSuccess"]:
            print(f"成功获取{date}的未上报学生列表。")
        num_unpost_students = res["module"]["total"]
        print(f"{num_unpost_students}名学生未在{date}上报。")
        unpost_students_ids = [student_info["xh"] for student_info in res["module"]["data"]]
        return unpost_students_ids

    def get_student_info_by_id(self, id: str):
        body = 'info={"xh":"' + id + '"}'
        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie": self.cookie,
            "Host": "xg.hit.edu.cn",
            "Origin": "https://xg.hit.edu.cn",
            "sec-ch-ua": '"Chromium";v="106", "Microsoft Edge";v="106", "Not;A=Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Windows",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.42",
            "X-Requested-With": "XMLHttpRequest"
        }
        res = requests.post(
            url=self.url_for_student_info,
            data=body,
            headers=headers,
        ).json()
        if res["isSuccess"]:
            print(f"成功获取学号为{id}的学生信息。")
        student_info = res["module"]["data"]
        return student_info

    def post_student_with_date_and_id(self, date: dict, id: str):
        student_info_dict = self.get_student_info_by_id(id)[0]
        post_student_dict = {}
        for k in self.student_post_dict:
            if k not in student_info_dict.keys():
                print(f"学生字典中缺少字段：{k}")
            else:
                post_student_dict[k] = student_info_dict[k]
        post_student_dict["RQ"] = f"{date['year']}-{date['month']}-{date['day']}"
        body = 'info={"model":' + json.dumps(post_student_dict) + '}'
        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie": self.cookie,
            "Host": "xg.hit.edu.cn",
            "Origin": "https://xg.hit.edu.cn",
            "sec-ch-ua": '"Chromium";v="106", "Microsoft Edge";v="106", "Not;A=Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Windows",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.42",
            "X-Requested-With": "XMLHttpRequest"
        }
        print(post_student_dict)
        res = requests.post(
            url=self.url_for_posting_student,
            data=body,
            headers=headers
        ).json()
        if res["isSuccess"]:
            print(f"成功完成学号为{id}的学生上报。")


if __name__ == "__main__":
    """
      使用方法：
        1. 打开浏览器，输入学工处导员用户名和密码。
        2. 使用f12查看报文中的cookie字段，替换下面的cookie字符串。
        3. 设置开始、结束日期，运行脚本，自动填报。
        4. 希望这一切早日结束。
    """
    cookie = "JSESSIONID=27282798C16220125E17A7AA22266634; JSESSIONID=221F5106405AFD5935A4B130BCC3978C"
    agent = Agent(cookie)
    agent.run_to_post_all_students(begin_date=datetime.date(2022, 8, 22), end_date=datetime.date(2022, 10, 16))
