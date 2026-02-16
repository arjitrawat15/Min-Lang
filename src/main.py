#!/usr/bin/env python3
"""
MinLang Compiler - Main Entry Point
Command-line interface for the MinLang compiler
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

from lexer import Lexer, LexerError, tokenize_file
from parser import Parser, ParserError, parse_file
from parser.ast_nodes import ast_to_string

# Version information
VERSION = "0.1.0"
COMPILER_NAME = "MinLang Compiler"


class CompilerError(Exception):
    """Base class for compiler errors"""
    pass


def print_tokens(tokens):
    """Print token stream"""
    print("\n=== TOKEN STREAM ===")
    for token in tokens:
        print(token)
    print()


def print_ast(ast):
    """Print Abstract Syntax Tree"""
    print("\n=== ABSTRACT SYNTAX TREE ===")
    print(ast_to_string(ast))
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
        
        # Phase 1: Lexical Analysis
        if args.verbose:
            print("Phase 1: Lexical Analysis")
        
        with open(filename, 'r') as f:
            source = f.read()
        
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        if args.tokens:
            print_tokens(tokens)
        
        if args.verbose:
            print(f"  Generated {len(tokens)} tokens")
        
        # Phase 2: Syntax Analysis
        if args.verbose:
            print("Phase 2: Syntax Analysis")
        
        parser = Parser(tokens)
        ast = parser.parse()
        
        if args.ast:
            print_ast(ast)
        
        if args.verbose:
            print("  AST generated successfully")
        
        # Phase 3: Semantic Analysis (Not yet implemented)
        if args.verbose:
            print("Phase 3: Semantic Analysis (TODO)")
        
        # Phase 4: Intermediate Code Generation (Not yet implemented)
        if args.verbose:
            print("Phase 4: Code Generation (TODO)")
        
        if args.verbose:
            print(f"\n✓ Compilation completed successfully")
        
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
        description=f'{COMPILER_NAME} v{VERSION} - Educational compiler for MinLang',
        epilog='For more information, see the documentation.'
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
        version=f'{COMPILER_NAME} v{VERSION}'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='enable verbose output'
    )
    
    parser.add_argument(
        '--tokens',
        action='store_true',
        help='print token stream'
    )
    
    parser.add_argument(
        '--ast',
        action='store_true',
        help='print abstract syntax tree'
    )
    
    parser.add_argument(
        '--tac',
        action='store_true',
        help='print three-address code (not yet implemented)'
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
