## Data file


```bash
├── data
│   ├── input.xls (the input for improve)
│   ├── output.xls (the output and ground truth)
│   ├── gen_output.xls (the generate output file that merges rows together from input.xls)

```

## Running the code

```bash
├── CSV_Format.py
│   ├── key_form_header (select form headers that linked from the input excel, used to merge rows together)
│   ├── improveFormat (take a CSV file and improve the format as described)
│   ├── evelMethod (evaluate whether the generated excel is the same as the given result)

```
Due to there is the main function directly in the CSV_Format.py file, 
the read, save path is also relative, we can directly run the code to generated merged excel.
