## Authentication & Task API Tests

Automated tests are implemented using **Pytest** to verify authentication, authorization, task management, and session security.

### Test Results

**Test Summary:**

| Metric | Result |
|---|---:|
| Total Tests | 6 |
| Passed | 6 |
| Failed | 0 |
| Execution Time | 4.21 seconds |
| Test Framework | Pytest 8.3.5 |
| Python Version | 3.10.0 |
| Platform | Windows |

### Test Execution Output

(myenv) PS D:\docker_demo\Docker-demo\fastapi_endpoints\tests> pytest test_auth_tasks.py -v 

```text
============================= test session starts ==============================

collected 6 items

test_auth_tasks.py::test_teacher_student_task_permissions_and_validation PASSED

test_auth_tasks.py::test_teacher_registration_and_login_require_teacher_credentials PASSED

test_auth_tasks.py::test_teacher_registration_requires_configuration PASSED

test_auth_tasks.py::test_refresh_rotation_and_logout_revoke_sessions PASSED

test_auth_tasks.py::test_expired_access_and_refresh_sessions_are_rejected PASSED

test_auth_tasks.py::test_tasks_support_pagination_search_and_filters PASSED

============================== 6 passed in 4.21s ================================

```

