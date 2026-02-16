# MinLang Compiler Architecture Diagram

## System Architecture (Mermaid Format)

```mermaid
graph TB
    subgraph Input
        A[MinLang Source Code<br/>.ml file]
    end
    
    subgraph "Phase 1: Lexical Analysis"
        B[Lexer/Tokenizer]
        C[Token Stream]
    end
    
    subgraph "Phase 2: Syntax Analysis"
        D[Parser]
        E[Abstract Syntax Tree<br/>AST]
    end
    
    subgraph "Phase 3: Semantic Analysis"
        F[Semantic Analyzer]
        G[Symbol Table]
        H[Type Checker]
        I[Annotated AST]
    end
    
    subgraph "Phase 4: Intermediate Code Generation"
        J[IR Generator]
        K[Three-Address Code<br/>TAC]
    end
    
    subgraph "Phase 5: Optimization"
        L[Optimizer]
        M[Optimized TAC]
    end
    
    subgraph "Phase 6: Code Generation"
        N[Code Generator]
        O[Target Code]
    end
    
    subgraph Output
        P[Executable/<br/>VM Bytecode]
    end
    
    A --> B
    B --> C
    C --> D
    D --> E
    E --> F
    F --> G
    F --> H
    G --> I
    H --> I
    I --> J
    J --> K
    K --> L
    L --> M
    M --> N
    N --> O
    O --> P
    
    style A fill:#e1f5fe
    style B fill:#fff9c4
    style D fill:#fff9c4
    style F fill:#fff9c4
    style J fill:#fff9c4
    style L fill:#fff9c4
    style N fill:#fff9c4
    style P fill:#c8e6c9
    
    classDef implemented fill:#a5d6a7
    classDef partial fill:#fff59d
    classDef planned fill:#ffccbc
    
    class B,C,D,E implemented
    class F,G,H,I partial
    class J,K,L,M,N,O planned
```

## Detailed Component Architecture

```mermaid
graph LR
    subgraph "Lexer Module"
        A1[token.py<br/>Token Definitions]
        A2[lexer.py<br/>Lexer Implementation]
    end
    
    subgraph "Parser Module"
        B1[ast_nodes.py<br/>AST Node Classes]
        B2[parser.py<br/>Recursive Descent Parser]
    end
    
    subgraph "Semantic Module"
        C1[symbol_table.py<br/>Symbol Table]
        C2[analyzer.py<br/>Semantic Analyzer]
    end
    
    subgraph "CodeGen Module"
        D1[intermediate.py<br/>IR Generator]
        D2[target.py<br/>Target Code Gen]
    end
    
    subgraph "Optimizer Module"
        E1[optimizer.py<br/>Optimization Passes]
    end
    
    subgraph "Utils Module"
        F1[error_handler.py<br/>Error Reporting]
        F2[visualizer.py<br/>AST Visualization]
    end
    
    A1 --> A2
    A2 --> B2
    B1 --> B2
    B2 --> C2
    C1 --> C2
    C2 --> D1
    D1 --> E1
    E1 --> D2
    F1 -.-> A2
    F1 -.-> B2
    F1 -.-> C2
    F2 -.-> B1
    
    style A1 fill:#a5d6a7
    style A2 fill:#a5d6a7
    style B1 fill:#a5d6a7
    style B2 fill:#a5d6a7
    style C1 fill:#ffccbc
    style C2 fill:#ffccbc
    style D1 fill:#ffccbc
    style D2 fill:#ffccbc
    style E1 fill:#ffccbc
```

## Data Flow Diagram

```mermaid
flowchart TD
    Start([Start]) --> Input[Read Source File]
    Input --> Lex{Lexical<br/>Analysis}
    Lex -->|Success| TokenStream[Token Stream]
    Lex -->|Error| LexError[Lexer Error<br/>Report & Exit]
    
    TokenStream --> Parse{Syntax<br/>Analysis}
    Parse -->|Success| AST[Abstract Syntax Tree]
    Parse -->|Error| ParseError[Parser Error<br/>Report & Exit]
    
    AST --> Semantic{Semantic<br/>Analysis}
    Semantic -->|Success| AnnotatedAST[Annotated AST +<br/>Symbol Table]
    Semantic -->|Error| SemanticError[Semantic Error<br/>Report & Exit]
    
    AnnotatedAST --> IRGen{IR<br/>Generation}
    IRGen -->|Success| TAC[Three-Address Code]
    IRGen -->|Error| IRError[IR Error<br/>Report & Exit]
    
    TAC --> Optimize{Optimization}
    Optimize --> OptimizedTAC[Optimized TAC]
    
    OptimizedTAC --> CodeGen{Code<br/>Generation}
    CodeGen -->|Success| TargetCode[Target Code]
    CodeGen -->|Error| CodeGenError[CodeGen Error<br/>Report & Exit]
    
    TargetCode --> Output([Output Executable])
    
    LexError --> End([End])
    ParseError --> End
    SemanticError --> End
    IRError --> End
    CodeGenError --> End
    Output --> End
    
    style Start fill:#e1f5fe
    style End fill:#e1f5fe
    style AST fill:#c8e6c9
    style AnnotatedAST fill:#c8e6c9
    style TAC fill:#c8e6c9
    style OptimizedTAC fill:#c8e6c9
    style TargetCode fill:#c8e6c9
    style LexError fill:#ffcdd2
    style ParseError fill:#ffcdd2
    style SemanticError fill:#ffcdd2
    style IRError fill:#ffcdd2
    style CodeGenError fill:#ffcdd2
```

## Class Hierarchy

```mermaid
classDiagram
    class Token {
        +TokenType type
        +Any value
        +int line
        +int column
        +__repr__()
        +__str__()
    }
    
    class TokenType {
        <<enumeration>>
        INT
        FLOAT
        IDENTIFIER
        PLUS
        MINUS
        ...
    }
    
    class Lexer {
        -str source
        -int position
        -int line
        -int column
        -char current_char
        +__init__(source)
        +advance()
        +peek()
        +get_next_token()
        +tokenize()
    }
    
    class ASTNode {
        <<abstract>>
        +NodeType node_type
        +int line
        +int column
    }
    
    class Program {
        +List~ASTNode~ declarations
    }
    
    class FunctionDeclaration {
        +str return_type
        +str identifier
        +List~ParameterDeclaration~ parameters
        +Block body
    }
    
    class VariableDeclaration {
        +str var_type
        +str identifier
        +ASTNode initializer
        +bool is_const
    }
    
    class Expression {
        <<abstract>>
    }
    
    class BinaryExpression {
        +str operator
        +ASTNode left
        +ASTNode right
    }
    
    class Parser {
        -List~Token~ tokens
        -int position
        -Token current_token
        +__init__(tokens)
        +parse()
        +parse_declaration()
        +parse_expression()
        +parse_statement()
    }
    
    Token --> TokenType
    Lexer --> Token
    Parser --> Token
    Parser --> ASTNode
    ASTNode <|-- Program
    ASTNode <|-- FunctionDeclaration
    ASTNode <|-- VariableDeclaration
    ASTNode <|-- Expression
    Expression <|-- BinaryExpression
    Program --> FunctionDeclaration
    Program --> VariableDeclaration
    FunctionDeclaration --> Expression
```

## Module Dependencies

```mermaid
graph TD
    Main[main.py] --> Lexer[lexer/]
    Main --> Parser[parser/]
    Main --> Utils[utils/]
    
    Parser --> Lexer
    Parser --> ASTNodes[parser/ast_nodes.py]
    
    Semantic[semantic/] --> Parser
    Semantic --> SymbolTable[semantic/symbol_table.py]
    
    CodeGen[codegen/] --> Semantic
    CodeGen --> IR[codegen/intermediate.py]
    
    Optimizer[optimizer/] --> CodeGen
    
    Utils --> Lexer
    Utils --> Parser
    
    style Main fill:#e1f5fe
    style Lexer fill:#a5d6a7
    style Parser fill:#a5d6a7
    style Semantic fill:#fff59d
    style CodeGen fill:#ffccbc
    style Optimizer fill:#ffccbc
    style Utils fill:#e1f5fe
```

## Legend

- **Green (Implemented)**: Lexer, Parser, AST Nodes
- **Yellow (Partial)**: Semantic Analysis (planned)
- **Orange (Planned)**: Code Generation, Optimization

## Implementation Status

| Phase | Component | Status | Completion |
|-------|-----------|--------|------------|
| 1 | Lexical Analysis | ✅ Complete | 100% |
| 2 | Syntax Analysis | ✅ Complete | 100% |
| 3 | Semantic Analysis | 📋 Planned | 0% |
| 4 | IR Generation | 📋 Planned | 0% |
| 5 | Optimization | 📋 Planned | 0% |
| 6 | Code Generation | 📋 Planned | 0% |

**Overall Project Completion: 30%**
