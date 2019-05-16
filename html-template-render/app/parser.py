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
    def __init__(self, content, indent):
        self.content = content
        self.indent = indent
        self.children = []

    def __repr__(self):
        return 'node(' + repr(self.content) + ', ' + repr(self.indent) + ') has ' + str(len(self.children)) + ' children'

    def getHTML(self, isClosing, params):
        pass

    def render(self, params):
        return '{}{}\n'.format(' ' * self.indent * 4, self.getHTML(False, params))


class TagNode(Node):
    def getHTML(self, isClosing, params):
        if isClosing == True:
            return "</{}>".format(self.content)
        else:
            return "<{}>".format(self.content)

    def render(self, params):
        out = super(TagNode, self).render(params)

        for child in self.children:
            out += child.render(params)

        out += '{}{}\n'.format(' ' * self.indent * 4,
                               self.getHTML(True, params))

        return out


class TextNode(Node):
    def getHTML(self, isClosing, params):
        return self.content

    def render(self, params):
        return super(TextNode, self).render(params)


class CodeNode(Node):
    def getHTML(self, isClosing, params):
        return str(eval(self.content, params))

    def render(self, params):
        return super(CodeNode, self).render(params)


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
                nodes.append(TextNode(data[2:], indent))
            elif data.startswith('| '):
                nodes.append(CodeNode(data[2:], indent))
            else:
                nodes.append(TagNode(data, indent))

        return nodes

    def __parse(self, tokens):
        root = tokens.pop(0)
        depthToParent = {0: root}
        for node in tokens:
            parent = depthToParent[node.indent - 1]
            parent.children.append(node)
            depthToParent[node.indent] = node

        return root
