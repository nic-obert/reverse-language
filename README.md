# **Reverse Language**
An **esoteric programming language** that works in **reverse**, compared to most popular languages.  
Many concepts are messed up, such as array indexes starting arbitrarily at 2, or semicolons `;` at the beginning of a statement, instead of being at the end.

This project is explained in detail in a series of articles on Medium. You can find it [here](https://medium.com/@nic-obert/list/esoteric-programming-language-457a0abd14d2).

<br>

## **Table of contents**
- [**Reverse Language**](#reverse-language)
  - [**Table of contents**](#table-of-contents)
  - [**Comments**](#comments)
  - [**Variable definition**](#variable-definition)
  - [**Arithmetic**](#arithmetic)
  - [**Boolean logic**](#boolean-logic)
  - [**Comparison**](#comparison)
  - [**Function definition**](#function-definition)
  - [**Function call**](#function-call)
  - [**Control flow**](#control-flow)
    - [**If statement**](#if-statement)
    - [**While loop**](#while-loop)
  - [**Operators and operator precedence**](#operators-and-operator-precedence)
    - [**Arithmetical operators**](#arithmetical-operators)
    - [**Assignment operators**](#assignment-operators)
    - [**Comparison operators**](#comparison-operators)
    - [**Logical operators**](#logical-operators)
    - [**Other operators**](#other-operators)
    - [**Operator precedence**](#operator-precedence)
  - [**Scopes**](#scopes)
  - [**Language built-in literals**](#language-built-in-literals)
  - [**Primitive data types**](#primitive-data-types)
    - [**Number**](#number)
    - [**String**](#string)
    - [**Boolean**](#boolean)
    - [**Array**](#array)
  - [**Language built-in functions**](#language-built-in-functions)
    - [**`print`**](#print)
    - [**`println`**](#println)
    - [**`toNumber`**](#tonumber)
    - [**`toString`**](#tostring)
    - [**`toBoolean`**](#toboolean)
    - [**`getInput`**](#getinput)
    - [**`getRandom`**](#getrandom)
    - [**`exit`**](#exit)
    - [**`getLength`**](#getlength)
    - [**`sleep`**](#sleep)
    - [**`getTime`**](#gettime)
    - [**`getType`**](#gettype)

<br>

## **Comments**
```
\\ This is a comment
```

## **Variable definition**

```
;<value> = identifier
;45 = MyNumber
```

## **Arithmetic**

```
;45 23 +    \\ Sum
;45 23 -    \\ Subtraction
;45 23 *    \\ Multiplication
;45 23 /    \\ Division
;45 23 %    \\ Remainder
```

## **Boolean logic**

`true` evaluates to `0`  
`false` evaluates to `1`

```
;a b &&     \\ a AND b
;a b ||     \\ a OR b
;a !        \\ NOT a
```

## **Comparison**

```
;a b <
;a b >
;a b ==
;a b !=
;a b <=
;a b >=
```

## **Function definition**

```
{
  ;return <return value>
  <code in function body>
} (<arg1>, <arg2>) <function name>
```
Here are a few exmples of real functions:
```
\\ Recursive Fibonacci function
{
  ;return number
  {
    ;(self, number 1 -)self (self, number 2 -)self + = number
  } number 1 > if
} (self, number) fib
```
```
\\ Greet every name in the array
{
  ;return null
  ;2 = i
  ;(array)getLength 2 + = stop
  {
    ;(i)toString ": Hello " + array i [] + = string
    ;(string)println
    ;i ++
  } i stop < while
} (array) greetNames
```

## **Function call**

```
;(<arg1>, <arg2>)functionName
```

## **Control flow**

Control flow statements don't push new scopes to the stack.
Every symbol declared in their bodies is accessible from the control flow operator scope.

### **If statement**
```
{
  <code in if body>
} <condition> if
```

### **While loop**
```
{
  <code in while body>
} <condition> while
```

## **Operators and operator precedence**

### **Arithmetical operators**
```
+   \\ Sum
-   \\ Subtraction
*   \\ Multiplication
/   \\ Division
%   \\ Remainder
++  \\ Increment
--  \\ Decrement
```

### **Assignment operators**
```
=   \\ Normal assignment
+=  \\ Sum assignment
-=  \\ Subtraction assignemnt
*=  \\ Multiplication assignemnt
/=  \\ Division assignment
%=  \\ Remainder assignment
```

### **Comparison operators**
```
==  \\ Is equal to
!=  \\ Is different from
<   \\ Is less than
>   \\ Is greater than
<=  \\ Is less than or equal to
>=  \\ Is greater than or equal to
```

### **Logical operators**
```
&&  \\ Logical and
||  \\ Logical or
!   \\ Logical not
```

### **Other operators**
```
,   \\ Comma operator
[]  \\ Index operator
()  \\ Call operator
```


### **Operator precedence**

| Priority | Operators                        | Description                                                                        |
|----------|----------------------------------|------------------------------------------------------------------------------------|
| 12       | () [] {}                         | Containers                                                                         |
| 11       | ++ --                            | Increment and decrement                                                            |
| 10       | !                                | Logical not                                                                        |
| 9        | * / %                            | Multiplication, division, modulo                                                   |
| 8        | + -                              | Plus, minus                                                                        |
| 7        | > < >= <=                        | Greater than, less than, greater than or equal, less than or equal                 |
| 6        | == !=                            | Equal, not equal                                                                   |
| 5        | &&                               | Logical and                                                                        |
| 4        | \|\|                             | Logical or                                                                         |
| 3        | = += -= *= /= %=                 | Assign, assign add, assign subtract, assign multiply, assign divide, assign modulo |
| 2        | else                             | Else statement                                                                     |
| 1        | if  while return  break continue | If statement, while loop, return statement, break statement, continue statement    |
| 0        | , ;                              | Literals, identifiers, comma, semicolon                                            |



## **Scopes**

New scopes are pushed to the stack when a function is called.
Every symbol declared in their bodies is accessible only from the function scope.
Functions cannot access symbols declared in outer scopes, except built-in functions.

```
;3 = var
\\ "var" is valid in the global scope

{
  \\ var is not valid anymore in this local scope
  
  ;2 = var
  \\ this "var" is the local variable

} () function

\\ "var" is still 3 in the global scope
```

## **Language built-in literals**
```
true
false
null
```


## **Primitive data types**
Although the language is dynamically typed, there is still a simple weak typing system.

### **Number**
The `Number` data type represents a real number, either decimal or integer.
```
;0 = number
```

### **String**
The `String` data type represents a sequence of characters.  
Literal strings are enclosed in double quotes: `"this is a string"`.
```
;"hello world!" = string
```

### **Boolean**
The `Boolean` data type represents a binary true-false condition.  
The literal boolean `true` evaluates to integer `0`.  
The literal boolean `false` evaluates to integer `1`.
```
;true = booleanTrue
;false = booleanFalse
```

### **Array**
The `Array` data type is a dynamic collection of elements. 
Literal arrays are enclosed in square brackets: `[1, 2, 3]`.   
Array indexes start at 2, so to access the first element of the array, you have to access it at index 2.
```
;[0, 1, 2, "hello"] = array
;array 2 [] \\ Access first array item at index 2
```

## **Language built-in functions**

### **`print`**
Print the given value to the console, without the endline character (`\n`).
  * Arguments: `STRING`, `NUMBER`, `BOOLEAN`, `ARRAY`, `NULL`.
  * Returns: `null`.

```
;("Hello World")print
```
Output:
```
Hello World
```

### **`println`**
Print the given value to the console, including the endline character (`\n`).
  * Arguments: `STRING`, `NUMBER`, `BOOLEAN`, `ARRAY`, `NULL`.
  * Returns: `null`

```
;("Hello World")println
```
Output:
```
Hello World

```

### **`toNumber`**
Convert a value to a number, if possible.
  * Arguments: `NUMBER`, `STRING`.
  * Returns: `NUMBER`

```
;("673")toNumber
```
Output:
```
673
```

### **`toString`**
Convert a value to a string, if possible.
  * Arguments: `STRING`, `NUMBER`, `BOOLEAN`, `ARRAY`, `NULL`.
  * Returns: `STRING`

```
;(673)toString
```
Output:
```
673
```

### **`toBoolean`**
Convert a value to a boolean, if possible.
  * Arguments: `BOOLEAN`, `STRING`, `NUMBER`.
  * Returns: `BOOLEAN`

```
;(673)toBoolean
;(0)toBoolean
;(1)toBoolean
```
Output:
```
false
true
false
```

### **`getInput`**
Get user input as a string.
  * Arguments: no arguments.
  * Returns: `STRING`
```
;()getInput
```
Output:
```
Whatever you type in the console
```

### **`getRandom`**
Get a random floating point number between 0 and 1.
  * Arguments: no arguments.
  * Returns: `NUMBER`
```
;()getRandom
```
Output:
```
0.4872
```

### **`exit`**
Terminate the program.
  * Arguments: status code (`NUMBER`).
  * Returns: does not return.
```
;(0)exit
```

### **`getLength`**
Get the length of the given data structure, if possible.
  * Arguments: `STRING`, `ARRAY`.
  * Returns: `NUMBER`
```
;("Hello World")getLength
;([5, 6, 3, 4])getLength
```
Output:
```
11
4
```

### **`sleep`**
Sleep for the specified amount of seconds.
  * Arguments: `NUMBER`.
  * Returns: `null`
```
;(10.5)sleep
```

### **`getTime`**
Get the current time in seconds since the epoch.
  * Arguments: no arguments.
  * Returns: `NUMBER`
```
;()getTime
```
Output:
```
1527098981.8
```

### **`getType`**
Get the type of the given data structure, if possible.
  * Arguments: `STRING`, `ARRAY`, `NUMBER`, `BOOLEAN`, `NULL`.
  * Returns: `STRING`
```
;("Hello World")getType
;([5, 6, 3, 4])getType
;(673)getType
;(true)getType
;(null)getType
```
Output:
```
STRING
ARRAY
NUMBER
BOOLEAN
NULL
```


