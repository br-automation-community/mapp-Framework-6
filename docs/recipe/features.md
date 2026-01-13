## 🧾 mapp Recipe Framework 6

The following features and functionality are included in the **mapp Recipe Framework 6**:  

• The infrastructure to set up **two distinct recipe files**, with a structure variable registered to each  

• The ability to **save recipes to a USB drive**  

• The ability to **preview and edit a recipe** on the **HMI** before loading it  

• The recipe system is set up in the **XML format**. (To convert to a **CSV recipe system**, see here.)

   1. Both the **RecipeXML.mprecipexml** and **RecipeCSV.mprecipecsv** configuration files are already included in the Framework to enable the ability to easily switch back and forth. Only **one** of these configuration files is used at a time (i.e. the **MpLink** from only one of these files is referenced in the application).

---

### 🔐 Access Rights

The ability to **create / delete / edit a recipe** on the **mapp View HMI** is restricted to the **Administrators** or **Service** roles.

The ability to **load a recipe** is restricted to the **Administrators**, **Service**, or **Operators** roles.

The default administrative user is **Admin** with default password **123ABc**. The password **must be changed after import**.

---

### ℹ️ Note

Note that if you **edit the active recipe**, the **PLC will begin using the updated values immediately**. You do **not** have to perform a **load command** after editing the active recipe.