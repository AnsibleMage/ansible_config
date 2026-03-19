# /rails-init - Rails 8 프로젝트 초기화

새로운 Rails 8 프로젝트를 생성하고 바이브코딩 환경을 설정합니다.

## 트리거
- "Rails 초기화", "새 프로젝트", "rails new"

## 실행 단계

### 1. 프로젝트 생성

```bash
rails new $ARGUMENTS \
  --database=postgresql \
  --css=tailwind \
  --skip-jbuilder \
  --skip-action-mailbox \
  --skip-test
```

### 2. 디렉토리 이동 및 의존성 설치

```bash
cd $ARGUMENTS
bundle install
```

### 3. Gemfile 확장 (RSpec, 품질 도구 추가)

Gemfile에 다음 gem 추가:

```ruby
group :development, :test do
  gem 'rspec-rails', '~> 6.1'
  gem 'factory_bot_rails'
  gem 'faker'
end

group :development do
  gem 'rubocop', require: false
  gem 'rubocop-rails', require: false
  gem 'rubocop-rspec', require: false
  gem 'bullet'
end

group :test do
  gem 'capybara'
  gem 'selenium-webdriver'
  gem 'shoulda-matchers'
  gem 'database_cleaner-active_record'
  gem 'simplecov', require: false
end
```

### 4. RSpec 초기화

```bash
bundle install
rails generate rspec:install
```

### 5. 바이브코딩 디렉토리 구조 생성

```bash
mkdir -p app/services
mkdir -p app/queries
mkdir -p docs
mkdir -p .claude
```

### 6. 기본 파일 생성

**app/services/application_service.rb**:
```ruby
class ApplicationService
  def self.call(...)
    new(...).call
  end
end
```

**app/services/result.rb**:
```ruby
class Result
  attr_reader :value, :errors

  def initialize(success:, value: nil, errors: [])
    @success = success
    @value = value
    @errors = Array(errors)
  end

  def success? = @success
  def failure? = !success?

  def self.success(value = nil) = new(success: true, value: value)
  def self.failure(errors) = new(success: false, errors: errors)
end
```

**.claude/project_context.md**:
```markdown
# Project Context

## Overview
[프로젝트 설명]

## Tech Stack
- Rails 8.0
- PostgreSQL
- Tailwind CSS
- Solid Queue/Cache/Cable

## Key Decisions
[기술 결정 사항]

## Current Sprint
[현재 작업]
```

### 7. 데이터베이스 생성

```bash
rails db:create
```

### 8. Git 초기화

```bash
git init
git add .
git commit -m "Initial commit: Rails 8 project setup

- Rails 8 with PostgreSQL and Tailwind CSS
- RSpec test framework
- Vibe Coding directory structure
- Service object pattern base classes

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
```

### 9. 완료 메시지

```
✓ Rails 8 프로젝트 '$ARGUMENTS' 생성 완료

다음 단계:
1. cd $ARGUMENTS
2. 요구사항을 말씀해주시면 PRD를 생성합니다.
3. /rails-prd로 PRD 생성

프로젝트 구조:
├── app/services/    # Service Objects
├── app/queries/     # Query Objects
├── docs/            # 문서 (PRD, TaskPlan)
├── .claude/         # Claude Code 설정
└── spec/            # RSpec 테스트
```

## 옵션

사용자가 추가 옵션을 지정할 수 있습니다:

- `--skip-tailwind`: Tailwind CSS 제외
- `--api`: API 전용 프로젝트
- 기타 Rails 옵션

## 주의사항

- PostgreSQL이 실행 중이어야 합니다
- Ruby 3.3+ 필요
- Rails 8.0+ 필요
