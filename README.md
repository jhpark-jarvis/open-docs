# OpenDocs

OpenDocs는 MapleStory 이벤트 공지 정보를 자동 수집하고, OCR 추출, 구조화, 문서화까지 이어가는 AI 기반 문서 플랫폼의 모노레포입니다.

이 저장소는 기능 구현보다 먼저, 앞으로 작업할 때 기준이 되는 프로젝트 구조와 개발 규칙을 정리하는 데 초점을 둡니다.

프로젝트의 최상위 운영 규칙은 [`agents.md`](./agents.md)입니다. 이 문서는 저장소 전체의 기준 문서로 취급합니다.

## 기술 스택

- 프론트엔드: `Next.js` App Router, `TypeScript`, `Tailwind CSS`
- 백엔드: `FastAPI`, `SQLAlchemy 2.0`, `Alembic`, `Pydantic Settings`
- 데이터베이스: `PostgreSQL`
- 로컬 실행: `Docker Compose`
- 인프라: `Terraform`, `ECS` 준비용 `infra/`

## 저장소 구조

```text
.
├─ apps/
│  ├─ api/        # FastAPI 백엔드
│  └─ web/        # Next.js 프론트엔드
├─ docs/          # 아키텍처, ADR, API 문서, 작업 메모
├─ infra/         # Terraform, ECS, 배포 관련 자료
├─ docker-compose.yml
├─ .env.example
└─ PROJECT_PLAN.md
```

## 로컬 실행

1. `.env.example`을 복사해 `.env`를 만듭니다.
2. `docker compose up --build`로 전체 스택을 실행합니다.
3. 프론트엔드는 `http://localhost:3000`에서 확인합니다.
4. 백엔드 헬스체크는 `http://localhost:8000/api/health`입니다.

## 현재 범위

- 이벤트 공지 수집 파이프라인의 골격을 먼저 준비합니다.
- OCR, LLM, 문서 생성, 파서, Nexon 연동은 서비스 경계만 먼저 잡고 필요한 부분부터 구현합니다.
- 인증/인가, 커뮤니티 리뷰 기능은 이후 단계에서 추가합니다.

## 작업 기준

- 비즈니스 로직은 아직 넣지 않습니다.
- 새로운 기능은 `apps/api/app/services/`의 책임 분리를 먼저 따릅니다.
- DB 모델을 추가하면 Alembic 마이그레이션도 함께 준비합니다.
- 문서성 내용은 `docs/`에, 인프라성 내용은 `infra/`에 둡니다.
- ECS 배포를 염두에 두고 설정은 환경변수 기반으로 유지합니다.
- 변경할 내용이 문서와 충돌하면 코드를 바꾸기 전에 관련 문서를 먼저 갱신합니다.

## 참고 문서

- 최상위 운영 규칙: [`agents.md`](./agents.md)
- 작업 단계와 우선순위: [`PROJECT_PLAN.md`](./PROJECT_PLAN.md)
- 제품/기술 문서 작성 기준: [`docs/README.md`](./docs/README.md)
- 인프라 작업 기준: [`infra/README.md`](./infra/README.md)

## 개발 규칙

- 코드 추가 전에 기존 구조와 파일 위치를 먼저 확인합니다.
- 새 파일은 가능한 한 현재 패키지 구조에 맞춰 추가합니다.
- 임시 실험 코드와 실제 제품 코드는 섞지 않습니다.
- 구현하지 않은 영역은 주석이나 파일명으로 의도를 드러냅니다.
