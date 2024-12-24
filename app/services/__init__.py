"""
Services package for handling business logic.

This package contains service classes that encapsulate the core business logic
of the application:

- CallService: Handles all call-related operations including loading, searching,
  and analyzing call data.
- ClaudeService: Manages interactions with the Claude AI API for answering
  questions about call transcripts.
"""

from .call_service import CallService
from .claude_service import ClaudeService

__all__ = ['CallService', 'ClaudeService'] 