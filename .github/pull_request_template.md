name: Pull Request
description: Create a pull request for this project
title: "[PR]: "
labels: ["triage"]
body:
  - type: markdown
    attributes:
      value: |
        Thanks for creating a pull request! Please fill out this template to help us review your contribution.

  - type: textarea
    id: description
    attributes:
      label: Description
      description: A clear and concise description of what this PR does.
    validations:
      required: true

  - type: textarea
    id: motivation
    attributes:
      label: Motivation
      description: Explain the motivation for making this change. What problem does it solve?
    validations:
      required: true

  - type: textarea
    id: testing
    attributes:
      label: Testing
      description: Describe the tests you performed to verify this change.
      placeholder: |
        - Ran existing test suite
        - Added new tests for X
        - Manually tested Y
    validations:
      required: true

  - type: checkboxes
    id: checklist
    attributes:
      label: Checklist
      description: Please ensure your PR meets the following criteria.
      options:
        - label: Code follows project style guidelines
        - label: Tests have been added or updated
        - label: Documentation has been updated (if applicable)
        - label: No breaking changes (or documented if breaking)
        - label: Security implications considered (if applicable)

  - type: input
    id: issue
    attributes:
      label: Related Issue
      description: Link to the issue this PR addresses (if any).
      placeholder: "Fixes #123"

  - type: dropdown
    id: breaking
    attributes:
      label: Breaking Change?
      description: Does this PR introduce a breaking change?
      options:
        - "No"
        - "Yes - describe in description"
      multiple: false
    validations:
      required: true

  - type: checkboxes
    id: terms
    attributes:
      label: Code of Conduct
      description: By submitting this pull request, you agree to follow our [Code of Conduct](../blob/main/CODE_OF_CONDUCT.md).
      options:
        - label: I agree to follow this project's Code of Conduct
          required: true
