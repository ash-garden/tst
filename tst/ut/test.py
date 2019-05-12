#!/usr/bin/python
# coding: UTF-8
import markdown
text = '''
| 左揃え | 中央揃え | 右揃え |
|:-------|:--------:|-------:|
|1       |2         |3       |
|4       |5         |6       |
'''
md = markdown.Markdown(extensions=["tables"]) # ---(*1)
html = md.convert(text) # ---(*2)
print(html)