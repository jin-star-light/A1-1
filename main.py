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
