#!/usr/bin/env python3
"""
MinLang Compiler - Main Entry Point
Command-line interface for the MinLang compiler with Semantic Analysis
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent))

from lexer import Lexer, LexerError
from parser import Parser, ParserError
from semantic import SemanticAnalyzer
from codegen import generate_tac, format_tac_output

# Version information
VERSION = "0.8.0"  # 80% Complete (Phases 1-4)
COMPILER_NAME = "MinLang Compiler"


class CompilerError(Exception):
    """Base class for compiler errors"""
    pass


def print_tokens(tokens):
    """Print token stream"""
    print("\n=== TOKEN STREAM ===")
    for token in tokens:
        print(f"  {token}")
    print()


def print_ast(ast):
    """Print Abstract Syntax Tree"""
    print("\n=== ABSTRACT SYNTAX TREE ===")
    # Simple AST printing
    def print_node(node, indent=0):
        prefix = "  " * indent
        node_name = type(node).__name__
        print(f"{prefix}{node_name}")
        
        # Print children
        for attr_name in dir(node):
            if attr_name.startswith('_'):
                continue
            attr = getattr(node, attr_name)
            if hasattr(attr, '__class__') and hasattr(attr.__class__, '__module__'):
                if 'ast_nodes' in attr.__class__.__module__:
                    print(f"{prefix}  {attr_name}:")
                    print_node(attr, indent + 2)
                elif isinstance(attr, list):
                    for i, item in enumerate(attr):
                        if hasattr(item, '__class__') and 'ast_nodes' in item.__class__.__module__:
                            print(f"{prefix}  {attr_name}[{i}]:")
                            print_node(item, indent + 2)
    
    print_node(ast)
    print()


def print_symbol_table(symbol_table):
    """Print symbol table"""
    print("\n=== SYMBOL TABLE ===")
    
    all_symbols = symbol_table.get_all_symbols()
    
    if not all_symbols:
        print("  (empty)")
        return
    
    # Group by scope level
    from collections import defaultdict
    by_scope = defaultdict(list)
    for symbol in all_symbols:
        by_scope[symbol.scope_level].append(symbol)
    
    for level in sorted(by_scope.keys()):
        print(f"\n  Scope Level {level}:")
        for symbol in by_scope[level]:
            init_marker = "✓" if symbol.is_initialized else "✗"
            print(f"    [{init_marker}] {symbol}")
    
    print()


def compile_file(filename: str, args: argparse.Namespace) -> bool:
    """
    Compile a MinLang source file
    
    Args:
        filename: Path to source file
        args: Command-line arguments
        
    Returns:
        True if compilation succeeded, False otherwise
    """
    try:
        # Check if file exists
        if not Path(filename).exists():
            print(f"Error: File '{filename}' not found", file=sys.stderr)
            return False
        
        if args.verbose:
            print(f"Compiling {filename}...")
            print(f"MinLang Compiler v{VERSION} (60% Complete)\n")
        
        # Read source code
        with open(filename, 'r') as f:
            source = f.read()
        
        # Phase 1: Lexical Analysis
        if args.verbose:
            print("Phase 1: Lexical Analysis")
        
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        if args.tokens:
            print_tokens(tokens)
        
        if args.verbose:
            print(f"  ✓ Generated {len(tokens)} tokens\n")
        
        # Phase 2: Syntax Analysis
        if args.verbose:
            print("Phase 2: Syntax Analysis")
        
        parser = Parser(tokens)
        ast = parser.parse()
        
        if args.ast:
            print_ast(ast)
        
        if args.verbose:
            print(f"  ✓ AST generated successfully\n")
        
        # Phase 3: Semantic Analysis
        if args.verbose:
            print("Phase 3: Semantic Analysis")
        
        analyzer = SemanticAnalyzer()
        success = analyzer.analyze(ast)
        
        if args.symbols:
            print_symbol_table(analyzer.symbol_table)
        
        if not success:
            # Print semantic errors
            print("\n✗ Semantic Analysis Failed\n", file=sys.stderr)
            analyzer.print_errors()
            return False
        
        if args.verbose:
            print(f"  ✓ Type checking completed")
            print(f"  ✓ Symbol table constructed")
            print(f"  ✓ Semantic analysis passed\n")
        
        # Phase 4: Intermediate Code Generation
        if args.verbose:
            print("Phase 4: Intermediate Code Generation")
        
        tac_program = generate_tac(ast, analyzer.symbol_table)
        
        if args.tac:
            print(format_tac_output(tac_program))
        
        if args.verbose:
            print(f"  ✓ Generated {len(tac_program.instructions)} TAC instructions")
            print(f"  ✓ Used {tac_program.temp_count} temporary variables")
            print(f"  ✓ Created {tac_program.label_count} labels\n")
        
        # Phase 5-6: Not yet implemented
        if args.verbose:
            print("Phase 5: Optimization (TODO)")
            print("Phase 6: Code Generation (TODO)")
        
        if args.verbose or not args.quiet:
            print(f"\n✓ Compilation completed successfully")
            print(f"   Phases 1-4 complete (Lexing, Parsing, Semantic, IR Generation)")
            print(f"   No errors found!")
        
        return True
        
    except LexerError as e:
        print(f"\n✗ Lexical Error: {e}", file=sys.stderr)
        return False
    
    except ParserError as e:
        print(f"\n✗ Syntax Error: {e}", file=sys.stderr)
        return False
    
    except Exception as e:
        print(f"\n✗ Unexpected Error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        return False


def main():
    """Main entry point for the compiler"""
    parser = argparse.ArgumentParser(
        prog='minlang',
        description=f'{COMPILER_NAME} v{VERSION} - Educational compiler for MinLang (80% Complete)',
        epilog='Phases 1-4 implemented: Lexical, Syntax, Semantic Analysis, IR Generation'
    )
    
    # Required arguments
    parser.add_argument(
        'input',
        help='MinLang source file to compile'
    )
    
    # Optional arguments
    parser.add_argument(
        '--version',
        action='version',
        version=f'{COMPILER_NAME} v{VERSION} (80%% Complete - Phases 1-4)'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='enable verbose output'
    )
    
    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='suppress success messages'
    )
    
    parser.add_argument(
        '--tokens',
        action='store_true',
        help='print token stream from lexer'
    )
    
    parser.add_argument(
        '--ast',
        action='store_true',
        help='print abstract syntax tree'
    )
    
    parser.add_argument(
        '--symbols',
        action='store_true',
        help='print symbol table'
    )
    
    parser.add_argument(
        '--tac',
        action='store_true',
        help='print three-address code (intermediate representation)'
    )
    
    parser.add_argument(
        '-O', '--optimize',
        action='store_true',
        help='enable optimizations (not yet implemented)'
    )
    
    parser.add_argument(
        '-o', '--output',
        metavar='FILE',
        help='output file for generated code'
    )
    
    parser.add_argument(
        '--run',
        action='store_true',
        help='run the compiled program (not yet implemented)'
    )
    
    args = parser.parse_args()
    
    # Compile the file
    success = compile_file(args.input, args)
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
