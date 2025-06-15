"""
HTML Template Renderer for Competitive Intelligence Visual Reports

This module provides functionality to render JSON data into HTML using templates.
"""

import json
import re
from pathlib import Path
from typing import Dict, Any, List, Optional


class TemplateRenderer:
    """
    Template renderer for converting JSON data to HTML reports.
    
    Supports Handlebars-like template syntax for data binding.
    """
    
    def __init__(self, template_dir: str = None):
        """
        Initialize the template renderer.
        
        Args:
            template_dir (str): Directory containing HTML templates
        """
        if template_dir is None:
            # Default to templates directory relative to this file
            self.template_dir = Path(__file__).parent
        else:
            self.template_dir = Path(template_dir)
    
    def render_competitive_intelligence_visual(self, data: Dict[str, Any]) -> str:
        """
        Render competitive intelligence visual report.
        
        Args:
            data (Dict[str, Any]): JSON data containing report information
            
        Returns:
            str: Rendered HTML content
        """
        template_path = self.template_dir / "competitive_intelligence_visual.html"
        
        if not template_path.exists():
            raise FileNotFoundError(f"Template not found: {template_path}")
        
        # Read template
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
        
        # Prepare template variables
        template_vars = self._prepare_template_variables(data)
        
        # Render template
        rendered_content = self._render_template(template_content, template_vars)
        
        return rendered_content
    
    def _prepare_template_variables(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prepare template variables from JSON data.
        
        Args:
            data (Dict[str, Any]): Raw JSON data
            
        Returns:
            Dict[str, Any]: Prepared template variables
        """
        # Extract metadata
        metadata = data.get("metadata", {})
        
        # Extract hero data
        hero_data = data.get("layer_1_hero", {})
        hero_snapshot = hero_data.get("hero_snapshot", {})
        key_metrics = hero_snapshot.get("key_metrics", {})
        value_curve = hero_data.get("value_curve", {})
        
        # Extract visual data
        visual_data = data.get("layer_2_visual", {})
        radar_data = visual_data.get("competitive_radar", {})
        timeline_data = visual_data.get("growth_timeline", [])
        metrics_data = visual_data.get("metrics_chart", {})
        
        # Extract cards data
        cards_data = data.get("layer_3_cards", {})
        insight_cards = cards_data.get("insight_cards", {})
        founder_canvas = cards_data.get("founder_moat_canvas", {})
        
        # Extract detailed data
        detailed_data = data.get("layer_4_detailed", {})
        research_data = detailed_data.get("detailed_research", {})
        
        # Extract UI config
        ui_config = data.get("ui_config", {})
        
        # Prepare variables
        template_vars = {
            # Metadata
            "product_name": metadata.get("product_name", "Unknown Product"),
            "report_date": metadata.get("report_date", ""),
            "version": metadata.get("version", "2.0"),
            
            # Hero snapshot
            "tagline": hero_snapshot.get("tagline", ""),
            "arr": key_metrics.get("arr", "未知"),
            "clients": key_metrics.get("clients", 0),
            "growth_90d": key_metrics.get("growth_90d", "未知"),
            "replication_difficulty": key_metrics.get("replication_difficulty", "中等"),
            
            # Growth color based on growth_90d
            "growth_color": self._get_growth_color(key_metrics.get("growth_90d", "")),
            
            # Value curve
            "problems": value_curve.get("problems", []),
            "solutions": value_curve.get("solutions", []),
            
            # Radar chart
            "radar_dimensions": json.dumps(radar_data.get("dimensions", [])),
            "radar_scores": json.dumps(radar_data.get("scores", [])),
            "competitors": radar_data.get("competitors", []),
            
            # Timeline
            "timeline": timeline_data,
            
            # Metrics chart
            "metrics_chart": metrics_data,
            
            # Insight cards
            "insight_cards": self._format_insight_cards(insight_cards),
            
            # Founder canvas
            "founder_name": founder_canvas.get("founder_info", {}).get("name", "未知"),
            "founder_title": founder_canvas.get("founder_info", {}).get("title", ""),
            "founder_avatar_url": founder_canvas.get("founder_info", {}).get("avatar_url", ""),
            "industry_knowhow": founder_canvas.get("quadrants", {}).get("industry_knowhow", ""),
            "capital_backing": founder_canvas.get("quadrants", {}).get("capital_backing", ""),
            "channel_resources": founder_canvas.get("quadrants", {}).get("channel_resources", ""),
            "community_influence": founder_canvas.get("quadrants", {}).get("community_influence", ""),
            
            # Detailed research
            "full_analysis": research_data.get("full_analysis", ""),
            "research_sources": research_data.get("research_sources", []),
            "data_gaps": research_data.get("data_gaps", []),
        }
        
        return template_vars
    
    def _get_growth_color(self, growth_str: str) -> str:
        """
        Determine color class based on growth string.
        
        Args:
            growth_str (str): Growth string like "+18%" or "-5%"
            
        Returns:
            str: CSS color class
        """
        if not growth_str or growth_str == "未知":
            return "text-gray-400"
        
        if growth_str.startswith("+"):
            return "text-green-400"
        elif growth_str.startswith("-"):
            return "text-red-400"
        else:
            return "text-gray-400"
    
    def _format_insight_cards(self, cards: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Format insight cards for template rendering.
        
        Args:
            cards (Dict[str, Any]): Raw cards data
            
        Returns:
            List[Dict[str, Any]]: Formatted cards list
        """
        formatted_cards = []
        
        # Define card order for consistent display
        card_order = [
            "pain_points", "target_users", "core_scenarios",
            "market_status", "tech_stack", "business_model"
        ]
        
        for card_key in card_order:
            if card_key in cards:
                card_data = cards[card_key]
                formatted_cards.append({
                    "title": card_data.get("title", ""),
                    "icon": card_data.get("icon", "info"),
                    "content": card_data.get("content", ""),
                    "evidence_url": card_data.get("evidence_url", "")
                })
        
        return formatted_cards
    
    def _render_template(self, template: str, variables: Dict[str, Any]) -> str:
        """
        Render template with variables using simple substitution.
        
        Args:
            template (str): Template content
            variables (Dict[str, Any]): Template variables
            
        Returns:
            str: Rendered content
        """
        rendered = template
        
        # Simple variable substitution
        for key, value in variables.items():
            placeholder = f"{{{{{key}}}}}"
            if isinstance(value, (str, int, float)):
                rendered = rendered.replace(placeholder, str(value))
            elif isinstance(value, list) and key in ["problems", "solutions"]:
                # Handle list rendering for problems/solutions
                rendered = self._render_list_items(rendered, key, value)
            elif isinstance(value, list) and key == "timeline":
                # Handle timeline rendering
                rendered = self._render_timeline(rendered, value)
            elif isinstance(value, list) and key == "insight_cards":
                # Handle insight cards rendering
                rendered = self._render_insight_cards(rendered, value)
            elif isinstance(value, list) and key == "data_gaps":
                # Handle data gaps rendering
                rendered = self._render_data_gaps(rendered, value)
            elif isinstance(value, list) and key == "research_sources":
                # Handle research sources rendering
                rendered = self._render_research_sources(rendered, value)
        
        return rendered
    
    def _render_list_items(self, template: str, key: str, items: List[str]) -> str:
        """
        Render list items in template.
        
        Args:
            template (str): Template content
            key (str): Variable key
            items (List[str]): List items
            
        Returns:
            str: Rendered template
        """
        # Find {{#each key}} ... {{/each}} blocks
        pattern = f"{{{{#each {key}}}}}(.*?){{{{/each}}}}"
        matches = re.findall(pattern, template, re.DOTALL)
        
        for match in matches:
            item_template = match.strip()
            rendered_items = []
            
            for item in items:
                # Replace {{this}} with actual item
                rendered_item = item_template.replace("{{this}}", str(item))
                rendered_items.append(rendered_item)
            
            # Replace the entire block
            block = f"{{{{#each {key}}}}}{match}{{{{/each}}}}"
            template = template.replace(block, "\n".join(rendered_items))
        
        return template
    
    def _render_timeline(self, template: str, timeline: List[Dict[str, Any]]) -> str:
        """
        Render timeline items in template.
        
        Args:
            template (str): Template content
            timeline (List[Dict[str, Any]]): Timeline data
            
        Returns:
            str: Rendered template
        """
        pattern = r"{{#each timeline}}(.*?){{/each}}"
        matches = re.findall(pattern, template, re.DOTALL)
        
        for match in matches:
            item_template = match.strip()
            rendered_items = []
            
            for item in timeline:
                rendered_item = item_template
                for field, value in item.items():
                    placeholder = f"{{{{{field}}}}}"
                    rendered_item = rendered_item.replace(placeholder, str(value))
                rendered_items.append(rendered_item)
            
            # Replace the entire block
            block = f"{{{{#each timeline}}}}{match}{{{{/each}}}}"
            template = template.replace(block, "\n".join(rendered_items))
        
        return template
    
    def _render_insight_cards(self, template: str, cards: List[Dict[str, Any]]) -> str:
        """
        Render insight cards in template.
        
        Args:
            template (str): Template content
            cards (List[Dict[str, Any]]): Cards data
            
        Returns:
            str: Rendered template
        """
        pattern = r"{{#each insight_cards}}(.*?){{/each}}"
        matches = re.findall(pattern, template, re.DOTALL)
        
        for match in matches:
            item_template = match.strip()
            rendered_items = []
            
            for card in cards:
                rendered_item = item_template
                for field, value in card.items():
                    placeholder = f"{{{{{field}}}}}"
                    rendered_item = rendered_item.replace(placeholder, str(value))
                
                # Handle conditional evidence_url
                if card.get("evidence_url"):
                    rendered_item = rendered_item.replace("{{#if evidence_url}}", "")
                    rendered_item = rendered_item.replace("{{/if}}", "")
                else:
                    # Remove the conditional block
                    conditional_pattern = r"{{#if evidence_url}}.*?{{/if}}"
                    rendered_item = re.sub(conditional_pattern, "", rendered_item, flags=re.DOTALL)
                
                rendered_items.append(rendered_item)
            
            # Replace the entire block
            block = f"{{{{#each insight_cards}}}}{match}{{{{/each}}}}"
            template = template.replace(block, "\n".join(rendered_items))
        
        return template
    
    def _render_data_gaps(self, template: str, gaps: List[str]) -> str:
        """
        Render data gaps in template.
        
        Args:
            template (str): Template content
            gaps (List[str]): Data gaps list
            
        Returns:
            str: Rendered template
        """
        pattern = r"{{#each data_gaps}}(.*?){{/each}}"
        matches = re.findall(pattern, template, re.DOTALL)
        
        for match in matches:
            item_template = match.strip()
            rendered_items = []
            
            for gap in gaps:
                rendered_item = item_template.replace("{{this}}", str(gap))
                rendered_items.append(rendered_item)
            
            # Replace the entire block
            block = f"{{{{#each data_gaps}}}}{match}{{{{/each}}}}"
            template = template.replace(block, "\n".join(rendered_items))
        
        return template
    
    def _render_research_sources(self, template: str, sources: List[Dict[str, Any]]) -> str:
        """
        Render research sources in template.
        
        Args:
            template (str): Template content
            sources (List[Dict[str, Any]]): Research sources data
            
        Returns:
            str: Rendered template
        """
        pattern = r"{{#each research_sources}}(.*?){{/each}}"
        matches = re.findall(pattern, template, re.DOTALL)
        
        for match in matches:
            item_template = match.strip()
            rendered_items = []
            
            for source in sources:
                rendered_item = item_template
                for field, value in source.items():
                    placeholder = f"{{{{{field}}}}}"
                    rendered_item = rendered_item.replace(placeholder, str(value))
                
                # Handle star rating
                reliability = source.get("reliability", 0)
                if "{{#repeat reliability}}" in rendered_item:
                    star_pattern = r"{{#repeat reliability}}(.*?){{/repeat}}"
                    star_match = re.search(star_pattern, rendered_item)
                    if star_match:
                        star_template = star_match.group(1)
                        stars = star_template * int(reliability)
                        rendered_item = re.sub(star_pattern, stars, rendered_item)
                
                rendered_items.append(rendered_item)
            
            # Replace the entire block
            block = f"{{{{#each research_sources}}}}{match}{{{{/each}}}}"
            template = template.replace(block, "\n".join(rendered_items))
        
        return template
    
    def save_rendered_report(self, html_content: str, output_path: str) -> str:
        """
        Save rendered HTML report to file.
        
        Args:
            html_content (str): Rendered HTML content
            output_path (str): Output file path
            
        Returns:
            str: Absolute path to saved file
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return str(output_path.absolute())


def render_competitive_intelligence_visual_report(
    data: Dict[str, Any], 
    output_path: Optional[str] = None,
    template_dir: Optional[str] = None
) -> str:
    """
    Convenience function to render a competitive intelligence visual report.
    
    Args:
        data (Dict[str, Any]): JSON report data
        output_path (Optional[str]): Output file path. If None, returns HTML string only.
        template_dir (Optional[str]): Template directory path
        
    Returns:
        str: Rendered HTML content or path to saved file
    """
    renderer = TemplateRenderer(template_dir)
    html_content = renderer.render_competitive_intelligence_visual(data)
    
    if output_path:
        saved_path = renderer.save_rendered_report(html_content, output_path)
        return saved_path
    else:
        return html_content


# Example usage
if __name__ == "__main__":
    # Example data structure
    example_data = {
        "metadata": {
            "product_name": "Example Product",
            "report_date": "2025-06-14",
            "version": "2.0"
        },
        "layer_1_hero": {
            "hero_snapshot": {
                "tagline": "AI驱动的示例产品解决方案",
                "key_metrics": {
                    "arr": "$1.2M",
                    "clients": 39,
                    "growth_90d": "+18%",
                    "replication_difficulty": "困难"
                }
            },
            "value_curve": {
                "problems": ["传统方案效率低", "成本过高", "用户体验差"],
                "solutions": ["AI自动化", "成本优化", "智能用户体验"]
            }
        },
        "layer_2_visual": {
            "competitive_radar": {
                "dimensions": ["定制化", "自动化深度", "开源透明", "生态", "价格"],
                "scores": [4.2, 3.8, 4.5, 3.2, 4.0],
                "competitors": []
            },
            "growth_timeline": [
                {
                    "date": "2024-03",
                    "milestone": "YC入选",
                    "type": "funding",
                    "description": "获得YC孵化器支持"
                }
            ]
        },
        "layer_3_cards": {
            "insight_cards": {
                "pain_points": {
                    "title": "核心痛点",
                    "icon": "AlertTriangle",
                    "content": "用户面临的主要问题...",
                    "evidence_url": ""
                }
            }
        },
        "layer_4_detailed": {
            "detailed_research": {
                "full_analysis": "详细分析内容...",
                "research_sources": [],
                "data_gaps": ["缺失信息1"]
            }
        },
        "ui_config": {}
    }
    
    # Render report
    html_output = render_competitive_intelligence_visual_report(example_data)
    print("HTML report generated successfully!")
    print(f"Length: {len(html_output)} characters")