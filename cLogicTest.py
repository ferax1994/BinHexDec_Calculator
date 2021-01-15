from calculatorLogic import *;

# ==========
#   Date: 01.2021.
# ==========

#simple test function for Calculator class.

calc = Calculator();
i = 0;
print("Typing 'end' breaks loop...\n");

while (True) :
    print("i = " + str(i) + "  ====================");
    
    a = input("Exp: ");
    b = input("Num: ");

    print("Is expression: " + str(Calculator.is_exp(a)));
    print("Number converted: " + Calculator.convert_output_toString(calc.convert(b)));

    i = i + 1;
    if (a == 'end') :
        break;
