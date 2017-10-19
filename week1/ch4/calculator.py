#!/usr/bin/python
#coding=utf-8
import sys
import os
from multiprocessing import Queue, Process
from collections import namedtuple

get_user_data = Queue()
write_data = Queue()

class Cfg(object):

    def __init__(self, cfg_path):
        with open(cfg_path, "r") as f:
            lines = f.readlines()
        self.JiShuL = float(lines[0].replace(" ", "").replace("\n", "").split("=")[1])
        self.JiShuH = float(lines[1].replace(" ", "").replace("\n", "").split("=")[1])
        self.insurance_percent = sum(
            [float(item.replace(" ", "").replace("\n", "").split("=")[1]) for item in lines[2:]]
        )

        # self.YangLao = lines[2].split(" = ")
        # self.YiLiao = lines[3].split(" = ")
        # self.ShiYe = lines[4].split(" = ")
        # self.GongShang = lines[5].split(" = ")
        # self.ShengYu = lines[6].split(" = ")
        # self.GongJiJin = lines[7].split(" = ")

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



def read_config(user_path):
    try:
        rds = Records(user_path)
        for user_data in rds.records:
            get_user_data.put(user_data)
    except Exception as e:
        print(e.__str__())

def calculat(cfg_path):
    cfg = Cfg(cfg_path)
    sc = SalaryCalculator(cfg)
    while True:
        try:
            name, salary = get_user_data.get(timeout=1)
        except Exception as e:
            return
        record = [name, salary]
        record.extend(sc.calculator(salary))
        write_data.put(record)



def write_log(record_path):
    with open(record_path, "w") as f:
        while True:
            try:
                item = write_data.get(timeout=1)
                f.write("{},{},{},{},{}\n".format(item[0],
                                                  item[1],
                                                  format(item[2], ".2f"),
                                                  format(item[3], ".2f"),
                                                  format(item[4], ".2f")
                                                  )
                        )
            except Exception as e:
                return



def main():
    args = sys.argv
    if len(args) != 7:
        print("Parameter Error")
        sys.exit(-1)
    if not ("-c" in args or "-d" in args  or "-o" in args):
        print("Parameter Error ")
        sys.exit(-1)

    if len(args) > (args.index("-c") + 1):
        if not os.path.isfile(args[args.index("-c")+1]):
            print("File Not Exist Error")
            sys.exit(-1)

    if len(args) > (args.index("-d") + 1):
        if not os.path.isfile(args[args.index("-d")+1]):
            print("File Not Exist Error")
            sys.exit(-1)

    if len(args) <= (args.index("-o") + 1):
        print("Parameter Error ")
        sys.exit(-1)

    cfg_path = args[args.index("-c")+1]
    user_path = args[args.index("-d")+1]
    record_path = args[args.index("-o")+1]
    Process(target=read_config, args=(user_path,)).start()
    Process(target=calculat, args=( cfg_path, )).start()
    Process(target=write_log, args=(record_path,)).start()


if __name__ == "__main__":
    main()
