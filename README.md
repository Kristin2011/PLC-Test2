# PLC-Test2

### This is a repo for PLC test 2 for Chaoqun Li

Below are the rules for the test file:

1. The test file can be empty
2. if the file is not empty, it must starts with ``void main()`` and end with ``end``, eg ``void main '(' ')' <stmt>* end``
3. A statement ``<stmt>`` can be a declaration statement ``<declaration_stmt> ``, assignemnt statement``<assignment_stmt>``, loop statement``<when_stmt>``, or a if statement``<if_satisfied_stmt>``
	i. Declaration statement, 
		``<declaration_stmt> --> ( int_one | int_two | int_four | 								int_eight ) identifier ';'``
		Explanation: int_one、int_two、int_four、int_eight are four kinds of available data type, identifier is the variable name.
		
	#### e.g. ``int_one aaaaaa;``
	ii. Assignemnt statement
	``<assignment_stmt> --> identifier '=' <expression> ';'``
	Explanation: the variable with be equal to a expression
	#### e.g. ``aaaaaa=(3-4)*5+bbbbbb;``
	iii. Loop statement
	``<when_stmt> --> when '(' <bool_expr> ')' '{' <stamt>* '}'
<bool_expr> --> <expression> ( '<=' | '>=' | '<' | '>' |'==' | '!=' ) <expression>``	
Explanation: keyword ``when`` can be treated similiar to while in **C**  language
	#### e.g. ``when(3<7){int_one aaaaaa;}``
	iV. If statement
	``<if_satisfied_stmt> --> if_satisfied '(' <bool_expr> ')' '{' <stmt>* '}' [ or '{' <stmt>* '}']``
	Explanation: keyword ``if_satisfied`` 	 can be treated similiar to ``if`` in **C** language, but ``else`` is replaced with ``or`` 
	#### e.g. ``if_satisfied(3<7){int_one aaaaaa;}``