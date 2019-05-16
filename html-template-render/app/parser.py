#!/usr/bin/env python3
"""This module converts templates to raw HTML

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

    def getHTML(self, isClosing):
        if self.type == "text":
            return self.content
        elif self.type == "code":
            return "{" + self.content + "}"
        elif isClosing == True:
            return "</{}>".format(self.content)
        else:
            return "<{}>".format(self.content)

    def render(self, params):
        indentStr = ' ' * self.indent * 4
        out = '{}{}\n'.format(indentStr, self.getHTML(False))

        for child in self.children:
            out += child.render(params)

        if self.type == 'element':
            out += '{}{}\n'.format(indentStr, self.getHTML(True))

        return out


class Template:
    def __init__(self, content):
        self.content = content

    def render(self, params):
        tokens = self.__tokenize(self.content)
        tree = self.__parse(tokens)
        html = tree.render(params)
        return html

    def __tokenize(self, content):
        nodes = []
        lines = list(filter(lambda x: x != "", content.split('\n')))
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

    def __parse(self, tokens):
        root = tokens.pop(0)
        depthToParent = {0: root}
        for node in tokens:
            parent = depthToParent[node.indent - 1]
            parent.children.append(node)
            depthToParent[node.indent] = node

        return root
