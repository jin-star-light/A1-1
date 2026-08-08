"""콘솔 기반 프롬프트 관리 프로그램."""

CATEGORIES = [
    "텍스트 생성",
    "이미지 생성",
    "영상 생성",
    "페르소나",
    "자동화",
    "기타",
]


def create_default_prompts():
    """프로그램 시작 시 사용할 기본 프롬프트 목록을 반환한다."""
    return [
        {
            "title": "블로그 글 작성 도우미",
            "content": (
                "당신은 10년 경력의 전문 블로거입니다. 주어진 주제에 대해 "
                "SEO에 최적화된 블로그 글을 작성해주세요."
            ),
            "category": "텍스트 생성",
            "favorite": False,
        },
        {
            "title": "제품 썸네일 생성",
            "content": (
                "제품의 특징과 대상 고객을 반영한 매력적인 썸네일 이미지를 "
                "생성해주세요."
            ),
            "category": "이미지 생성",
            "favorite": False,
        },
        {
            "title": "IT 컨설턴트 페르소나",
            "content": (
                "당신은 기업의 문제를 분석하고 실행 가능한 해결책을 제안하는 "
                "15년 경력의 IT 컨설턴트입니다."
            ),
            "category": "페르소나",
            "favorite": False,
        },
    ]


prompts = create_default_prompts()


def show_menu(output_func=print):
    """메인 메뉴를 출력한다."""
    menu_lines = [
        "\n=== 나만의 프롬프트 관리 ===",
        "1. 프롬프트 추가",
        "2. 프롬프트 목록",
        "3. 카테고리별 조회",
        "4. 프롬프트 검색",
        "5. 프롬프트 상세 보기",
        "6. 즐겨찾기 관리",
        "7. 즐겨찾기 목록",
        "0. 종료",
    ]
    for line in menu_lines:
        output_func(line)


def read_required(message, input_func, output_func):
    """공백이 아닌 값이 입력될 때까지 요청한다."""
    while True:
        value = input_func(message).strip()
        if value:
            return value
        output_func("입력값은 비워둘 수 없습니다.")


def choose_category(input_func, output_func):
    """기본 목록 또는 직접 입력으로 카테고리를 선택한다."""
    while True:
        output_func("\n카테고리 선택:")
        for index, category in enumerate(CATEGORIES, start=1):
            output_func(f"{index}) {category}")
        output_func("0) 직접 입력")

        choice = input_func("선택: ").strip()
        if choice == "0":
            return read_required("카테고리: ", input_func, output_func)
        if choice.isdigit() and 1 <= int(choice) <= len(CATEGORIES):
            return CATEGORIES[int(choice) - 1]
        output_func("올바른 카테고리 번호를 입력해주세요.")


def add_prompt(prompt_list, input_func=input, output_func=print):
    """새 프롬프트를 목록에 추가한다."""
    output_func("\n=== 프롬프트 추가 ===")
    title = read_required("제목: ", input_func, output_func)
    content = read_required("내용: ", input_func, output_func)
    category = choose_category(input_func, output_func)

    prompt_list.append(
        {
            "title": title,
            "content": content,
            "category": category,
            "favorite": False,
        }
    )
    output_func("프롬프트가 추가되었습니다!")


def show_list(prompt_list, output_func=print):
    """저장된 모든 프롬프트의 요약 목록을 출력한다."""
    output_func("\n=== 프롬프트 목록 ===")
    if not prompt_list:
        output_func("저장된 프롬프트가 없습니다.")
        return

    for index, prompt in enumerate(prompt_list, start=1):
        favorite = " ⭐" if prompt["favorite"] else ""
        output_func(
            f"{index}. [{prompt['category']}] {prompt['title']}{favorite}"
        )
    output_func(f"\n총 {len(prompt_list)}개의 프롬프트")


def show_by_category(prompt_list, input_func=input, output_func=print):
    """선택한 카테고리의 프롬프트만 출력한다."""
    output_func("\n=== 카테고리별 조회 ===")
    category = choose_category(input_func, output_func)
    matches = [
        prompt for prompt in prompt_list if prompt["category"] == category
    ]

    output_func(f"\n[{category}] 카테고리 프롬프트:")
    if not matches:
        output_func("해당 카테고리에 등록된 프롬프트가 없습니다.")
        return

    for index, prompt in enumerate(matches, start=1):
        favorite = " ⭐" if prompt["favorite"] else ""
        output_func(f"{index}. {prompt['title']}{favorite}")
    output_func(f"\n총 {len(matches)}개의 프롬프트")


def search_prompt(prompt_list, input_func=input, output_func=print):
    """제목 또는 내용에서 키워드와 일치하는 프롬프트를 출력한다."""
    output_func("\n=== 프롬프트 검색 ===")
    keyword = read_required("검색어: ", input_func, output_func).casefold()
    matches = [
        prompt
        for prompt in prompt_list
        if keyword in prompt["title"].casefold()
        or keyword in prompt["content"].casefold()
    ]

    if not matches:
        output_func("검색 결과가 없습니다.")
        return

    output_func("\n검색 결과:")
    for index, prompt in enumerate(matches, start=1):
        favorite = " ⭐" if prompt["favorite"] else ""
        output_func(
            f"{index}. [{prompt['category']}] {prompt['title']}{favorite}"
        )
    output_func(f"\n{len(matches)}개의 프롬프트를 찾았습니다.")


def get_prompt_by_number(prompt_list, value, output_func):
    """1부터 시작하는 번호를 실제 프롬프트로 변환한다."""
    if not value.isdigit():
        output_func("올바른 프롬프트 번호를 입력해주세요.")
        return None

    index = int(value) - 1
    if not 0 <= index < len(prompt_list):
        output_func("올바른 프롬프트 번호를 입력해주세요.")
        return None
    return prompt_list[index]


def show_detail(prompt_list, input_func=input, output_func=print):
    """선택한 프롬프트의 전체 내용을 출력한다."""
    output_func("\n=== 프롬프트 상세 보기 ===")
    value = input_func("번호 입력: ").strip()
    prompt = get_prompt_by_number(prompt_list, value, output_func)
    if prompt is None:
        return

    favorite = "⭐" if prompt["favorite"] else "아니오"
    output_func("─" * 28)
    output_func(f"제목: {prompt['title']}")
    output_func(f"카테고리: {prompt['category']}")
    output_func(f"즐겨찾기: {favorite}")
    output_func("─" * 28)
    output_func("내용:")
    output_func(prompt["content"])
    output_func("─" * 28)


def toggle_favorite(prompt_list, input_func=input, output_func=print):
    """선택한 프롬프트의 즐겨찾기 상태를 반전한다."""
    output_func("\n=== 즐겨찾기 관리 ===")
    value = input_func("프롬프트 번호 입력: ").strip()
    prompt = get_prompt_by_number(prompt_list, value, output_func)
    if prompt is None:
        return

    prompt["favorite"] = not prompt["favorite"]
    if prompt["favorite"]:
        output_func(
            f"'{prompt['title']}' 프롬프트를 즐겨찾기에 추가했습니다!"
        )
    else:
        output_func(
            f"'{prompt['title']}' 프롬프트를 즐겨찾기에서 해제했습니다!"
        )


def main(prompt_list=None, input_func=input, output_func=print):
    """메뉴 선택을 반복 처리한다."""
    if prompt_list is None:
        prompt_list = prompts

    while True:
        show_menu(output_func)
        choice = input_func("선택: ").strip()

        if choice == "0":
            output_func("프로그램을 종료합니다.")
            break

        if choice == "1":
            add_prompt(prompt_list, input_func, output_func)
            continue

        if choice == "2":
            show_list(prompt_list, output_func)
            continue

        if choice == "3":
            show_by_category(prompt_list, input_func, output_func)
            continue

        if choice == "4":
            search_prompt(prompt_list, input_func, output_func)
            continue

        if choice == "5":
            show_detail(prompt_list, input_func, output_func)
            continue

        if choice == "6":
            toggle_favorite(prompt_list, input_func, output_func)
            continue

        output_func("잘못된 선택입니다. 메뉴 번호를 다시 입력해주세요.")


if __name__ == "__main__":
    main()
