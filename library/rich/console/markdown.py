from rich import print as rich_print
from rich.markdown import Markdown

nome = "Ramon"
markdown_text = """
# Título Principal
## Subtítulo
- Item 1
- Item 2
```python
def saudacao():
    return "Olá, mundo!"
```     
meu nome é **Ramon** e eu tenho *30 anos*.

menu - pizza
- sushi
1. Item 1
2. Item 2
>>> Citação


"""
rich_print(Markdown(markdown_text))