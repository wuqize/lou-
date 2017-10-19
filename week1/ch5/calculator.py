#!/usr/bin/python
#coding=utf-8
import sys
import os
import configparser
import getopt
from datetime import datetime
from multiprocessing import Queue, Process
from collections import namedtuple

get_user_data = Queue()
write_data = Queue()

class Cfg(object):

    def __init__(self, cfg_path, choice):
        config = configparser.ConfigParser()
        config.read(cfg_path)
        choice = choice.upper()
        self.JiShuL = float(config[choice]["JiShuL"])
        self.JiShuH = float(config[choice]["JiShuH"])

        self.YangLao = float(config[choice]["YangLao"])
        self.YiLiao = float(config[choice]["YiLiao"])
        self.ShiYe = float(config[choice]["ShiYe"])
        self.GongShang = float(config[choice]["GongShang"])
        self.ShengYu = float(config[choice]["ShengYu"])
        self.GongJiJin = float(config[choice]["GongJiJin"])

        self.insurance_percent = sum(
            [
            self.YangLao,
            self.YiLiao,
            self.ShiYe ,
            self.GongShang,
            self.ShengYu,
            self.GongJiJin
        ]
        )

class Records(object):

    def __init__(self, record_path):
        self.records = []
        with open(record_path, "r") as f:
            for line in f:
                self.records.extend([line.split(",")])
        for item in self.records:
            item[1] = int(item[1])

class SalaryCalculator(object):

    def __init__(self, cfg):
        self.cfg = cfg

    def get_tax_amount_payable(self, salary, insurance):
        taxable_income = salary - insurance - 3500
        if taxable_income <= 0:
            tax_amount_payable = 0
        elif taxable_income < 1500:
            tax_amount_payable = taxable_income * 0.03 - 0
        elif taxable_income < 4500:
            tax_amount_payable = taxable_income * 0.1 - 105
        elif taxable_income < 9000:
            tax_amount_payable = taxable_income * 0.2 - 555
        elif taxable_income < 35000:
            tax_amount_payable = taxable_income * 0.25 - 1005
        elif taxable_income < 55000:
            tax_amount_payable = taxable_income * 0.3 - 2755
        elif taxable_income < 80000:
            tax_amount_payable = taxable_income * 0.35 - 5505
        else:
            tax_amount_payable = taxable_income * 0.45 - 13505
        return tax_amount_payable


    def calculator(self, salary):
        if salary > self.cfg.JiShuH:
            cal_salary = self.cfg.JiShuH
        elif salary < self.cfg.JiShuL:
            cal_salary = self.cfg.JiShuL
        else:
            cal_salary = salary
        insurance = cal_salary * self.cfg.insurance_percent
        tax_amount_payable = self.get_tax_amount_payable(salary, insurance)
        after_tax_salary = salary - insurance -tax_amount_payable
        return insurance, tax_amount_payable, after_tax_salary



def read_records(user_path):
    try:
        rds = Records(user_path)
        for user_data in rds.records:
            get_user_data.put(user_data)
    except Exception as e:
        print(e.__str__())


def calculat(cfg_path, city):
    cfg = Cfg(cfg_path, city)
    sc = SalaryCalculator(cfg)
    while True:
        try:
            name, salary = get_user_data.get(timeout=1)
        except Exception as e:
            return
        record = [name, salary]
        record.extend(sc.calculator(salary))
        record.append(datetime.strftime(datetime.now(), "%Y-%m-%d %H-%M-%S"))
        print(record)
        write_data.put(record)



def write_log(record_path):
    with open(record_path, "w") as f:
        while True:
            try:
                item = write_data.get(timeout=1)
                f.write("{},{},{},{},{},{}\n".format(item[0],
                                                  item[1],
                                                  format(item[2], ".2f"),
                                                  format(item[3], ".2f"),
                                                  format(item[4], ".2f"),
                                                  item[5]
                                                  )
                        )
            except Exception as e:
                return



def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hC:c:d:o:", ["help",])
    except getopt.GetoptError as err:
        print(err.__str__())
        sys.exit(-1)

    cfg_path = None
    user_path = None
    record_path = None
    city = "default"
    for o, a in opts:
        if o == "-v":
            verbose = True
        elif o in ("-h", "--help"):
            print("Usage: calculator.py -C cityname -c configfile -d userdata -o resultdata")
            sys.exit(-1)
        elif o == "-C":
            city = a
        elif o == "-c":
            cfg_path = a
        elif o == "-d":
            user_path = a
        elif o == "-o":
            record_path = a
        else:
            assert False, "unhandled option"

    if not(user_path and cfg_path):
        print("Usage: calculator.py -C cityname -c configfile -d userdata -o resultdata")
        sys.exit(-1)

    if not os.path.isfile(cfg_path):
        print("CONFIG File Not Exist Error")
        sys.exit(-1)

    if not os.path.isfile(user_path):
        print("USER DATA File Not Exist Error")
        sys.exit(-1)

    Process(target=read_records, args=(user_path,)).start()
    Process(target=calculat, args=( cfg_path, city)).start()
    Process(target=write_log, args=(record_path,)).start()



if __name__ == "__main__":
    main()

