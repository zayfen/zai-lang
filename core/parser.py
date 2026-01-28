from lark import Lark

GRAMMAR = r"""
    ?start: job

    job: "job" IDENTIFIER context_def conversion_def task_def+

    context_def: "context" IDENTIFIER "{" (context_item (","? context_item)*)? "}"
    context_item: IDENTIFIER ":" expression

    conversion_def: "conversion" IDENTIFIER "{" (conversion_item (","? conversion_item)*)? "}"
    conversion_item: IDENTIFIER ":" expression

    task_def: "task" IDENTIFIER "(" [params] ")" "{" statement* "}"
    params: IDENTIFIER ("," IDENTIFIER)*

    ?statement: var_decl
              | assignment
              | if_stmt
              | while_stmt
              | response_stmt
              | process_stmt
              | ask_stmt
              | exec_stmt
              | notify_stmt
              | wait_stmt
              | task_call
              | return_stmt

    var_decl: "var" IDENTIFIER "=" expression
    assignment: target "=" expression
    ?target: IDENTIFIER | context_var
    context_var: CONTEXT_DOT IDENTIFIER
    
    if_stmt: "if" condition block ["else" block]
    while_stmt: "while" condition block
    block: "{" statement* "}"

    process_stmt: "process" simple_expression [ "{" "extract" ":" "[" string ("," string)* "]" "}" ]
    
    ask_stmt: "ask" string
    
    exec_stmt: "exec" simple_expression [ "{" "filter" ":" "[" string ("," string)* "]" "}" ]
    
    notify_stmt: "notify" IDENTIFIER expression expression
    
    wait_stmt: "[" IDENTIFIER "," IDENTIFIER "]" "=" "wait" IDENTIFIER

    task_call: "call" IDENTIFIER "(" [args] ")"
    args: assignment ("," assignment)*

    return_stmt: success_stmt | fail_stmt
    success_stmt: "success" expression expression
    fail_stmt: "fail" expression expression
    
    response_stmt: ("reply" | "say") expression

    ?expression: binary_op
               | simple_expression
               | template_render
               | context_var

    ?simple_expression: string
                      | number
                      | IDENTIFIER
                      | "(" expression ")"

    binary_op: expression OPERATOR expression
    OPERATOR: "+" | "-" | "*" | "/" | "==" | "!=" | ">" | "<" | ">=" | "<=" | "&&" | "||"

    template_render: IDENTIFIER "{" args "}"

    ?condition: expression

    IDENTIFIER: /[a-zA-Z_][a-zA-Z0-9_]*/
    CONTEXT_DOT.10: "context."
    MULTILINE_STRING.2: /\"\"\"(.|\n)*?\"\"\"/
    ESCAPED_STRING: /"([^"\\\r\n]|\\.)*"/
    string: ESCAPED_STRING | MULTILINE_STRING
    number: SIGNED_NUMBER

    %import common.SIGNED_NUMBER
    %import common.WS
    %import common.CPP_COMMENT
    %ignore WS
    %ignore CPP_COMMENT
"""

def get_parser():
    return Lark(GRAMMAR, start='job', parser='lalr')

if __name__ == "__main__":
    parser = get_parser()
    print("AgentLang Parser initialized successfully.")
