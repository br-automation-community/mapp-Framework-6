## 🔧 Required Modifications

The Framework by default provides a solid foundation, but in order to integrate it fully into your application there are a few modifications that must be made. The following list of modifications are required to get the Framework in a functional state within the application.

>
>🚨 **IMPORTANT:**  
>The steps on this page must be executed in order to get the Framework into a functional state!
>
---

1. Change the passwords for the **Admin**, **Operator**, and **Service_Tech** users. This is done in the **User.user** file in the Configuration View (**AccessAndSecurity → UserRoleSystem → User.user**). Note that if you already had users in your project with these same names prior to import, your existing users will remain unchanged and you do not need to update the passwords.

2. If you imported the **mapp View front end** with the Framework, assign the **mapp View content** (content ID = **UserX_content**) to an area on a page within your visualization.

3. If you did **not** import the mapp View front end,  connect the **HmiUserX** structure elements to your visualization accordingly.