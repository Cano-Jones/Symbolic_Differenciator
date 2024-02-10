#!/usr/bin/env python
"""
Derivative_Calculator.py

This program computes the derivative of a given expression entered by keyboard as a string.

Expressions might include variables and constants of multiple lengths (such as 'const_1', 'vel' 'Force'...), usual operators (+, -, *, /, ^) and functions.
Functions must be preceded by a \ symbol, and the argument between braces {}.
    Standard elementary functions are defined:
        \sqrt{x}     Square root of x
        \ln{x}       Natural logarithm of x
        \exp{x}      Exponential function of x
        \sin{x}      Sine of x
        \cos{x}      Cosine of x
        \tan{x}      Tangent of x
        \arcsin{x}   Inverse sine function of x
        \arccos{x}   Inverse cosine function of x
        \arctan{x}   Inverse tangent function of x
        \sinh{x}     Hiperbolic sine of x
        \cosh{x}     Hiperbolic cosine of x
        \tanh{x}     Hiperbolic tangent of x
        \arcsinh{x}  Inverse hiperbolic sine of x
        \arccosh{x}  Inverse hiperbolic cosine of x
        \arctanh{x}  Inverse hiperbolic tangent of x
    User might use undefined functions with the same syntax, the program will return D{\f{x}} for the derivative of the undefine function \f{x}.

This program asks for two inputs: The expression to derivate, and the variable of derivation (if no variable is given, it will be considered to be 'x').

Example of operation:

        $ python3 Derivative_Calculator.py
        Diferenciate: 2*x+\sin{x}-\f{\sqrt{x}}
        With respect to:
        = 2+\cos{x}-1/(2*\sqrt{x})*D{\f{x}}

:Author: Cano Jones, Alejandro
:Date: March 2023
:LinkedIn: www.linkedin.com/in/canojonesalejandro
:GitHub: https://github.com/Cano-Jones
"""

#Allowed operators + the function denominator \
Operators={'+', '-', '*', '/', '^', '\\'}

def IsOnlyTerm(expression):
    """
    IsOnlyTerm(expression)

    Determines if 'expression' doesn't include sums, products or powers (excluding those that are part of the argument of a function).
    It returns a boolean value:
        True if the expression is a unique term, False otherwise.

    Some examples might be:

    IsOnlyTerm('2*x+\sqrt{2*x}') -> False
    IsOnlyTerm('3*y') -> False
    IsOnlyTerm('\sqrt{2*x}') -> True
    IsOnlyTerm('value_2') -> True
    """

    #If the given expression doesnt include any operator, then per definition must be only one term.
    if set(expression).intersection(Operators)==set(): return True

    #An exception is when the oprators are part of the argument of a function \func{arg}

    #If the expression doesnt start with \ and end with } it cannot be only one term (there would be other things)
    elif expression[0]=='\\' and expression[-1]=='}':

        """
        There could be two functions in the same expression \f_1{arg_1}+\f_2{arg_2} and still get pass the conditional,
        to verify that there is only one function (excepting others present on arguments), we count the difference in the
        amount of { and } pass the firt {; if the diference is negative at some point, then there must be a secont function. 
        """

        #we find the index of the first {
        first_brace=0
        for index in range(2,len(expression)-1):
            if expression[index]=='{':
                first_brace=index
                break
        
        #On this loop we compute the difference of {,} at each position pass the first { if it becomes negative, then there are more terms
        braces_index=0
        for index in range(first_brace, len(expression)-1):
            if expression[index]=='{': braces_index+=1
            elif expression[index]=='}': braces_index-=1

            if braces_index==0: return False
        return True
    
    #Another exception is when an undefined derivative appears D{\funct{arg}}

    #The undefined derivatives start with D and end with }
    elif expression[0]=='D' and expression[-1]=='}':

        #Similar to the previous algorithm, we must check if there are other Derivatives or Functions passed the first derivative

        first_brace=0
        for index in range(1,len(expression)-1):
            if expression[index]=='{':
                first_brace=index
                break

        braces_index=0
        for index in range(first_brace, len(expression)-1):
            if expression[index]=='{': braces_index+=1
            elif expression[index]=='}': braces_index-=1

            if braces_index==0: return False
        return True
            
    #If there are operators in the expression, and it isnt a function or a undefined derivative, then there must be other terms

    else: return False
        

def Clean_Expression(expression):
    """
    Clean_Expression(expression)

    This function tries to make the input expression more readable by erasing some useless information such as zero sums or unity products.

    Clean_Expression('1*x)  -> x
    """

    #Operators are consider to be sufficiently 'clean'
    if expression in Operators: return expression


    #More than one run of the algorithm might be needed,
    run=True
    #We keep 'cleaning' the expression until it stops changing
    while run:

        original= expression

        expression=expression.replace('1*', '')
        expression=expression.replace('(1)*', '')
        expression=expression.replace('*1', '')
        expression=expression.replace('*(1)', '')
        expression=expression.replace('(0+', '(')
        expression=expression.replace('(0-', '(-')
        expression=expression.replace('+0)', ')')
        expression=expression.replace('-0)', '')

        if original==expression: run=False

    #The cleaned expression is returned
    return expression

def GetArg(function):
    """
    GetArg(function)

    Given a function (e.g. \sin{arg}) this algorithm return the argument (arg) of said function as a string.
    """

    #The input must be only one function to make sense, if not, False value is returned
    if not IsOnlyTerm(function) and function[0]=='\\': return False

    #We find the position of the first brace {
    first_brace=0
    for index in range(1,len(function)-1):
        if function[index]=='{':
            first_brace=index+1
            break
    #The return argument must be between the first brace and the end brace }
    return function[first_brace:-1]


def Sum_Separate(expression):
    """
    Sum_Separate(expression)

    This functions creates a list of the monomials present on expression.
    Each monomial is checked for useless parenthesis, before returning the list of monomials alingside the addition operator that precedes it (+-)

    Sum_Separate('-(\sqrt{2+x}*2)+3/(2+x)') -> ['-', '\sqrt{2+x}*2', '+', '3/(2+x)']
    """

    #If the expression is an empty string, then thats the list
    if expression=='': return ['']
    #If there are no additions or subtractions, then thats the list
    if '+' not in expression and '-' not in expression: return [expression]
    
    Sums=[] #List that will record the operators and monomials
    term_start=0 #Variable that will record the index of the string in which the monomial stars

    #We got to skip monomials that might be between parenthesis or be part of function arguments
    parenthesis_index=0
    braces_index=0
    #This loop will check if a given string element is + or - and if its between parenthesis or is inside a function argument
    for i in range(len(expression)):
        #We keep trak of the number of parenthesis and braces to check wether we are or not out of exceptions
        if expression[i]=='(': parenthesis_index+=1
        elif expression[i]==')': parenthesis_index-=1
        elif expression[i]=='{': parenthesis_index+=1
        elif expression[i]=='}': parenthesis_index-=1
        #If element is + or - and we are out of parenthesis and braces we add the operator and previous monomial to list
        elif expression[i] in '+-' and parenthesis_index==0 and braces_index==0:
            if i>0:
                    Sums.append(expression[term_start:i])
                    Sums.append(expression[i])
            else: Sums.append(expression[i])
            term_start=i+1
    if term_start!=len(expression): Sums.append(expression[term_start:])
    

    #Over this loop, we check wether present parenthesis are needed, if not, we erase them
    for index in range(len(Sums)):
        aux=False
        #If the monomial starts with ( and ends with ) it might be of the form '(2*x/3)'  and thus useless
        if Sums[index][0]=='(' and Sums[index][-1]==')':
            if Sums[index].count('(')==1: Sums[index]=Sums[index][1:-1]
            else:
                for i in range(1, len(Sums[index])-1):
                    if Sums[index][i]=='(': parenthesis_index+=1
                    elif Sums[index][i]==')': parenthesis_index-=1

                    if parenthesis_index<0: aux=True

                if not aux: Sums[index]=Sums[index][1:-1]
    
    #The list is returned
    return Sums

def Prod_Separate(expression):
    """
    Prod_Separate(expression)

    The function returns a list of three elements, consisting on two expressions and an operand '*' or '/' if there are such operators on the original expression.
    The first element of the list will be either a product or the denominator of a fraction, the second element, will be the operation between the other elements and the
    third element will be the rest of the expression given as an input. 
    For an input consisting on multiple products and division, it will order the elements first on products and then divisions.

    Prod_Separate('2*x*(2+y)/\ln{x}*y^2/2) -> ['2', '*' 'x*(2+y)*y^2/(\ln{x}*2)']
    Prod_Separate('(2+3*(x*\ln{y}))/2/(3*x)) -> ['2+3*(x*\ln{y})', '/', 2*(3*x)]
    """

    if expression=='': return [expression] #For an empty expression, the result is an empty list
    if '*' not in expression and '/' not in expression: return [expression] #If there are no product or division operands, then there is nothing to separate

    Prods=[] #List where each element of the expression will be listed
    term_start=0 #Position in which each element of expression starts

    parenthesis_index=0 #Counter of parenthesis
    braces_index=0 #Counter of braces

    #Loop of each element in expression
    for i in range(len(expression)):
        #We keep track of we are inside something
        if expression[i]=='(': parenthesis_index+=1
        elif expression[i]==')': parenthesis_index-=1
        elif expression[i]=='{': braces_index+=1
        elif expression[i]=='}': braces_index-=1

        #if we find a * or / operand and we arent inside something, we need to record it
        elif expression[i] in '*/' and parenthesis_index==0 and braces_index==0:
            Prods.append(expression[term_start:i])
            Prods.append(expression[i])
            term_start=i+1
    #we need to add the whole expression
    if term_start!=len(expression): Prods.append(expression[term_start:])

    #Here we get rid of unnecessary parenthesis
    for index in range(len(Prods)):
        aux=False
        if Prods[index][0]=='(' and Prods[index][-1]==')':
            if Prods[index].count('(')==1: Prods[index]=Prods[index][1:-1]
            else:
                for i in range(1, len(Prods[index])-1):
                    if Prods[index][i]=='(': parenthesis_index+=1
                    elif Prods[index][i]==')': parenthesis_index-=1

                    if parenthesis_index<0: aux=True

                if not aux: Prods[index]=Prods[index][1:-1]
    
    #If there is a division, we need to order the elements in such a way that all divisors are a single element at the end
    if '/' in Prods:
        #If there are only 3 elements, the list is already ordered
        if len(Prods)==3: return Prods

        products=[Prods[0]] #List consisting on all products
        divisors=[] #List consisting on all divisors
        #We sort all elements into this two lists
        for index in range(1,len(Prods),2):
            if Prods[index]=='*':
                products.append(Prods[index+1])
            if Prods[index]=='/': divisors.append(Prods[index+1])
        
        if len(products)>1: #If there are more than on product, we need to create the third eelement of the returned list as the denominator and numerator of a fraction
            aux=''
            for prod in products[1:]:
                if aux=='': aux+=prod if IsOnlyTerm(prod) else '('+prod+')'
                else: aux+='*'+prod if IsOnlyTerm(prod) else '*('+prod+')'
            aux+='/'
            for div in divisors:
                if aux[-1]=='/': aux+= div if IsOnlyTerm(div) else '('+div+')'
                else: aux+= '/'+div if IsOnlyTerm(div) else '/('+div+')'
            
            return [Prods[0], '*', aux]
    
        else: #If there is only one product, it will be the denominator of the fraction
            aux=''
            for div in divisors:
                if aux=='': aux+= div if IsOnlyTerm(div) else '('+div+')'
                else: aux+= '*'+div if IsOnlyTerm(div) else '*('+div+')'
            
            return [Prods[0], '/', aux]
    
    if len(Prods)==3: return Prods
    #We create two expressions consisting on a first product and the rest of products on a single expression
    aux=''
    for prod in Prods[2:]:
        if prod=='*': aux+='*'
        else : aux+=prod if IsOnlyTerm(prod) else '('+prod+')'
    
    if aux=='': return [Prods[0]]

    return [Prods[0], '*', aux]



def Exponen_Separate(expression):
    if '^' not in expression: return [expression]


    Expons=[]
    term_start=0

    parenthesis_index=0
    braces_index=0

    for index in range(len(expression)):
        if expression[index]=='(': parenthesis_index+=1
        elif expression[index]==')': parenthesis_index-=1
        elif expression[index]=='{': braces_index+=1
        elif expression[index]=='}': braces_index-=1

        elif expression[index]=='^' and parenthesis_index==0 and braces_index==0:
            if index==0: Expons.append(expression[:index])
            else:
                Expons.append(expression[term_start:index])
                Expons.append('^')
                term_start=index+1
    if term_start!=len(expression): Expons.append(expression[term_start:])

    for index in range(len(Expons)):
        aux=False
        if Expons[index][0]=='(' and Expons[index][-1]==')':
            if Expons[index].count('(')==1: Expons[index]=Expons[index][1:-1]
            else:
                for i in range(1, len(Expons[index])-1):
                    if Expons[index][i]=='(': parenthesis_index+=1
                    elif Expons[index][i]==')': parenthesis_index-=1

                    if parenthesis_index<0: aux=True

                if not aux: Expons[index]=Expons[index][1:-1]
    
    aux=''
    for exp in Expons[2:]:
        if exp!='^':
            if aux=='': aux+=exp if IsOnlyTerm(exp) else '('+exp+')'
            else: aux+='^'+exp if IsOnlyTerm(exp)==1 else '^('+exp+')'

    return [Expons[0], '^', aux]



def Compute_Derivative(expression, var='x'):
    """
    Compute_Derivative(expression, var='x')

    As its name depicts, this is the main function in which the derivatives are computed.
    Two inputs are given: the expression to derivate and the avriable upon to derivate to.

    The functions makes use of the recursivity of the derivative rules, mainly the chain rules.
    It returns a string containing the derivative.
    """
    
    #It is considered that the derivative of a operator is itself (D{+}=+) for simplicity
    if expression in Operators: return expression

    #If there are no operators in the expresion, then its the simplest case: either is the variable or not... 
    if set(expression).intersection(Operators)==set():
        if expression==var: return '1' #D_x{x}=1
        else: return '0' #D_x{y}=0

    #If the expression does have some operator, then derivation rules must be met
    Result='' #String variable in which the derivative will be written

    #The simplest case of derivative is the sum (Derivative of the sum is the sum of derivatives)

    Sums=Sum_Separate(expression) #We check how many monomials are in the expression
    if len(Sums)>1: #If there are more tan one monomials, then there are sums or substractions
        for term in Sums: #For each element of the Sums list (either monomial or + or -)
            D_term=Compute_Derivative(term, var) #We compute the derivative of such element
            
            if D_term=='0': #If the rerivative is zero, we can negletc the term
                if Result=='': continue
                elif Result[-1] in '+-': Result=Result[:-1]
                continue

            if term in'+-': #If the element is an operator we consider if its needed to be added (+ at the begining is not necesary)
                if term=='+' and Result=='': continue
                Result+=term

            #Otherwise, we add the monomial (with parenthesis if needed, examples might be -(2+x))

            elif Result=='' or Result[-1]=='+': Result+=D_term

            else:
                aux=D_term
                Result+= aux if len(Sum_Separate(aux))==1 else '('+aux+')'
        if Result=='': return '0'

        #We return the string result
        return Clean_Expression(Result)
    
    #The next simplest case is the monomial with products, here we use the product rule or division rule
    Prods=Prod_Separate(expression) #We check how many products are in the expression
    if len(Prods)>1: #If there are more tan one product, then there are * or /

        #The expression can be written as first@second (where @ is either * or /), rules need the derivative of the two terms

        D_first=Clean_Expression(Compute_Derivative(Prods[0], var))
        D_second=Clean_Expression(Compute_Derivative(Prods[2], var))
        Result=''#String variable in which the derivative will be written

        if Prods[1]=='*': #If @ is * then we apply the product rule D{a*b}=D{a}*b+a*D{b}
            if D_first=='0':
                if D_second=='0': return '0'

                Result+=Prods[0]+'*' if len(Sum_Separate(Prods[0]))==1 else '('+Prods[0]+')*'
                Result+=D_second if len(Sum_Separate(D_second))==1 else '('+D_second+')'
            
            elif D_second=='0':
                Result+=D_first+'*' if len(Sum_Separate(D_first))==1 else '('+D_first+')*'
                Result+=Prods[2] if len(Sum_Separate(Prods[2]))==1 else '('+Prods[2]+')'
            else:
                Result+=D_first+'*' if len(Sum_Separate(D_first))==1 else '('+D_first+')*'
                Result+=Prods[2]+'+' if len(Sum_Separate(Prods[2]))==1 else '('+Prods[2]+')+'
                Result+=Prods[0]+'*' if len(Sum_Separate(Prods[0]))==1 else '('+Prods[0]+')*'
                Result+=D_second if len(Sum_Separate(D_second))==1 else '('+D_second+')'
        
        elif Prods[1]=='/': #If @ is / then we apply the division rule D{a/b}=(D{a}*b-a*D{b})/b^2
            if D_first=='0':
                if D_second=='0': return '0'

                Result+='-'+Prods[0] if len(Sum_Separate(Prods[0]))==1 else '('+Prods[0]+')'
                Result+='*'+D_second if len(Sum_Separate(D_second))==1 else '('+D_second+')'
                Result+= '/'+Prods[2]+'^2' if IsOnlyTerm(Prods[2]) else '/('+Prods[2]+')^2'
            
            elif D_second=='0':
                Result+=D_first+'/' if len(Sum_Separate(D_first))==1 else '('+D_first+')/'
                Result+=Prods[2] if IsOnlyTerm(Prods[2]) else '('+Prods[2]+')'
            
            else:
                Result+='('+D_first+'*' if len(Sum_Separate(D_first))==1 else '(('+D_first+')*'
                Result+=Prods[2]+'-' if len(Sum_Separate(Prods[2]))==1 else '('+Prods[2]+')-'
                Result+=Prods[0]+'*' if len(Sum_Separate(Prods[0]))==1 else '('+Prods[0]+')*'
                Result+=D_second+')/' if len(Sum_Separate(D_second))==1 else '('+D_second+'))/'
                Result+= Prods[2]+'^2' if IsOnlyTerm(Prods[2]) else '('+Prods[2]+')^2'

                
        #We return the result
        return Clean_Expression(Result)

    #If the expression is not a monomial or a product, it might be a power a^b
    Expons=Exponen_Separate(expression) #We check how many exponents are in the expression
    if len(Expons)>1: #If the length of the list is more than one, there are exponents

        #Exponent rule D{a^b}=a^b*(D{b}*\ln{a}+b*D{a}/a)
        D_first=Clean_Expression(Compute_Derivative(Expons[0], var))
        D_second=Clean_Expression(Compute_Derivative(Expons[2], var))
        Result=''#String variable in which the derivative will be written

        if D_first=='0':
            if D_second=='0': return '0'

            Result+=Expons[0]+'^' if IsOnlyTerm(Expons[0]) else '('+Expons[0]+')^'
            Result+=Expons[2]+'*' if IsOnlyTerm(Expons[2]) else '('+Expons[2]+')*'
            Result+=D_second if len(Sum_Separate(D_second))==1 else '('+D_second+')'
            if Expons[0]=='1': return '0'
            else: Result+='*\ln{'+Expons[0]+'}'
        
        elif D_second=='0':
            Result+=Expons[2]+'*' if len(Sum_Separate(Expons[2]))==1 else '('+Expons[2]+')*'
            if Expons[2]!='1':
                Result+=Expons[0] if len(Sum_Separate(Expons[0]))==1 else '('+Expons[0]+')'
                Result+='^('+Expons[2]+'-1)'
            Result+='*'+D_first if len(Sum_Separate(D_first)) else '*('+D_first+')'
        
        else:
            Result+=Expons[0]+'^' if IsOnlyTerm(Expons[0]) else '('+Expons[0]+')^'
            Result+=Expons[2]+'*(' if IsOnlyTerm(Expons[2]) else '('+Expons[2]+')*('
            Result+=D_second+'*' if len(Sum_Separate(D_second))==1 else '('+D_second+')*'
            Result+='\ln{'+Expons[0]+'}+'
            Result+=Expons[2]+'*' if IsOnlyTerm(Expons[2]) else '('+Expons[2]+')*'
            Result+=D_first+'/' if len(Sum_Separate(D_first)) else '('+D_first+')/'
            Result+=Expons[0]+')' if IsOnlyTerm(Expons[0]) else '('+Expons[0]+'))'
        
        #We return the result
        return Clean_Expression(Result)
    
    #Second to last posibility are functions with arguments
    if IsOnlyTerm(expression) and expression[0]=='\\':
        arg=GetArg(expression) #We get the argument of the function
        D_arg=Clean_Expression(Compute_Derivative(arg, var)) #And its derivative
        if D_arg=='0': return '0' #If the derivative of the argument is zero, the derivative of the function is zero
        Result=''#String variable in which the derivative will be written

        #Here we apply the chain rule D{\f{arg}}=D{arg}*D{\f{x}}
        #We check if the function is defined, if so, we return the corresponding derivative
        if expression[:6]=='\sqrt{':
            Result+=D_arg if len(Sum_Separate(D_arg))==1 else '('+D_arg+')'
            Result+='/(2*\sqrt{'+arg+'})'

        elif expression[:4]=='\ln{':
            Result+=D_arg+'/' if len(Sum_Separate(D_arg))==1 else '('+D_arg+')/'
            Result+=arg if IsOnlyTerm(arg) else '('+arg+')'
        
        elif expression[:5]=='\exp{':
            Result+=D_arg if len(Sum_Separate(D_arg))==1 else '('+D_arg+')'
            Result+='*\exp{'+arg+'}'
        
        elif expression[:5]=='\sin{':
            Result+='\cos{'+arg+'}*'
            Result+=D_arg if len(Sum_Separate(D_arg))==1 else '('+D_arg+')'
        
        elif expression[:5]=='\cos{':
            Result+='-\sin{'+arg+'}*'
            Result+=D_arg if len(Sum_Separate(D_arg))==1 else '('+D_arg+')'
        
        elif expression[:5]==r'\tan{':
            Result+=D_arg if len(Sum_Separate(D_arg))==1 else '('+D_arg+')'
            Result+='\cos{'+arg+'}^2'

        elif expression[:8]==r'\arcsin{':
            Result+=D_arg if len(Sum_Separate(D_arg))==1 else '('+D_arg+')'
            Result+='/\sqrt{1-'+arg+'^2}' if IsOnlyTerm(arg) else '/\sqrt{1-('+arg+')^2}'

        elif expression[:8]==r'\arccos{':
            Result+='-'+D_arg if len(Sum_Separate(D_arg))==1 else '-('+D_arg+')'
            Result+='/\sqrt{1-'+arg+'^2}' if IsOnlyTerm(arg) else '/\sqrt{1-('+arg+')^2}'
        
        elif expression[:8]==r'\arctan{':
            Result+=D_arg if len(Sum_Separate(D_arg))==1 else '('+D_arg+')'
            Result+='/(1+'+arg+'^2)' if IsOnlyTerm(arg) else '/(1+('+arg+')^2)'
        
        elif expression[:6]=='\sinh{':
            Result+=D_arg if len(Sum_Separate(D_arg))==1 else '('+D_arg+')'
            Result+='*\cosh{'+arg+'}'

        elif expression[:6]=='\cosh{':
            Result+=D_arg if len(Sum_Separate(D_arg))==1 else '('+D_arg+')'
            Result+='*\sinh{'+arg+'}'
        
        elif expression[:6]==r'\tanh{':
            Result+=D_arg if len(Sum_Separate(D_arg))==1 else '('+D_arg+')'
            Result+='/\cosh{'+arg+'}^2'
        
        elif expression[:9]==r'\arcsinh{':
            Result+=D_arg if len(Sum_Separate(D_arg))==1 else '('+D_arg+')'
            Result+='/\sqrt{1+'+arg+'^2}' if IsOnlyTerm(arg) else '/\sqrt{1-('+arg+')^2}'
        
        elif expression[:9]==r'\arccosh{':
            Result+=D_arg if len(Sum_Separate(D_arg))==1 else '('+D_arg+')'
            Result+='/\sqrt{'+arg+'^2-1}' if IsOnlyTerm(arg) else '/\sqrt{('+arg+')^2-1}'
        
        elif expression[:9]==r'\arctanh{':
            Result+=D_arg if len(Sum_Separate(D_arg))==1 else '('+D_arg+')'
            Result+='/(1-'+arg+'^2)' if IsOnlyTerm(arg) else '/(1-('+arg+')^2)'

        
        else: #If its not defined, the the returned string is just the chain rule
            Result+=D_arg if len(Sum_Separate(D_arg))==1 else '('+D_arg+')'
            Result+= '*D{'+expression
            Result=Result[:-len(arg)-1]
            Result+=var+'}}'

        #We return the result
        return Clean_Expression(Result)
            
    #If no other conditional, the derivative is unkwnown
    return 'D{'+Clean_Expression(expression)+'}'

######################################################

def Main():
    input_ex=input('Diferenciate: ')
    var=input('With respect to: ')

    if var=='': var='x'

    print('= '+Compute_Derivative(input_ex, var))

if __name__ == "__main__":
    Main()

