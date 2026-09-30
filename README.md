# Programming with Python — Assignment 2

**Course:** Programming with Python (202044504)  
**Program:** B.Tech. Information Technology — Semester V

This repository contains Python 3 solutions for the ten questions in Assignment 2.

## Solutions

| File | Question |
|---|---|
| `Q1_Regex_Email_Intelligence_Extractor.py` | Streaming email extraction and domain summary |
| `Q2_Offline_HTML_Product_Ranker.py` | Offline HTML product extraction and ranking |
| `Q3_MySQL_Student_Course_Analytics.py` | MySQL student-course analytics from CSV |
| `Q4_SQL_Join_Query_Builder_Validator.py` | Whitelisted, parameterized SQL query builder |
| `Q5_Tkinter_MySQL_Contact_Manager.py` | Tkinter contact manager with MySQL |
| `Q6_Log_Anomaly_Detector_Sliding_Window.py` | Sliding-window login anomaly detection |
| `Q7_Generator_JSONL_ETL_Pipeline.py` | Streaming JSONL ETL and summaries |
| `Q8_Matrix_Path_Optimizer.py` | Dynamic programming maximum-score path |
| `Q9_OOP_Inventory_Merger.py` | Inventory classes and `+` operator overloading |
| `Q10_Python_Data_Visualization_Dashboard.py` | CSV cleaning, statistics and chart export |

## Requirements

- Python 3.10 or newer.
- Q1, Q2, Q4, Q6, Q7, Q8 and Q9 use the standard library.
- Q3 and Q5 require `mysql-connector-python`.
- Q10 requires `pandas` and `matplotlib`.
- Tkinter must be available for Q5's GUI.

Install optional packages:

```bash
python3 -m pip install mysql-connector-python pandas matplotlib
```

## Notes

- Q2's HTML parser expects recognizable product/name/price/rating classes or `itemprop` attributes. Adapt `ProductParser` to the exact saved HTML structure if needed.
- Q3 expects `students.csv` columns `student_id,name,spi` and `registration.csv` columns `student_id,course_id`. Create the target MySQL database before running.
- Q4 prints a validated SQL template and parameter list; values are parameterized and identifiers are selected from a whitelist.
- Q5 requires a pre-created MySQL database. The program creates the `Contact` table automatically.
- Q6 expects timestamps in `HH:MM` format and logs sorted by timestamp.
- Q7 processes JSON Lines incrementally. Its `corrupted` count is the total number of invalid records in the file and is shown on each device summary.
- Q9 uses a documented command format because the assignment does not specify a complete textual grammar for inventory files and operations.
- Q10 fills missing or invalid subject marks with that subject's mean (or zero if the entire column is missing).

## Run

```bash
python3 Q1_Regex_Email_Intelligence_Extractor.py
```

For submission, rename files to your faculty's required convention, such as `YOUR_ENROLLMENT_Assignment2_Q1.py`. Test each program with sample, boundary, invalid and self-created cases, and ensure you can explain the implementation.
