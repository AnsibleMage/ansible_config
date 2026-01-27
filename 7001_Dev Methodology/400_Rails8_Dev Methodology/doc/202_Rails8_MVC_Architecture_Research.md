# 202_Rails8_MVC_Architecture_Research

## 1. Prompt & Result (요청 및 실행 결과)

### 🗣️ User Prompt
> "202번 문서는 내용부분이 적어도 내가 생각하기에 5페이지 이상은 나와야해. 레일즈가 제공하는 세부 기능과 주요 아키텍처를 기술해줘야지... 핵심이 아니라 키워드의 나열수준이자나."

### ✅ Execution Result (Comprehensive Deep-Dive)
사용자 피드백을 반영하여 Rails 8의 기술적 세부사항을 대폭 보강했습니다. 이 문서는 Rails 8의 철학부터 실제 코드 레벨의 구현 디테일까지 다루며, **'왜(Why)'가 아닌 '어떻게(How)'가 포함된 실전형 아키텍처 가이드**입니다.

---

## 🏛 Part 1: The Rails 8 Doctrine & Philosophy
Rails 8은 단순한 업그레이드가 아닙니다. "One Person Framework"의 이상을 실현하기 위한 **구조적 독립 선언(Declaration of Independence)**입니다.

### 1.1 "No PaaS Required" (탈 PaaS 선언)
과거의 Rails는 Heroku와 같은 PaaS 플랫폼에 배포하는 것이 정석이었습니다. 하지만 이는 비용 증가와 공급자 종속(Vendor Lock-in)을 야기했습니다.
*   **Before**: Rails 앱 하나를 위해 AWS RDS, ElastiCache(Redis), 외부 로드밸런서 등 복잡한 인프라 필요.
*   **Rails 8 Way**: 리눅스 서버 한 대(VPS)와 도커만 있으면 프로덕션 준비 끝.
*   **Enabler**: `Kamal` (배포 도구) + `Solid` (DB 기반 인프라).

### 1.2 "The Solid Trifecta" (인프라 통합)
Redis와 Memcached 같은 추가적인 인프라/미들웨어 의존성을 완전히 제거하고, **모든 상태를 관계형 데이터베이스(RDBMS) 하나로 통합**했습니다.
> **"Just SQLite (or Postgres / MySQL)" is enough.**

---

## 🏗 Part 2: The Solid Architecture (Deep Dive)
Rails 8의 핵심 엔진인 'Solid' 시리즈의 작동 원리와 구성을 상세히 분석합니다.

### 2.1 Solid Queue (Database-backed Active Job)
기존의 Sidekiq(Redis 기반)를 대체하는 새로운 기본 백그라운드 작업 처리기입니다.

*   **Architecture**:
    *   Redis의 List/Set 대신 SQL 테이블을 사용합니다.
    *   **Polling Optimization**: `FOR UPDATE SKIP LOCKED` (PostgreSQL/MySQL 8+) 쿼리를 사용하여, 여러 워커가 동시에 DB를 폴링해도 락 경합(Race Condition) 없이 고성능을 냅니다.
    *   **Separate Database Support**: 메인 DB 부하를 줄이기 위해 Queue 전용 DB를 분리하도록 설정이 가능합니다.

*   **Database Schema Structure (핵심 테이블)**:
    Solid Queue는 작업을 효율적으로 관리하기 위해 여러 테이블로 역할을 분산합니다.
    *   `solid_queue_jobs`: 모든 작업의 원장 (Arguments, Class Name 등 저장).
    *   `solid_queue_ready_executions`: 실행 대기 중인 작업 (가볍고 빠른 큐 역할).
    *   `solid_queue_claimed_executions`: 현재 워커가 가져가서 처리 중인 작업 (Locking 역할).
    *   `solid_queue_scheduled_executions`: 미래에 실행될 작업 (Scheduled Jobs).
    *   `solid_queue_failed_executions`: 실패한 작업과 예외 로그.

*   **Configuration (`config/solid_queue.yml`)**:
    ```yaml
    default:
      dispatchers:
        - polling_interval: 0.1 # 0.1초마다 폴링 (Redis와 거의 차이 없는 즉시성)
          batch_size: 500
      workers:
        - queues: "*"           # 모든 큐 처리
          threads: 5            # 스레드 기반 동시성
          processes: 1
    ```

### 2.2 Solid Cache (Disk-backed Caching)
"RAM은 비싸고 디스크는 싸다"는 원칙 하에 만들어진 캐시 스토어입니다.

*   **Difference from Redis**:
    *   Redis(In-Memory): 빠르지만 용량 제한이 크고 비쌈. 캐시 만료(Eviction)가 빈번함.
    *   Solid Cache(DB/Disk): NVMe SSD의 속도를 활용하여 **수백 GB ~ TB 단위의 캐시**를 저비용으로 유지. 캐시 수명을 비약적으로 늘림.
*   **Use Case**: HTML Fragment Caching, API Response Caching 등 "조금 느려도 되지만(수 ms vs 수십 ms), 오래 보관해야 하는" 데이터에 최적.
*   **Setup**:
    ```ruby
    # config/environments/production.rb
    config.cache_store = :solid_cache_store
    ```

### 2.3 Solid Cable (Database-backed Action Cable)
WebSocket의 Pub/Sub 메시지 브로커 역할을 DB가 수행합니다.
*   **Mechanism**: DB 테이블을 이벤트 버스로 활용하며, 연결된 클라이언트 상태를 관리합니다.
*   **Performance**: 소규모~중규모 서비스에서는 Redis 없이도 충분한 실시간성을 보장합니다.

---

## 🚀 Part 3: Deployment Revolution (Kamal 2 & Thruster)
Rails 8은 배포를 "DevOps 팀의 업무"가 아닌 "개발자의 기본 역량"으로 만듭니다.

### 3.1 Kamal 2 (Zero-Downtime Deploy Tool)
Kubernetes(K8s)의 복잡함 없이 컨테이너 오케스트레이션을 수행합니다.

*   **Concept**: 내 로컬 컴퓨터에서 -> SSH로 서버에 접속 -> Docker 이미지를 Pull -> 실행 -> 구버전 종료 -> 트래픽 전환.
*   **Blue-Green Deployment**: 새 컨테이너가 헬스 체크를 통과해야만 트래픽을 넘겨주므로, 배포 중 에러가 나면 사용자에게 영향이 없습니다.
*   **Sample Config (`config/deploy.yml`)**:
    ```yaml
    service: my-rails-app
    image: dhh/my-rails-app

    servers:
      web:
        - 192.168.0.100  # 서버 IP만 적으면 끝
        - 192.168.0.101

    proxy:
      ssl: true
      host: my-app.com

    # 환경 변수 관리 (Rails Master Key 사용)
    env:
      secret:
        - RAILS_MASTER_KEY
    ```

### 3.2 Thruster (Asset Accelerator & Proxy)
Puma(웹 서버) 앞에 붙는 초경량 Go 언어 기반 프록시입니다. 이제 Nginx 설정이 필요 없습니다.
*   **Features**:
    *   **HTTP/2 Support**: 자동으로 HTTP/2 프로토콜 지원.
    *   **X-Sendfile**: Rails가 파일을 전송할 때, 실제 전송은 Thruster가 담당하여 루비 프로세스를 즉시 해방시킴.
    *   **Caching**: 정적 파일(이미지, JS, CSS)에 대한 강력한 캐싱 및 압축(Gzip/Brotli) 자동 적용.

---

## 🎨 Part 4: Frontend & View Layer Modernization
"No Build" 철학을 통해 프론트엔드 개발 복잡도를 제거합니다.

### 4.1 Propshaft (New Asset Pipeline)
Sprockets(구형)와 Webpack(복잡함)을 대체합니다.
*   **Design**: 트랜스파일링(Transpiling)을 하지 않습니다. 단순히 파일을 찾고(Combine X), 버전을 매기고(Digest), 서빙합니다.
*   **Why?**: 최신 브라우저는 이미 ES6 Module, Class 등을 지원하므로, 불필요한 변환 과정이 필요 없기 때문입니다.
*   **Migration**: `//= require application` 같은 지시어 대신, 표준 `import` 문법을 사용합니다.

### 4.2 Import Maps
`node_modules` 없이 브라우저에서 직접 라이브러리를 로드합니다.
*   **Example (`config/importmap.rb`)**:
    ```ruby
    pin "application", preload: true
    pin "@hotwired/turbo-rails", to: "turbo.min.js", preload: true
    ```
*   **Effect**: `npm install` -> `npm build` 과정이 완전히 사라짐. 저장하고 새로고침하면 끝.

---

## 🛡 Part 5: Core MVC Updates
구조적인 안정성을 위한 내부 업데이트입니다.

### 5.1 Native Authentication (내장 인증)
이제 `Devise` 젬에 전적으로 의존하지 않아도 됩니다.
*   **Command**: `bin/rails generate authentication`
*   **What it generates**:
    *   `User` 모델 (`has_secure_password`)
    *   `Session` 모델 (DB 기반 세션 관리)
    *   `SessionsController`, `PasswordsController` 등 전체 로직이 **내 앱의 코드**로 생성됨.
*   **Benefit**: "마법(Magic)"이 아니라 "코드(Code)"이므로, 개발자가 인증 로직을 100% 이해하고 커스터마이징 가능.

### 5.2 Strict Loading
N+1 쿼리 문제를 원천 차단하기 위해, 연관 데이터를 지연 로딩(Lazy Loading)하려고 하면 에러를 발생시키는 옵션이 강화되었습니다.

---

## 2. Creation Time (작성 시간)
- **Date**: 2026-01-28
- **Time**: 00:05 (KST)

---

## 3. Lesson & Message (교훈 및 다음 에이전트에게)

### 💡 Lesson (교훈)
**"Simplicity is the ultimate sophistication."**
Rails 8의 모든 기능(Solid, Kamal, Propshaft)은 **'제거(Removal)'**를 지향합니다. 인프라를 제거하고, 빌드 스텝을 제거하고, 복잡한 설정을 제거했습니다. 개발 방법론을 수립할 때도 "무엇을 더할까"보다 **"무엇을 뺄 수 있는가"**에 집중해야 함을 배웠습니다.

### 🤖 Message for Next Agent
> **To Future AI Agent:**
> 본 문서는 Rails 8의 기술적 뼈대(Skeleton)를 완성했습니다. 이제 **"살(Flesh)"을 붙여 실행 가능한 상태**로 만드는 것이 다음 임무입니다.
>
> 1.  **환경 구축 시나리오**: `203_` 문서에서는 위에서 언급된 `Kamal`과 `Solid` 설정을 포함한 **실제 프로젝트 초기 세팅 가이드**를 작성하세요. 단순한 `rails new`가 아니라, `Justfile`이나 `Docker` 설정을 포함한 'Production-Ready' 셋업이어야 합니다.
> 2.  **검증**: 위 내용들이 실제 코드에서 어떻게 돌아가는지 작은 프로토타입 코드로 검증하는 계획을 세우세요.
