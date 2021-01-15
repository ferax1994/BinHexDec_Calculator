#Dec-Bin-Hex calculator - Logic

# ==========
#   Date: 01.2021.
#
# ==========

import re;

class InabilityToAsignError(Exception) :
    pass;
class InabilityToClearStringError(Exception) :
    pass;

# ==========
#   Programer global guidelines:
#
#       About defining and using functions:
#           regular functions : Takes created INSTANCE of the class as one of the parameters (through self).
#                               Using these functions on INSTANCE of class.
#                               Can change object variables (slots).
#                               Cannot change class variables.
#
#           static functions :  Takes ONLY function parametars.
#                               Using them on both INSTANCE of class (object) and CLASS itself.
#                               Can change object variables (explicitly named) but it is NOT RECOMENDED!!
#                               Cannot change class variables.
#
#           class functions :   Takes the CLASS (definition, in python also an object) as one of the parameters (through cls).
#                               Using them WITHOUT INSTANCING.
#                               Cannot change class instance variables (slots).
#                               Can change class variables.
#
#       About raising exceptions :
#           class exceptionName(Exception) : Creation of custom exception.
#           raise exceptionName("exception string") : Causing custom exception, which can be cathced ANYWHERE on the
#                                                      path: function_1(raised) --> *[...] --> *[function_n] --> module(main program).
#                                                      **exception handling expected like 'except exceptionName as workName', print(str(workName)).
#
#       About python documentation :
#           Slot variables == object variables
#       
#       
#
# ==========

class Calculator(object) :
    """Calculator class is a main class for expression evaluation and number conversion.
    Objects are initialized without parameters. 
    
    Communication and data exchange with environment is achieved through complex functions. It is strongly advised to use them as explained below.
    
    Provides functions for implementation of 2 major calculator functionalities:
        1. CONVERSION : number (only one) in string format (Number string) converted to 3 formats. Formats: Binary/Hexadecimal/Decimal.
        2. CALCULATION : evaluating expression in string format (Expression string) to a single number in string format (Number string) uppon which
                            (1.) is performed.

    Math calculation rules:
        1. Negation is the only unary operator --> it is not considered as operation, rather as a negative number.
        2. All operations are binary.
        3. Only round '(', ')' parenthensis allowed.



    Class variables:
        _digitBin, _digitHex, _digitDec : list of String. List of digits accepted in formats: Binary/Hexadecimal/Decimal.
        _numFormatStr : list of String. Only 2 possible string beginings for Binary/Hexadecimal Number string.
        _numBaseOptions : list of String. Contains suported number bases.
        _operators : list of String. Contains supported expression operators.
        _groupation : list of String. Contains left/right parenthensis.

        
    Constructor arguments:
        None


    Slot variables:
        Public:
            history : list of: (String,String,String,bool) | String. Contains conversions/calculations from the moment Calculator object was instanced (created).
                        **(binary, hexadecimal, decimal, negation), where 3 types are String, and negation is bool.
                        **expression, is String.

            
        Private:
            _expression : String. Current object focused expression for calculation.
            _number : Integer. Current object focused number for conversion/calculation.
            _strBin, _strHex, _strDec : String. Current object focused string representations of _number.
            _negation : bool. Current object focused number prefix --> True == _number is negative, False == _number is positive.
                                **negation in Calculator class is only a flag, does not change number strings or number itself.
                                **reason being python negative number representation as: negativeNumber = -positiveNumber.


    Override object functions:
        __str__(self) : (String,int,bool). Returns string representation of object, using 3 variables: expression string, number integer, negation bool.

        
    Defines object functions:
        get_history(self) : list of: (String,String,String,bool) | String. Returns history of conversions/calculations.
        convert(self,String) : (String,String,String). Takes Number string, converts it, returns converted tuple: (binary, hexadecimal, decimal).
            **CONVERSION
        _convert_output_form(self) : (String,String,String). Concats missing '-' (negation character) after CONVERSION, for output.
        _history_log1(self) : None. Appends current calculator number values after CONVERSION to object variable history.
        _history_log2(self) : None. Appends current calculator expression value after CALCULATION to object variable history.

        
    Defines class functions:
        Conversion (on number):
            is_correct_baseNumber(cls, numStr, base) : bool. Is given Number string correctly formated, and in the given base.
            is_num(cls, numStr) : bool. Is given Number string in correct form.
            _is_hex_str(cls, numStr), _is_bin_str(numStr), _is_dec_str(numStr) : bool. Is given (positive) Number string in bin/hex/dec format.
            _is_string(cls, numStr) : bool. Is given Number string: a string and not empty.
            
        Calculation (on expression):
            is_exp(cls, expStr) : bool. Is given Expression string corectly formated.
            _is_correct_groupation(cls, expStr) : bool. Is given Expression string (focus only parenthensis) corectly grouped by parenthensis.
            _is_correct_parenthensis_environment(cls, expStr) : bool. Is given Expression strings (focus only parenthensis) environment of parenthensis correct.
            _is_correct_operation(cls, expStr) : bool. Is given Expression string (focus only number/operator expression) correct.


    Defines static functions:
        stringClearStrip(numStr) : String. Returns Number string or Expression string cleared of 'spaces' and 'newlines'.
        convert_output_toString(out) : String. Returns nicer plain string of (String,String,String) convert() output.
        history_el_toString(el) : String. Returns nicer plain string of history list element.
        
    Exceptions:
        InabilityToAsignError : Exception. If Number string cannot be converted to bin/hex/dec format.
        InabilityToClearStringError : Exception. If there is no string to clear in input.
        **TypeError exception, if Number string in bad format.
    """
    
    _digitBin = ['0','1'];
    _digitDec = ['0','1','2','3','4','5','6','7','8','9'];
    _digitHex = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']; #allNumCharacters
    _numFormatStr = ['0b','0x'];
    _numBaseOptions = ['1', '2', '4', '8', '16', '32', 'full'];

    _operators = ['+', '-', '*', '/', '|', '&'];
    _groupation = ['(', ')'];


    # ==========
    # INITIALIZATION :
    # ==========

    __slots__ = ('_expression', '_number', '_strBin', '_strHex', '_strDec', '_negation', 'history');
    
    def __init__(self, parent=None) :
        self._expression = "";
        
        self._number = 0;

        self._strBin = "";
        self._strHex = "";
        self._strDec = "";

        self._negation = False;

        self.history = [];

    def __str__(self) :
        """Returns (current) string representation of Calculator() object."""

        try :
            s = (self.expression, self._number, self._negation); 
        except :
            #catches all exceptions
            s = "Empty Calculator";

        return s;

    def get_history(self) :
        """Arguments:
                None
                
        Returns:
            history : list of: (String,String,String,bool) | String.


        Returns whole history log of conversion/calculator from the moment Calculator was instanced.

        
        **elements of the list are in strict form:
            (binary,hexadecimal,decimal,negation) : where 3 types are String and negation is bool.
            expression : String.
        """

        return self.history;


    # ==========
    # CONVERSION :
    # ==========
    
    def convert(self, numStr) :
        """Arguments:
                numStr : String. Possible number in string form. Number string.

        Returns:
            package : (String, String, String). Tuple of 3 string values in strict and important order: (binary, hexadecimal, decimal).


        Public function used upon any string.


        Uses private functions:
            _convert_output_form() : (String,String,String). Prepares object variables of 3 number types for return (handling negation).
            _history_log1() : None. Updates (add state to) object variable history.
        Uses class functions:
            is_num() : bool. Secures Number string corectness. See is_num().

        Uses static functions:
            stringClearStrip() : String. Clears input string from spaces/newlines if possible, else raises InabilityToClearStringError.
            
        Does:
            1) Tries to strip Number string of 'spaces' and 'newlines', else raises TypeError.
            2) Checks if Number string: is a string, not empty, correct number form, else raises TypeError.
            3) Handles negative numbers by removing '-' character and testing/converting uppon their positive part.
                **we can do that and be sure that conversions and tests are valid because in python negativeNumber = -positiveNumber.
            4) Tries to convert number into binary,hexadecimal,decimal form, and update object variables, else raises InabilityToAsignError.
            5) Updating object variable history
            6) Preparing output form (String,String,String) and returns.

        Raises:
            InabilityToAsignError; if Number string cannot be converted to bin/hex/dec format.
            TypeError; if Number string: isnt string, cannot be stripped, is in bad format.
        """
        
        #** _is_num tests for size also
        #
        #   bin(int) --> binary number as string from int.
        #
        #   hex(int) --> hexadecimal number as string from int.
        #
        #   str(int) --> decimal number as string from int.

        try :
            numStr = self.stringClearStrip(numStr);
        except InabilityToClearStringError as incS :
            raise TypeError("Calculator.convert(): Number argument isnt string!; " + str(incS));
        except :
            raise TypeError("Calculator.convert(): Number argument invalid!");
        
        if (self.is_num(numStr)) :
            if (numStr[0] == '-') :
                #positive part of number taken
                numStr = numStr[1:];
                self._negation = True;
            else :
                #positive already
                self._negation = False;
                
            d = len(numStr);
            if (d > 2) :
                firstTwoChar = numStr[:2].lower();
                if (firstTwoChar == self._numFormatStr[0]) :
                    #bin
                    self._strBin = numStr[:2].lower() + numStr[2:].upper();
                    try :
                        self._number = int(self._strBin, base=2);
                        self._strBin = bin(self._number)[:2].lower() + bin(self._number)[2:].upper();
                        self._strHex = hex(self._number)[:2].lower() + hex(self._number)[2:].upper();
                        self._strDec = str(self._number);
                        
                    except ValueError :
                        #catches inability to convert binary string to int number, or other conversions
                        print("Value error: strBin --> numDec");
                        raise InabilityToAsignError("Calculator: Convert: cannot asign what is already a checked number to other variables...");
                    except :
                        print("Some other error! strBin --> numDec");
                        raise InabilityToAsignError("Calculator: Convert: cannot asign what is already a checke number to other variables...");
                    
                elif (firstTwoChar == self._numFormatStr[1]) :
                    #hex
                    self._strHex = numStr[:2].lower() + numStr[2:].upper();
                    try :
                        self._number = int(self._strHex, base=16);
                        self._strBin = bin(self._number)[:2].lower() + bin(self._number)[2:].upper();
                        self._strHex = hex(self._number)[:2].lower() + hex(self._number)[2:].upper();
                        self._strDec = str(self._number);
                    except ValueError :
                        #catches inability to convert hexadecimal string to int number, or other conversions
                        print("Value error: strHex --> numDec");
                        raise InabilityToAsignError("Calculator: Convert: cannot asign what is already a checked number to other variables...");
                    except :
                        print("Some other error! strHex --> numDec");
                        raise InabilityToAsignError("Calculator: Convert: cannot asign what is already a checked number to other variables...");
                else :
                   #dec
                    self._strDec = numStr.upper();
                    try :
                        self._number = int(self._strDec);
                        self._strBin = bin(self._number)[:2].lower() + bin(self._number)[2:].upper();
                        self._strHex = hex(self._number)[:2].lower() + hex(self._number)[2:].upper();
                        self._strDec = str(self._number);
                    except ValueError :
                        #catches inablity to convert in string to int number, or other
                        print("Value error: strDec --> numDec");
                        raise InabilityToAsignError("Calculator: Convert: cannot asign what is already a checked number to other variables...");
                    except :
                        print("Some other error! strDec --> numDec");
                        raise InabilityToAsignError("Calculator: Convert: cannot asign what is already a checked number to other variables...");
            else :
                # (d <= 2) and/or dec
                self._strDec = numStr.upper();
                try :
                    self._number = int(self._strDec);
                    self._strBin = bin(self._number)[:2].lower() + bin(self._number)[2:].upper();
                    self._strHex = hex(self._number)[:2].lower() + hex(self._number)[2:].upper();
                    self._strDec = str(self._number);
                except ValueError :
                    #catches inablity to convert in string to int number, or other
                    print("Value error: strDec --> numDec");
                    raise InabilityToAsignError("Calculator: Convert: cannot asign what is already a number to other variables...");
                except :
                    print("Some other error! strDec --> numDec");
                    raise InabilityToAsignError("Calculator: Convert: cannot asign what is already a number to other variables...");


            #if all conditions are met, in this part we are sure our number formats are valid!
            #current state stored in history (conversion function)

            self._history_log1();
            package = self._convert_output_form();
            return package;
        else :
            #is not correct number format
            raise TypeError("Calculator.convert(): Number argument in wrong format!");
        
        raise TypeError("Calculator.convert(): Unknown function end!");

    def _convert_output_form(self) :
        if (self._negation) :
                #negative 
                sB = '-' + self._strBin;
                sH = '-' + self._strHex;
                sD = '-' + self._strDec;
        else :
            #positive
            sB = self._strBin;
            sH = self._strHex;
            sD = self._strDec;
            
        return (sB,sH,sD);

    def _history_log1(self) :
        self.history.append((self._strBin, self._strHex, self._strDec, self._negation));

    def _history_log2(self) :
        self.history.append(self.expression);


    # ==========
    # CALCULATION :
    # ==========

    #FINISH ME
        

    # ==========
    # TESTS (CLASS) NUMBER/STRING :
    # ==========
    
    @classmethod
    def is_correct_baseNumber(cls, numStr, base) :
        """Arguments:
                numStr : String. Possible number in string form == Number string.
                base : String. Possible base in string form.

        Returns:
            True/False : bool.


        Public function used upon cleared and plain string like [-numStr | numStr].

        
        Uses class functions:
            is_num() : bool. Secures Number string corectness. See is_num().

        Does:
            1) Checks if Number string: is a string, not empty, correct form. Checks if base string/character is correct.
            2) Strips Number string of negation character (negation important only for decimal number format)
            3) Checks for:
                a) Bin - strips Number string of binFormat, and checks conditions for binary based number (negation unimportant).
                b) Hex - strips Number string of hexFormat, and checks conditions for hexadecimal based number (negation unimportant).
                c) Dec - Converts Number string to integer number, and checks conditions on decimal value and base-bit long number range.
                    **handles negation with help of local negation flag variable.
        """
        
        negFlag = False;

        if ((cls.is_num(numStr)) and (base in cls._numBaseOptions)) :
            neg = numStr[0];
            if (neg == '-') :
                numStr = numStr[1:];
                negFlag = True;
            else :
                negFlag = False;
            
            d = len(numStr);
            if (d > 2) :
                firstTwoChar = numStr[:2].lower();
                restNum = numStr[2:].upper();
                restNumLen = len(restNum);
                if (firstTwoChar == cls._numFormatStr[0]) :
                    #bin
                    #no negation processing needed
                    if (base == 'full') :
                        return True;
                    else :
                        baseNum = int(base);
                        if (baseNum >= restNumLen) :
                            return True;
                        else :
                            return False;
                
                    #safety return for bin-part
                    return False;
                elif (firstTwoChar == cls._numFormatStr[1]) :
                    #hex
                    #no negation processing needed
                    if (base == 'full') :
                        return True;
                    else :
                        baseNum = int(base);
                        if (baseNum < 4) : 
                            return False;
                        elif ((baseNum == 4) and (restNumLen == 1)) : #4-bit --> 1 hex digit
                            return True;
                        elif ((baseNum == 8) and (restNumLen <= 2)) : #8-bit --> 2 hex digits
                            return True;
                        elif ((baseNum == 16) and (restNumLen <= 4)) : #16-bit --> 4 hex digits
                            return True;
                        elif ((baseNum == 32) and (restNumLen <= 8)) : #32-bit --> 8 hex digits
                            return True;
                        else :
                            #any other restNumLen value
                            return False;

                    #safety return for hex-part
                    return False;
                else :
                    #dec
                    #negation processing added
                    if (base == 'full') :
                        return True;
                    else :
                        baseNum = int(base);
                        if (negFlag) :
                            #it is negative
                            decStr = '-' + numStr;
                        else :
                            decStr = numStr;
                        decNum = int(decStr);
                        if ((baseNum == 1) and ((decNum >= -1) and (decNum <= 0))) :  #1-bit --> decNum = [-1,0] 
                            return True;
                        elif ((baseNum == 2) and ((decNum >= -2) and (decNum <= 1))) : #2-bit --> decNum = [-2,1]
                            return True;
                        elif ((baseNum == 4) and ((decNum >= -8) and (decNum <= 7))) : #4-bit --> decNum = [-8,7]
                            return True;
                        elif ((baseNum == 8) and ((decNum >= -128) and (decNum <= 127))) : #8-bit --> decNum = [-128,127]
                            return True;
                        elif ((baseNum == 16) and ((decNum >= -32768) and (decNum <= 32767))) : #16-bit --> decNum = [-32768, 32767]
                              return True;
                        elif ((baseNum == 32) and ((decNum >= -pow(2, 31)) and (decNum <= pow(2,31)-1))) : #32-bit --> decNum = [-2^31, 2^31 - 1]
                              return True;
                        else :
                              #any other combination
                              return False;
                    #safety return for dec-part
                    return False;
            else :
                # (d <= 2)
                if (base == 'full') :
                    return True;
                else :
                    baseNum = int(base);
                    if (negFlag) :
                        #it is negative
                        decStr = '-' + numStr;
                    else :
                        decStr = numStr;
                    decNum = int(decStr);
                    if ((baseNum == 1) and ((decNum >= -1) and (decNum <= 0))) :  #1-bit --> decNum = [-1,0] 
                            return True;
                    elif ((baseNum == 2) and ((decNum >= -2) and (decNum <= 1))) : #2-bit --> decNum = [-2,1]
                        return True;
                    elif ((baseNum == 4) and ((decNum >= -8) and (decNum <= 7))) : #4-bit --> decNum = [-8,7]
                        return True;
                    elif (baseNum == 8) : #8-bit --> decNum = [-128,127]
                        return True;
                    elif (baseNum == 16) : #16-bit --> decNum = [-32768, 32767]
                        return True;
                    elif (baseNum == 32) : #32-bit --> decNum = [-2^31, 2^31 - 1]
                        return True;
                    else :
                        #any other combination
                        return False;
                #safety return for dec-part
                return False;
        else :
            #not correct string, is not num
            return False;

        #safety-function return
        return False;
            
    @classmethod
    def is_num(cls,numStr) :
        """Arguments:
                numStr : String. Possible number in string form == Number string.

        Returns:
            True/False : bool.


        Public function used upon cleared and plain string like ' -numStr | numStr '.


        Uses class functions:
            _is_right_stringForm() : bool. To check whether number string is string and not empty.
            _is_bin_str(), _is_hex_str(), _is_dec_str() : bool. To check is number string in allowed formats.
                **number string is prepared as non-negative, so listed functions dont have to worry about dealing with negation.
                                                                    
        Does:
            1) checks if Number string: is a string and not empty.
            2) if first character in number string is '-', assumes negation, removes first character and tests 'positive' part of number string.. 
        """
        
        if (cls._is_string(numStr)) :
            negTest = numStr[0];
            if (negTest == '-') :
                #negative number expectation
                positiveStr = numStr[1:];
                if ((cls._is_hex_str(positiveStr)) or (cls._is_bin_str(positiveStr)) or (cls._is_dec_str(positiveStr))) :
                    return True;
                else :
                    #print("Calculator.is_num: Negative and invalid num string!");
                    return False;
            else :
                #positive number expectation
                if ((cls._is_hex_str(numStr)) or (cls._is_bin_str(numStr)) or (cls._is_dec_str(numStr))) :
                    return True;
                else :
                    #print("Calculator.is_num: Positive and invalid num string!");
                    return False;
                
            #safety ifRightForm-return
            return False;
        else :
            #empty or invalid string
            #print("Calculator.is_num: Invalid string!");
            return False;
    
        #for safety
        #print("Calculator.is_num: Invalid string!");
        return False;

    @classmethod
    def _is_hex_str(cls, numStr) :
        """Arguments:
                numStr : String. Possible hexadecimal number in string form.

        Returns:
            True/False : bool.


        Private function used upon cleared, positive and plain string like ' numStr '.


        Does:
            1) Checks first 2 letters, and do they represent hexadecimal form '0x'.
            2) Checks whether letters in number string are hexadecimal digits.
            3) Tries to make integer out of number string (possible overflows).
        """
        
        d = len(numStr);
        if (d > 2) :
            firstTwoChar = numStr[:2].lower();
            if (firstTwoChar == cls._numFormatStr[1]) :
                #hex
                restNum = numStr[2:].upper();
                for l in restNum :
                    if (l in cls._digitHex) :
                        continue;
                    else :
                        #print("Calculator._is_hex_str: Number starts as hex, but its not!");
                        return False;
                try :
                    testDec = int(restNum, base=16);
                except :
                    #print("Calculator._is_hex_str: Possible hex number overflow!!");
                    return False;

                #passed conditions
                return True;
            else :
                #print("Calculator._is_hex_str: Missing hex start format!");
                return False;
        else :
            # (d <= 2) --> too short string
            #print("Calculator._is_hex_str: Too short string!");
            return False;

        #safety function-return
        #print("Calculator._is_hex_str: rough end!");
        return False;

    @classmethod
    def _is_bin_str(cls, numStr) :
        """Arguments:
                numStr : String. Possible binary number in string form.

        Returns:
            True/False : bool.


        Private function used upon cleared, positive and plan string like ' numStr '.


        Does:
            1) Checks first 2 letters, and do they represent binary form '0b'.
            2) Checks whether letters in number string are binary digits.
            3) Tries to make integer out of number string (possible overflows).
        """
        
        d = len(numStr);
        if (d > 2) :
            firstTwoChar = numStr[:2].lower();
            if (firstTwoChar == cls._numFormatStr[0]) :
                #bin
                restNum = numStr[2:].upper();
                for l in restNum :
                    if (l in cls._digitBin) :
                         continue;
                    else :
                        #print("Calculator._is_bin_str: Number starts as bin, but its not!");
                        return False;
                try :
                    testDec = int(restNum, base=2);
                except :
                    #print("Calculator._is_bin_str: Possible bin number overflow!!");
                    return False;

                #passed conditions
                return True;
            else :
                #missing bin start format
                #print("Calculator._is_bin_str: Missing bin start format!");
                return False;
        else :
            # (d <= 2) --> too short string
            #print("Calculator._is_bin_str: Too short string!");
            return False;

        #safety function-return
        #print("Calculator._is_bin_str: rough end!");
        return False;
                

    @classmethod
    def _is_dec_str(cls, numStr) :
        """Arguments:
                numStr : String. Possible decimal number in string form.

        Returns:
            True/False : bool.


        Private function used upon cleared, positive and plain string like ' numStr '.


        Does:
            1) Check whether letters in number string are decimal digits.
            2) Tries to make integer out of number string (possible overflows).
        """
        
        restNum = numStr.upper();
        for l in restNum :
            if (l in cls._digitDec) :
                continue;
            else :
                #print("Calculator._is_dec_str: Invalid dec digits!");
                return False;
        try :
            testDec = int(restNum);
        except :
            #print("Calculator._is_dec_str: Possible number dec overflow!!");
            return False;
        
        return True;
        
    @classmethod
    def _is_string(cls, numStr) :
        if (isinstance(numStr, str)) :
            # if string is anything but "" (empty), its is considered as: True
            if (numStr) :
                return True;
            else :
                return False;

            #safety if-return
            return False;
        else :
            return False;

        #safety function-return
        return False;

    # ==========
    # TESTS (CLASS) EXPRESSION :
    # ==========

    @classmethod
    def is_exp(cls, expStr) :
        """Arguments:
                expStr : String. Possible expresion (with operators and parenthensis) in string form. Expression string.

        Returns:
            True/False : bool.


        Public function used upon clear and plain string like ' num ( operator num operator num ) operator ( num ) '.


        Uses class functions:
            _is_correct_groupation() : bool. Secures Expression string is in right form. See _is_correct_groupation().
        
        Does:
            1. Creates local variables, among which:
                workStr : String. Working string as a copy of Expression string, to be changed in function.
                    **keeps the same size (length) as original
                lP_list, rP_list : list of int. Stores all positions of left/right parenthensis in the Expression string.
                
            2. Checks whether Expression string: is even a string, is in right form (using _is_correct_groupation() function).
            3. Iterates through lists of positions (for exactly that many iterations) and:
                a) Determines 2 correct neighbouring left/right parenthensis, and medExp string between them.
                b) Checks whether medExp string is a correct num/operator expression.
                c) If (b), replaces whole medExp and positions of left (lastL) and right (afterR), with zeroes (clearly a number).
                d) Position of parenthensis in lists are removed.
            4. If loop ends, checks if whatever is left is num/operator expression, and if so: returns True.
        """
        
        lStr = len(expStr);
        lP_list = [];
        rP_list = [];
        i = 0;
        defNum = '0';
        workStr = expStr;

        #creating local variables of class variables
        lP = cls._groupation[0]; #')'
        rP = cls._groupation[1]; #'('
        
        if (cls._is_string(expStr)) :
            if (cls._is_correct_groupation(expStr)) :
                for i in range(lStr) :
                    c = expStr[i];
                    if (c == lP) :
                        lP_list.append(i);
                    elif (c == rP) :
                        rP_list.append(i);
                    else :
                        continue;

                lSize = len(lP_list);
                for i in range(len(lP_list)) :
                    lastL = lP_list[-1]; #last '(' position in expStr
                    afterR = [l+lastL for l in range(lStr) if (l+lastL in rP_list)][0];     #first ')' after last '(' positioned in expStr.
                                                                                            #rPos > lPos, for this checked formated string
                                                                                            #one-line function returns a list, thats why [0]
                                                                                            
                    #print("LastL: " + str(lastL) + " afterR: " + str(afterR)); ---->JUST FOR TESTING
                    medExp = workStr[(lastL+1):afterR];   #expression between neighbour '(' and ')'
                    if (cls._is_correct_operation(medExp)) :
                        lP_list.remove(lastL);
                        rP_list.remove(afterR);
                        workStr = workStr[:lastL] + defNum*(afterR-lastL+1) + workStr[(afterR+1):];
                                                                                    #whole '( exp )' is replaced by '00000' in working string
                                                                                    #enough for test function
                        print(workStr); #----->JUST FOR TESTING
                        continue;
                    else :
                        print("Between isnt exp!");
                        return False;
                if ((workStr)and(cls._is_correct_operation(workStr))) :
                    return True
                else :
                    return False;
                        
                
            else :
                #groupation of parenthensis isnt right
                return False;
        else :
            #empty or invalid string
            return False;

        #safety function-return
        return False;


    @classmethod
    def _is_correct_groupation(cls,expStr) :
        """Arguments:
                expStr : String. Possible expresion (with operators and parenthensis) in string form. Expression string.

        Returns:
            True/False : bool.


        Private function used upon cleared, plain string like ' num operator(num operator num)operator num '.


        Uses class functions:
            _is_correct_parenthensis_environment() : bool. Checks whether the environment around parenthensis is in correct form.
        
        Does:
            1. Checks whether the number of right and left parenthensis is the same in Expression string.
            2. Condition (1) in combination with: _is_correct_parenthensis_environment(), completely tests Expression string for groupation conditions.
        """

        lStr = len(expStr);

        lP_num = 0;
        rP_num = 0;

        #creating local variables of class variables.
        lP = cls._groupation[0]; #'('
        rP = cls._groupation[1]; #')'

        if (cls._is_correct_parenthensis_environment(expStr)) :
            for i in range(lStr) :
                c = expStr[i];
                if (c == lP) :
                    lP_num = lP_num + 1;
                elif (c == rP):
                    rP_num = rP_num + 1;
                else :
                    continue;
            if (lP_num == rP_num) :
                #same number of left/right parenthensis
                return True;
            else :
                return False;
                
        else :
            #istn even correct parenthensis form
            return False;
                
        #safety function-return
        return False;

    @classmethod
    def _is_correct_parenthensis_environment(cls,expStr) :
        """Arguments:
                expStr : String. Possible expresion (with operators and parenthensis) in string form. Expression string.

        Returns:
            True/False : bool.


        Private function used upon cleared, plain string like ' num operator(num operator num)operator num '.
        

        Does:
            Check whether characters in Expression string are parenthensis, and if so:
                1) Checks whether parenthensis is first or last character of Expression string.
                    a) Adjusts conditions accordingly (nextCharacter doesent exist at the end AND beforeCharacter doesent exist at beginning).
                    b) Checks if [next | before] character is allowed.
                2) Checks whether parenthensis is in the middle of Expression string.
                    a) Adjusts conditions accordingly (both next and before characters exists).
                    b) Checks if [next and before] character is allowed.
                3) Breaks the loop, and returns as False, if any of conditions arent met.
                4) If the loop ends, returns as True.
        """
        
        i = 0;
        lStr = len(expStr);

        #creating local variables of class variables. Variable _operators remained class variable.
        lP = cls._groupation[0]; #'('
        rP = cls._groupation[1]; #')'
        neg = '-';
        digits = cls._digitHex; #'[0-F]'
            #digits are sufficient for conditioning because '0x' and '0b', both starts with zero.
        
        for i in range(lStr) :
            c = expStr[i];
            
            # ==========
            # LEFT PARENTHENSIS TESTS '('
            # ==========
            
            if ((c == lP)and(i == 0)) :     # ===== '(' at first position 
                nextC = expStr[i+1];
                if (nextC == neg) :
                    #allowed to be negative
                    continue;
                elif (nextC.upper() in digits) :
                    #digit after '(' good
                    continue;
                elif (nextC == lP) :
                    #'(' in a row
                    continue;
                else :
                    #unknown after '(' isnt allowed
                    return False;
                
            elif ((c == lP)and(i == lStr-1)) :      # ===== '(' at last position
                #never allowed
                return False;
            
            elif ((c == lP)and(i < lStr-1)) :       # ===== '(' in the middle
                beforeC = expStr[i-1];
                nextC = expStr[i+1];
                if ((nextC == neg)and(beforeC in cls._operators)) :
                    #like ' + ( -2 '
                    continue;
                elif ((nextC == neg)and(beforeC == lP)) :
                    #like ' ( ( -2 '
                    continue;
                elif ((nextC.upper() in digits)and(beforeC in cls._operators)) :
                    #like ' + ( 2 '
                    continue;
                elif ((nextC == lP)and(beforeC in cls._operators)) :
                    #like ' + ( ( '
                    continue;
                elif ((nextC.upper() in digits)and(beforeC == lP)) :
                    #like ' ( ( 2 '
                    continue;
                elif ((nextC == lP)and(beforeC == lP)) :
                    #like ' ( ( ( '
                    continue;
                else :
                    #all other combinations arent allowed
                    return False;
                       
            # ==========
            # RIGHT PARENTHENSIS TEST ')'
            # ==========
                       
            elif ((c == rP)and(i == 0)) :       # ===== ')' at first position
                #never allowed
                return False;
            elif ((c == rP)and(i == lStr-1)) :  # ===== ')' at last position
                beforeC = expStr[i-1];
                if (beforeC.upper() in cls._digitHex) :
                    #digit before ')' good
                    continue;
                elif (beforeC == rP) :
                    #')' in a row
                    continue;
                else :
                    #'unknown before ')' isnt allowed
                    return False;
            elif ((c == rP)and(i < lStr-1)) :   # ===== ')' in the middle
                beforeC = expStr[i-1];
                nextC = expStr[i+1];
                if ((beforeC.upper() in digits)and(nextC in cls._operators)) :
                    #like ' 2 ) +'
                    continue;
                elif ((beforeC.upper() in digits)and(nextC == rP)) :
                    #like ' 2 ) )'
                    continue;
                elif ((beforeC == rP)and(nextC in cls._operators)) :
                    #like ' ) ) +'
                    continue;
                elif ((beforeC == rP)and(nextC == rP)) :
                    #like ' ) ) )'
                    continue;
                else :
                    #all other combinations arent allowed
                    return False;
            else :
                #all other characters in Expression string except parenthensis
                continue;
            
        #for-loop ending
        return True;
                
    @classmethod
    def _is_correct_operation(cls,expStr) :
        """Arguments:
                expStr : String. Possible expresion (only with operators) in string form. Expression string.

        Returns:
            True/False : bool.


        Private function used upon cleared, positive or negative, plain string like [operator num operator num].


        Uses class functions:
            is_num() : bool. To check are Expression string parts in right Number string form.

        Does:
            1) Check whether characters in Expression string are operators, and if so:
                a) Tests part of Expression string before occurance of an operator (negation at start is exception of the rule).
                b) Tests part of Expression string between operators.
                c) Tests part of Expression string after last operator (or if no operators at all were present).
                **with is_num() function
            2) Breaks loop and returns as False, if any of conditions arent met.
            3) If the loop ends, returns as True.
        """
        
        i = 0;
        start = 0;
        lStr = len(expStr);
        
        for i in range(lStr) :
            c = expStr[i];
            if ((c == '-')and(i == 0)) :
                #negation prefix of single number or at start of expression, it will be included in number (correct, see is_num()).
                continue;
            elif ((c in cls._operators)and(i < lStr-1)) :
                #normal mode, tests string before occurance of operator
                end = i;
                if (cls.is_num(expStr[start:end])) :
                    start = i + 1;
                    continue;
                else :
                    return False;
            elif ((c in cls._operators)and(i == lStr-1)) :
                #operator as a last character - always false
                return False;
            elif (i == lStr-1) :
                #normal mode, tests string which is without operator, or last string in expression.
                end = i + 1;
                if (cls.is_num(expStr[start:end])) :
                    continue;
                else :
                    return False;
                
            else :
                #doesent worry about other characters, is_num() will test them
                continue;

        return True;
                
        
    # ==========
    # STATIC FUNCTIONS:
    # ==========
    
    @staticmethod
    def stringClearStrip(numStr) :
        """Arguments:
                numStr : String.
                
        Returns:
            newNumStr : String.

        Uses CLASS function: !!!(not recomended for static function, but necessary) 
            _is_string() : bool. To determine whether string argument is passed.

        Does:
            Strips (clears) input string of every: 'space' ('\s') and 'new line' ('\n') characters.
        
        **uses regular expression re.sub (substitution).
        
        Raises:
            InabilityToClearStringError; if argument isnt string.
        """

        if (Calculator._is_string(numStr)) :
            newNumStr = re.sub(r"\s|\n", "", numStr);
            return newNumStr;
        else :
            raise InabilityToClearStringError("Calculator.stringClearStrip(): No string to clear!");


    @staticmethod
    def convert_output_toString(out) :
        try :
            s = 'Bin: ' + out[0] + ' , Hex: '  + out[1] + ' , Dec: ' + out[2];
        except :
            s = "Calculator.convert_output_toString : Illegal format!";
        return s;

    @staticmethod
    def history_el_toString(el) :
        """Arguments:
                el : (String,String,String,bool) | String. 
                    **(binary,hexadecimal,decimal,negation) : 3 types as String, negation as bool.
                    **expression : String.

        Returns:
            s : String.
        """
                
        try :
            s = 'Bin: ' + el[0] + ', Hex: ' + el[1] + ', Dec: ' + el[2] + ', Neg: ' + str(el[3]);
        except :
            s = el;

        return s;
