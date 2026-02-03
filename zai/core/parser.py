from lark import Lark

GRAMMAR = r"""
    start: (agent | context_def | persona_def | import_stmt)+

    agent: "agent" IDENTIFIER import_stmt* (context_def | persona_def)* skill_def+

    import_stmt: "import" string

    config_file: (context_def | persona_def | import_stmt)*

    context_def: "context" IDENTIFIER "{" (context_item (","? context_item)*)? "}"
    context_item: IDENTIFIER ":" expression

    persona_def: "persona" IDENTIFIER "{" persona_item* "}"
    persona_item: IDENTIFIER (":" expression | persona_block)
    persona_block: "{" persona_fragment* "}"
    ?persona_fragment: expression | persona_if
    persona_if: "if" condition persona_block ["else" persona_block]

    skill_def: "skill" IDENTIFIER "(" [params] ")" block
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
              | start_stmt
              | skill_invoke
              | return_stmt
 
    start_stmt: "start" IDENTIFIER

    var_decl: "var" IDENTIFIER "=" expression
    assignment: target "=" expression
    ?target: IDENTIFIER | context_var
    context_var: CONTEXT_DOT IDENTIFIER
    
    if_stmt: "if" condition block ["else" block]
    while_stmt: "while" condition block
    block: "{" statement* "}"

    process_stmt: "process" expression [ "{" "extract" ":" "[" string ("," string)* "]" "}" ]
    
    ask_stmt: "ask" string
    
    exec_stmt: "exec" simple_expression [ "{" "filter" ":" "[" string ("," string)* "]" "}" ]
    
    notify_stmt: "notify" IDENTIFIER expression expression
    
    wait_stmt: "[" IDENTIFIER "," IDENTIFIER "]" "=" "wait" IDENTIFIER

    skill_invoke: "invoke" IDENTIFIER "(" [args] ")"
    args: assignment ("," assignment)*

    return_stmt: success_stmt | fail_stmt
    success_stmt: "success" expression expression
    fail_stmt: "fail" expression expression
    
    response_stmt: ("reply" | "say") expression

    ?expression: binary_op
               | simple_expression
               | template_render
               | context_var
               | persona_ref

    persona_ref: IDENTIFIER "." IDENTIFIER

    ?simple_expression: string
                      | number
                      | boolean
                      | IDENTIFIER
                      | "(" expression ")"

    boolean: "true" -> true
           | "false" -> false

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
    return Lark(GRAMMAR, start=['start', 'agent', 'config_file', 'context_def', 'persona_def'], parser='earley')
