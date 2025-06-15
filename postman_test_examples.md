# Postman测试示例

## 基础信息
- **Base URL**: `https://your-app-name.onrender.com` (部署后替换)
- **本地测试**: `http://localhost:8000`

## API端点测试

### 1. 健康检查
**GET** `/health`
```
无需参数
```
**预期响应**:
```json
{
  "status": "healthy",
  "message": "GPT Researcher API is running"
}
```

### 2. 生成研究报告 (主要功能)
**POST** `/report/`

**Headers**:
```
Content-Type: application/json
```

**Body (JSON)**:
```json
{
  "task": "分析人工智能的发展趋势",
  "report_type": "research_report",
  "report_source": "web",
  "tone": "Objective",
  "repo_name": "test",
  "branch_name": "main",
  "generate_in_background": false
}
```

**可选的report_type值**:
- `research_report` - 研究报告
- `competitive_intelligence` - 竞争情报
- `resource_report` - 资源报告
- `outline_report` - 大纲报告

**可选的tone值**:
- `Objective` - 客观
- `Formal` - 正式
- `Analytical` - 分析性
- `Persuasive` - 说服性
- `Informative` - 信息性
- `Explanatory` - 解释性

**预期响应**:
```json
{
  "research_id": "task_1234567890_分析人工智能的发展趋势",
  "research_information": {
    "source_urls": ["url1", "url2"],
    "research_costs": 0.05,
    "visited_urls": ["url1", "url2"],
    "research_images": []
  },
  "report": "# 人工智能发展趋势分析\n\n...",
  "docx_path": "outputs/task_1234567890_分析人工智能的发展趋势.docx",
  "pdf_path": "outputs/task_1234567890_分析人工智能的发展趋势.pdf"
}
```

### 3. 获取生成的报告文件
**GET** `/report/{research_id}`

**示例**: `/report/task_1234567890_分析人工智能的发展趋势`

**预期响应**: 下载DOCX文件

### 4. 列出文件
**GET** `/files/`

**预期响应**:
```json
{
  "files": ["file1.txt", "file2.pdf"]
}
```

### 5. 上传文件
**POST** `/upload/`

**Body**: form-data
- Key: `file`
- Type: File
- Value: 选择要上传的文件

### 6. 删除文件
**DELETE** `/files/{filename}`

**示例**: `/files/test.txt`

## 测试建议

### 简单测试流程:
1. 先测试 `/health` 确保服务正常
2. 测试 `/report/` 生成一个简单的报告
3. 使用返回的 `research_id` 测试 `/report/{research_id}` 下载报告
4. 测试文件上传和列表功能

### 注意事项:
- 报告生成可能需要1-3分钟，请耐心等待
- 如果设置 `generate_in_background: true`，会立即返回，需要稍后查询结果
- 确保环境变量配置正确（API密钥等）
