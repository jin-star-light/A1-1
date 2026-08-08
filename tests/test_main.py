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


class AddPromptTests(unittest.TestCase):
    def test_add_prompt_retries_blank_fields_and_appends_prompt(self):
        import main

        prompt_list = []
        answers = iter(["   ", "회의록 요약", "", "회의 내용을 요약해주세요.", "1"])
        output = []

        main.add_prompt(prompt_list, lambda _message: next(answers), output.append)

        self.assertEqual(
            prompt_list,
            [
                {
                    "title": "회의록 요약",
                    "content": "회의 내용을 요약해주세요.",
                    "category": "텍스트 생성",
                    "favorite": False,
                }
            ],
        )
        self.assertEqual(output.count("입력값은 비워둘 수 없습니다."), 2)
        self.assertEqual(output[-1], "프롬프트가 추가되었습니다!")

    def test_add_prompt_accepts_a_custom_category(self):
        import main

        prompt_list = []
        answers = iter(["제목", "내용", "0", "나만의 분류"])

        main.add_prompt(prompt_list, lambda _message: next(answers), lambda _line: None)

        self.assertEqual(prompt_list[0]["category"], "나만의 분류")


class PromptListTests(unittest.TestCase):
    def test_show_list_displays_number_category_title_and_favorite(self):
        import main

        prompt_list = [
            {
                "title": "첫 번째",
                "content": "내용",
                "category": "텍스트 생성",
                "favorite": True,
            },
            {
                "title": "두 번째",
                "content": "내용",
                "category": "이미지 생성",
                "favorite": False,
            },
        ]
        output = []

        main.show_list(prompt_list, output.append)

        self.assertEqual(
            output,
            [
                "\n=== 프롬프트 목록 ===",
                "1. [텍스트 생성] 첫 번째 ⭐",
                "2. [이미지 생성] 두 번째",
                "\n총 2개의 프롬프트",
            ],
        )

    def test_show_list_explains_when_no_prompts_exist(self):
        import main

        output = []
        main.show_list([], output.append)

        self.assertEqual(
            output,
            ["\n=== 프롬프트 목록 ===", "저장된 프롬프트가 없습니다."],
        )


class CategoryFilterTests(unittest.TestCase):
    def test_show_by_category_displays_only_matching_prompts(self):
        import main

        prompt_list = [
            {
                "title": "텍스트 도우미",
                "content": "내용",
                "category": "텍스트 생성",
                "favorite": True,
            },
            {
                "title": "이미지 도우미",
                "content": "내용",
                "category": "이미지 생성",
                "favorite": False,
            },
        ]
        output = []

        main.show_by_category(prompt_list, lambda _message: "1", output.append)

        self.assertIn("\n[텍스트 생성] 카테고리 프롬프트:", output)
        self.assertIn("1. 텍스트 도우미 ⭐", output)
        self.assertNotIn("이미지 도우미", "\n".join(output))
        self.assertEqual(output[-1], "\n총 1개의 프롬프트")

    def test_show_by_category_explains_when_no_matches_exist(self):
        import main

        output = []
        main.show_by_category([], lambda _message: "6", output.append)

        self.assertEqual(output[-1], "해당 카테고리에 등록된 프롬프트가 없습니다.")


if __name__ == "__main__":
    unittest.main()
