import unittest


from templite import (
    TemplateEngine,
    tokenize,
    Text,
    Expr,
    Comment,
    For,
    EndFor,
    parse_expr,
)


class TemplateTest(unittest.TestCase):
    def render(self, text: str, ctx: dict, expected: str, filters: dict = None):
        engine = TemplateEngine()
        if filters:
            for filter_name, fn in filters.items():
                engine.register_filter(filter_name, fn)
        template = engine.create(text)
        rendered = template.render(ctx)
        self.assertEqual(expected, rendered)

    def test_plain_text(self):
        for text in [
            "This is a simple message",
            "<h1>This is a html message</h1>",
            "This is a multi line message\n this is line2 of the message",
        ]:
            self.render(text, {}, text)

    def test_expr_single(self):
        self.render("hello {{name}}", {"name": "world"}, "hello world")

    def test_expr_array(self):
        self.render("hello {{names[0]}}", {"names": ["wang"]}, "hello wang")

    def test_expr_dict(self):
        self.render("hello {{names['guest']}}", {"names": {"guest": 123}}, "hello 123")

    def test_expr_multi(self):
        self.render(
            "Hello, {{name}} in {{year}}",
            {"name": "he", "year": 2020},
            "Hello, he in 2020",
        )

    def test_expr_variable_missing(self):
        with self.assertRaises(NameError):
            self.render("{{name}}", {}, "")

    def test_expr_with_addition_filter(self):
        first = lambda x: x[0]
        self.render(
            "Hello, {{ name | upper | first}}!",
            {"name": "alice"},
            "Hello, A!",
            filters={"first": first},
        )

    def test_expr_filter_missing(self):
        with self.assertRaises(NameError):
            self.render(
                "Hello, {{ name | upper | first}}!",
                {"name": "alice"},
                "Hello, A!",
            )

    def test_comment(self):
        self.render("Hello, {# This is a comment. #}World!", {}, "Hello, World!")


class TokenTest(unittest.TestCase):
    def test_single_variable(self):
        tokens = tokenize("Hello, {{name}}!")
        self.assertEqual(tokens, [Text("Hello, "), Expr("name"), Text("!")])

    def test_two_variables(self):
        tokens = tokenize("Hello, {{name}} in {{year}}")
        self.assertEqual(
            tokens, [Text("Hello, "), Expr("name"), Text(" in "), Expr("year")]
        )

    def test_parse_repr(self):
        cases = [
            ("name", "name", []),
            ("name | upper", "name", ["upper"]),
            ("name | upper | strip", "name", ["upper", "strip"]),
            (
                "'a string with | inside' | upper | strip",
                "'a string with | inside'",
                ["upper", "strip"],
            ),
        ]
        for expr, varname, filters in cases:
            parsed_varname, parsed_filters = parse_expr(expr)
            self.assertEqual(parsed_filters, filters)
            self.assertEqual(parsed_varname, varname)

    def test_parse_comment(self):
        tokens = tokenize("Hello, {# name #} abc")
        self.assertEqual(tokens, [Text("Hello, "), Comment("name"), Text(" abc")])

    def test_parse_for_loop(self):
        tokens = tokenize("{% for row in rows %}Loop {{ row }}{% endfor %}")
        self.assertEqual(
            tokens,
            [
                For("row", "rows"),
                Text("Loop "),
                Expr("row"),
                EndFor(),
            ],
        )


if __name__ == "__main__":
    unittest.main()
