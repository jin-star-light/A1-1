import unittest


class DefaultPromptTests(unittest.TestCase):
    def test_default_prompts_have_required_fields(self):
        from main import CATEGORIES, create_default_prompts

        prompts = create_default_prompts()

        self.assertGreaterEqual(len(prompts), 3)
        for prompt in prompts:
            self.assertEqual(
                set(prompt), {"title", "content", "category", "favorite"}
            )
            self.assertIn(prompt["category"], CATEGORIES)
            self.assertFalse(prompt["favorite"])


if __name__ == "__main__":
    unittest.main()
