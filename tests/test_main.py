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

    def test_choose_category_retries_unicode_digit_that_int_rejects(self):
        import main

        answers = iter(["²", "1"])
        output = []

        category = main.choose_category(
            lambda _message: next(answers), output.append
        )

        self.assertEqual(category, "텍스트 생성")
        self.assertIn("올바른 카테고리 번호를 입력해주세요.", output)


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


class PromptSearchTests(unittest.TestCase):
    def test_search_prompt_matches_title_or_content_case_insensitively(self):
        import main

        prompt_list = [
            {
                "title": "Blog Helper",
                "content": "SEO 글쓰기",
                "category": "텍스트 생성",
                "favorite": True,
            },
            {
                "title": "업무 도우미",
                "content": "BLOG 초안 검토",
                "category": "자동화",
                "favorite": False,
            },
            {
                "title": "이미지 도우미",
                "content": "썸네일 생성",
                "category": "이미지 생성",
                "favorite": False,
            },
        ]
        output = []

        main.search_prompt(prompt_list, lambda _message: "  blog  ", output.append)

        self.assertIn("1. [텍스트 생성] Blog Helper ⭐", output)
        self.assertIn("2. [자동화] 업무 도우미", output)
        self.assertNotIn("이미지 도우미", "\n".join(output))
        self.assertEqual(output[-1], "\n2개의 프롬프트를 찾았습니다.")

    def test_search_prompt_explains_when_no_matches_exist(self):
        import main

        output = []
        main.search_prompt([], lambda _message: "없는 검색어", output.append)

        self.assertEqual(output[-1], "검색 결과가 없습니다.")


class PromptDetailTests(unittest.TestCase):
    def test_show_detail_displays_every_prompt_field(self):
        import main

        prompt_list = [
            {
                "title": "상세 프롬프트",
                "content": "전체 내용입니다.",
                "category": "페르소나",
                "favorite": True,
            }
        ]
        output = []

        main.show_detail(prompt_list, lambda _message: "1", output.append)

        rendered = "\n".join(output)
        self.assertIn("제목: 상세 프롬프트", rendered)
        self.assertIn("카테고리: 페르소나", rendered)
        self.assertIn("즐겨찾기: ⭐", rendered)
        self.assertIn("내용:\n전체 내용입니다.", rendered)

    def test_show_detail_rejects_an_invalid_number(self):
        import main

        output = []
        main.show_detail([], lambda _message: "잘못된 값", output.append)

        self.assertEqual(output[-1], "올바른 프롬프트 번호를 입력해주세요.")

    def test_show_detail_rejects_unicode_digit_that_int_rejects(self):
        import main

        output = []
        main.show_detail([], lambda _message: "²", output.append)

        self.assertEqual(output[-1], "올바른 프롬프트 번호를 입력해주세요.")


class FavoriteToggleTests(unittest.TestCase):
    def test_toggle_favorite_adds_and_then_removes_favorite(self):
        import main

        prompt_list = [
            {
                "title": "즐겨찾기 대상",
                "content": "내용",
                "category": "기타",
                "favorite": False,
            }
        ]
        output = []

        main.toggle_favorite(prompt_list, lambda _message: "1", output.append)
        self.assertTrue(prompt_list[0]["favorite"])
        self.assertEqual(
            output[-1], "'즐겨찾기 대상' 프롬프트를 즐겨찾기에 추가했습니다!"
        )

        main.toggle_favorite(prompt_list, lambda _message: "1", output.append)
        self.assertFalse(prompt_list[0]["favorite"])
        self.assertEqual(
            output[-1], "'즐겨찾기 대상' 프롬프트를 즐겨찾기에서 해제했습니다!"
        )

    def test_toggle_favorite_rejects_out_of_range_number(self):
        import main

        output = []
        main.toggle_favorite([], lambda _message: "1", output.append)

        self.assertEqual(output[-1], "올바른 프롬프트 번호를 입력해주세요.")


class FavoriteListTests(unittest.TestCase):
    def test_show_favorites_displays_only_favorite_prompts(self):
        import main

        prompt_list = [
            {
                "title": "선택됨",
                "content": "내용",
                "category": "자동화",
                "favorite": True,
            },
            {
                "title": "선택 안 됨",
                "content": "내용",
                "category": "기타",
                "favorite": False,
            },
        ]
        output = []

        main.show_favorites(prompt_list, output.append)

        self.assertIn("1. [자동화] 선택됨 ⭐", output)
        self.assertNotIn("선택 안 됨", "\n".join(output))
        self.assertEqual(output[-1], "\n총 1개의 즐겨찾기")

    def test_show_favorites_explains_when_no_favorites_exist(self):
        import main

        output = []
        main.show_favorites([], output.append)

        self.assertEqual(output[-1], "즐겨찾기된 프롬프트가 없습니다.")


class FullConsoleWorkflowTests(unittest.TestCase):
    def test_menu_dispatch_keeps_added_and_favorite_state_until_exit(self):
        import main

        prompt_list = []
        answers = iter(
            [
                "1",
                "새 프롬프트",
                "새 내용",
                "1",
                "2",
                "6",
                "1",
                "7",
                "3",
                "1",
                "4",
                "새 프롬프트",
                "5",
                "1",
                "0",
            ]
        )
        output = []

        main.main(prompt_list, lambda _message: next(answers), output.append)

        self.assertEqual(len(prompt_list), 1)
        self.assertTrue(prompt_list[0]["favorite"])
        rendered = "\n".join(output)
        self.assertIn("=== 프롬프트 목록 ===", rendered)
        self.assertIn("=== 즐겨찾기 목록 ===", rendered)
        self.assertIn("[텍스트 생성] 카테고리 프롬프트:", rendered)
        self.assertIn("1개의 프롬프트를 찾았습니다.", rendered)
        self.assertIn("내용:\n새 내용", rendered)
        self.assertEqual(output[-1], "프로그램을 종료합니다.")


if __name__ == "__main__":
    unittest.main()
