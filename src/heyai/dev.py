from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich import box

MARKDOWN_DATA = """
# My Awesome Function

This is a brief explanation of a really cool function I wrote. It takes a list of numbers and returns the sum of the squares of those numbers.

## Code Example (Python)

```python
def sum_of_squares(numbers):
    total = 0
    for number in numbers:
        total += number ** 2
        return total

# Example Usage:
my_numbers = [1, 2, 3, 4, 5]
result = sum_of_squares(my_numbers)
print(f"The sum of squares is: {result}")
```
"""


def main():
    console = Console()
    md = Markdown(MARKDOWN_DATA, code_theme="dracula")
    panel = Panel(md, padding=(1, 4), box=box.HORIZONTALS)
    console.print(panel)
