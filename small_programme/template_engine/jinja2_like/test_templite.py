import unittest


from templite import Template, tokenize, Text, Expr


class TemplateTest(unittest.TestCase):
    def render(self, text: str, ctx: dict, expected: str):
        rendered = Template(text).render(ctx)
        self.assertEqual(expected, rendered)

    def test_plain_text(self):
        for text in [
            "This is a simple message",
            "<h1>This is a html message</h1>",
            "This is a multi line message\n this is line2 of the message",
        ]:
            self.render(text, {}, text)


class TokenTest(unittest.TestCase):
    def test_single_variable(self):
        tokens = tokenize("Hello, {{name}}!")
        self.assertEqual(tokens, [Text("Hello, "), Expr("name"), Text("!")])

    def test_two_variables(self):
        tokens = tokenize("Hello, {{name}} in {{year}}")
        self.assertEqual(
            tokens, [Text("Hello, "), Expr("name"), Text(" in "), Expr("year")]
        )


if __name__ == "__main__":
    unittest.main()
