## 🔧 Required Modifications

The Framework by default provides a **solid foundation**, but in order to integrate it fully into your application there are a few modifications that must be made. The following list of modifications is required to get the Framework into a **functional state** within the application.

🚨 **IMPORTANT:**  
The steps on this page must be executed in order to get the Framework into a functional state.

---

1. **Change the passwords** for the **Admin**, **Operator**, and **Service_Tech** users.  
   This is done in the **User.user** file in the **Configuration View** (**AccessAndSecurity → UserRoleSystem → User.user**). Note that if you already had users in your project with these same names prior to import,  
   your existing users will remain unchanged and you do not need to update the passwords.

2. The **Audit Framework** uses **retained variables**, which require **nonzero remanent memory**.  
   This must be configured in the **CPU memory configuration** if it is not already configured.

3. If you imported the **mapp View front end** with the Framework:

     1. Assign the **mapp View content**  (content ID = **Audit_content**) to an area on a page within your visualization.

     2. The ability to **configure automatic archive export** is restricted to the **Administrators** role, and the ability to **create an immediate export** is restricted to the **Administrators** or **Service** role.  Therefore, add a way to **log in on the HMI** (for example, by importing the **mapp UserX** framework).

4. If you did **not** import the mapp View front end, connect the **HmiAudit** structure elements  
   to your visualization accordingly (see here for more details).
