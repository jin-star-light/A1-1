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


class ConsoleMenuTests(unittest.TestCase):
    def test_show_menu_displays_every_choice(self):
        import main

        output = []
        main.show_menu(output.append)

        self.assertEqual(
            output,
            [
                "\n=== 나만의 프롬프트 관리 ===",
                "1. 프롬프트 추가",
                "2. 프롬프트 목록",
                "3. 카테고리별 조회",
                "4. 프롬프트 검색",
                "5. 프롬프트 상세 보기",
                "6. 즐겨찾기 관리",
                "7. 즐겨찾기 목록",
                "0. 종료",
            ],
        )

    def test_main_repeats_after_invalid_choice_and_then_exits(self):
        import main

        answers = iter(["잘못된 입력", "0"])
        output = []

        main.main([], lambda _message: next(answers), output.append)

        self.assertEqual(output.count("\n=== 나만의 프롬프트 관리 ==="), 2)
        self.assertIn("잘못된 선택입니다. 메뉴 번호를 다시 입력해주세요.", output)
        self.assertEqual(output[-1], "프로그램을 종료합니다.")


if __name__ == "__main__":
    unittest.main()
