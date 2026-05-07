"""
File: input_validation.py
Author: Alexander Leykand
Date: 04/18/2026
Assignment: Lab 2

Description:
This module defines the input_value function wrapper with all the supporting functions.
"""


def range_validation_error(num, gt, ge, lt, le):
    """
    Validate whether a numeric value falls within specified bounds.

    Parameters:
        num (float or int):
            The value to validate.

        gt (float or int, optional):
            Value that 'num' must be greater than.

        ge (float or int, optional):
            Value that 'num' must be greater than or equal to.

        lt (float or int, optional):
            Value that 'num' must be less than.

        le (float or int, optional):
            Value that 'num' must be less than or equal to.

    Returns:
        str:
            An error message describing the violated constraint.
            Returns an empty string if the value satisfies all conditions.
    """
    if gt is not None and not (num > gt):
        return f"Wrong input! Must be greater than {gt}."
    elif ge is not None and not (num >= ge):
        return f"Wrong input! Must be greater than or equal to {ge}."
    elif lt is not None and not (num < lt):
        return f"Wrong input! Must be less than {lt}."
    elif le is not None and not (num <= le):
        return f"Wrong input! Must be less than or equal to {le}."
    else:
        return ""


def prompt_customization(gt, ge, lt, le):
    """
    Generate appendage to the prompt describing numeric range constraints.

    Parameters:
        gt (float or int, optional):
            Value that input must be greater than.

        ge (float or int, optional):
            Value that input must be greater than or equal to.

        lt (float or int, optional):
            Value that input must be less than.

        le (float or int, optional):
            Value that input must be less than or equal to.

    Returns:
        str:
            A formatted string describing the applicable constraints,
            ending with a colon and newline character.
    """
    prompt = ""
    if gt is not None:
        prompt += " greater than " + str(gt)
    if ge is not None:
        prompt += " greater than or equal to " + str(ge)
    if lt is not None:
        prompt += " less than " + str(lt)
    if le is not None:
        prompt += " less than or equal to " + str(le)

    prompt += ":\n"
    return prompt


def input_number(num_type, prompt, error, gt, ge, lt, le):
    """
    Prompt the user for numeric input and validate it against optional range constraints.

    The function repeatedly prompts the user until a valid numeric value
    is entered that satisfies the specified boundary conditions.

    Parameters:
        num_type (str):
            The numeric type to convert the input to ("int" or "float").

        prompt (str):
            The message displayed to request user input.

        error (str):
            The error message displayed when the input cannot be converted
            to the specified numeric type.

        gt (float or int, optional):
            Value that input must be greater than.

        ge (float or int, optional):
            Value that input must be greater than or equal to.

        lt (float or int, optional):
            Value that input must be less than.

        le (float or int, optional):
            Value that input must be less than or equal to.

    Returns:
        int or float:
            A validated numeric value that satisfies the specified constraints.
    """
    prompt += prompt_customization(gt, ge, lt, le)
    num = 0

    while True:
        try:
            if num_type == "int":
                num = int(input(prompt))
            if num_type == "float":
                num = float(input(prompt))
            # validate range
            range_error_message = range_validation_error(num, gt, ge, lt, le)
            if range_error_message:
                print(range_error_message)
                continue
            return num
        except ValueError:
            print(error)


def input_int(prompt="Please enter an integer",
              error="Only whole numbers are allowed.",
              gt=None, ge=None, lt=None, le=None):
    """
    Prompt the user for integer input and validate it against optional range constraints.

    This function is a convenience wrapper around the input_number function
    that specifically enforces integer input.

    Parameters:
        prompt (str, optional):
            The message displayed to request user input.
            Default is "Please enter an integer".

        error (str, optional):
            The error message displayed when noninteger input is entered.
            Default is "Only whole numbers are allowed."

        gt (int, optional):
            Value that input must be greater than.

        ge (int, optional):
            Value that input must be greater than or equal to.

        lt (int, optional):
            Value that input must be less than.

        le (int, optional):
            Value that input must be less than or equal to.

    Returns:
        int:
            A validated integer that satisfies the specified constraints.
    """
    return input_number("int", prompt, error, gt, ge, lt, le)


def input_float(prompt="Please enter a decimal number",
                error="Only decimal numeric input is allowed.",
                gt=None, ge=None, lt=None, le=None):
    """
    Prompt the user for floating-point input and validate it against optional range constraints.

    This function is a convenience wrapper around the input_number function
    that specifically enforces float input.

    Parameters:
        prompt (str, optional):
            The message displayed to request user input.
            Default is "Please enter a decimal number".

        error (str, optional):
            The error message displayed when non-numeric input is entered.
            Default is "Only decimal numeric input is allowed."

        gt (float, optional):
            Value that input must be greater than.

        ge (float, optional):
            Value that input must be greater than or equal to.

        lt (float, optional):
            Value that input must be less than.

        le (float, optional):
            Value that input must be less than or equal to.

    Returns:
        float:
            A validated floating-point number that satisfies the specified constraints.
    """
    return input_number("float", prompt, error, gt, ge, lt, le)


def input_string(prompt="Please enter the text specified by validation function:",
                 error="Your entry did not pass validation.",
                 valid=lambda x: True if x.strip() else False):
    """
    Prompt the user for string input and validate it using a custom validation function.

    The function repeatedly prompts the user until the provided validation
    function returns True for the entered text.

    Parameters:
        prompt (str, optional):
            The message displayed to request user input.
            Default is "Please enter the text specified by validation function:".

        error (str, optional):
            The error message displayed when validation fails.
            Default is "Your entry did not pass validation."

        valid (callable, optional):
            A function that accepts a string argument and returns True if the
            input is valid, or False otherwise. The default validation ensures
            that the input is not empty or whitespace.

    Returns:
        str:
            A validated string that satisfies the provided validation function.
    """
    while True:
        entry = input(prompt).strip()
        if valid(entry):
            return entry
        else:
            print(error)


def y_or_n(prompt="Please enter Y for Yes or N for No:\n",
           error="Invalid response. Y/N or Yes/No is expected:\n"):
    """
    Prompt the user for a Yes/No response and return the corresponding Boolean value.

    The function repeatedly prompts the user until a valid affirmative or
    negative response is entered. Accepted responses are "y", "yes", "n",
    and "no", regardless of letter case.

    Parameters:
        prompt (str, optional):
            The message displayed to request user input.
            Default is "Please enter Y for Yes or N for No:\n".

        error (str, optional):
            The error message displayed when an invalid response is entered.
            Default is "Invalid response. Y/N or Yes/No is expected:\n".

    Returns:
        bool:
            True if the user enters an affirmative response ("y" or "yes").
            False if the user enters a negative response ("n" or "no").
    """
    while True:
        reply = input(prompt).lower()
        if reply in ["y", "yes"]:
            return True
        elif reply in ["n", "no"]:
            return False
        else:
            print(error)


def select_item(prompt="Please select one from the list",
                error="Invalid selection. Please try again:\n",
                choices=("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"),
                mappings=None):
    """
      Prompt the user to select an item from a predefined list of choices.

      The function supports two selection modes:
      1. Direct matching against a tuple/list of choices.
      2. Mapping user input to custom values using a dictionary.

      Parameters:
          prompt (str, optional):
              The message displayed to request user input.

          error (str, optional):
              The error message displayed when the input is invalid.

          choices (tuple, optional):
              A sequence of valid selectable options. Default is days of the week.

          mappings (dict, optional):
              A dictionary mapping user input strings to return values.
              If provided, selection is validated against this dictionary as well
              as the choices list.

      Returns:
          str:
              The selected item from the choices list or the mapped value
              from the mappings dictionary.
      """
    while True:
        selection = input(prompt + " " + str(choices) + "\n").lower()

        # If mapping dictionary is provided, use it for selection
        if mappings is not None and selection in mappings:
                return mappings.get(selection)

        choices_lowercase = list(map(lambda x: x.lower(), choices))
        if selection in choices_lowercase:
            return choices[(choices_lowercase.index(selection))]
        else:
            print(error)


def input_value(input_type, **kvargs):
    """
    Dispatch user input validation to the appropriate input function based on type.

    This function acts as a centralized router that selects and calls the
    appropriate input-handling function (e.g., integer, float, string, etc.)
    based on the specified input_type.

    Parameters:
        input_type (str):
            The type of input to process. Valid options include:
            "int", "float", "string", "y_or_n", and "item".

        **kvargs:
            Arbitrary keyword arguments passed directly to the selected
            input function (such as prompt, error message, or validation rules).

    Returns:
        Any:
            The validated value returned by the selected input function.
    """
    type_function = {"int": input_int,
                     "float": input_float,
                     "string": input_string,
                     "y_or_n": y_or_n,
                     "item": select_item}
    return type_function.get(input_type)(**kvargs)
