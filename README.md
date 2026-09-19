# CI/CD Test Data Discovery and Provisioning

This sample implements the workflow described in the CI/CD Test Data Strategy:

1. Maintain a central catalog of reusable test-data/template repositories.
2. Discover a matching repository based on technology stack, purpose, scenario and commit requirement.
3. Provision a test branch from an existing repository.
4. Clean up the temporary branch after execution.

## Structure

```text
.
├── metadata/
│   └── test-template-repos.json
├── scripts/
│   ├── discover_test_data.py
│   ├── provision_test_data.py
│   └── cleanup_test_data.py
└── .github/
    └── workflows/
        ├── test-data-discovery.yml
        ├── provision-test-data.yml
        └── cleanup-test-data.yml
```

## Important

The catalog values are sample values and should be replaced with the organization's approved repositories, branches and naming standards.

The provisioning script deliberately starts with branch creation in an existing repository. Full repository creation from a template should be added only after the GitHub Enterprise repository/template policy and permissions are confirmed.
