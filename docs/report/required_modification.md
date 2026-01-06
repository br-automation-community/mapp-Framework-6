## 🔧 Required Modifications

The Framework by default provides a **solid foundation**, but in order to integrate it fully into your application, a few modifications must be made.

The following list of modifications is required to get the Framework into a **functional state** within the application.

> 🚨 **IMPORTANT:**  
> The steps on this page must be executed in order to get the Framework into a functional state.
>

---

### 1. Transfer the Report package to the file device

The **UserPartition\Report** package in the **Logical View** must be transferred to the **mappReportFiles** file device (which by default is **USER_PATH:\Report**).

For example, this can be done via an **initial installation**.

![report][def]

---

### 2. Update report configurations with application data

Update the provided **report configurations** with meaningful data from the application.

By default, the reports display **sample data**. For more details, see here.

The screenshot at the bottom of this page shows the general connection between **process variables**, the **report configuration**, and the **output report**.

---

### 3. Change default user passwords

Change the passwords for the **Admin**, **Operator**, and **Service_Tech** users.

This is done in the **User.user** file in the **Configuration View**  
(**AccessAndSecurity → UserRoleSystem → User.user**).

If users with the same names already existed in the project prior to importing the Framework, those users will remain unchanged and the passwords do not need to be updated.

---

### 4. Integrate the mapp View front end (if imported)

If you imported the **mapp View front end** with the Framework:

   a.Assign the **mapp View content** (content ID = **Report_content**) to an area on a page within your visualization.

   b.The ability to **delete a report** on the **mapp View HMI** is restricted to the **Administrators** or **Service** role. Therefore, add a way to **log in on the HMI** (for example, by importing the **mapp UserX** framework).

   c.If you are using **mapp View 5.16 or 5.17**, change **usePlugin** to **false** on the **PDFViewer** widget on ReportDialog_View_content. This configures the widget to use the browser’s internal PDF viewer rather than the JavaScript plugin. Otherwise, reports will not display correctly on the mapp View HMI. An improvement to the JavaScript plugin was made in **mapp View 5.18** .

---

### 5. Integrate the HMI without mapp View

If you did **not** import the mapp View front end with the Framework, connect the **HmiReport** structure elements to your visualization accordingly (see general information for more details).

![report2][def2]

[def]: images/report1.png
[def2]: images/report2.png