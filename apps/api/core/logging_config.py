"""Logging configuration using structlog."""

import logging
import sys
from typing import Any

import structlog
from structlog.types import EventDict, Processor

from apps.config.settings import settings


def add_app_context(logger: Any, method_name: str, event_dict: EventDict) -> EventDict:
    """Add application context to log entries."""
    event_dict["app"] = settings.app_name
    event_dict["environment"] = settings.environment
    event_dict["version"] = settings.app_version
    return event_dict


def drop_color_message_key(logger: Any, method_name: str, event_dict: EventDict) -> EventDict:
    """Drop color message key for non-terminal output."""
    event_dict.pop("color_message", None)
    return event_dict


def configure_logging() -> None:
    """Configure structlog for the application."""
    
    # Configure standard logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=settings.log_level,
    )
    
    # Shared processors for all loggers
    shared_processors: list[Processor] = [
        # Add log level
        structlog.stdlib.add_log_level,
        # Add timestamp
        structlog.processors.TimeStamper(fmt="iso"),
        # Add application context
        add_app_context,
        # Add logger name
        structlog.stdlib.add_logger_name,
        # Add call stack if debug mode
        structlog.processors.StackInfoRenderer() if settings.debug else structlog.processors.DropStackInfoRenderer(),
    ]
    
    if settings.log_format == "json":
        # JSON format for production
        processors = shared_processors + [
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ]
        
        renderer = structlog.processors.JSONRenderer()
    else:
        # Text format for development
        processors = shared_processors + [
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ]
        
        renderer = structlog.dev.ConsoleRenderer(colors=True)
    
    # Configure structlog
    structlog.configure(
        processors=processors,
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )
    
    # Configure standard logging formatter
    formatter = structlog.stdlib.ProcessorFormatter(
        processor=renderer,
        processors=[
            drop_color_message_key,
        ] if settings.log_format == "json" else [],
    )
    
    # Apply formatter to all handlers
    for handler in logging.root.handlers:
        handler.setFormatter(formatter)
    
    # Silence noisy loggers
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)


def get_logger(name: str) -> structlog.stdlib.BoundLogger:
    """Get a logger instance with the given name."""
    return structlog.get_logger(name)
