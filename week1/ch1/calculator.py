#!/usr/bin/python
#coding=utf-8
import sys

def main():
	args = sys.argv
	if len(args) != 2:
		print("Parameter Error")
		sys.exit(-1)
	try:
		salary = int(args[1])
	except:
		print("Parameter Error")
		sys.exit(-1)

	taxable_income = salary - 3500
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
	print(format(tax_amount_payable, ".2f"))
	
if __name__ == "__main__":
	main()