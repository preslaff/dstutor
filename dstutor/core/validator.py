"""
Code validation system for exercises
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, Tuple, Optional
import traceback
import sys
from io import StringIO


class CodeValidator:
    """Validates user code against expected results"""

    def __init__(self):
        self.allowed_imports = {
            'numpy': np,
            'np': np,
            'pandas': pd,
            'pd': pd,
            'matplotlib': None,  # Will be imported if needed
            'plt': None,
            'seaborn': None,
            'sns': None,
        }

    def validate(self,
                 user_code: str,
                 expected_result: Any,
                 validation_rules: Dict) -> Tuple[bool, str]:
        """
        Execute user code and validate against expected result

        Args:
            user_code: The code submitted by user
            expected_result: Expected solution (for reference)
            validation_rules: Validation configuration

        Returns:
            (is_correct, feedback_message)
        """
        # Create execution namespace
        namespace = self._create_namespace()

        # Capture stdout
        old_stdout = sys.stdout
        sys.stdout = captured_output = StringIO()

        try:
            # Execute user code
            exec(user_code, namespace)

            # Restore stdout
            sys.stdout = old_stdout

            # Check if validation has multiple variable checks
            validation_type = validation_rules.get('type', 'value_check')
            checks = validation_rules.get('checks', [])

            # If we have a checks array with variable definitions, validate those
            if checks and isinstance(checks, list) and len(checks) > 0:
                # Check if first item has 'variable' key (multi-variable validation)
                if 'variable' in checks[0]:
                    return self._validate_variables(namespace, checks)

            # Otherwise, check for single 'result' variable
            if 'result' not in namespace:
                return False, "Please store your answer in a variable called 'result'"

            user_result = namespace['result']

            # Apply validation rules
            return self._apply_validation_rules(
                user_result,
                expected_result,
                validation_rules
            )

        except SyntaxError as e:
            sys.stdout = old_stdout
            return False, f"Syntax Error: {str(e)}\nCheck your code for typos."

        except NameError as e:
            sys.stdout = old_stdout
            return False, f"Name Error: {str(e)}\nMake sure all variables are defined."

        except Exception as e:
            sys.stdout = old_stdout
            error_type = type(e).__name__
            return False, f"{error_type}: {str(e)}"

    def _create_namespace(self) -> Dict:
        """Create safe execution namespace with allowed imports"""
        namespace = {
            '__builtins__': __builtins__,
            'pd': pd,
            'np': np,
        }

        # Add matplotlib if needed
        try:
            import matplotlib.pyplot as plt
            import seaborn as sns
            namespace['plt'] = plt
            namespace['sns'] = sns
        except ImportError:
            pass

        return namespace

    def _apply_validation_rules(self,
                                 user_result: Any,
                                 expected: Any,
                                 rules: Dict) -> Tuple[bool, str]:
        """
        Apply validation rules based on validation type

        Args:
            user_result: User's result
            expected: Expected result (reference)
            rules: Validation configuration

        Returns:
            (is_correct, feedback_message)
        """
        validation_type = rules.get('type', 'value_check')

        if validation_type == 'dataframe_check':
            return self._validate_dataframe(user_result, rules.get('checks', []))

        elif validation_type == 'array_check':
            return self._validate_array(user_result, rules.get('checks', []))

        elif validation_type == 'value_check':
            return self._validate_value(
                user_result,
                expected,
                rules.get('tolerance', 0.001)
            )

        elif validation_type == 'type_check':
            return self._validate_type(user_result, rules.get('expected_type'))

        elif validation_type == 'function_check':
            return self._validate_function(user_result, rules.get('test_cases', []))

        elif validation_type == 'shape_check':
            return self._validate_shape(user_result, rules.get('expected_shape'))

        else:
            return False, f"Unknown validation type: {validation_type}"

    def _validate_dataframe(self, df: Any, checks: list) -> Tuple[bool, str]:
        """Validate DataFrame properties"""

        # Check if it's actually a DataFrame
        if not isinstance(df, pd.DataFrame):
            return False, f"Expected pandas DataFrame, got {type(df).__name__}"

        for check in checks:
            check_type = check.get('type')

            if check_type == 'shape':
                expected_shape = tuple(check['expected'])
                if df.shape != expected_shape:
                    return False, f"Shape mismatch: got {df.shape}, expected {expected_shape}"

            elif check_type == 'columns':
                expected_cols = check['expected']
                if list(df.columns) != expected_cols:
                    return False, f"Column mismatch: got {list(df.columns)}, expected {expected_cols}"

            elif check_type == 'dtypes':
                for col, expected_dtype in check['expected'].items():
                    if col not in df.columns:
                        return False, f"Column '{col}' not found"
                    if str(df[col].dtype) != expected_dtype:
                        return False, f"Column '{col}' has wrong dtype: {df[col].dtype}"

            elif check_type == 'values':
                expected_values = check.get('expected_values')
                if expected_values:
                    actual_values = df.values.tolist()
                    if actual_values != expected_values:
                        return False, "Values don't match expected result"

            elif check_type == 'not_empty':
                if df.empty:
                    return False, "DataFrame is empty"

            elif check_type == 'no_nulls':
                if df.isnull().any().any():
                    return False, "DataFrame contains null values"

        return True, "Correct! ✅"

    def _validate_array(self, arr: Any, checks: list) -> Tuple[bool, str]:
        """Validate NumPy array properties"""

        # Check if it's a numpy array
        if not isinstance(arr, np.ndarray):
            return False, f"Expected numpy array, got {type(arr).__name__}"

        for check in checks:
            check_type = check.get('type')

            if check_type == 'shape':
                expected_shape = tuple(check['expected'])
                if arr.shape != expected_shape:
                    return False, f"Shape mismatch: got {arr.shape}, expected {expected_shape}"

            elif check_type == 'dtype':
                expected_dtype = check['expected']
                if str(arr.dtype) != expected_dtype:
                    return False, f"Dtype mismatch: got {arr.dtype}, expected {expected_dtype}"

            elif check_type == 'values':
                expected_values = np.array(check['expected'])
                if not np.allclose(arr, expected_values, rtol=1e-5, atol=1e-8):
                    return False, "Values don't match expected result"

            elif check_type == 'min_max':
                if 'min' in check and arr.min() < check['min']:
                    return False, f"Minimum value {arr.min()} is below expected {check['min']}"
                if 'max' in check and arr.max() > check['max']:
                    return False, f"Maximum value {arr.max()} is above expected {check['max']}"

        return True, "Correct! ✅"

    def _validate_value(self,
                        user_value: Any,
                        expected_value: Any,
                        tolerance: float = 0.001) -> Tuple[bool, str]:
        """Validate a single value"""

        # Check type match
        if type(user_value) != type(expected_value):
            return False, f"Type mismatch: got {type(user_value).__name__}, expected {type(expected_value).__name__}"

        # Numeric comparison with tolerance
        if isinstance(expected_value, (int, float, np.number)):
            if abs(user_value - expected_value) <= tolerance:
                return True, "Correct! ✅"
            else:
                return False, f"Value mismatch: got {user_value}, expected {expected_value}"

        # Exact comparison for other types
        if user_value == expected_value:
            return True, "Correct! ✅"
        else:
            return False, f"Value mismatch: got {user_value}, expected {expected_value}"

    def _validate_type(self, result: Any, expected_type: str) -> Tuple[bool, str]:
        """Validate type of result"""

        type_map = {
            'DataFrame': pd.DataFrame,
            'Series': pd.Series,
            'ndarray': np.ndarray,
            'list': list,
            'dict': dict,
            'int': int,
            'float': float,
            'str': str,
        }

        expected_type_obj = type_map.get(expected_type)
        if not expected_type_obj:
            return False, f"Unknown expected type: {expected_type}"

        if isinstance(result, expected_type_obj):
            return True, "Correct! ✅"
        else:
            return False, f"Type mismatch: got {type(result).__name__}, expected {expected_type}"

    def _validate_function(self, func: Any, test_cases: list) -> Tuple[bool, str]:
        """Validate a function against test cases"""

        if not callable(func):
            return False, "Result is not a callable function"

        for i, test_case in enumerate(test_cases, 1):
            inputs = test_case.get('input')
            expected_output = test_case.get('output')

            try:
                # Call function with inputs
                if isinstance(inputs, dict):
                    actual_output = func(**inputs)
                elif isinstance(inputs, (list, tuple)):
                    actual_output = func(*inputs)
                else:
                    actual_output = func(inputs)

                # Check output
                if actual_output != expected_output:
                    return False, f"Test case {i} failed: expected {expected_output}, got {actual_output}"

            except Exception as e:
                return False, f"Test case {i} raised error: {str(e)}"

        return True, "All test cases passed! ✅"

    def _validate_shape(self, result: Any, expected_shape: tuple) -> Tuple[bool, str]:
        """Validate shape of array-like object"""

        if not hasattr(result, 'shape'):
            return False, f"Result has no shape attribute (type: {type(result).__name__})"

        expected_shape = tuple(expected_shape)
        if result.shape != expected_shape:
            return False, f"Shape mismatch: got {result.shape}, expected {expected_shape}"

        return True, "Correct! ✅"

    def _validate_variables(self, namespace: Dict, checks: list) -> Tuple[bool, str]:
        """
        Validate multiple variables against expected values

        Args:
            namespace: Execution namespace containing user's variables
            checks: List of variable checks from YAML validation rules

        Returns:
            (is_correct, feedback_message)
        """
        errors = []

        for check in checks:
            var_name = check.get('variable')
            expected_value = check.get('expected')
            expected_type = check.get('type')

            # Check if variable exists
            if var_name not in namespace:
                errors.append(f"Variable '{var_name}' not found")
                continue

            user_value = namespace[var_name]

            # Check type
            type_map = {'int': int, 'float': float, 'str': str, 'bool': bool}
            if expected_type and expected_type in type_map:
                if not isinstance(user_value, type_map[expected_type]):
                    errors.append(f"Variable '{var_name}' has wrong type: expected {expected_type}, got {type(user_value).__name__}")
                    continue

            # Check value
            if expected_value is not None:
                if isinstance(expected_value, float):
                    if abs(user_value - expected_value) > 0.001:
                        errors.append(f"Variable '{var_name}' has wrong value: expected {expected_value}, got {user_value}")
                else:
                    if user_value != expected_value:
                        errors.append(f"Variable '{var_name}' has wrong value: expected {expected_value}, got {user_value}")

        if errors:
            return False, "\n".join(errors)
        else:
            return True, "Correct! ✅ All variables match the expected values and types."
