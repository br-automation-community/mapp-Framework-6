## 👤 mapp UserX Framework Features

The following features and functionality are included in the **mapp UserX Framework**:  

• **Local user management** (as opposed to **Active Directory**)  

• Ability to **import / export user information** via the **HMI**  

• Global language and measurement system selectors (if you imported mappView front end)  

• The following **predefined roles**:  
  Everyone, Operators, Service, Administrators  

• The following **predefined users**:  
  User, AdminDefault, Admin, Operator, ServiceTech, SystemUser  

---

### 🔐 Access Rights

The ability to **view / edit / add / delete / import / export users** in the **UserList widget** on the  
**mapp View HMI** is restricted to the **Administrators** role.

The default administrative user is **Admin** with default password **123ABc**.  
The password **must be changed after import**.

The startup user is **AdminDefault** with the default password **123ABc**.
Normally, the startup user is assigned only the Everyone role. However, to allow immediate
demonstration of the mapp Framework’s functionalities,the startup user is provided
with multiple roles by default.
Therefore, the startup user **must be changed after import**.

The system user required for backend operations such as importing and exporting users
is **SystemUser**, with the hard-coded (in UserXMgr.var file) password **123456ABCdef**.
The password **must be changed after import**.  
If any automatic logout mechanism is configured, the system user must be logged in again
in the UserX Manager program before performing user import/export.
If password expiration or compulsory password change is configured, a new password must be
provided to the MpUserXLogin FB.  
Alternatively, instead of using a dedicated system user, the currently logged-in HMI user
can be used. In this case, the username and password must be passed over OPC UA via
binding to the MpUserXLogin FB.
If this method is used, keep in mind that the current user's password may become readable
in the Watch window, the mappView diagnostic page, or by another OPC UA client with
administrator rights.

