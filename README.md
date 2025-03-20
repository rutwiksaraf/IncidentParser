# 🚔 Incident Data Extractor

### 👤 **Author:**  
**Rutwik Saraf**

---

**## 📌 Introduction**

This Python application **extracts incident data** from a **PDF file**, stores it in a **database**, and provides functions to **populate** and **retrieve** incident information.

---

**## 📜 Functions Overview**

### 🔹 `fetchIncidents(url)`
- Fetches a **PDF file** from a given **URL**.
- Returns a **byte buffer** of the PDF contents.

### 🔹 `extractIncidents(buffer)`
- Extracts **incident data** from the provided **PDF buffer**.
- Parses incident details from the **text inside the PDF**.

### 🔹 `createDB()`
- Creates an **SQLite database** with a table to store **incident information**.

### 🔹 `populateDB(connection, incidents)`
- Populates the **SQLite database** with a **list of incident records**.

### 🔹 `status(connection)`
- Prints the **incident counts**, grouped by the **nature of the incident**.

---

**## 🚀 Approach**

The **main goal** of this project is to:
1. **Fetch** incident reports from PDFs.
2. **Extract** relevant information.
3. **Store** the data in an **SQLite database** for easy querying.

---

**## 🏛 Database Development Approach**

### 🔹 **Creating the Database**
- Implemented an **SQLite database** to store **incident data** in a **structured format**.
- **Columns included**:  
  ✅ **Date**  
  ✅ **Incident Number**  
  ✅ **Location**  
  ✅ **Nature of Incident**  
  ✅ **ORI**

### 🔹 **Data Population**
- Extracted **incident data** from a **PDF file**.
- Inserted the extracted data into the **SQLite database**.

---

**## 📦 Required Installation Commands**

To install dependencies, run:

```sh
pip install pypdf
pip install pytest
```

## **🎯 How to Run the Code**

### **Running the Project**

```sh
pipenv run python project0/main.py --incidents "PDF URL"
```

### **Running the test cases**

```sh
pipenv run python -m pytest
```

## 🎥 **Demo**
🔗 [Project Demo](https://github.com/user-attachments/assets/566e22c2-7d8e-4ad0-ac62-a8ae404f012d) 

## **Assumptions**
1. The PDF format is structured consistently.
2. Incident natures will be textually similar enough for grouping.
3. Incident data can be properly parsed from the PDF content using basic string operations.
