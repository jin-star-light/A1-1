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

        output_func("잘못된 선택입니다. 메뉴 번호를 다시 입력해주세요.")


if __name__ == "__main__":
    main()
