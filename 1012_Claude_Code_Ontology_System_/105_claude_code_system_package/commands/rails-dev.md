# /rails-dev - TDD 기반 개발

작업계획서의 태스크를 TDD 방식으로 개발합니다.

## 트리거
- "개발", "TDD", "구현해줘", "/rails-dev [태스크명]"

## 실행 단계

### 1. 태스크 확인

```javascript
// TODO에서 태스크 상태 업데이트
TaskUpdate({
  taskId: "[ID]",
  status: "in_progress"
})
```

`docs/TaskPlan.md`에서 해당 태스크 상세 확인:
- 수용 기준
- 의존성
- 예상 파일

### 2. RED - 실패하는 테스트 작성

#### Model Spec 예시
```ruby
# spec/models/[model]_spec.rb
require 'rails_helper'

RSpec.describe [Model], type: :model do
  describe 'validations' do
    it { is_expected.to validate_presence_of(:field) }
  end

  describe 'associations' do
    it { is_expected.to belong_to(:parent) }
    it { is_expected.to have_many(:children) }
  end
end
```

#### Request Spec 예시
```ruby
# spec/requests/[resources]_spec.rb
require 'rails_helper'

RSpec.describe '[Resources] API', type: :request do
  describe 'GET /[resources]' do
    it 'returns list' do
      get '/[resources]'
      expect(response).to have_http_status(:ok)
    end
  end
end
```

#### System Spec 예시
```ruby
# spec/system/[feature]_spec.rb
require 'rails_helper'

RSpec.describe '[Feature]', type: :system do
  it 'allows user to [action]' do
    visit [path]
    # ...
    expect(page).to have_content('[expected]')
  end
end
```

### 3. 테스트 실행 (실패 확인)

```bash
bundle exec rspec [spec_file]
# Expected: FAIL
```

### 4. GREEN - 테스트 통과하는 최소 코드 작성

#### Generator 사용 (필요시)
```bash
rails generate model [Model] [fields]
rails generate controller [Controller] [actions]
rails generate migration [Migration]
```

#### 마이그레이션 실행
```bash
rails db:migrate
```

#### 모델 구현
```ruby
# app/models/[model].rb
class [Model] < ApplicationRecord
  # 관계
  belongs_to :parent
  has_many :children

  # 유효성 검사
  validates :field, presence: true

  # Scope
  scope :active, -> { where(active: true) }
end
```

#### 컨트롤러 구현
```ruby
# app/controllers/[resources]_controller.rb
class [Resources]Controller < ApplicationController
  def index
    @resources = [Model].all
  end

  def create
    @resource = [Model].new(resource_params)
    if @resource.save
      redirect_to @resource
    else
      render :new, status: :unprocessable_entity
    end
  end

  private

  def resource_params
    params.require(:resource).permit(:field1, :field2)
  end
end
```

### 5. 테스트 실행 (통과 확인)

```bash
bundle exec rspec [spec_file]
# Expected: PASS
```

### 6. REFACTOR - 코드 개선

- 코드 중복 제거
- Concern 추출 (필요시)
- Service Object 분리 (필요시)
- RuboCop 자동 수정

```bash
bundle exec rubocop -a
```

### 7. 테스트 재실행 (통과 유지)

```bash
bundle exec rspec
# Expected: PASS
```

### 8. 커밋

```bash
git add .
git commit -m "feat: [feature description]

- [변경사항 1]
- [변경사항 2]

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
```

### 9. 태스크 완료

```javascript
TaskUpdate({
  taskId: "[ID]",
  status: "completed"
})
```

## TDD 사이클 요약

```
┌───────────┐     ┌───────────┐     ┌───────────┐
│    RED    │ ──► │   GREEN   │ ──► │ REFACTOR  │
│  테스트   │     │   구현    │     │   개선    │
│  (실패)   │     │  (통과)   │     │ (통과유지) │
└───────────┘     └───────────┘     └───────────┘
      ▲                                   │
      └───────────────────────────────────┘
```

## 출력 예시

```
📋 태스크: T1.5 User 모델 구현

🔴 RED: 테스트 작성
   → spec/models/user_spec.rb (15 examples)
   → bundle exec rspec spec/models/user_spec.rb
   → 15 examples, 15 failures ✓

🟢 GREEN: 코드 작성
   → app/models/user.rb
   → db/migrate/..._create_users.rb
   → rails db:migrate
   → bundle exec rspec spec/models/user_spec.rb
   → 15 examples, 0 failures ✓

🔵 REFACTOR: 코드 개선
   → Concern 추출: Authenticatable
   → RuboCop 자동 수정
   → bundle exec rspec
   → 15 examples, 0 failures ✓

📝 COMMIT: feat: implement User model with authentication

✅ 태스크 완료

다음 태스크: T1.6 Sessions Controller
```

## 다음 단계

- `/rails-test`: 전체 테스트 실행 및 커버리지 확인
- `/rails-deploy`: 프로덕션 배포
