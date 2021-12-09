# **Reverse Language**
An esoteric programming language that works in reverse

- [**Reverse Language**](#reverse-language)
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
  - [Operator precedence](#operator-precedence)
  - [Printing to the console](#printing-to-the-console)
  - [Scopes](#scopes)

<br>

## Variable definition

```
;<value> = identifier
;45 = MyNumber
```

## Arithmetic

```
;45 23 + = sumResult
;45 23 - = subtractionResult
;45 23 * = multiplicationResult
;45 23 / = divisionResult
```

## Boolean logic

`true` evaluates to `0`  
`false` evaluates to `1`

```
;a b &&
;a b ||
;a !
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
  return <return value>
  <code in function body>
} (<arg1>, <arg2>) <return type>
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

## Operator precedence

The operator precedence is the same as in C, otherwise it would be a pain to program in such a non-intuitive system.

## Printing to the console

```
;(<value to print>)print
;(<value to print>)println
```

## Scopes

The scope system is the same as in C. Only the global scope, outer scopes and and the local scope are accessible.  
The outermost scope it exactly the same as the global scope.

