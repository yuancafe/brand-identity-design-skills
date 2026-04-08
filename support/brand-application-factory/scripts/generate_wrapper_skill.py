#!/usr/bin/env python3
"""Generate a brand-specific wrapper skill from a brand-pack."""

from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path
from typing import Any


TOOL_PROMPT_BLUEPRINTS = {
    "figma-mcp.md": {
        "title": "Figma MCP",
        "task": "Create or refine [screen/frame/component/system] for [specific use case].",
        "read_first": [
            "reference-style-distillation.md",
            "brand-foundation-design.md",
            "ui-ux-design.md",
            "design-index.md",
            "tool-adapter-index.md",
            "tool-adapters/figma-mcp.md",
        ],
        "goal": "Build a Figma result that stays faithful to the approved brand system.",
        "constraint_labels": [
            "Brand posture",
            "Typography behavior",
            "Color logic",
            "Grid and spacing",
            "Component tone",
            "Avoid",
        ],
        "notes": [
            "Use clear frame hierarchy and auto-layout where relevant.",
            "Prefer reusable components and variants.",
            "Do not invent a new visual language.",
        ],
    },
    "stitch.md": {
        "title": "Stitch",
        "task": "Generate [screen/page/layout] for [specific use case].",
        "read_first": [
            "reference-style-distillation.md",
            "brand-foundation-design.md",
            "ui-ux-design.md",
            "design-index.md",
            "tool-adapter-index.md",
            "tool-adapters/stitch.md",
        ],
        "goal": "Produce a layout that matches the approved brand direction and is usable as a fast AI-generated design draft.",
        "constraint_labels": [
            "Brand posture",
            "Layout attitude",
            "Typography behavior",
            "Color logic",
            "Interaction tone",
            "Avoid",
        ],
        "notes": [
            "Use the brand files to define hierarchy before styling details.",
            "Keep the screen practical for later refinement in production tools.",
            "Avoid novelty that breaks the approved system.",
        ],
    },
    "pencil.md": {
        "title": "Pencil",
        "task": "Create [wireframe/flow/screen set] for [specific use case].",
        "read_first": [
            "brand-foundation-design.md",
            "ui-ux-design.md",
            "design-index.md",
            "tool-adapter-index.md",
            "tool-adapters/pencil.md",
        ],
        "goal": "Produce a concept, wireframe, or early visual draft that stays within the approved brand system.",
        "constraint_labels": [
            "Brand posture",
            "Hierarchy and information density",
            "Typography behavior",
            "Color usage",
            "Wireframe fidelity",
            "Avoid",
        ],
        "notes": [
            "Prefer clear structural decisions over ornamental styling.",
            "Keep the draft easy to evolve into higher-fidelity outputs later.",
            "Do not drift into a new visual system while sketching.",
        ],
    },
    "adobe-illustrator.md": {
        "title": "Adobe Illustrator",
        "task": "Create or refine [logo/vector pattern/signage/packaging master art] for [specific use case].",
        "read_first": [
            "brand-foundation-design.md",
            "application-design.md",
            "design-index.md",
            "tool-adapter-index.md",
            "tool-adapters/adobe-illustrator.md",
        ],
        "goal": "Produce vector-first work that follows the approved brand system and construction logic.",
        "constraint_labels": [
            "Logo or shape logic",
            "Geometry and alignment",
            "Stroke and corner behavior",
            "Color restrictions",
            "Export needs",
            "Avoid",
        ],
        "notes": [
            "Keep construction explicit.",
            "Do not fake automated precision where manual vector judgment is required.",
        ],
    },
    "adobe-photoshop.md": {
        "title": "Adobe Photoshop",
        "task": "Create or refine [mockup/poster/key visual/social graphic] for [specific use case].",
        "read_first": [
            "reference-style-distillation.md",
            "brand-foundation-design.md",
            "application-design.md",
            "design-index.md",
            "tool-adapter-index.md",
            "tool-adapters/adobe-photoshop.md",
        ],
        "goal": "Produce a Photoshop-oriented composition or mockup that stays on-brand and is ready for downstream production.",
        "constraint_labels": [
            "Mood and atmosphere",
            "Typography handling",
            "Palette and contrast",
            "Image treatment",
            "Mockup realism",
            "Avoid",
        ],
        "notes": [
            "Keep text legible and editable where practical.",
            "Use Photoshop for image-led execution, not to redefine the identity system.",
        ],
    },
    "canva.md": {
        "title": "Canva",
        "task": "Create [social post/deck/template/poster/flyer] for [specific use case].",
        "read_first": [
            "brand-foundation-design.md",
            "application-design.md",
            "design-index.md",
            "tool-adapter-index.md",
            "tool-adapters/canva.md",
        ],
        "goal": "Produce a template-friendly Canva result that remains consistent across repeated use.",
        "constraint_labels": [
            "Brand posture",
            "Template logic",
            "Typography behavior",
            "Color logic",
            "Safe-area and resizing expectations",
            "Avoid",
        ],
        "notes": [
            "Optimize for reusable layouts and fast team editing.",
            "Do not overfit the design to one size if multiple variants are expected.",
        ],
    },
    "inkscape.md": {
        "title": "Inkscape",
        "task": "Create or refine [vector graphic/layout diagram/signage artwork] for [specific use case].",
        "read_first": [
            "brand-foundation-design.md",
            "application-design.md",
            "design-index.md",
            "tool-adapter-index.md",
            "tool-adapters/inkscape.md",
        ],
        "goal": "Produce open vector artwork that follows the approved brand system and can be edited without proprietary tooling.",
        "constraint_labels": [
            "Shape logic",
            "Geometry and spacing",
            "Stroke behavior",
            "Color restrictions",
            "Export needs",
            "Avoid",
        ],
        "notes": [
            "Prefer clear, editable vector construction.",
            "Keep the file maintainable for future non-Adobe editing.",
        ],
    },
    "image-generation-models.md": {
        "title": "Image Generation Models",
        "task": "Generate [poster/key visual/background/concept image/supporting graphic] for [specific use case].",
        "read_first": [
            "reference-style-distillation.md",
            "brand-foundation-design.md",
            "application-design.md",
            "design-index.md",
            "tool-adapter-index.md",
            "tool-adapters/image-generation-models.md",
        ],
        "goal": "Produce a brand-aligned visual that can be used directly or refined later in design tools.",
        "constraint_labels": [
            "Subject",
            "Scene or composition",
            "Lighting and materials",
            "Palette and atmosphere",
            "Typography expectation",
            "Avoid",
        ],
        "notes": [
            "Do not copy a reference brand literally.",
            "Treat generated typography as non-final unless the model is only producing a background or concept image.",
        ],
    },
}


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def slugify(value: str) -> str:
    parts = re.findall(r"[\w-]+", value.lower())
    return "-".join(parts) or "brand"


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def build_bundle_reference(pack: dict[str, Any]) -> str:
    lines = ["# Application Bundles", ""]
    for recipe in pack.get("application_recipes", []):
        lines.append(f"## {recipe['family']}")
        lines.append(f"- default route: {recipe['default_route']}")
        lines.append(f"- template fit: {recipe['template_fit']}")
        lines.append(f"- sample items: {', '.join(recipe['sample_items'])}")
        lines.append(f"- export formats: {', '.join(recipe['export_formats'])}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def write_optional_text(path: Path, value: str | None) -> None:
    if value:
        write_text(path, value if value.endswith("\n") else value + "\n")


def write_design_docs(skill_dir: Path, pack: dict[str, Any]) -> None:
    design_docs = pack.get("design_md_documents", {}) or {}
    write_optional_text(
        skill_dir / "references" / "reference-style-distillation.md",
        pack.get("reference_style_distillation"),
    )
    write_optional_text(
        skill_dir / "references" / "brand-foundation-design.md",
        design_docs.get("brand_foundation_design"),
    )
    write_optional_text(
        skill_dir / "references" / "ui-ux-design.md",
        design_docs.get("ui_ux_design"),
    )
    write_optional_text(
        skill_dir / "references" / "application-design.md",
        design_docs.get("application_design"),
    )
    write_optional_text(
        skill_dir / "references" / "design-index.md",
        design_docs.get("design_index"),
    )


def copy_text_file(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)


def copy_tool_adapter_references(skill_dir: Path, bundle_root: Path) -> None:
    references_root = bundle_root / "references"
    copy_text_file(
        references_root / "TOOL_ADAPTER_INDEX.md",
        skill_dir / "references" / "tool-adapter-index.md",
    )

    adapters_src = references_root / "tool-adapters"
    adapters_dst = skill_dir / "references" / "tool-adapters"
    if adapters_dst.exists():
        shutil.rmtree(adapters_dst)
    shutil.copytree(adapters_src, adapters_dst)


def extract_bullets(markdown: str | None, limit: int = 4) -> list[str]:
    if not markdown:
        return []

    bullets: list[str] = []
    for raw_line in markdown.splitlines():
        line = raw_line.strip()
        if line.startswith("- ") or line.startswith("* "):
            bullets.append(line[2:].strip())
        if len(bullets) >= limit:
            break
    return bullets


def summarize_mapping(mapping: dict[str, Any] | None) -> str:
    if not isinstance(mapping, dict) or not mapping:
        return "Derive from the bundled design files."

    parts = [f"{key} {value}" for key, value in mapping.items() if value]
    return "; ".join(parts) if parts else "Derive from the bundled design files."


def summarize_logo_system(logo_system: dict[str, Any] | None) -> str:
    if not isinstance(logo_system, dict) or not logo_system:
        return "Use the approved logo system from BRAND_FOUNDATION_DESIGN.md."

    parts = []
    for key in ("primary", "secondary", "icon", "clear_space", "minimum_size"):
        value = logo_system.get(key)
        if value:
            parts.append(f"{key.replace('_', ' ')} {value}")
    return "; ".join(parts) if parts else "Use the approved logo system from BRAND_FOUNDATION_DESIGN.md."


def choose_component_tone(pack: dict[str, Any]) -> str:
    ui_bullets = extract_bullets(pack.get("design_md_documents", {}).get("ui_ux_design"))
    application_bullets = extract_bullets(
        pack.get("design_md_documents", {}).get("application_design")
    )
    cues = ui_bullets or application_bullets
    return "; ".join(cues[:3]) if cues else "Derive from UI_UX_DESIGN.md and APPLICATION_DESIGN.md."


def choose_reference_cues(pack: dict[str, Any]) -> str:
    cues = extract_bullets(pack.get("reference_style_distillation"))
    return "; ".join(cues[:3]) if cues else "Derive from REFERENCE_STYLE_DISTILLATION.md."


def build_prompt_values(pack: dict[str, Any]) -> dict[str, str]:
    brand = pack.get("brand", {})
    brand_guideline = pack.get("brand_guideline", {})
    brand_tokens = pack.get("brand_tokens", {})
    graphic = brand_tokens.get("graphic", {})
    playbook = pack.get("style_playbook_selection", {})

    foundation_bullets = extract_bullets(
        pack.get("design_md_documents", {}).get("brand_foundation_design")
    )
    ui_bullets = extract_bullets(pack.get("design_md_documents", {}).get("ui_ux_design"))
    application_bullets = extract_bullets(
        pack.get("design_md_documents", {}).get("application_design")
    )

    posture = brand_guideline.get("summary") or (
        f"{brand.get('name', 'This brand')} should feel consistent with the approved identity system."
    )
    playbook_line = playbook.get("lead_playbook") or "Use the approved playbook selection."
    typography = summarize_mapping(brand_tokens.get("type"))
    colors = summarize_mapping(brand_tokens.get("color"))
    graphic_system = summarize_mapping(graphic)
    logo_logic = summarize_logo_system(pack.get("logo_system"))
    foundation_cues = (
        "; ".join(foundation_bullets[:3]) if foundation_bullets else "Derive from BRAND_FOUNDATION_DESIGN.md."
    )
    ui_cues = "; ".join(ui_bullets[:3]) if ui_bullets else "Derive from UI_UX_DESIGN.md."
    application_cues = (
        "; ".join(application_bullets[:3]) if application_bullets else "Derive from APPLICATION_DESIGN.md."
    )
    corner_behavior = (
        f"Use {graphic.get('corner_radius')} corner behavior."
        if graphic.get("corner_radius") is not None
        else "Follow the approved corner and edge behavior in BRAND_FOUNDATION_DESIGN.md."
    )

    return {
        "brand_posture": f"{posture} Lead playbook: {playbook_line}.",
        "typography": typography,
        "colors": colors,
        "graphic_system": graphic_system,
        "component_tone": choose_component_tone(pack),
        "layout_attitude": foundation_cues,
        "interaction_tone": ui_cues,
        "hierarchy_density": ui_cues,
        "wireframe_fidelity": "Keep fidelity appropriate to early concept work while preserving the approved hierarchy.",
        "logo_logic": logo_logic,
        "corner_behavior": corner_behavior,
        "palette_contrast": colors,
        "mood_atmosphere": foundation_cues,
        "image_treatment": application_cues,
        "mockup_realism": "Use believable production context without overpowering the identity system.",
        "template_logic": application_cues,
        "shape_logic": logo_logic,
        "subject": "[replace with subject while staying inside the approved brand world]",
        "scene_composition": application_cues,
        "lighting_materials": foundation_cues,
        "palette_atmosphere": f"{colors} Atmosphere cues: {choose_reference_cues(pack)}",
        "type_expectation": "Prefer adding final typography later in design tools unless this image is only a non-text background.",
        "export_needs": "[replace with exact file formats, sizes, and handoff expectations]",
        "resizing": "Keep the layout modular enough for repeated size variants and safe-area adjustments.",
        "avoid": "Do not invent a new visual language, break the approved logo/color/type system, or imitate reference brands too literally.",
    }


def constraint_value_for(label: str, values: dict[str, str]) -> str:
    mapping = {
        "Brand posture": values["brand_posture"],
        "Typography behavior": values["typography"],
        "Color logic": values["colors"],
        "Grid and spacing": values["graphic_system"],
        "Component tone": values["component_tone"],
        "Layout attitude": values["layout_attitude"],
        "Interaction tone": values["interaction_tone"],
        "Hierarchy and information density": values["hierarchy_density"],
        "Color usage": values["colors"],
        "Wireframe fidelity": values["wireframe_fidelity"],
        "Logo or shape logic": values["logo_logic"],
        "Geometry and alignment": values["graphic_system"],
        "Stroke and corner behavior": values["corner_behavior"],
        "Color restrictions": values["colors"],
        "Export needs": values["export_needs"],
        "Mood and atmosphere": values["mood_atmosphere"],
        "Typography handling": values["typography"],
        "Palette and contrast": values["palette_contrast"],
        "Image treatment": values["image_treatment"],
        "Mockup realism": values["mockup_realism"],
        "Template logic": values["template_logic"],
        "Safe-area and resizing expectations": values["resizing"],
        "Shape logic": values["shape_logic"],
        "Geometry and spacing": values["graphic_system"],
        "Stroke behavior": values["corner_behavior"],
        "Subject": values["subject"],
        "Scene or composition": values["scene_composition"],
        "Lighting and materials": values["lighting_materials"],
        "Palette and atmosphere": values["palette_atmosphere"],
        "Typography expectation": values["type_expectation"],
        "Avoid": values["avoid"],
    }
    return mapping[label]


def render_brand_prompt(
    brand_name: str,
    file_name: str,
    blueprint: dict[str, Any],
    values: dict[str, str],
) -> str:
    prompt_lines = [
        f"Use the bundled brand files as the source of truth for {brand_name}.",
        "",
        "Task:",
        f"- {blueprint['task']}",
        "",
        "Read first:",
    ]
    prompt_lines.extend(f"- {item}" for item in blueprint["read_first"])
    prompt_lines.extend(
        [
            "",
            "Output goal:",
            f"- {blueprint['goal']}",
            "",
            "Key constraints:",
        ]
    )
    prompt_lines.extend(
        f"- {label}: {constraint_value_for(label, values)}"
        for label in blueprint["constraint_labels"]
    )
    prompt_lines.extend(["", "Execution notes:"])
    prompt_lines.extend(f"- {note}" for note in blueprint["notes"])

    title = blueprint["title"]
    prompt_block = "\n".join(prompt_lines)
    return (
        f"# {brand_name} {title} Prompt\n\n"
        f"Use this ready-to-adapt prompt when directing {title} work for {brand_name}.\n\n"
        "## Ready-to-use prompt\n\n"
        "```text\n"
        f"{prompt_block}\n"
        "```\n"
    )


def build_prompt_index(brand_name: str) -> str:
    lines = [
        f"# {brand_name} Tool Prompt Skeleton Index",
        "",
        "These files are brand-specific prompt starters automatically generated from the approved brand pack.",
        "",
        "## Read order",
        "",
        "1. `reference-style-distillation.md`",
        "2. `brand-foundation-design.md`",
        "3. `ui-ux-design.md` when relevant",
        "4. `application-design.md`",
        "5. `design-index.md`",
        "6. `tool-adapter-index.md`",
        "7. matching adapter file",
        "8. matching prompt file under `tool-prompt-skeletons/`",
        "",
        "## Available brand-specific prompts",
        "",
    ]
    lines.extend(f"- `tool-prompt-skeletons/{name}`" for name in TOOL_PROMPT_BLUEPRINTS)
    lines.extend(
        [
            "",
            "## Rule",
            "",
            "These are already filled with the approved brand constraints. Replace only the task-specific placeholders, not the core identity logic.",
            "",
        ]
    )
    return "\n".join(lines)


def write_brand_prompt_suite(skill_dir: Path, pack: dict[str, Any]) -> None:
    brand_name = pack.get("brand", {}).get("name", "Brand")
    values = build_prompt_values(pack)
    write_text(
        skill_dir / "references" / "tool-prompt-skeleton-index.md",
        build_prompt_index(brand_name),
    )
    for file_name, blueprint in TOOL_PROMPT_BLUEPRINTS.items():
        write_text(
            skill_dir / "references" / "tool-prompt-skeletons" / file_name,
            render_brand_prompt(brand_name, file_name, blueprint, values),
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("brand_pack", type=Path, help="Path to a final brand-pack JSON file")
    parser.add_argument("output_dir", type=Path, help="Directory to create the wrapper skill in")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = Path(__file__).resolve().parent.parent
    bundle_root = root.parent.parent
    template_path = root / "assets" / "wrapper_skill_template.md"
    brand_guidelines_template_path = root / "assets" / "brand_guidelines_skill_template.md"

    pack = load_json(args.brand_pack)
    brand_name = pack.get("brand", {}).get("name", "Brand")
    brand_slug = pack.get("brand", {}).get("slug") or slugify(brand_name)
    applications_skill_name = f"{brand_slug}-brand-applications"
    applications_skill_dir = args.output_dir / applications_skill_name
    guidelines_skill_name = f"{brand_slug}-brand-guidelines"
    guidelines_skill_dir = args.output_dir / guidelines_skill_name

    template = template_path.read_text(encoding="utf-8")
    applications_skill_md = template.format(
        skill_name=applications_skill_name,
        brand_name=brand_name,
        brand_slug=brand_slug,
        pack_rel_path="assets/brand_pack.json",
        bundle_ref_rel_path="references/application-bundles.md",
    )
    guidelines_template = brand_guidelines_template_path.read_text(encoding="utf-8")
    guidelines_skill_md = guidelines_template.format(
        skill_name=guidelines_skill_name,
        brand_name=brand_name,
        brand_slug=brand_slug,
        pack_rel_path="assets/brand_pack.json",
    )

    write_text(applications_skill_dir / "SKILL.md", applications_skill_md)
    write_json(applications_skill_dir / "assets" / "brand_pack.json", pack)
    write_text(
        applications_skill_dir / "references" / "application-bundles.md",
        build_bundle_reference(pack),
    )
    write_design_docs(applications_skill_dir, pack)
    copy_tool_adapter_references(applications_skill_dir, bundle_root)
    write_brand_prompt_suite(applications_skill_dir, pack)

    write_text(guidelines_skill_dir / "SKILL.md", guidelines_skill_md)
    write_json(guidelines_skill_dir / "assets" / "brand_pack.json", pack)
    write_design_docs(guidelines_skill_dir, pack)
    copy_tool_adapter_references(guidelines_skill_dir, bundle_root)
    write_brand_prompt_suite(guidelines_skill_dir, pack)

    print(
        json.dumps(
            {
                "application_skill_name": applications_skill_name,
                "guidelines_skill_name": guidelines_skill_name,
                "output_dir": str(args.output_dir),
                "brand_name": brand_name,
                "generated_tool_prompts": sorted(TOOL_PROMPT_BLUEPRINTS),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
