import unittest

from app.app import app


class SecurityRegressionTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.demo = {"nome": "Demo", "sobrenome": "User", "id_colaborador": "LAB-001"}

    def test_preview_has_no_credentials_and_uses_reserved_domain(self):
        response = self.client.post("/", data={**self.demo, "criar_email": "on"})
        body = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("demo.user@example.invalid", body)
        self.assertNotIn("Senha:", body)
        self.assertNotIn("DU LAB-001", body)
        self.assertIn("No account has been created", body)

    def test_missing_fields_do_not_crash(self):
        self.assertEqual(self.client.post("/", data={}).status_code, 400)

    def test_script_markup_is_rejected_and_not_reflected(self):
        response = self.client.post("/", data={**self.demo, "nome": "<script>alert(1)</script>"})
        self.assertEqual(response.status_code, 400)
        self.assertNotIn(b"<script>", response.data)

    def test_quotes_are_escaped_by_template(self):
        response = self.client.post("/", data={**self.demo, "sobrenome": "O'Example"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"O&#39;Example", response.data)

    def test_unicode_names_and_normalized_username(self):
        response = self.client.post("/", data={**self.demo, "nome": "Jos\u00e9"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"jose.user", response.data)

    def test_unusable_username_returns_validation_error(self):
        self.assertEqual(self.client.post("/", data={**self.demo, "nome": "\u6d4b\u8bd5"}).status_code, 400)

    def test_control_characters_and_long_fields_rejected(self):
        for field, value in [("nome", "A" * 81), ("id_colaborador", "id\nvalue"), ("sobrenome", " ")]:
            with self.subTest(field=field):
                self.assertEqual(self.client.post("/", data={**self.demo, field: value}).status_code, 400)

    def test_body_size_limit(self):
        self.assertEqual(self.client.post("/", data={"nome": "x" * 5000}).status_code, 413)

    def test_untrusted_host_rejected(self):
        self.assertEqual(self.client.get("/", headers={"Host": "untrusted.invalid"}).status_code, 400)

    def test_response_headers_on_success_and_error(self):
        for response in [self.client.get("/"), self.client.post("/", data={})]:
            self.assertEqual(response.headers["Cache-Control"], "no-store")
            self.assertEqual(response.headers["X-Content-Type-Options"], "nosniff")
            self.assertIn("frame-ancestors 'none'", response.headers["Content-Security-Policy"])


if __name__ == "__main__":
    unittest.main()
