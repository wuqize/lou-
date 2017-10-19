#!/usr/bin/python
#coding=utf-8
import sys


def get_insurance(salary):
    return salary * (8 + 2 + 0.5 + 0 + 0 + 6) / 100

def get_tax_amount_payable(salary, insurance):
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

def calculator(args):
    employees = []
    for item in args[1:]:
        job_num, salary = item.split(":")
        employees.append([int(job_num), int(salary)])

    for item in employees:
        insurance = get_insurance(item[1])
        after_tax_salary = item[1] - insurance - get_tax_amount_payable(item[1], insurance)
        print("{}:{}".format(
            item[0],
            format(after_tax_salary, ".2f"))
        )

def main():
    args = sys.argv
    if len(args) <= 1:
        print("Parameter Error")
        sys.exit(-1)
    try:
        calculator(args)
    except Exception as e:
        print("Parameter Error")
        sys.exit(-1)

if __name__ == "__main__":
    main()
