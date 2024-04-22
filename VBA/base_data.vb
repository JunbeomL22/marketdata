Option Explicit

Sub LoadETFBaseData()
    Dim ws As Worksheet
    Dim sheet_name as String
    Dim dt as String
    Dim python_code as String
    Dim file_name as String
    Dim output_head as String

    sheet_name = "BaseData"
    Set ws = ThisWorkbook.Sheets(sheet_name)

    dt = ws.Range("C3").Value
    file_name = ws.Range("C4").Value
    output_head = ws.Range("C5").Value
    ' erase the 1000 rows and 30 columns from output_head 
    ws.Range(output_head).Resize(1000, 30).ClearContents

    python_code = "import base_data;"
    python_code = python_code & "base_data.load_etf_base_data("
    python_code = python_code & "dt='" & dt & "',"
    python_code = python_code & "file_name='" & file_name & "',"
    python_code = python_code & "output_head='" & output_head & "')"

    RunPython python_code
End Sub

Sub SaveETFBaseData()
    Dim ws As Worksheet
    Dim sheet_name as String
    Dim dt as String
    Dim python_code as String
    Dim file_name as String

    sheet_name = "BaseData"
    Set ws = ThisWorkbook.Sheets(sheet_name)

    dt = ws.Range("C3").Value
    file_name = ws.Range("C4").Value

    python_code = "import base_data;"
    python_code = python_code & "base_data.save_etf_base_data("
    python_code = python_code & "date='" & dt & "',"
    python_code = python_code & "file_name='" & file_name & "')"

    RunPython python_code
End Sub