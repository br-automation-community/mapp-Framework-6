## 📁 FIFO (First-In-First-Out) Functionality

The **mapp File Framework** comes with the option of enabling a **FIFO (first-in-first-out)** for a file device of your choosing. 

There are a few key details regarding this feature:

• The **FIFO deletes the oldest files** once the file device starts filling up.  There are two configuration options for you to define what **"filling up"** means for your application. A dialog box on the **HMI** allows you to choose between the following:

  1. Define a **maximum memory size** and delete the oldest file once the total file device contents exceeds this size. 

  2. Define a **maximum number of files** and delete the oldest file once the number of files on the file device exceeds this value. 

• The user must select **one file device** for the FIFO to be active on. 

• Once activated, the FIFO will **check this file device periodically** for size and number of files. 

• The FIFO will monitor **all files in the root directory** of the selected file device.Files contained within **any sub-folders will not be checked**. 
