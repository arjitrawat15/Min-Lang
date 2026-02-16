#!/usr/bin/env python3
"""
MinLang Compiler - Main Entry Point

A complete compiler implementation for MinLang programming language.
Demonstrates all phases of compilation from lexical analysis to code generation.

Usage:
    python main.py <source_file> [options]
    
Example:
    python main.py examples/hello_world.min --verbose --ast
"""

import sys
import argparse
from pathlib import Path

# Import compiler components
from src.lexer import tokenize, LexerError, Token
from src.parser import parse, ParserError, ASTPrinter
from src.utils import ErrorHandler


def read_source_file(filename: str) -> str:
    """
    Read source code from file
    
    Args:
        filename: Path to source file
        
    Returns:
        Source code as string
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        sys.exit(1)


def print_tokens(tokens: list):
    """Print token stream in readable format"""
    print("\n" + "=" * 80)
    print(" TOKEN STREAM")
    print("=" * 80)
    print(f"{'Index':<8} {'Type':<20} {'Value':<20} {'Position':<15}")
    print("-" * 80)
    
    for i, token in enumerate(tokens):
        value_str = repr(token.value) if token.value is not None else ''
        position = f"{token.line}:{token.column}"
        print(f"{i:<8} {token.type.name:<20} {value_str:<20} {position:<15}")
    
    print("=" * 80)
    print(f"Total tokens: {len(tokens)}\n")


def print_ast(ast):
    """Print Abstract Syntax Tree"""
    print("\n" + "=" * 80)
    print(" ABSTRACT SYNTAX TREE (AST)")
    print("=" * 80)
    printer = ASTPrinter()
    ast.accept(printer)
    print("=" * 80 + "\n")


def compile_file(filename: str, args):
    """
    Main compilation function
    
    Args:
        filename: Source file path
        args: Command line arguments
    """
    error_handler = ErrorHandler(verbose=args.verbose)
    
    # Read source code
    if args.verbose:
        print(f"Reading source file: {filename}")
    
    source_code = read_source_file(filename)
    
    if args.verbose:
        print(f"Source code loaded: {len(source_code)} characters")
    
    # ========================================================================
    # PHASE 1: Lexical Analysis
    # ========================================================================
    
    try:
        if args.verbose:
            print("\n[PHASE 1] Running Lexical Analysis...")
        
        tokens = tokenize(source_code, filename)
        
        if args.verbose:
            print(f"✓ Lexical analysis complete: {len(tokens)} tokens generated")
        
        if args.tokens:
            print_tokens(tokens)
        
    except LexerError as e:
        error_handler.report_error(str(e))
        return False
    
    # ========================================================================
    # PHASE 2: Syntax Analysis (Parsing)
    # ========================================================================
    
    try:
        if args.verbose:
            print("\n[PHASE 2] Running Syntax Analysis (Parsing)...")
        
        ast = parse(tokens)
        
        if args.verbose:
            print("✓ Syntax analysis complete: AST generated")
        
        if args.ast:
            print_ast(ast)
        
    except ParserError as e:
        error_handler.report_error(str(e))
        return False
    
    # ========================================================================
    # PHASE 3: Semantic Analysis (TODO - Not yet implemented)
    # ========================================================================
    
    if args.verbose:
        print("\n[PHASE 3] Semantic Analysis (Not yet implemented)")
        print("TODO: Type checking, symbol table, scope analysis")
    
    # ========================================================================
    # PHASE 4: Intermediate Code Generation (TODO - Not yet implemented)
    # ========================================================================
    
    if args.verbose:
        print("\n[PHASE 4] IR Generation (Not yet implemented)")
        print("TODO: Three-Address Code generation")
    
    # ========================================================================
    # PHASE 5: Optimization (TODO - Not yet implemented)
    # ========================================================================
    
    if args.optimize and args.verbose:
        print("\n[PHASE 5] Optimization (Not yet implemented)")
        print("TODO: Constant folding, dead code elimination, etc.")
    
    # ========================================================================
    # PHASE 6: Code Generation (TODO - Not yet implemented)
    # ========================================================================
    
    if args.verbose:
        print("\n[PHASE 6] Code Generation (Not yet implemented)")
        print("TODO: Target code emission")
    
    # Success!
    if not error_handler.has_errors():
        print("\n✓ Compilation successful!")
        if args.verbose:
            print(f"\nNote: This is a partial implementation (30% complete)")
            print("Full compilation pipeline to be completed by team members.")
        return True
    
    error_handler.print_summary()
    return False


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='MinLang Compiler - Educational compiler implementation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py program.min                    # Compile a program
  python main.py program.min --verbose          # Verbose output
  python main.py program.min --tokens --ast     # Show tokens and AST
  python main.py program.min -o output.asm      # Specify output file
  python main.py program.min --optimize         # Enable optimizations

Project Status: ~30%% Complete (Lexer + Basic Parser implemented)
        """
    )
    
    parser.add_argument('input', help='Input source file (.min)')
    parser.add_argument('-o', '--output', help='Output file path')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Enable verbose output')
    parser.add_argument('--tokens', action='store_true',
                       help='Display token stream')
    parser.add_argument('--ast', action='store_true',
                       help='Display abstract syntax tree')
    parser.add_argument('--ir', action='store_true',
                       help='Display intermediate representation (not yet implemented)')
    parser.add_argument('--optimize', action='store_true',
                       help='Enable optimization passes (not yet implemented)')
    parser.add_argument('--version', action='version', version='MinLang Compiler v0.3.0')
    
    args = parser.parse_args()
    
    # Validate input file
    if not Path(args.input).exists():
        print(f"Error: Input file '{args.input}' not found", file=sys.stderr)
        sys.exit(1)
    
    # Print header
    if args.verbose:
        print("=" * 80)
        print(" MinLang Compiler v0.3.0")
        print(" Educational Compiler Implementation")
        print("=" * 80)
    
    # Compile
    success = compile_file(args.input, args)
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
