# **Reverse Language**
An esoteric programming language that works in reverse, compared to most popular languages.  
Many concepts are messed up, such as array indexes starting arbitrarily at 2, or semicolons `;` at the beginning of a statement, instead of being at the end.

This project is explained in detail in a series of articles on Medium. You can find it [here](https://medium.com/@nic-obert/list/esoteric-programming-language-457a0abd14d2).

<br>

## Table of contents
- [**Reverse Language**](#reverse-language)
  - [Table of contents](#table-of-contents)
  - [Comments](#comments)
  - [Variable definition](#variable-definition)
  - [Arithmetic](#arithmetic)
  - [Boolean logic](#boolean-logic)
  - [Comparison](#comparison)
  - [Function definition](#function-definition)
  - [Function call](#function-call)
  - [Control flow](#control-flow)
    - [If statement](#if-statement)
    - [While loop](#while-loop)
    - [For loop](#for-loop)
  - [Operators and operator precedence](#operators-and-operator-precedence)
    - [Arithmetical operators](#arithmetical-operators)
    - [Assignment operators](#assignment-operators)
    - [Comparison operators](#comparison-operators)
    - [Logical operators](#logical-operators)
    - [Other operators](#other-operators)
    - [Operator precedence](#operator-precedence)
  - [Printing to the console](#printing-to-the-console)
  - [Scopes](#scopes)
  - [Language built-in literals](#language-built-in-literals)
  - [Primitive data types](#primitive-data-types)
    - [Number](#number)
    - [String](#string)
    - [Boolean](#boolean)
    - [Array](#array)
  - [Language built-in functions](#language-built-in-functions)

<br>

## Comments
```
\\ this is a comment
```

## Variable definition

```
;<value> = identifier
;45 = MyNumber
```

## Arithmetic

```
;45 23 +    \\ sum
;45 23 -    \\ subtraction
;45 23 *    \\ multiplication
;45 23 /    \\ division
;45 23 %    \\ remainder
```

## Boolean logic

`true` evaluates to `0`  
`false` evaluates to `1`

```
;a b &&     \\ a AND b
;a b ||     \\ a OR b
;a !        \\ NOT a
```

## Comparison

```
;a b <
;a b >
;a b ==
;a b !=
;a b <=
;a b >=
```

## Function definition

```
{
  ;return <return value>
  <code in function body>
} (<arg1>, <arg2>) <function name>
```
Here are a few exmples of real functions:
```
\\ Fibonacci function
{
  ;return number
  {
    ;(number 1 -)fib (number 2 -)fib + = number
  } number 1 >
} (number) fib
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

## Function call

```
;(<arg1>, <arg2>)functionName
```

## Control flow

### If statement
```
{
  <code in if body>
} <condition> if
```

### While loop
```
{
  <code in while body>
} <condition> while
```

### For loop
```
{
  <code in for loop body>
} <condition> for
```

## Operators and operator precedence

### Arithmetical operators
```
+   \\ sum
-   \\ subtraction
*   \\ multiplication
/   \\ division
%   \\ remainder
++  \\ increment
--  \\ decrement
```

### Assignment operators
```
=   \\ normal assignment
+=  \\ sum assignment
-=  \\ subtraction assignemnt
*=  \\ multiplication assignemnt
/=  \\ division assignment
%=  \\ remainder assignment
```

### Comparison operators
```
==  \\ is equal to
!=  \\ is different from
<   \\ is less than
>   \\ is greater than
<=  \\ is less than or equal to
>=  \\ is greater than or equal to
```

### Logical operators
```
&&  \\ and
||  \\ or
!   \\ not
```

### Other operators
```
,   \\ comma operator
[]  \\ index operator
()  \\ call operator
```


### Operator precedence

The operator precedence is the same as in C, otherwise it would be a pain to program in such a non-intuitive system.



## Printing to the console

```
;(<value to print>)print
;(<value to print>)println
```

## Scopes

The scope system is the same as in C. Only the global scope, outer scopes and and the local scope are accessible.  
The outermost scope it exactly the same as the global scope.

```
;3 = var
\\ "var" is valid in the global scope

{
  \\ var is not valid anymore in this local scope
  
  ;2 = var
  \\ this "var" is the local variable
}

\\ "var" is still 3 in the global scope
```

## Language built-in literals
```
true
false
null
```


## Primitive data types
Although the language is dynamically typed, there is still a simple weak typing system.

### Number
The `Number` data type represents a real number, either decimal or integer.
```
;0 = number
```

### String
The `String` data type represents a sequence of characters.  
Literal strings are enclosed in double quotes: `"this is a string"`.
```
;"hello world!" = string
```

### Boolean
The `Boolean` data type represents a binary true-false condition.  
The literal boolean `true` evaluates to integer `0`.  
The literal boolean `false` evaluates to integer `1`.
```
;true = booleanTrue
;false = booleanFalse
```

### Array
The `Array` data type is a dynamic collection of elements. 
Literal arrays are enclosed in square brackets: `[1, 2, 3]`.   
Array indexes start at 2, so to access the first element of the array, you have to access it at index 2.
```
;[0, 1, 2, "hello"] = array
;array 2 [] \\ access first array item at index 2
```

## Language built-in functions
```
\\ print to the console
;("hello ")print
;("world")println

\\ convert a value to a number, if possible
;("673")toNumber

\\ convert a value to a string, if possible
;(673)toString

\\ convert a value to a boolean, if possible
;(1)toBoolean   \\ returns false
;(0)toBoolean   \\ returns true

\\ get user input as a string
;()getInput

\\ get a random integer number
;()getRandom

\\ terminate the program
;(<integer status code>)exit

\\ get the length of the given data structure, if possible
;("hello world")getLength   \\ 11
;([5, 6, 3, 4])getLength    \\ 4
```

