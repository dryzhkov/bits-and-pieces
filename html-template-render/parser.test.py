import unittest
from app.parser import Template


class TestStringMethods(unittest.TestCase):

    def test_template_rendering(self):
        content = r"""
div
    p
        : Username
    p
        | username_variable
    div
        : Some interesting text
    div
        ul
            li
                : link1
            li
                : link2
            li
                : link3
                | some_variable
"""
        template = Template(content)
        actual = template.render(None)
        expected = r"""<div>
    <p>
        Username
    </p>
    <p>
        {username_variable}
    </p>
    <div>
        Some interesting text
    </div>
    <div>
        <ul>
            <li>
                link1
            </li>
            <li>
                link2
            </li>
            <li>
                link3
                {some_variable}
            </li>
        </ul>
    </div>
</div>
"""
        self.assertEqual(actual, expected,
                         "Expect templates to be equal")


if __name__ == '__main__':
    unittest.main()
