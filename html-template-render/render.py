#!/usr/bin/env python3
"""This module converts templates to HTML

    Example:
        Source:
            div
                p
                    : Username
                p
                    | username_variable

        Result:
            <div>
                <p>
                    Username
                </p>
                <p>
                    bob@example.com
                </p>
            </div>

"""


from pprint import pprint as pp
import re


class Node:

    def __init__(self, type, content, indent):
        self.type = type
        self.content = content
        self.indent = indent
        self.children = []

    def __repr__(self):
        return 'node(' + repr(self.type) + ', ' + repr(self.content) + ', ' + repr(self.indent) + ') has ' + str(len(self.children)) + ' children'

    def getHTML(self):
        if self.type == "text":
            return self.content
        elif self.type == "code":
            return self.content
        else:
            return "<{}>".format(self.content)

    def toHTML(self):
        pp(' ' * self.indent * 4 + self.getHTML())
        for child in self.children:
            child.toHTML()


template = r"""
div
    p
        : Username
    p
        | username_variable
"""


def render(tmpl):
    tokens = tokenize(tmpl)
    pp(tokens)
    tree = parse(tokens)
    html = tree.toHTML()
    return html


def tokenize(tmpl):
    nodes = []
    lines = list(filter(lambda x: x != "", tmpl.split('\n')))
    for line in lines:
        m = re.match('( *)(.*)', line)
        spaces, data = m.group(1), m.group(2)
        indent = len(spaces) // 4

        if data.startswith(': '):
            nodes.append(Node("text", data[2:], indent))
        elif data.startswith('| '):
            nodes.append(Node('code', data[2:], indent))
        else:
            nodes.append(Node('element', data, indent))

    return nodes


def parse(tokens):
    root = tokens.pop(0)
    depthToParent = {0: root}
    for node in tokens:
        parent = depthToParent[node.indent - 1]
        pp(parent)
        parent.children.append(node)
        depthToParent[node.indent] = node

    return root


htmlOut = render(template)
pp(htmlOut)
