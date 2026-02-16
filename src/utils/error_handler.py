"""
Error Handler for MinLang Compiler
Provides centralized error reporting and formatting
"""

from typing import Optional
import sys


class CompilerError(Exception):
    """Base class for all compiler errors"""
    def __init__(self, message: str, line: int = 0, column: int = 0, filename: str = ""):
        self.message = message
        self.line = line
        self.column = column
        self.filename = filename
        super().__init__(self.format_error())
    
    def format_error(self) -> str:
        """Format error message with location info"""
        location = ""
        if self.filename:
            location = f"{self.filename}:"
        if self.line > 0:
            location += f"{self.line}:"
        if self.column > 0:
            location += f"{self.column}:"
        
        if location:
            return f"{location} {self.message}"
        return self.message


class ErrorHandler:
    """Centralized error handling and reporting"""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.error_count = 0
        self.warning_count = 0
        self.errors = []
        self.warnings = []
    
    def report_error(self, message: str, line: int = 0, column: int = 0, filename: str = ""):
        """Report an error"""
        self.error_count += 1
        error_msg = self._format_message("ERROR", message, line, column, filename)
        self.errors.append(error_msg)
        print(error_msg, file=sys.stderr)
    
    def report_warning(self, message: str, line: int = 0, column: int = 0, filename: str = ""):
        """Report a warning"""
        self.warning_count += 1
        warning_msg = self._format_message("WARNING", message, line, column, filename)
        self.warnings.append(warning_msg)
        if self.verbose:
            print(warning_msg, file=sys.stderr)
    
    def report_info(self, message: str):
        """Report informational message"""
        if self.verbose:
            print(f"INFO: {message}")
    
    def _format_message(self, level: str, message: str, line: int, column: int, filename: str) -> str:
        """Format error/warning message"""
        location = ""
        if filename:
            location = f"{filename}:"
        if line > 0:
            location += f"{line}:"
        if self.column > 0:
            location += f"{column}:"
        
        if location:
            return f"{location} {level}: {message}"
        return f"{level}: {message}"
    
    def has_errors(self) -> bool:
        """Check if any errors were reported"""
        return self.error_count > 0
    
    def print_summary(self):
        """Print error/warning summary"""
        if self.error_count > 0 or self.warning_count > 0:
            print(f"\nCompilation summary: {self.error_count} error(s), {self.warning_count} warning(s)")
