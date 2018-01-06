# The MIT License (MIT)
#
# Copyright (c) 2015-2017 Stefan Fischer
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""Prompt and verify user input on the command line.

The project was initiated by Stefan Fischer.

"""

import getpass
import re

__author__ = "Stefan Fischer"
__contact__ = "Stefan Fischer <sfischer13@ymail.com>"
__copyright__ = "Copyright (c) 2015-2017 Stefan Fischer"
__credits__ = []
__date__ = "2017-06-05"
__license__ = "MIT"
__status__ = "development"
__version__ = "0.4.1"

PROMPT = "? "
"""Prompt that will be shown by default."""
RE_EMAIL_SIMPLE = re.compile(r"^[^@]+@[^@]+\.[^@]+$")
"""Regular expression for email addresses."""


def character(prompt=None, empty=False, default=None):
    """Prompt a single character.

    Parameters
    ----------
    prompt : str, optional
        Use an alternative prompt.
    empty : bool, optional
        Allow an empty response.
    default : str, optional
        Value to return if response is empty.

    Returns
    -------
    str or None
        A str if the user entered a single-character, non-empty string.
        None if the user pressed only Enter and ``empty`` was True.

    """
    s = input(_make_prompt(prompt, default))
    if not s:
        if default is not None:
            return default
        elif empty:
            return None
    elif len(s) == 1:
        return s
    else:
        return character(prompt=prompt, empty=empty)


def email(prompt=None, empty=False, mode="simple", default=None):
    """Prompt an email address.

    This check is based on a simple regular expression and does not verify
    whether an email actually exists.

    Parameters
    ----------
    prompt : str, optional
        Use an alternative prompt.
    empty : bool, optional
        Allow an empty response.
    mode : {'simple'}, optional
        'simple' will use a simple regular expression.
        No other mode is implemented yet.
    default : str, optional
        Value to return if response is empty.

    Returns
    -------
    str or None
        A str if the user entered a likely email address.
        None if the user pressed only Enter and ``empty`` was True.

    """
    if mode == "simple":
        s = input(_make_prompt(prompt, default))
        if not s:
            if default is not None:
                return default
            elif empty:
                return None
        else:
            if RE_EMAIL_SIMPLE.match(s):
                return s
            else:
                return email(prompt=prompt, empty=empty, mode=mode)
    else:
        raise ValueError


def integer(prompt=None, empty=False, default=None):
    """Prompt an integer.

    Parameters
    ----------
    prompt : str, optional
        Use an alternative prompt.
    empty : bool, optional
        Allow an empty response.
    default : int, optional
        Value to return if response is empty.

    Returns
    -------
    int or None
        An int if the user entered a valid integer.
        None if the user pressed only Enter and ``empty`` was True.

    """
    s = input(_make_prompt(prompt, default))
    if not s:
        if default is not None:
            return default
        elif empty:
            return None
    else:
        try:
            return int(s)
        except ValueError:
            return integer(prompt=prompt, empty=empty)


def real(prompt=None, empty=False, default=None):
    """Prompt a real number.

    Parameters
    ----------
    prompt : str, optional
        Use an alternative prompt.
    empty : bool, optional
        Allow an empty response.
    default : float, optional
        Value to return if response is empty.

    Returns
    -------
    float or None
        A float if the user entered a valid real number.
        None if the user pressed only Enter and ``empty`` was True.

    """
    s = input(_make_prompt(prompt, default))
    if not s:
        if default is not None:
            return default
        elif empty:
            return None
    else:
        try:
            return float(s)
        except ValueError:
            return real(prompt=prompt, empty=empty)


def regex(pattern, prompt=None, empty=False, flags=0, default=None):
    """Prompt a string that matches a regular expression.

    Parameters
    ----------
    pattern : str
        A regular expression that must be matched.
    prompt : str, optional
        Use an alternative prompt.
    empty : bool, optional
        Allow an empty response.
    flags : int, optional
        Flags that will be passed to ``re.match``.
    default : str, optional
        Value to substitute as input if response is empty.

    Returns
    -------
    Match or None
        A match object if the user entered a matching string.
        None if the user pressed only Enter and ``empty`` was True.

    See Also
    --------
    re.match

    """
    s = input(_make_prompt(prompt, default))
    if not s:
        if default is not None:
            s = default
        elif empty:
            return None

    m = re.match(pattern, s, flags=flags)
    if m:
        return m
    else:
        return regex(pattern, prompt=prompt, empty=empty, flags=flags)


def secret(prompt=None, empty=False, default=None):
    """Prompt a string without echoing.

    Parameters
    ----------
    prompt : str, optional
        Use an alternative prompt.
    empty : bool, optional
        Allow an empty response.
    default : float, optional
        Value to return if response is empty.

    Returns
    -------
    str or None
        A str if the user entered a non-empty string.
        None if the user pressed only Enter and ``empty`` was True.

    Raises
    ------
    getpass.GetPassWarning
        If echo free input is unavailable.

    See Also
    --------
    getpass.getpass

    """
    s = getpass.getpass(prompt=_make_prompt(prompt, default))
    if not s:
        if default is not None:
            return default
        elif empty:
            return None
    else:
        if s:
            return s
        else:
            return secret(prompt=prompt, empty=empty)


def string(prompt=None, empty=False, default=None):
    """Prompt a string.

    Parameters
    ----------
    prompt : str, optional
        Use an alternative prompt.
    empty : bool, optional
        Allow an empty response.
    default : float, optional
        Value to return if response is empty.

    Returns
    -------
    str or None
        A str if the user entered a non-empty string.
        None if the user pressed only Enter and ``empty`` was True.

    """
    s = input(_make_prompt(prompt, default))
    if not s:
        if default is not None:
            return default
        elif empty:
            return None
    else:
        if s:
            return s
        else:
            return string(prompt=prompt, empty=empty)


def choice(choices, instruction='Select one of the following: ',
           prompt=None, empty=False, default=None):
    """Prompt for a selection from constrained set of choices.

    Parameters
    ----------
    choices : iterable of str
        Ordered choices for user to select
    instruction : str, optional
        Text to appear above available choices
    prompt : str, optional
        Use an alternative prompt.
    empty : bool, optional
        Allow an empty response
    default : float, optional
        Value (found in ``choices``) to return if response is empty.

    Raises
    ------
    ValueError
        If choices is not a sequence of one or more values

    Returns
    -------
        An item from ``choices`` if the user selected a choice.
        None if the user pressed only Enter and ``empty`` was True.

    """
    choices = tuple(choices)
    if len(choices) < 1:
        raise ValueError('Need minimum of one choice!')

    print(instruction)
    for num, cho in enumerate(choices):
        print('    {n}: {c}'.format(n=(num + 1), c=cho))

    s = input(_make_prompt(prompt, default))

    try:
        num = int(s) - 1
        if num < 0:
            raise ValueError
        return choices[num]
    except (ValueError, IndexError):
        if not s:
            if default is not None:
                return default
            elif empty:
                return None
        else:
            return choice(choices, instruction, prompt, empty)


def boolean(prompt=None, yes='y', no='n', default=None, sensitive=False,
            partial=True):
    """Prompt for a yes/no response.

    Parameters
    ----------
    prompt : str, optional
        Use an alternative prompt.
    yes : str, optional
        Response corresponding to 'yes'.
    no : str, optional
        Response correspnding to 'no'.
    default : bool, optional
        The return value if user inputs empty response.
    sensitive : bool, optional
        If True, input is case sensitive.
    partial : bool, optional
        Can user type 'y' or 'ye' for 'yes' and 'n' for 'no'?

    Returns
    -------
    bool
        Either True (if user selects 'yes') or False (if user selects 'no')

    """
    def norm(x):
        return x if sensitive else str(x).lower()

    def to_bool(c):
        """Business logic for converting input to boolean."""
        if partial and len(c):
            if norm(yes).startswith(norm(c)):
                return True
            elif norm(no).startswith(norm(c)):
                return False
        else:
            if norm(yes) == norm(c):
                return True
            elif norm(no) == norm(c):
                return False
        raise ValueError

    if prompt is None:
        y = '[{}]'.format(yes) if default is True else yes
        n = '[{}]'.format(no) if default is False else no
        prompt = '{y}/{n}? '.format(y=y, n=n)

    s = input(prompt)
    if (default is not None) and not s:
       return default

    try:
        return to_bool(s)
    except ValueError:
        return boolean(prompt=prompt, yes=yes, no=no, default=default,
                       sensitive=sensitive, partial=partial)


def _make_prompt(prompt, default):
    if not prompt:
        prompt = '[{}]? '.format(default) if default else PROMPT
    return prompt
