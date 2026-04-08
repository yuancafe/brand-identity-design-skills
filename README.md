# Brand Identity Design Skills

[English](#english) | [中文](#中文)

## English

Brand Identity Design Skills is a full VIS system for AI-assisted brand work. It is not just a set of prompts for logo or UI exploration. It is a bundled workflow that turns brand strategy, visual direction, identity production, application expansion, and governance handoff into reusable skill logic plus machine-readable design outputs.

This bundle is built for teams who want AI to work from explicit brand rules instead of vague taste prompts. It combines:

- a 5-step public VIS workflow
- support skills for scope planning, routing, playbook selection, and packaging
- design-markdown outputs for AI-readable brand guidance
- tool adapters for different design tools and model families
- auto-generated brand-specific wrapper skills and prompt files

The design-markdown approach is informed by the broader `DESIGN.md` ecosystem around Stitch and examples such as VoltAgent's `awesome-design-md`, then expanded from UI/UX into full brand identity and VIS work.

It also incorporates useful methodology from the local `visual-identity-direction` skill, including strategy-to-visual translation, creative-brief discipline, moodboard rationale, logo-brief structure, photography direction, and typography/color reasoning.

### What this bundle does

- Diagnose a brand project and choose the right production route
- Distill multiple reference brands into an original direction instead of copying them
- Build the core identity system
- Expand the identity into application families and touchpoints
- Publish a machine-readable `brand-pack`
- Generate AI-readable design files for foundation, UI/UX, and applications
- Generate thin wrapper skills for downstream brand use
- Auto-generate brand-specific prompts for each supported tool and model family

### Public skills

- `brand-discovery-strategy`
- `visual-concept-exploration`
- `identity-system-production`
- `brand-application-system`
- `brand-governance-rollout`

### Support skills

- `brand-style-playbook-selector`
- `application-scope-planner`
- `application-route-classifier`
- `application-template-factory`
- `application-mockup-composer`
- `brand-application-factory`

### Core outputs

Design-markdown outputs:

- `REFERENCE_STYLE_DISTILLATION.md`
- `BRAND_FOUNDATION_DESIGN.md`
- `UI_UX_DESIGN.md`
- `APPLICATION_DESIGN.md`
- `DESIGN_INDEX.md`

Packaging outputs:

- `brand_pack.json`
- `<brand-slug>-brand-applications`
- `<brand-slug>-brand-guidelines`

Tool-enablement outputs:

- `TOOL_ADAPTER_INDEX.md`
- `references/tool-adapters/*.md`
- `TOOL_PROMPT_SKELETON_INDEX.md`
- `references/tool-prompt-skeletons/*.md`

### What gets auto-generated

When the bundle reaches the packaging stage, it does not stop at generic documentation.

It automatically generates:

- a final machine-readable `brand_pack.json`
- a brand-specific applications wrapper skill
- a brand-specific guidelines wrapper skill
- a self-contained set of tool adapters inside each generated wrapper
- a self-contained set of brand-specific prompt files inside each generated wrapper

Those brand-specific prompt files are generated for:

- Figma MCP
- Stitch
- Pencil
- Adobe Illustrator
- Adobe Photoshop
- Canva
- Inkscape
- image-generation models such as Doubao, Kling, Nano Banana, and similar tools

So downstream design work can start from brand-filled prompts instead of blank generic templates.

### Workflow

1. `brand-discovery-strategy`
   Diagnose the project, audit existing assets, define scope, and build the strategic base.
2. `visual-concept-exploration`
   Translate strategy into visual territories, distill references, and choose the strongest direction.
3. `identity-system-production`
   Build the identity core and the first structured brand payload.
4. `brand-application-system`
   Turn the identity into application families, production routes, and scaling logic.
5. `brand-governance-rollout`
   Finalize the pack, governance, handoff documents, and reusable automation layer.

### Why application production is a separate phase

Application production is not just “more design.” It has its own scope logic, route logic, output logic, and scaling constraints. This bundle treats it as an explicit layer so teams can handle a small set of touchpoints or a large rollout without flattening everything into one vague guideline file.

### Repository structure

- `skills/`
  Public VIS workflow skills
- `support/`
  Internal packaging, routing, and production support skills
- `references/`
  Shared architecture notes, adapter contracts, and prompt skeleton references
- `README.md`
  Package overview
- `CHANGELOG.md`
  Version history

### Important notes

- The public repository keeps paths generic and does not expose local absolute installation paths.
- `brand_pack.json` is the downstream source of truth for automation.
- Illustrator-heavy work is still treated as `manual_vector`.
- Canva-friendly work is routed through template logic.
- Photoshop-friendly work is routed through mockup logic.
- The wrapper layer is intentionally thin. It should apply the approved system, not redefine it.

### Key files

- `references/V3_ARCHITECTURE.md`
- `references/PROCESS_SYNTHESIS.md`
- `references/TOOL_ADAPTER_INDEX.md`
- `references/TOOL_PROMPT_SKELETON_INDEX.md`
- `support/brand-application-factory/scripts/build_brand_pack.py`
- `support/brand-application-factory/scripts/generate_wrapper_skill.py`
- `support/brand-application-factory/assets/sample_brand_foundation.json`

## 中文

Brand Identity Design Skills 是一套面向 AI 协作的完整 VIS 系统。它不是只给 logo 或 UI 灵感的 prompt 集，而是把品牌策略、视觉方向、识别系统生产、应用扩展、治理交接，统一封装成可复用的 skill 工作流和机器可读输出。

这个 bundle 的目标，是让 AI 不是凭模糊审美“猜品牌”，而是根据明确的品牌规则来工作。它把下面几层整合在一起：

- 5 步公开 VIS 工作流
- scope、route、playbook、packaging 等支持技能
- AI 可读的 design markdown 输出
- 面向不同设计工具和模型的 adapter
- 自动生成的品牌专属 wrapper skill 和 prompt 文件

其中 design-markdown 的思路参考了 Stitch 周边的 `DESIGN.md` 生态，以及 VoltAgent 的 `awesome-design-md`，但能力范围从 UI/UX 扩展到了完整 VIS。

同时也吸收了本地 `visual-identity-direction` skill 中可复用的方法论，包括 strategy-to-visual translation、creative brief、moodboard rationale、logo brief、摄影方向，以及字体和色彩推导逻辑。

### 这个 bundle 能做什么

- 诊断品牌项目并选择正确生产路径
- 把多个参考品牌提炼成原创方向，而不是直接模仿
- 构建核心识别系统
- 把识别系统扩展成应用家族和触点体系
- 产出机器可读的 `brand-pack`
- 生成 foundation、UI/UX、application 三层 AI 可读设计文件
- 生成可直接下游调用的 wrapper skill
- 为每种支持的工具和模型自动生成品牌专属 prompt

### 公开技能

- `brand-discovery-strategy`
- `visual-concept-exploration`
- `identity-system-production`
- `brand-application-system`
- `brand-governance-rollout`

### 支持技能

- `brand-style-playbook-selector`
- `application-scope-planner`
- `application-route-classifier`
- `application-template-factory`
- `application-mockup-composer`
- `brand-application-factory`

### 核心输出

design-markdown 输出：

- `REFERENCE_STYLE_DISTILLATION.md`
- `BRAND_FOUNDATION_DESIGN.md`
- `UI_UX_DESIGN.md`
- `APPLICATION_DESIGN.md`
- `DESIGN_INDEX.md`

包装输出：

- `brand_pack.json`
- `<brand-slug>-brand-applications`
- `<brand-slug>-brand-guidelines`

工具协同输出：

- `TOOL_ADAPTER_INDEX.md`
- `references/tool-adapters/*.md`
- `TOOL_PROMPT_SKELETON_INDEX.md`
- `references/tool-prompt-skeletons/*.md`

### 哪些内容是自动生成的

当流程走到 packaging 阶段时，bundle 不只是产出通用文档。

它会自动生成：

- 最终 machine-readable `brand_pack.json`
- 品牌专属 applications wrapper skill
- 品牌专属 guidelines wrapper skill
- 每个 wrapper 内自带的一套 tool adapters
- 每个 wrapper 内自带的一套品牌专属 prompt 文件

这些品牌专属 prompt 目前覆盖：

- Figma MCP
- Stitch
- Pencil
- Adobe Illustrator
- Adobe Photoshop
- Canva
- Inkscape
- 文生图模型，如豆包、可灵、Nano Banana 及类似工具

也就是说，下游做设计时，不需要再从空白通用模板开始改，而是直接从品牌已填充好的 prompt 出发。

### 工作流

1. `brand-discovery-strategy`
   做项目诊断、资产盘点、范围判断，建立策略基础。
2. `visual-concept-exploration`
   把策略翻译成视觉方向，提炼参考风格，并收敛到最优方向。
3. `identity-system-production`
   构建识别系统核心，并产出第一版结构化品牌数据。
4. `brand-application-system`
   把识别系统扩展成应用家族、生产路线和规模化逻辑。
5. `brand-governance-rollout`
   完成最终 pack、治理规则、交付文件和可复用自动化层。

### 为什么 application 要单独成阶段

Application 不是“再做一些设计”，而是独立的一层生产系统，有自己的范围逻辑、路由逻辑、输出逻辑和规模化约束。只有把它单独拆出来，才能稳定处理少量触点，也能支撑大规模 rollout，而不是把所有东西压成一份模糊 guideline。

### 仓库结构

- `skills/`
  公开 VIS 工作流技能
- `support/`
  内部 packaging、routing、production 支持技能
- `references/`
  共享架构说明、adapter contract 和 prompt skeleton 参考
- `README.md`
  项目总览
- `CHANGELOG.md`
  版本历史

### 重要说明

- 公开仓库只保留泛化路径，不暴露本地绝对安装路径。
- `brand_pack.json` 是后续自动化的唯一事实来源。
- Illustrator 重型工作仍然归为 `manual_vector`。
- 适合 Canva 的内容走模板生产逻辑。
- 适合 Photoshop 的内容走样机生产逻辑。
- wrapper 层刻意保持轻量，它负责应用已批准的系统，而不是重新定义系统。

### 关键文件

- `references/V3_ARCHITECTURE.md`
- `references/PROCESS_SYNTHESIS.md`
- `references/TOOL_ADAPTER_INDEX.md`
- `references/TOOL_PROMPT_SKELETON_INDEX.md`
- `support/brand-application-factory/scripts/build_brand_pack.py`
- `support/brand-application-factory/scripts/generate_wrapper_skill.py`
- `support/brand-application-factory/assets/sample_brand_foundation.json`
