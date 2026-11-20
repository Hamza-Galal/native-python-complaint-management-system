# Native Python Complaint Management System



## Authentication and Authorization



### Default Admin Account



The system automatically creates an ADMIN account when the application starts.



| Field | Value |

|---|---|

| Name | System Administrator |

| Email | admin@cms.local |

| Default Password | Admin@12345 |

| Role | ADMIN |



### Admin Password Configuration



For local development, the system uses `Admin@12345` when `CMS_ADMIN_PASSWORD` is not configured.



To use a custom password, set the environment variable before starting the application.



**Windows CMD:**



```cmd

set CMS_ADMIN_PASSWORD=YourStrongPassword123

python src\main.py

```



**Windows PowerShell:**



```powershell

$env:CMS_ADMIN_PASSWORD = "YourStrongPassword123"

python src\main.py

```



The password must contain at least 8 characters.



**Security Note:** The default password is intended for local development only. Always configure a strong password in production environments.



### Important Note



The current repositories use in-memory storage. Users and tokens are not persisted after the application stops. The default ADMIN account is recreated when the application starts.

