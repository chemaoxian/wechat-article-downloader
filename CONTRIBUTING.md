# Contributing to WeChat Article Downloader

首先，感谢你考虑为这个项目做出贡献！

## 🤝 行为准则

本项目采用 [Contributor Covenant](CODE_OF_CONDUCT.md) 行为准则。参与本项目即表示您同意遵守其条款。

## 📋 如何贡献

### 报告 Bug

如果你发现 Bug，请创建 Issue 并包含以下信息：

1. **清晰的标题** - 简明扼要地描述问题
2. **复现步骤** - 详细说明如何复现问题
3. **期望行为** - 描述你认为应该发生什么
4. **实际行为** - 描述实际发生了什么
5. **环境信息** - Node.js/Python 版本、操作系统等

### 提出新功能

新功能建议欢迎通过 Issue 提出！请包含：

1. **使用场景** - 描述新功能的使用场景
2. **实现思路** - 如果有，请描述你设想如何实现
3. **替代方案** - 是否考虑过其他解决方案

### 提交代码

#### 1. Fork 并克隆

```bash
git clone https://github.com/chemaoxian/wechat-article-downloader.git
cd wechat-article-downloader
```

#### 2. 创建分支

```bash
git checkout -b feature/your-feature-name
# 或
git checkout -b fix/your-bug-fix
```

#### 3. 开发

**Node.js 开发**：
```bash
npm install
npm test
npm run lint
```

**Python 开发**：
```bash
pip install -e ".[dev]"
pytest tests/python/
flake8 src/python/
```

#### 4. 代码规范

**Node.js**:
- 遵循 ESLint 规则
- 使用 JSDoc 注释
- 保持代码简洁

**Python**:
- 遵循 PEP 8
- 使用类型提示
- 添加文档字符串

#### 5. 测试

确保所有测试通过：

```bash
# Node.js
npm test

# Python
pytest tests/python/ -v
```

#### 6. 提交 Commit

```bash
git commit -m "type: description"

# type 可以是：
# - feat: 新功能
# - fix: Bug 修复
# - docs: 文档更新
# - style: 代码格式
# - refactor: 重构
# - test: 测试
# - chore: 构建/工具
```

#### 7. 推送并创建 PR

```bash
git push origin feature/your-feature-name
```

然后在 GitHub 上创建 Pull Request。

## 📖 PR 指南

好的 PR 应该包含：

- [ ] 清晰的描述
- [ ] 关联的 Issue（如果有）
- [ ] 测试覆盖
- [ ] 文档更新
- [ ] 通过所有 CI 检查

### PR 模板

```markdown
## 描述
简要描述此 PR 的目的

## 相关 Issue
Fixes #123

## 变更类型
- [ ] 新功能
- [ ] Bug 修复
- [ ] 文档更新
- [ ] 重构
- [ ] 其他

## 测试
- [ ] 已添加测试
- [ ] 所有现有测试通过

## 检查清单
- [ ] 代码遵循项目规范
- [ ] 已更新文档
- [ ] 无破坏性变更（或已说明）
```

## 🎯 开发路线图

查看 [README.md](README.md#-开发路线图) 了解当前开发重点。

## 📧 联系方式

- GitHub Issues: [Issues](https://github.com/chemaoxian/wechat-article-downloader/issues)
- Email: 443224841@qq.com

## 🙏 感谢贡献者

感谢所有为这个项目做出贡献的人！
