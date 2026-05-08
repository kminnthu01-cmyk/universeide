"""
Universe IDE - Validator Module

Data validation.
"""

from typing import Any, Callable, Dict


# ============================================================================
# VALIDATOR
# ============================================================================

class Validator:
    """Validator"""
    
    def __init__(self):
        self.rules = {}
        
    def add_rule(self, field: str, validator: Callable):
        if field not in self.rules:
            self.rules[field] = []
        self.rules[field].append(validator)
        
    def validate(self, data: Dict) -> Dict:
        errors = {}
        for field, validators in self.rules.items():
            for validator in validators:
                if not validator(data.get(field)):
                    if field not in errors:
                        errors[field] = []
                    errors[field].append(f"Invalid {field}")
        return errors


__all__ = ["Validator"]