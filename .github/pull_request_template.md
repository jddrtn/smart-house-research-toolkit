## Summary

Briefly describe what this pull request changes.

## Why is this change useful?

Explain the problem being solved or the research/development need behind the change.

## Dataset assumptions

If this change interacts with the DigiTech Smart House Data Pack, describe any assumptions made about:

- dataset release year;
- source system;
- file structure;
- sensor or location;
- measurements;
- date coverage.

Write `not applicable` if the change does not depend on dataset structure.

## Testing

Describe how the change was tested.

Before submitting, please confirm:

- [ ] `pytest` passes
- [ ] `ruff check src tests` passes
- [ ] New behaviour has tests where appropriate
- [ ] Public functions have useful docstrings
- [ ] Documentation has been updated where necessary
- [ ] No DigiTech Smart House source dataset files have been committed

## Related issue

Closes #