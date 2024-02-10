# Symbolic Differenciator
This python project uses the recursive properties of the derivative to differentiate a mathematical expression consisting on fundamental operators such as addition (`+`), substraction (`-`), multiplication (`*`), division (`/`) and exponentiation (`^`); alongside elementary functions (including square roots, logarithms, exponentials, trigononometric functions and hyperbolic functions). It also allows the use of undefined functions and variables with multiple lengths. 

Once executed, the program will ask for the expression to differenciate, and will be entered as a string of characteres given by keyboard. The expression must follow the usual order of operations and parenthesis. Functions must be preceded by the `\` reserved character, followed by its name, and then the argument between braces `{arg}` an example of a function might be `\func{arg}`.The derivative of unknown elements will be described by `D{unknown}`. A complete list of defined functions can be found at the end of this markdown.

Once given this imput, the program will ask the user for a derivation variable, if no input is given, the derivation variable will be considered to be `x`.

This is an example of the program execution:

`$ python3 Derivative_Calculator.py`

`Diferenciate: 2*x+\sin{x}-\f{\sqrt{x}}`

 `With respect to:`

`= 2+\cos{x}-1/(2*\sqrt{x})*D{\f{x}}`

---

### List of defined functions
> - `\sqrt{x}`     Square root of x
> - `\ln{x}`      Natural logarithm of x
> - `\exp{x}`      Exponential function of x
> - `\sin{x}`      Sine of x
> - `\cos{x}`      Cosine of x
> - `\tan{x}`      Tangent of x
> - `\arcsin{x}`   Inverse sine function of x
> - `\arccos{x}`   Inverse cosine function of x
> - `\arctan{x}`   Inverse tangent function of x
> - `\sinh{x}`     Hiperbolic sine of x
> - `\cosh{x}`     Hiperbolic cosine of x
> - `\tanh{x}`     Hiperbolic tangent of x
> - `\arcsinh{x}`  Inverse hiperbolic sine of x
> - `\arccosh{x}`  Inverse hiperbolic cosine of x
> - `\arctanh{x}`  Inverse hiperbolic tangent of x
