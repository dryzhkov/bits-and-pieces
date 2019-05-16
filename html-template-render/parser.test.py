import unittest
from app.parser import Template


class TestStringMethods(unittest.TestCase):

    def test_template_rendering(self):
        content = r"""
div
    p
        : Email
    p
        | email
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
"""
        template = Template(content)
        actual = template.render({'email': 'bob@example.com'})
        expected = r"""<div>
    <p>
        Email
    </p>
    <p>
        bob@example.com
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
            </li>
        </ul>
    </div>
</div>
"""
        self.assertEqual(actual, expected,
                         "Expect templates to be equal")


if __name__ == '__main__':
    unittest.main()
